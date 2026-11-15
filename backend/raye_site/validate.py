"""Input checks. Anything that reaches the database or a mail header goes
through here first."""

import re

MAX_EMAIL = 254
MAX_LOCAL = 64
MAX_LABEL = 63

# the local parts people actually use: letters, digits and . _ + -, with
# dots never first, last or doubled. Stricter than RFC 5322 on purpose.
_LOCAL = re.compile(r"[A-Za-z0-9_+-]+(?:\.[A-Za-z0-9_+-]+)*")
_LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?")
_TLD = re.compile(r"(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})")

LANGS = ("fr", "en")
_YES = {"1", "on", "yes", "true", "oui"}


def _ascii_domain(domain: str) -> str | None:
    domain = domain.lower()
    if domain.isascii():
        return domain
    try:
        return domain.encode("idna").decode("ascii").lower()
    except UnicodeError:
        return None


def normalise_email(raw: object) -> str | None:
    """The address in lower case with an ASCII domain, or None if it is not
    a plain, deliverable-looking address."""
    if not isinstance(raw, str):
        return None
    value = raw.strip(" \t")
    if not value or len(value) > MAX_EMAIL or value.count("@") != 1:
        return None
    local, domain = value.split("@")
    if not local or len(local) > MAX_LOCAL or not _LOCAL.fullmatch(local):
        return None
    domain = _ascii_domain(domain)
    if not domain:
        return None
    labels = domain.split(".")
    if len(labels) < 2:
        return None
    for label in labels:
        if len(label) > MAX_LABEL or not _LABEL.fullmatch(label):
            return None
    if not _TLD.fullmatch(labels[-1]):
        return None
    email = f"{local.lower()}@{domain}"
    if len(email) > MAX_EMAIL:
        return None
    return email


def parse_lang(raw: object) -> str:
    if isinstance(raw, str) and raw.strip().lower() in LANGS:
        return raw.strip().lower()
    return "fr"


def truthy(raw: object) -> bool:
    if raw is True:
        return True
    return isinstance(raw, str) and raw.strip().lower() in _YES
