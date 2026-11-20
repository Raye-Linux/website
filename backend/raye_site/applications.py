"""Applications to join the Raye team, sent from the "Join the team" pages.

What is kept, and nothing more (see the privacy page, section "applications"):

    the role, the page language, an email address OR a Raye account id,
    the Discord username, the languages and skills the person typed, why
    they want to help, the version of the consent text they ticked, the
    dates, and the staff decision.

No IP address is stored: the rate limits count addresses in memory only
(ratelimit.py). The email address never goes to Discord: the staff
channel gets the role, the Discord username and the text, so the address
stays in this database and in the staff panel.

An application is written to the database BEFORE the staff channel is
told. If Discord does not answer, nothing is lost: the row keeps
notified_at NULL and deliver_pending() tries again later, with a growing
wait, on every new application, every ten minutes from the server and
from `raye-site-admin applications notify`.

The webhook address is a secret. It is read from the first readable file
of Config.join_webhook_paths (default /etc/raye-site/join-webhook, one
line, a Discord webhook URL), and it is never printed or logged.

Hooks for the staff panel (next mission): list(), get(), decide(),
role_given(), withdraw(), delete(), purge(), and DISCORD_ROLES, which
maps each role of the site to a key of discord/state.json "roles"."""

import json
import logging
import re
import secrets
import sqlite3
import threading
import time
import urllib.error
import urllib.request
from contextlib import closing

from .bugs import AGENT, clean, load_webhook
from .ratelimit import RateLimiter
from .validate import normalise_email, truthy

log = logging.getLogger(__name__)

CONSENT_VERSION = "2026-11-20"
MAX_BODY = 8192

# the roles of the site, in the order of the pages, and the key of the
# Discord role each one gives once the Raye Team approves it
# (discord/state.json "roles"; the ids are read there, never copied here)
DISCORD_ROLES = {
    "beta": "beta_tester",
    "public-beta": "public_beta_tester",
    "beta-dev": "beta_tester_dev",
    "moderator": "moderator",
    "translator": "translator",
    "developer": "raye_developer",
    "other": "contributor",
}
ROLE_NAMES = {
    "beta": "Beta tester (private beta)", "public-beta": "Public beta tester",
    "beta-dev": "Beta tester Dev", "moderator": "Discord moderator",
    "translator": "Translator", "developer": "Developer", "other": "Designer or other",
}
STATUSES = ("pending", "approved", "declined", "withdrawn")
DECISIONS = ("approved", "declined")

DISCORD_MAX = 37
LANGUAGES_MAX = 120
SKILLS_MAX = 600
WHY_MIN = 30
WHY_MAX = 1500
LINKS_MAX = 3                 # web addresses in all the text together
PER_IP_HOUR = 3
ALL_HOUR = 40
TIMEOUT = 10
NOTIFY_TRIES = 12             # then it waits for a human (admin notify --all)
KEEP_DECIDED = 30 * 24 * 3600     # declined or withdrawn: deleted 30 days after
KEEP_PENDING = 180 * 24 * 3600    # never decided: deleted after 180 days

# Discord usernames since 2023: 2 to 32 of a-z 0-9 _ . with no ".."; the old
# form name#1234 is still accepted, people paste it
DISCORD_NEW = re.compile(r"^(?!.*\.\.)[a-z0-9_.]{2,32}$")
DISCORD_OLD = re.compile(r"^[^@#:`\s][^@#:`]{0,30}[^@#:`\s]#\d{4}$")
LINK = re.compile(r"https?://|www\.", re.I)
REFERENCE = re.compile(r"^[0-9a-f]{16}$")

SCHEMA = """
CREATE TABLE IF NOT EXISTS applications (
    id               TEXT PRIMARY KEY,
    role             TEXT NOT NULL,
    lang             TEXT NOT NULL CHECK (lang IN ('fr', 'en')),
    email            TEXT,
    account_id       TEXT,
    discord          TEXT NOT NULL,
    languages        TEXT NOT NULL DEFAULT '',
    skills           TEXT NOT NULL DEFAULT '',
    why              TEXT NOT NULL,
    consent_version  TEXT NOT NULL,
    status           TEXT NOT NULL DEFAULT 'pending'
                     CHECK (status IN ('pending', 'approved', 'declined', 'withdrawn')),
    created_at       REAL NOT NULL,
    notified_at      REAL,
    notify_attempts  INTEGER NOT NULL DEFAULT 0,
    next_notify_at   REAL NOT NULL DEFAULT 0,
    decided_at       REAL,
    decided_by       TEXT,
    decision_note    TEXT,
    role_given_at    REAL,
    CHECK (email IS NOT NULL OR account_id IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS applications_status ON applications(status, created_at);
CREATE INDEX IF NOT EXISTS applications_notify ON applications(notified_at, next_notify_at);
"""

FIELDS = ("id", "role", "lang", "email", "account_id", "discord", "languages", "skills", "why",
          "consent_version", "status", "created_at", "notified_at", "notify_attempts",
          "decided_at", "decided_by", "decision_note", "role_given_at")


def discord_name(raw):
    """The Discord username as people type it, checked, or None."""
    if not isinstance(raw, str):
        return None
    value = raw.strip().lstrip("@").strip()
    if not value or len(value) > DISCORD_MAX:
        return None
    if "#" in value:
        return value if DISCORD_OLD.match(value) and not value.endswith("#0000") else None
    value = value.lower()
    return value if DISCORD_NEW.match(value) else None


def _text(fields, key, limit, required=0):
    value = fields.get(key)
    if value is None or value == "":
        value = ""
    if not isinstance(value, str):
        raise ValueError("bad_request")
    if len(value) > limit:
        raise ValueError("too_long")
    value = clean(value, limit)
    if len(value) < required:
        raise ValueError("why_short" if key == "why" else "missing")
    return value


def validate(fields):
    """An application as a dict, or ValueError(code). The codes are the
    ones ANSWERS in server.py words for the visitor."""
    lang = "en" if fields.get("lang") == "en" else "fr"
    role = fields.get("role")
    if role not in DISCORD_ROLES:
        raise ValueError("bad_role")
    app = {"role": role, "lang": lang, "email": None, "account_token": None}
    token = fields.get("account_token")
    if token:
        if not isinstance(token, str) or not re.fullmatch(r"[A-Za-z0-9._~+/=-]{16,512}", token):
            raise ValueError("bad_request")
        app["account_token"] = token
    else:
        app["email"] = normalise_email(fields.get("email"))
        if app["email"] is None:
            raise ValueError("email")
    app["discord"] = discord_name(fields.get("discord"))
    if app["discord"] is None:
        raise ValueError("discord")
    app["languages"] = _text(fields, "languages", LANGUAGES_MAX)
    app["skills"] = _text(fields, "skills", SKILLS_MAX)
    app["why"] = _text(fields, "why", WHY_MAX, WHY_MIN)
    if role == "translator" and not app["languages"]:
        raise ValueError("languages")
    if sum(len(LINK.findall(app[k])) for k in ("languages", "skills", "why")) > LINKS_MAX:
        raise ValueError("links")
    if not truthy(fields.get("consent")):
        raise ValueError("consent")
    return app


class Store:
    """The applications table, in the backend's SQLite file."""

    def __init__(self, path, clock=time.time):
        self.path = path
        self.clock = clock

    def _connect(self):
        conn = sqlite3.connect(self.path, timeout=15)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self):
        import os
        old = os.umask(0o077)
        try:
            with closing(self._connect()) as conn:
                conn.executescript(SCHEMA)
        finally:
            os.umask(old)

    def add(self, app, account_id=None):
        """(reference, created). An open application for the same role from
        the same person (address, account or Discord name) is not doubled:
        its reference comes back and created is False."""
        now = self.clock()
        email = None if account_id else app["email"]
        with closing(self._connect()) as conn, conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                "SELECT id FROM applications WHERE role = ? AND status = 'pending' AND"
                " (discord = ? OR email = ? OR account_id = ?)",
                (app["role"], app["discord"], email, account_id)).fetchone()
            if row:
                return row["id"], False
            ref = secrets.token_hex(8)
            conn.execute(
                "INSERT INTO applications (id, role, lang, email, account_id, discord, languages,"
                " skills, why, consent_version, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (ref, app["role"], app["lang"], email, account_id, app["discord"],
                 app["languages"], app["skills"], app["why"], CONSENT_VERSION, now))
            return ref, True

    @staticmethod
    def _row(row):
        return {k: row[k] for k in FIELDS} if row else None

    def get(self, ref):
        if not isinstance(ref, str) or not REFERENCE.match(ref):
            return None
        with closing(self._connect()) as conn:
            return self._row(conn.execute("SELECT * FROM applications WHERE id = ?",
                                          (ref,)).fetchone())

    def list(self, status=None, role=None, limit=200):
        sql, args = "SELECT * FROM applications WHERE 1=1", []
        if status:
            sql += " AND status = ?"
            args.append(status)
        if role:
            sql += " AND role = ?"
            args.append(role)
        sql += " ORDER BY created_at DESC LIMIT ?"
        args.append(int(limit))
        with closing(self._connect()) as conn:
            return [self._row(r) for r in conn.execute(sql, args).fetchall()]

    def counts(self):
        with closing(self._connect()) as conn:
            rows = conn.execute("SELECT status, count(*) FROM applications GROUP BY status")
            out = dict.fromkeys(STATUSES, 0)
            out.update({r[0]: r[1] for r in rows})
            out["not_notified"] = conn.execute(
                "SELECT count(*) FROM applications WHERE notified_at IS NULL").fetchone()[0]
            return out

    def decide(self, ref, decision, staff, note=""):
        """Approve or decline a pending application. True when it changed.
        staff is who decided (their Discord name or account id), kept for
        the record; the role itself is given by the staff panel, which then
        calls role_given()."""
        if decision not in DECISIONS:
            raise ValueError("decision must be approved or declined")
        if not isinstance(staff, str) or not staff.strip():
            raise ValueError("who decided is required")
        with closing(self._connect()) as conn, conn:
            return conn.execute(
                "UPDATE applications SET status = ?, decided_at = ?, decided_by = ?,"
                " decision_note = ? WHERE id = ? AND status = 'pending'",
                (decision, self.clock(), staff.strip()[:80], (note or "")[:500], ref)).rowcount > 0

    def role_given(self, ref):
        with closing(self._connect()) as conn, conn:
            return conn.execute(
                "UPDATE applications SET role_given_at = ? WHERE id = ? AND status = 'approved'",
                (self.clock(), ref)).rowcount > 0

    def withdraw(self, ref):
        with closing(self._connect()) as conn, conn:
            return conn.execute(
                "UPDATE applications SET status = 'withdrawn', decided_at = ? WHERE id = ?"
                " AND status = 'pending'", (self.clock(), ref)).rowcount > 0

    def delete(self, ref):
        """Erase one application at once (a deletion request)."""
        with closing(self._connect()) as conn, conn:
            return conn.execute("DELETE FROM applications WHERE id = ?", (ref,)).rowcount > 0

    def delete_person(self, email=None, discord=None):
        """Erase every application of one person; returns how many."""
        email = normalise_email(email) if email else None
        discord = discord_name(discord) if discord else None
        if not email and not discord:
            return 0
        with closing(self._connect()) as conn, conn:
            return conn.execute("DELETE FROM applications WHERE email = ? OR discord = ?",
                                (email, discord)).rowcount

    def purge(self):
        now = self.clock()
        with closing(self._connect()) as conn, conn:
            decided = conn.execute(
                "DELETE FROM applications WHERE status IN ('declined', 'withdrawn')"
                " AND decided_at < ?", (now - KEEP_DECIDED,)).rowcount
            stale = conn.execute(
                "DELETE FROM applications WHERE status = 'pending' AND created_at < ?",
                (now - KEEP_PENDING,)).rowcount
        return {"decided": decided, "stale_pending": stale}

    # the staff channel

    def due(self, limit=20, every=False):
        with closing(self._connect()) as conn:
            if every:
                rows = conn.execute("SELECT * FROM applications WHERE notified_at IS NULL"
                                    " ORDER BY created_at LIMIT ?", (limit,))
            else:
                rows = conn.execute(
                    "SELECT * FROM applications WHERE notified_at IS NULL AND next_notify_at <= ?"
                    " AND notify_attempts < ? ORDER BY created_at LIMIT ?",
                    (self.clock(), NOTIFY_TRIES, limit))
            return [self._row(r) for r in rows.fetchall()]

    def notified(self, ref):
        with closing(self._connect()) as conn, conn:
            conn.execute("UPDATE applications SET notified_at = ? WHERE id = ?",
                         (self.clock(), ref))

    def notify_failed(self, ref):
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT notify_attempts FROM applications WHERE id = ?",
                               (ref,)).fetchone()
            if row is None:
                return
            tries = row[0] + 1
            # 2, 4, 8 ... minutes, at most six hours
            wait = min(6 * 3600, 60 * 2 ** tries)
            conn.execute("UPDATE applications SET notify_attempts = ?, next_notify_at = ?"
                         " WHERE id = ?", (tries, self.clock() + wait, ref))


def staff_message(app):
    """The post for the private staff channel. No email address: it stays
    in the database and the staff panel."""
    fields = [{"name": "Discord", "value": app["discord"], "inline": True},
              {"name": "Page language", "value": "French" if app["lang"] == "fr" else "English",
               "inline": True},
              {"name": "Contact", "inline": True,
               "value": "Raye account" if app.get("account_id") else "Email (in the staff panel)"}]
    if app["languages"]:
        fields.append({"name": "Languages", "value": app["languages"][:1024]})
    if app["skills"]:
        fields.append({"name": "Skills", "value": app["skills"][:1024]})
    fields.append({"name": "Why", "value": app["why"][:1024]})
    return {
        "username": "rayelinux.com",
        "embeds": [{
            "title": "New application: " + ROLE_NAMES[app["role"]],
            "color": 0x7B3CFF,
            "fields": fields,
            "footer": {"text": "Reference %s · approve or decline in the staff panel" % app["id"]},
        }],
        "allowed_mentions": {"parse": []},
    }


class Accounts:
    """Checks a Raye account token against the account server
    (GET /v1/me). Off until RAYE_ACCOUNT_API_URL is set: the account
    service is not online yet, and the form then asks for an email."""

    def __init__(self, base, opener=None):
        self.base = base
        self.opener = opener or urllib.request.build_opener()

    def ready(self):
        return bool(self.base)

    def check(self, token):
        """(account id, email) of a valid token with a confirmed address, or None."""
        req = urllib.request.Request(self.base + "/v1/me", headers={
            "Authorization": "Bearer " + token, "Accept": "application/json",
            "User-Agent": "rayelinux.com"})
        try:
            with self.opener.open(req, timeout=TIMEOUT) as r:
                data = json.loads(r.read(65536))
        except (urllib.error.HTTPError, OSError, ValueError):
            return None
        if not isinstance(data, dict) or not data.get("email_verified"):
            return None
        ident, email = data.get("id"), normalise_email(data.get("email"))
        if not isinstance(ident, str) or not re.fullmatch(r"[0-9a-fA-F-]{8,64}", ident) or not email:
            return None
        return ident, email


class Applications:
    """What the HTTP handler uses: limits, storage, the staff channel."""

    def __init__(self, store, webhook_paths=(), clock=time.time, opener=None, accounts=None,
                 background=True):
        self.store = store
        self.webhook = load_webhook(webhook_paths)
        self.clock = clock
        self.opener = opener or urllib.request.build_opener()
        self.accounts = accounts or Accounts(None)
        self.background = background
        self.limiter = RateLimiter(PER_IP_HOUR, 3600, clock)
        self.everyone = RateLimiter(ALL_HOUR, 3600, clock)
        self._sending = threading.Lock()

    def submit(self, app):
        """Store the application, then tell the staff. Returns the reference.
        The account, when one signs in, replaces the email address."""
        account_id = None
        if app.get("account_token"):
            if not self.accounts.ready():
                raise ValueError("account_unavailable")
            found = self.accounts.check(app["account_token"])
            if found is None:
                raise ValueError("account")
            account_id, app["email"] = found
        ref, created = self.store.add(app, account_id=account_id)
        if created:
            log.info("application stored (%s)", app["role"])
            self.notify_soon()
        return ref

    def notify_soon(self):
        if not self.background:
            self.deliver_pending()
            return
        threading.Thread(target=self.deliver_pending, daemon=True).start()

    def deliver_pending(self, every=False):
        """Tell the staff channel about every application it has not seen.
        Returns (sent, failed). One run at a time."""
        if not self.webhook:
            return 0, 0
        if not self._sending.acquire(blocking=False):
            return 0, 0
        sent = failed = 0
        try:
            for app in self.store.due(every=every):
                if self._post(staff_message(app)):
                    self.store.notified(app["id"])
                    sent += 1
                else:
                    self.store.notify_failed(app["id"])
                    failed += 1
        finally:
            self._sending.release()
        if failed:
            log.warning("staff channel not told about %d application(s); will retry", failed)
        return sent, failed

    def _post(self, payload):
        """Never logs the address nor the text."""
        req = urllib.request.Request(self.webhook + "?wait=true",
                                     data=json.dumps(payload).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              "User-Agent": AGENT})
        try:
            with self.opener.open(req, timeout=TIMEOUT) as r:
                return 200 <= r.status < 300
        except urllib.error.HTTPError as exc:
            log.warning("join webhook answered %s", exc.code)
        except (OSError, ValueError) as exc:
            log.warning("join webhook unreachable (%s)", type(exc).__name__)
        return False
