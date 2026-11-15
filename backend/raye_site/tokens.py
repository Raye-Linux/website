"""Link tokens: 32 random bytes, url-safe. Only the SHA-256 is kept."""

import hashlib
import re
import secrets

_SHAPE = re.compile(r"[A-Za-z0-9_-]{43}")


def new_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def well_formed(raw: object) -> bool:
    return isinstance(raw, str) and bool(_SHAPE.fullmatch(raw))
