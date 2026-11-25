"""The staff panel: look at the applications to join the team, move them
through new -> in review -> accepted / declined, keep internal notes.

Who may come in:
  * a Raye account with the "staff" role, when the account server is online
    (GET /v1/me answers roles: ["staff", ...] and a verified email);
  * until then, the admin token: one long random string in
    /etc/raye-site/staff-token (root, 0600). Who acts must give a name, kept
    in the log.
Nothing is public: every route answers 401 without a good credential, the
same answer for a wrong token and for no token. Wrong tokens are counted per
visitor in memory (5 in 10 minutes, then 429). The token is sent in the
Authorization header, never in a cookie, so a page of another site cannot
make the browser act on its own.

Everything staff does is written to staff_log (who, what, which reference,
when). Opening an application (it shows the email address) is logged too.
The log keeps no address and no text of the applications; the notes die with
their application (deletion, purge)."""

import hmac
import logging
import re
import secrets
import time
from contextlib import closing

from .ratelimit import RateLimiter

log = logging.getLogger(__name__)

TOKEN_MIN = 24
FAILS_PER_10_MIN = 5
NOTE_MAX = 1000
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 ._-]{1,38}[A-Za-z0-9.]$")
REF_RE = re.compile(r"^[0-9a-f]{16}$")

# what staff sees -> where it lives in the table
STATES = ("new", "in_review", "accepted", "declined", "withdrawn")
ACTIONS = ("in_review", "new", "accepted", "declined", "role_given")


def state_of(row):
    """The panel's word for an application."""
    if row["status"] == "pending":
        return "in_review" if row.get("in_review_at") else "new"
    return {"approved": "accepted"}.get(row["status"], row["status"])


def load_token(paths):
    """The admin token from the first readable file, or None. Too short a
    token switches the panel off rather than protect it with nothing."""
    for path in paths:
        try:
            with open(path, encoding="utf-8") as f:
                value = f.read().strip()
        except (OSError, UnicodeDecodeError):
            continue
        if len(value) >= TOKEN_MIN and value.isprintable() and " " not in value:
            return value
        log.warning("staff token file ignored: too short or not one word")
    return None


class Forbidden(Exception):
    pass


class Staff:
    def __init__(self, store, token_paths=(), accounts=None, clock=time.time):
        self.store = store
        self.token = load_token(token_paths)
        self.accounts = accounts
        self.clock = clock
        self.fails = RateLimiter(FAILS_PER_10_MIN, 600, clock)

    def enabled(self):
        return bool(self.token) or bool(self.accounts and self.accounts.ready())

    # who is asking

    def authenticate(self, ip, bearer, claimed_name):
        """(staff name) or raises Forbidden('limited'|'denied'|'name')."""
        # only failures are counted: a good staff member is never limited
        if self.fails.over(ip):
            raise Forbidden("limited")
        who = self._who(bearer, claimed_name)
        if who is None:
            self.fails.hit(ip)
            raise Forbidden("denied")
        if who == "":
            raise Forbidden("name")
        return who

    def _who(self, bearer, claimed_name):
        if not bearer or len(bearer) > 600:
            return None
        if self.token and hmac.compare_digest(bearer.encode(), self.token.encode()):
            name = (claimed_name or "").strip()
            return name if NAME_RE.match(name) else ""
        if self.accounts and self.accounts.ready():
            found = self.accounts.check_staff(bearer)
            if found:
                return "account:" + found
        return None

    # the log

    def record(self, staff, action, ref=None, detail=""):
        with closing(self.store._connect()) as conn, conn:
            conn.execute("INSERT INTO staff_log (at, staff, action, app_id, detail)"
                         " VALUES (?,?,?,?,?)",
                         (self.clock(), staff[:80], action, ref, detail[:200]))

    def log_rows(self, limit=100):
        with closing(self.store._connect()) as conn:
            rows = conn.execute("SELECT at, staff, action, app_id, detail FROM staff_log"
                                " ORDER BY id DESC LIMIT ?", (max(1, min(int(limit), 500)),))
            return [{"at": r[0], "staff": r[1], "action": r[2], "ref": r[3], "detail": r[4]}
                    for r in rows.fetchall()]

    # reading

    @staticmethod
    def _summary(row):
        # the list never carries the email, the Discord name stays
        return {"ref": row["id"], "state": state_of(row), "role": row["role"],
                "lang": row["lang"], "discord": row["discord"],
                "created_at": row["created_at"], "decided_at": row["decided_at"],
                "role_given_at": row["role_given_at"]}

    def list(self, state=None, role=None):
        if state is not None and state not in STATES:
            raise ValueError("state")
        status = {"accepted": "approved", "new": "pending", "in_review": "pending"}.get(
            state, state)
        rows = self.store.list(status=status, role=role, limit=500)
        out = [self._summary(r) for r in rows]
        if state in ("new", "in_review"):
            out = [r for r in out if r["state"] == state]
        return out

    def counts(self):
        out = dict.fromkeys(STATES, 0)
        for row in self.store.list(limit=100000):
            out[state_of(row)] += 1
        return out

    def notes(self, ref):
        with closing(self.store._connect()) as conn:
            rows = conn.execute("SELECT at, staff, text FROM staff_notes WHERE app_id = ?"
                                " ORDER BY id", (ref,))
            return [{"at": r[0], "staff": r[1], "text": r[2]} for r in rows.fetchall()]

    def detail(self, ref, staff):
        row = self.store.get(ref)
        if row is None:
            return None
        self.record(staff, "view", ref)
        data = self._summary(row)
        data.update(email=row["email"], account=bool(row["account_id"]),
                    languages=row["languages"], skills=row["skills"], why=row["why"],
                    decided_by=row["decided_by"], decision_note=row["decision_note"],
                    notes=self.notes(ref))
        return data

    # acting

    def act(self, ref, action, staff, note=""):
        """Move an application. Returns the new state, or None when it
        cannot move that way (or does not exist)."""
        if action not in ACTIONS:
            raise ValueError("action")
        row = self.store.get(ref)
        if row is None:
            return None
        pending = row["status"] == "pending"
        now = self.clock()
        ok = False
        if action in ("in_review", "new"):
            with closing(self.store._connect()) as conn, conn:
                ok = pending and conn.execute(
                    "UPDATE applications SET in_review_at = ? WHERE id = ? AND status = 'pending'",
                    (now if action == "in_review" else None, ref)).rowcount > 0
        elif action == "accepted":
            ok = self.store.decide(ref, "approved", staff, note)
        elif action == "declined":
            ok = self.store.decide(ref, "declined", staff, note)
        elif action == "role_given":
            ok = self.store.role_given(ref)
        if not ok:
            return None
        self.record(staff, action, ref)
        return state_of(self.store.get(ref))

    def add_note(self, ref, staff, text):
        if not isinstance(text, str):
            raise ValueError("note")
        text = text.replace("\r\n", "\n").strip()
        if not text or len(text) > NOTE_MAX:
            raise ValueError("note")
        if self.store.get(ref) is None:
            return False
        with closing(self.store._connect()) as conn, conn:
            conn.execute("INSERT INTO staff_notes (app_id, at, staff, text) VALUES (?,?,?,?)",
                         (ref, self.clock(), staff[:80], text))
        self.record(staff, "note", ref)
        return True


def new_token():
    """A token to put in /etc/raye-site/staff-token."""
    return secrets.token_urlsafe(32)
