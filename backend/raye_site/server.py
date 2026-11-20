"""HTTP API behind nginx: signup, confirmation and unsubscribe.

Listens on loopback only. nginx is the only client; it passes the real
visitor address in X-Real-IP, which is trusted from loopback and nowhere
else."""

import ipaddress
import json
import logging
import signal
import sys
import threading
import time
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from . import applications, bugs, community, moderation, pages, support
from .config import Config
from .mailer import Worker
from .ratelimit import RateLimiter
from .store import Store
from .validate import normalise_email, parse_lang, truthy

log = logging.getLogger(__name__)

MAX_BODY = 4096
SIGNUPS_PER_IP_HOUR = 5
LINK_HITS_PER_IP = 30          # per 10 minutes, confirm and unsubscribe together
GLOBAL_SIGNUPS_HOUR = 300      # all visitors together, protects the mail server

PAGE_CSP = ("default-src 'none'; style-src 'self'; img-src 'self'; form-action 'self'; "
            "base-uri 'none'; frame-ancestors 'none'")

ANSWERS = {
    "ok": {
        "fr": "Merci ! Si l'adresse est valide, un courriel de confirmation est en route. "
              "Cliquez sur son lien pour finaliser l'inscription.",
        "en": "Thank you! If the address is valid, a confirmation email is on its way. "
              "Click its link to finish signing up. Check your inbox.",
    },
    "email": {"fr": "Cette adresse courriel ne semble pas valide.",
              "en": "That email address doesn't look right."},
    "consent": {"fr": "Cochez la case pour accepter de recevoir le courriel de lancement.",
                "en": "Tick the box to agree to get the launch email."},
    "rate": {"fr": "Trop de demandes en peu de temps. Réessayez un peu plus tard.",
             "en": "Too many requests in a short time. Please try again later."},
    "bad_request": {"fr": "Demande invalide.", "en": "Invalid request."},
}

# "Join the team": what the visitor reads for each answer of /api/join
JOIN_ANSWERS = {
    "ok": {"fr": "Merci ! Votre candidature est arrivée. La Raye Team la lit et vous répond sur "
                 "Discord ou par courriel.",
           "en": "Thank you! Your application arrived. The Raye Team reads it and answers you on "
                 "Discord or by email."},
    "bad_role": {"fr": "Ce rôle n'existe pas.", "en": "That role does not exist."},
    "email": ANSWERS["email"],
    "discord": {"fr": "Ce nom d'utilisateur Discord ne semble pas valide (2 à 32 caractères : "
                      "lettres, chiffres, _ et .).",
                "en": "That Discord username doesn't look right (2 to 32 characters: letters, "
                      "digits, _ and .)."},
    "why_short": {"fr": "Dites-nous en quelques phrases pourquoi vous voulez aider (30 caractères "
                        "au moins).",
                  "en": "Tell us in a few sentences why you want to help (30 characters at "
                        "least)."},
    "languages": {"fr": "Indiquez les langues que vous pouvez traduire.",
                  "en": "Say which languages you can translate."},
    "links": {"fr": "Trop de liens dans le texte : trois au plus.",
              "en": "Too many links in the text: three at most."},
    "too_long": {"fr": "Un des champs est trop long.", "en": "One of the fields is too long."},
    "missing": {"fr": "Un champ obligatoire est vide.", "en": "A required field is empty."},
    "consent": {"fr": "Cochez la case pour accepter que nous gardions votre candidature.",
                "en": "Tick the box to agree that we keep your application."},
    "account": {"fr": "La connexion au compte Raye a échoué. Réessayez, ou utilisez une adresse "
                      "courriel.",
                "en": "Signing in with the Raye account failed. Try again, or use an email "
                      "address."},
    "account_unavailable": {"fr": "Les comptes Raye ne sont pas encore ouverts : utilisez une "
                                  "adresse courriel.",
                            "en": "Raye accounts are not open yet: use an email address."},
    "rate": ANSWERS["rate"],
    "bad_request": ANSWERS["bad_request"],
}


def _limit_key(address: str) -> str:
    """What the rate limits count. One IPv6 /64 is one home or one server:
    counting single addresses would hand a visitor 2^64 fresh quotas."""
    try:
        ip = ipaddress.ip_address(address.strip())
    except ValueError:
        return address
    if ip.version == 6:
        if ip.ipv4_mapped is not None:
            return str(ip.ipv4_mapped)
        return str(ipaddress.ip_network(f"{ip}/64", strict=False))
    return str(ip)


def client_ip(peer: str, header: str | None, trusted) -> str:
    """The rate-limit key of the visitor. X-Real-IP only counts when it
    comes from the local nginx."""
    if peer in trusted and header:
        try:
            return _limit_key(str(ipaddress.ip_address(header.strip())))
        except ValueError:
            pass
    return _limit_key(peer)


class App:
    """What the handler needs, shared by all request threads."""

    def __init__(self, config: Config, store: Store, worker, clock=time.time):
        self.config = config
        self.store = store
        self.worker = worker
        self.signups = RateLimiter(SIGNUPS_PER_IP_HOUR, 3600, clock)
        self.links = RateLimiter(LINK_HITS_PER_IP, 600, clock)
        self.global_cap = GLOBAL_SIGNUPS_HOUR
        self.support = support.Support(config.support_ollama_url, config.support_model, clock)
        self.bugs = bugs.Bugs(
            bugs.load_webhook(config.bug_webhook_paths), clock,
            review_url=bugs.load_webhook(config.bug_review_paths),
            classifier=moderation.Classifier(config.support_ollama_url, config.support_model))
        self.feed = bugs.Feed(config.bugs_api_url, config.bugs_guild, clock)
        join_store = applications.Store(config.db_path, clock)
        join_store.init()
        self.join = applications.Applications(
            join_store, config.join_webhook_paths, clock,
            accounts=applications.Accounts(config.account_api_url))
        self.community = community.Community(config.discord_invite, clock)


class BadRequest(Exception):
    def __init__(self, status: HTTPStatus = HTTPStatus.BAD_REQUEST):
        super().__init__(status.phrase)
        self.status = status


class Handler(BaseHTTPRequestHandler):
    server_version = "raye-site"
    sys_version = ""
    protocol_version = "HTTP/1.1"
    timeout = 15

    @property
    def app(self) -> App:
        return self.server.app

    # logging: path only, never the query string (it carries tokens)

    def log_message(self, fmt, *args):
        pass

    def log_request(self, code="-", size="-"):
        path = urllib.parse.urlsplit(getattr(self, "path", "")).path
        code = getattr(code, "value", code)
        log.info("%s %s %s", getattr(self, "command", "-"), path[:100], code)

    # responses

    def _send(self, status: int, body: bytes, ctype: str, extra=None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        if ctype.startswith("text/html"):
            self.send_header("Content-Security-Policy", PAGE_CSP)
            self.send_header("X-Frame-Options", "DENY")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        if self.close_connection:
            self.send_header("Connection", "close")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, status: int, payload: dict, extra=None) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8", extra)

    def _page(self, status: int, kind: str, lang, form_action=None, token=None,
              extra=None) -> None:
        body = pages.render(kind, lang, form_action, token).encode("utf-8")
        self._send(status, body, "text/html; charset=utf-8", extra)

    def _text(self, status: int, text: str) -> None:
        self._send(status, text.encode(), "text/plain; charset=utf-8")

    # request parsing

    def _ip(self) -> str:
        return client_ip(self.client_address[0], self.headers.get("X-Real-IP"),
                         self.app.config.trusted_proxies)

    def _route(self) -> tuple[str, dict]:
        parts = urllib.parse.urlsplit(self.path)
        try:
            query = urllib.parse.parse_qs(parts.query, max_num_fields=10)
        except ValueError:
            raise BadRequest()
        return parts.path, {k: v[0] for k, v in query.items()}

    def _read_body(self, max_body: int = MAX_BODY) -> tuple[str, dict]:
        """('json'|'form', fields). Raises BadRequest."""
        if "chunked" in self.headers.get("Transfer-Encoding", "").lower():
            raise BadRequest(HTTPStatus.LENGTH_REQUIRED)
        length = self.headers.get("Content-Length")
        if length is None:
            raise BadRequest(HTTPStatus.LENGTH_REQUIRED)
        try:
            size = int(length)
        except ValueError:
            raise BadRequest(HTTPStatus.BAD_REQUEST)
        if size < 0:
            raise BadRequest(HTTPStatus.BAD_REQUEST)
        if size > max_body:
            raise BadRequest(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        raw = self.rfile.read(size)
        ctype = self.headers.get("Content-Type", "").split(";")[0].strip().lower()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            raise BadRequest(HTTPStatus.BAD_REQUEST)
        if ctype == "application/json":
            try:
                data = json.loads(text)
            except (ValueError, RecursionError):
                raise BadRequest(HTTPStatus.BAD_REQUEST)
            if not isinstance(data, dict):
                raise BadRequest(HTTPStatus.BAD_REQUEST)
            return "json", data
        if ctype == "application/x-www-form-urlencoded":
            try:
                fields = urllib.parse.parse_qs(text, keep_blank_values=True,
                                               max_num_fields=20, strict_parsing=False)
            except ValueError:
                raise BadRequest(HTTPStatus.BAD_REQUEST)
            return "form", {k: v[0] for k, v in fields.items()}
        raise BadRequest(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    # verbs

    def _reject(self, exc: BadRequest) -> None:
        # whatever is left of this request must not be read as the next one
        self.close_connection = True
        self._json(exc.status.value, {"ok": False, "error": "bad_request"})

    def do_GET(self):
        if self.headers.get("Content-Length") or self.headers.get("Transfer-Encoding"):
            # a body we will not read must not be taken for the next request
            self.close_connection = True
        try:
            path, query = self._route()
        except BadRequest as exc:
            return self._reject(exc)
        if path == "/api/health":
            return self._text(200, "ok\n")
        if path == "/api/confirm":
            return self._link_page("confirm", query.get("t"))
        if path == "/api/unsubscribe":
            return self._link_page("unsubscribe", query.get("t"))
        if path == "/api/community":
            return self._json(*self.app.community.status(),
                              extra={"Cache-Control": "public, max-age=300"})
        if path == "/api/bugs":
            return self._json(*self.app.feed.topics())
        if path.startswith("/api/bugs/"):
            return self._json(*self.app.feed.topic(path[len("/api/bugs/"):]))
        if path in ("/api/subscribe", "/api/support/chat", "/api/support/bug", "/api/join"):
            return self._text(405, "method not allowed\n")
        return self._page(404, "not_found", None)

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        try:
            path, query = self._route()
            if path == "/api/support/chat":
                return self._support()
            if path == "/api/support/bug":
                return self._bug()
            if path == "/api/join":
                return self._join()
            if path not in ("/api/subscribe", "/api/confirm", "/api/unsubscribe"):
                self.close_connection = True
                return self._page(404, "not_found", None)
            kind, fields = self._read_body()
        except BadRequest as exc:
            return self._reject(exc)
        if path == "/api/subscribe":
            return self._subscribe(kind, fields)
        token = fields.get("t") or query.get("t")
        if path == "/api/confirm":
            return self._link_post("confirm", token, truthy(fields.get("news")))
        return self._link_post("unsubscribe", token)

    def _not_allowed(self):
        self._text(405, "method not allowed\n")

    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = _not_allowed

    # signup

    def _subscribe(self, kind: str, fields: dict):
        lang = parse_lang(fields.get("lang"))
        as_json = kind == "json" or "application/json" in self.headers.get("Accept", "")

        def answer(status, key, extra=None):
            if as_json:
                return self._json(status, {"ok": key == "ok", "error": None if key == "ok" else key,
                                           "message": ANSWERS[key][lang]}, extra)
            page = {"ok": "subscribed", "email": "bad_email", "consent": "no_consent",
                    "rate": "rate"}[key]
            return self._page(status, page, lang, extra=extra)

        ip = self._ip()
        if not self.app.signups.hit(ip):
            return answer(429, "rate", {"Retry-After": str(self.app.signups.retry_after(ip))})
        if fields.get("website"):
            return answer(200, "ok")  # a robot filled the hidden field
        email = normalise_email(fields.get("email"))
        if email is None:
            return answer(400, "email")
        if not truthy(fields.get("consent")):
            return answer(400, "consent")
        if self.app.store.queued_last_hour() >= self.app.global_cap:
            log.warning("global signup cap reached")
            return answer(429, "rate", {"Retry-After": "600"})
        # a "news" field is ignored here: that choice is made on the
        # confirmation page, by whoever owns the address
        if self.app.store.subscribe(email, lang):
            self.app.worker.wake()
        return answer(200, "ok")

    # bug reports

    def _bug(self):
        b = self.app.bugs

        def answer(status, code=None, extra=None):
            if code:
                self.close_connection = True
            self._json(status, {"ok": code is None, "error": code}, extra)

        if not b.ready():
            return answer(503, "not_configured")
        try:
            kind, fields = self._read_body(bugs.MAX_BODY)
        except BadRequest as exc:
            code = "too_large" if exc.status == HTTPStatus.REQUEST_ENTITY_TOO_LARGE else "bad_request"
            return answer(exc.status.value, code)
        if kind != "json":
            return answer(415, "bad_request")
        if fields.get("website"):
            return answer(200)  # a robot filled the hidden field
        try:
            report = bugs.validate(fields)
        except ValueError as exc:
            return answer(400, str(exc))
        ip = self._ip()
        if not b.limiter.hit(ip):
            return answer(429, "rate_limited", {"Retry-After": str(b.limiter.retry_after(ip))})
        if not b.everyone.hit("all"):
            return answer(429, "rate_limited", {"Retry-After": "600"})
        if not b.handle(report):
            return answer(502, "not_sent")
        return answer(200)

    # join the team

    def _join(self):
        j = self.app.join
        lang = "fr"
        as_json = True

        def answer(status, key, extra=None, ref=None):
            if key != "ok":
                self.close_connection = True
            if as_json:
                payload = {"ok": key == "ok", "error": None if key == "ok" else key,
                           "message": JOIN_ANSWERS[key][lang]}
                if ref:
                    payload["reference"] = ref
                return self._json(status, payload, extra)
            return self._page(status, "join_ok" if key == "ok" else "join_" + (
                "rate" if key == "rate" else "error"), lang, extra=extra)

        try:
            kind, fields = self._read_body(applications.MAX_BODY)
        except BadRequest as exc:
            return answer(exc.status.value, "too_long" if exc.status ==
                          HTTPStatus.REQUEST_ENTITY_TOO_LARGE else "bad_request")
        lang = "en" if fields.get("lang") == "en" else "fr"
        as_json = kind == "json" or "application/json" in self.headers.get("Accept", "")
        if fields.get("website"):
            return answer(200, "ok")  # a robot filled the hidden field
        try:
            app = applications.validate(fields)
        except ValueError as exc:
            return answer(400, str(exc))
        # only well-formed applications count: a typo must not lock anyone out
        ip = self._ip()
        if not j.limiter.hit(ip):
            return answer(429, "rate", {"Retry-After": str(j.limiter.retry_after(ip))})
        if not j.everyone.hit("all"):
            log.warning("global application cap reached")
            return answer(429, "rate", {"Retry-After": "600"})
        try:
            ref = j.submit(app)
        except ValueError as exc:
            return answer(400, str(exc))
        return answer(200, "ok", ref=ref)

    # help bubble

    def _support(self):
        s = self.app.support

        def refuse(status, code, extra=None):
            self.close_connection = True
            self._json(status, {"ok": False, "error": code}, extra)

        if not s.url or not s.kb:
            return refuse(503, "not_configured")
        try:
            kind, fields = self._read_body(support.MAX_BODY)
        except BadRequest as exc:
            code = "too_large" if exc.status == HTTPStatus.REQUEST_ENTITY_TOO_LARGE else "bad_request"
            return refuse(exc.status.value, code)
        if kind != "json":
            return refuse(415, "bad_request")
        ip = self._ip()
        if not s.limiter.hit(ip):
            return refuse(429, "rate_limited", {"Retry-After": str(s.limiter.retry_after(ip))})
        try:
            lang, messages = support.validate(fields)
        except ValueError as exc:
            return refuse(400, str(exc))
        if not s.enter():
            return refuse(503, "busy", {"Retry-After": "20"})
        try:
            self._support_stream(s, *s.prepare(lang, messages))
        finally:
            s.leave()

    def _support_stream(self, s, body, sources):
        self.close_connection = True
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-transform")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Connection", "close")
        self.end_headers()

        def send(raw: bytes):
            self.wfile.write(raw)
            self.wfile.flush()

        def event(name, data):
            head = f"event: {name}\n" if name else ""
            send((head + "data: " + json.dumps(data, ensure_ascii=False) + "\n\n").encode())

        try:
            event("meta", {"sources": sources})
            for piece in s.stream(body, lambda: send(b": wait\n\n")):
                event(None, {"t": piece})
        except (BrokenPipeError, ConnectionResetError):
            s.count(True)   # the visitor left; model errors come as RuntimeError
            return
        except Exception:   # model down, timeout, bad stream
            s.count(False)
            try:
                event("error", {"code": "model_unavailable"})
            except OSError:
                pass
            return
        s.count(True)
        try:
            event("done", {})
        except OSError:
            pass

    # links

    def _limited(self) -> bool:
        ip = self._ip()
        if self.app.links.hit(ip):
            return False
        self._page(429, "rate", None, extra={"Retry-After": str(self.app.links.retry_after(ip))})
        return True

    def _link_page(self, what: str, token):
        if self._limited():
            return
        store = self.app.store
        if what == "confirm":
            state, lang = store.check_confirm(token)
            if state == "pending":
                return self._page(200, "confirm_ask", lang, "/api/confirm", token)
            return self._confirm_result(state, lang)
        state, lang = store.check_unsubscribe(token)
        if state == "active":
            return self._page(200, "unsub_ask", lang, "/api/unsubscribe", token)
        return self._unsub_result(state, lang)

    def _link_post(self, what: str, token, news: bool = False):
        if self._limited():
            return
        if what == "confirm":
            state, lang = self.app.store.confirm(token, news=news)
            return self._confirm_result(state, lang)
        state, lang = self.app.store.unsubscribe(token)
        return self._unsub_result(state, lang)

    def _confirm_result(self, state, lang):
        status, kind = {"confirmed": (200, "confirmed"), "already": (200, "confirm_already"),
                        "expired": (410, "confirm_expired")}.get(state, (404, "invalid"))
        self._page(status, kind, lang)

    def _unsub_result(self, state, lang):
        status, kind = {"done": (200, "unsub_done"),
                        "already": (200, "unsub_already")}.get(state, (404, "invalid"))
        self._page(status, kind, lang)


MAX_CONNECTIONS = 40
BUSY = (b"HTTP/1.1 503 Service Unavailable\r\nContent-Type: text/plain\r\n"
        b"Content-Length: 5\r\nRetry-After: 5\r\nConnection: close\r\n\r\nbusy\n")


class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 64

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_max_connections(MAX_CONNECTIONS)

    def set_max_connections(self, n: int) -> None:
        """At most n requests handled at once, one thread each; the rest
        get a 503 straight away instead of piling up threads."""
        self._slots = threading.BoundedSemaphore(n)

    def process_request(self, request, client_address):
        slots = self._slots
        if not slots.acquire(blocking=False):
            try:
                request.sendall(BUSY)
            except OSError:
                pass
            self.shutdown_request(request)
            return
        try:
            threading.Thread(target=self._serve_one, args=(request, client_address, slots),
                             daemon=True).start()
        except RuntimeError:
            slots.release()
            self.shutdown_request(request)

    def _serve_one(self, request, client_address, slots) -> None:
        try:
            self.process_request_thread(request, client_address)
        finally:
            slots.release()


def make_server(config: Config, store: Store, worker, clock=time.time) -> Server:
    httpd = Server((config.listen_host, config.listen_port), Handler)
    httpd.app = App(config, store, worker, clock)
    return httpd


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s",
                        stream=sys.stderr)
    config = Config.from_env()
    store = Store(config.db_path)
    store.init()
    worker = Worker(store, config)
    httpd = make_server(config, store, worker)

    def stop(*_):
        # shutdown() waits for serve_forever, so run it outside the signal frame
        threading.Thread(target=httpd.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    worker.start()

    def retry_staff_channel():
        # applications the staff channel has not heard of yet, every ten minutes
        while True:
            time.sleep(600)
            try:
                httpd.app.join.deliver_pending()
            except Exception:   # never let this thread die
                log.exception("staff channel retry failed")

    threading.Thread(target=retry_staff_channel, daemon=True).start()
    log.info("listening on %s:%d", config.listen_host, config.listen_port)
    try:
        httpd.serve_forever()
    finally:
        worker.stop()
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
