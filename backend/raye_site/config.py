"""Settings, read once from the environment the systemd unit gives us."""

import ipaddress
import os
from dataclasses import dataclass, field

DEFAULT_SMTP_ENV = "/etc/raye-site/smtp.env"
DEFAULT_TLS_NAME = "mail.example.org"
DEFAULT_SENDER = "Raye Linux <bonjour@rayelinux.com>"
DEFAULT_BUG_WEBHOOK = "/etc/raye-site/bug-webhook"
DEFAULT_BUG_REVIEW_WEBHOOK = "/etc/raye-site/bug-review-webhook"
# the Discord webhook of the private staff channel told about each application
DEFAULT_JOIN_WEBHOOK = "/etc/raye-site/join-webhook"
DEFAULT_DISCORD_INVITE = "TrxhUkabyB"


@dataclass(frozen=True)
class SmtpSettings:
    host: str
    port: int
    user: str
    password: str = field(repr=False)
    sender: str = DEFAULT_SENDER


@dataclass(frozen=True)
class Config:
    db_path: str
    site_url: str = "https://rayelinux.com"
    listen_host: str = "127.0.0.1"
    listen_port: int = 8081
    smtp_env_paths: tuple = (DEFAULT_SMTP_ENV,)
    smtp_tls_name: str = DEFAULT_TLS_NAME
    smtp_cafile: str | None = None
    trusted_proxies: tuple = ("127.0.0.1", "::1")
    # the help bubble: an Ollama server; unset, the bubble answers 503
    support_ollama_url: str | None = None
    support_model: str = "TechorayeAI:latest"
    # the Discord webhook of the #bugs forum (a secret, never logged)
    bug_webhook_paths: tuple = ()
    bug_review_paths: tuple = ()
    # the #bugs topics, read from the Discord bot's API
    bugs_api_url: str | None = None
    bugs_guild: str | None = None
    # "Join the team": the staff channel webhook (a secret, never logged)
    join_webhook_paths: tuple = ()
    # the Raye account server, to sign an application with an account;
    # unset while accounts are not online, and the form asks for an email
    account_api_url: str | None = None
    # the invite code whose public numbers the Community page shows
    discord_invite: str | None = None

    @classmethod
    def from_env(cls, env=None) -> "Config":
        env = os.environ if env is None else env
        state = env.get("STATE_DIRECTORY", "/var/lib/raye-site").split(":")[0]
        db = env.get("RAYE_SITE_DB") or os.path.join(state, "site.db")

        url = env.get("RAYE_SITE_URL", "https://rayelinux.com").rstrip("/")
        if not url.startswith("https://"):
            raise ValueError("RAYE_SITE_URL must be https")

        host = env.get("RAYE_SITE_HOST", "127.0.0.1")
        if not ipaddress.ip_address(host).is_loopback:
            raise ValueError("the backend only listens on loopback")
        port = int(env.get("RAYE_SITE_PORT", "8081"))

        # systemd copies /etc/raye-site/ into the credentials directory;
        # a directory credential "smtp" gives one file per entry, smtp_<name>
        paths = []
        creds = env.get("CREDENTIALS_DIRECTORY")
        if creds:
            paths += [os.path.join(creds, "smtp_smtp.env"), os.path.join(creds, "smtp")]
        paths.append(env.get("RAYE_SITE_SMTP_ENV", DEFAULT_SMTP_ENV))
        bug_paths = [os.path.join(creds, "smtp_bug-webhook")] if creds else []
        bug_paths.append(env.get("RAYE_SITE_BUG_WEBHOOK", DEFAULT_BUG_WEBHOOK))
        review_paths = [os.path.join(creds, "smtp_bug-review-webhook")] if creds else []
        review_paths.append(env.get("RAYE_SITE_BUG_REVIEW_WEBHOOK", DEFAULT_BUG_REVIEW_WEBHOOK))
        join_paths = [os.path.join(creds, "smtp_join-webhook")] if creds else []
        join_paths.append(env.get("RAYE_SITE_JOIN_WEBHOOK", DEFAULT_JOIN_WEBHOOK))

        return cls(
            db_path=db,
            site_url=url,
            listen_host=host,
            listen_port=port,
            smtp_env_paths=tuple(paths),
            smtp_tls_name=env.get("SMTP_TLS_NAME", DEFAULT_TLS_NAME),
            smtp_cafile=env.get("RAYE_SITE_SMTP_CAFILE") or None,
            support_ollama_url=support_url(env.get("RAYE_SUPPORT_OLLAMA_URL")),
            support_model=env.get("RAYE_SUPPORT_MODEL") or "TechorayeAI:latest",
            bug_webhook_paths=tuple(bug_paths),
            bug_review_paths=tuple(review_paths),
            bugs_api_url=support_url(env.get("RAYE_BUGS_API_URL")),
            bugs_guild=env.get("RAYE_BUGS_GUILD") if (env.get("RAYE_BUGS_GUILD") or "").isdigit() else None,
            join_webhook_paths=tuple(join_paths),
            account_api_url=account_url(env.get("RAYE_ACCOUNT_API_URL")),
            discord_invite=env.get("RAYE_DISCORD_INVITE", DEFAULT_DISCORD_INVITE) or None,
        )


def support_url(value):
    """The Ollama address, plain http on the local network only: the
    questions must never leave our own servers."""
    if not value:
        return None
    from urllib.parse import urlsplit
    parts = urlsplit(value)
    if parts.scheme != "http" or not parts.hostname:
        raise ValueError("RAYE_SUPPORT_OLLAMA_URL must be http://<local address>:<port>")
    ip = ipaddress.ip_address(parts.hostname)
    if not (ip.is_private or ip.is_loopback):
        raise ValueError("RAYE_SUPPORT_OLLAMA_URL must be on the local network")
    return value.rstrip("/")


def account_url(value):
    """The account server: https, or plain http on loopback (same machine)."""
    if not value:
        return None
    from urllib.parse import urlsplit
    parts = urlsplit(value)
    if not parts.hostname:
        raise ValueError("RAYE_ACCOUNT_API_URL must be https://<host>")
    if parts.scheme != "https":
        try:
            loopback = ipaddress.ip_address(parts.hostname).is_loopback
        except ValueError:
            loopback = False
        if parts.scheme != "http" or not loopback:
            raise ValueError("RAYE_ACCOUNT_API_URL must be https (or http on loopback)")
    return value.rstrip("/")
