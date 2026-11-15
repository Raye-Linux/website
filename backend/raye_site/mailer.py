"""Sending: SMTP submission with STARTTLS, and the background thread that
works through the queue. A mail that cannot go out (no credentials yet,
server down, bad password) stays queued and is retried later."""

import logging
import smtplib
import ssl
import threading
import time

from .config import DEFAULT_SENDER, SmtpSettings
from .emails import _address, build_confirmation, build_launch

log = logging.getLogger(__name__)

NO_CREDENTIALS_RETRY = 300
MAX_BACKOFF = 3600
SMTP_TIMEOUT = 20
PURGE_EVERY = 3600


def backoff(attempts: int) -> int:
    return min(60 * 2 ** min(attempts, 12), MAX_BACKOFF)


def _parse_env(text: str) -> dict:
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key, sep, value = line.partition("=")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def load_smtp_settings(paths) -> SmtpSettings | None:
    """The first complete settings file among paths, or None."""
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                values = _parse_env(f.read())
        except (OSError, UnicodeDecodeError):
            continue
        try:
            port = int(values.get("SMTP_PORT", ""))
        except ValueError:
            continue
        host, user = values.get("SMTP_HOST"), values.get("SMTP_USER")
        password = values.get("SMTP_PASSWORD")
        if not (host and user and password and 0 < port < 65536):
            continue
        return SmtpSettings(host=host, port=port, user=user, password=password,
                            sender=values.get("SMTP_FROM") or DEFAULT_SENDER)
    return None


class _SMTP(smtplib.SMTP):
    """Connects to an address but checks the certificate against a name:
    the mail server is reached on the LAN, its certificate is for its
    public name."""

    def __init__(self, tls_name: str, timeout: float):
        self._tls_name = tls_name
        super().__init__(timeout=timeout)

    def connect(self, host="localhost", port=0, source_address=None):
        reply = super().connect(host, port, source_address)
        self._host = self._tls_name  # used by starttls() for SNI and the name check
        return reply


def send(settings: SmtpSettings, msg, to: str, tls_name: str, cafile: str | None = None,
         timeout: float = SMTP_TIMEOUT) -> None:
    context = ssl.create_default_context(cafile=cafile)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    envelope_from = _address(settings.sender).addr_spec
    with _SMTP(tls_name, timeout) as smtp:
        smtp.connect(settings.host, settings.port)
        smtp.ehlo("rayelinux.com")
        if not smtp.has_extn("starttls"):
            # never log in without TLS
            raise smtplib.SMTPNotSupportedError("server does not offer STARTTLS")
        smtp.starttls(context=context)
        smtp.ehlo("rayelinux.com")
        smtp.login(settings.user, settings.password)
        smtp.send_message(msg, from_addr=envelope_from, to_addrs=[to])


def _short(exc: Exception) -> str:
    text = f"{type(exc).__name__}: {exc}".replace("\n", " ")
    return text[:200]


class Worker:
    def __init__(self, store, config, clock=time.time):
        self.store = store
        self.config = config
        self.clock = clock
        self.poll_seconds = 30
        self._event = threading.Event()
        self._stop = False
        self._last_purge = 0.0
        self.thread = threading.Thread(target=self._run, name="mail-queue", daemon=True)

    def _links(self, confirm: str, unsub: str) -> tuple[str, str]:
        base = self.config.site_url
        return f"{base}/api/confirm?t={confirm}", f"{base}/api/unsubscribe?t={unsub}"

    def process_once(self) -> dict:
        out = {"sent": 0, "retry": 0, "dropped": 0}
        jobs = self.store.jobs_due()
        if not jobs:
            return out
        settings = load_smtp_settings(self.config.smtp_env_paths)
        for job in jobs:
            if settings is None:
                self.store.job_failed(job.id, "no credentials", NO_CREDENTIALS_RETRY)
                log.info("mail #%d queued: SMTP credentials missing, retry in %d s",
                         job.id, NO_CREDENTIALS_RETRY)
                out["retry"] += 1
                continue
            if job.kind == "launch":
                unsub = self.store.issue_unsub(job.subscriber_id)
                unsub_url = self._links("", unsub)[1]
            else:
                confirm, unsub = self.store.issue_tokens(job.subscriber_id)
                confirm_url, unsub_url = self._links(confirm, unsub)
            try:
                if job.kind == "launch":
                    msg = build_launch(job.email, job.lang, unsub_url, settings.sender)
                else:
                    msg = build_confirmation(job.email, job.lang, confirm_url, unsub_url,
                                             settings.sender)
                send(settings, msg, job.email, self.config.smtp_tls_name,
                     self.config.smtp_cafile)
            except smtplib.SMTPRecipientsRefused as exc:
                self.store.forget_unsub(unsub)
                codes = [code for code, _ in exc.recipients.values()]
                if codes and all(code >= 500 for code in codes):
                    self.store.job_dropped(job.id)
                    log.warning("mail #%d dropped: recipient refused (%s)", job.id, codes)
                    out["dropped"] += 1
                else:
                    self._retry(job, exc)
                    out["retry"] += 1
            except (smtplib.SMTPException, OSError, ValueError) as exc:
                self.store.forget_unsub(unsub)
                self._retry(job, exc)
                out["retry"] += 1
            else:
                self.store.job_sent(job.id)
                log.info("mail #%d sent (%s, %s)", job.id, job.kind, job.lang)
                out["sent"] += 1
        return out

    def _retry(self, job, exc: Exception) -> None:
        delay = backoff(job.attempts)
        self.store.job_failed(job.id, _short(exc), delay)
        log.warning("mail #%d not sent (%s), retry in %d s", job.id, _short(exc), delay)

    def _tick(self) -> None:
        now = self.clock()
        if now - self._last_purge >= PURGE_EVERY:
            self._last_purge = now
            removed = self.store.purge()
            if any(removed.values()):
                log.info("purge: %s", removed)
        self.process_once()

    def _run(self) -> None:
        while not self._stop:
            try:
                self._tick()
            except Exception:  # keep the thread alive, the next tick retries
                log.exception("mail queue tick failed")
            self._event.wait(self.poll_seconds)
            self._event.clear()

    def start(self) -> None:
        self.thread.start()

    def wake(self) -> None:
        self._event.set()

    def stop(self) -> None:
        self._stop = True
        self._event.set()
        self.thread.join(timeout=30)
