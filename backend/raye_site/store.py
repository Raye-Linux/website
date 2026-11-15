"""The list itself, in SQLite.

subscribers   one row per address: lang, consent, times. No IP address.
unsub_tokens  SHA-256 of every unsubscribe link we mailed (one per mail).
jobs          mails still to send. A job holds no token: tokens are made
              when the mail actually goes out, so a mail that waits for
              days still gets a link valid 48 h from its arrival.
confirm_log   when confirmation mails were asked for, to cap them at
              three per address per day.
"""

import os
import sqlite3
import time
from contextlib import closing
from dataclasses import dataclass

from .tokens import hash_token, new_token, well_formed
from .validate import normalise_email

CONSENT_VERSION = "2026-10-31"
CONFIRM_TTL = 48 * 3600
MAX_CONFIRM_MAILS = 3          # per address and per 24 h
JOB_MAX_AGE = 7 * 24 * 3600    # a mail that could not go out in a week is dropped
KEEP_UNSUBSCRIBED = 30 * 24 * 3600

SCHEMA = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS subscribers (
    id                 INTEGER PRIMARY KEY,
    email              TEXT NOT NULL UNIQUE,
    lang               TEXT NOT NULL CHECK (lang IN ('fr', 'en')),
    news               INTEGER NOT NULL DEFAULT 0,
    consent_version    TEXT NOT NULL,
    created_at         REAL NOT NULL,
    confirmed_at       REAL,
    unsubscribed_at    REAL,
    confirm_hash       TEXT UNIQUE,
    confirm_expires_at REAL
);
CREATE TABLE IF NOT EXISTS unsub_tokens (
    hash          TEXT PRIMARY KEY,
    subscriber_id INTEGER NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    created_at    REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS jobs (
    id            INTEGER PRIMARY KEY,
    kind          TEXT NOT NULL,
    subscriber_id INTEGER NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    created_at    REAL NOT NULL,
    next_at       REAL NOT NULL,
    attempts      INTEGER NOT NULL DEFAULT 0,
    last_error    TEXT
);
CREATE TABLE IF NOT EXISTS confirm_log (
    subscriber_id INTEGER NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    at            REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS announcements (
    subscriber_id INTEGER NOT NULL REFERENCES subscribers(id) ON DELETE CASCADE,
    kind          TEXT NOT NULL,
    at            REAL NOT NULL,
    PRIMARY KEY (subscriber_id, kind)
);
CREATE INDEX IF NOT EXISTS jobs_next ON jobs(next_at);
CREATE INDEX IF NOT EXISTS confirm_log_sub ON confirm_log(subscriber_id, at);
"""


@dataclass(frozen=True)
class Job:
    id: int
    subscriber_id: int
    email: str
    lang: str
    attempts: int
    kind: str = "confirm"


class Store:
    def __init__(self, path: str, clock=time.time):
        self.path = path
        self.clock = clock

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=15)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init(self) -> None:
        old = os.umask(0o077)
        try:
            with closing(self._connect()) as conn:
                conn.execute("PRAGMA journal_mode = WAL")
                conn.executescript(SCHEMA)
        finally:
            os.umask(old)

    # signup

    def subscribe(self, email: str, lang: str) -> bool:
        """Record a signup. True when a confirmation mail was queued.
        The caller answers the same way whatever this returns.

        Anyone can type any address, so a signup never changes an existing
        entry's language or choices: those belong to whoever confirms."""
        now = self.clock()
        with closing(self._connect()) as conn, conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM subscribers WHERE email = ?", (email,)).fetchone()
            if row is None:
                sid = conn.execute(
                    "INSERT INTO subscribers (email, lang, news, consent_version, created_at)"
                    " VALUES (?, ?, 0, ?, ?)",
                    (email, lang, CONSENT_VERSION, now)).lastrowid
            elif row["confirmed_at"] is not None and row["unsubscribed_at"] is None:
                return False  # already on the list; nothing to say to anyone
            else:
                sid = row["id"]
                if row["unsubscribed_at"] is not None:
                    # coming back: a fresh double opt-in, old links stay dead
                    conn.execute(
                        "UPDATE subscribers SET created_at = ?, confirmed_at = NULL,"
                        " unsubscribed_at = NULL, confirm_hash = NULL, news = 0,"
                        " confirm_expires_at = NULL, consent_version = ? WHERE id = ?",
                        (now, CONSENT_VERSION, sid))
                    conn.execute("DELETE FROM unsub_tokens WHERE subscriber_id = ?", (sid,))
                if conn.execute("SELECT 1 FROM jobs WHERE subscriber_id = ?", (sid,)).fetchone():
                    return False  # a mail is already waiting
            asked = conn.execute(
                "SELECT count(*) FROM confirm_log WHERE subscriber_id = ? AND at > ?",
                (sid, now - 24 * 3600)).fetchone()[0]
            if asked >= MAX_CONFIRM_MAILS:
                return False
            conn.execute("INSERT INTO confirm_log (subscriber_id, at) VALUES (?, ?)", (sid, now))
            conn.execute(
                "INSERT INTO jobs (kind, subscriber_id, created_at, next_at)"
                " VALUES ('confirm', ?, ?, ?)", (sid, now, now))
            return True

    def queued_last_hour(self) -> int:
        with closing(self._connect()) as conn:
            return conn.execute("SELECT count(*) FROM confirm_log WHERE at > ?",
                                (self.clock() - 3600,)).fetchone()[0]

    # outgoing queue

    def jobs_due(self, limit: int = 20) -> list[Job]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT j.id, j.subscriber_id, s.email, s.lang, j.attempts, j.kind FROM jobs j"
                " JOIN subscribers s ON s.id = j.subscriber_id"
                " WHERE j.next_at <= ? ORDER BY j.next_at LIMIT ?",
                (self.clock(), limit)).fetchall()
        return [Job(r["id"], r["subscriber_id"], r["email"], r["lang"], r["attempts"],
                    r["kind"]) for r in rows]

    def queue_size(self) -> int:
        with closing(self._connect()) as conn:
            return conn.execute("SELECT count(*) FROM jobs").fetchone()[0]

    def issue_tokens(self, subscriber_id: int) -> tuple[str, str]:
        """New confirmation and unsubscribe links for the mail about to go.
        The confirmation link replaces any earlier one."""
        now = self.clock()
        confirm, unsub = new_token(), new_token()
        with closing(self._connect()) as conn, conn:
            conn.execute("UPDATE subscribers SET confirm_hash = ?, confirm_expires_at = ?"
                         " WHERE id = ?", (hash_token(confirm), now + CONFIRM_TTL, subscriber_id))
            conn.execute("INSERT INTO unsub_tokens (hash, subscriber_id, created_at)"
                         " VALUES (?, ?, ?)", (hash_token(unsub), subscriber_id, now))
        return confirm, unsub

    def issue_unsub(self, subscriber_id: int) -> str:
        """A new unsubscribe link, for a mail that carries no confirmation."""
        unsub = new_token()
        with closing(self._connect()) as conn, conn:
            conn.execute("INSERT INTO unsub_tokens (hash, subscriber_id, created_at)"
                         " VALUES (?, ?, ?)", (hash_token(unsub), subscriber_id, self.clock()))
        return unsub

    def queue_announcement(self, kind: str, dry_run: bool = False) -> int:
        """Queue one mail of this kind for every confirmed, still subscribed
        address that has not had it and has none waiting. Returns how many."""
        now = self.clock()
        with closing(self._connect()) as conn, conn:
            ids = [r[0] for r in conn.execute(
                "SELECT id FROM subscribers s WHERE confirmed_at IS NOT NULL"
                " AND unsubscribed_at IS NULL"
                " AND NOT EXISTS (SELECT 1 FROM announcements a"
                "                 WHERE a.subscriber_id = s.id AND a.kind = ?)"
                " AND NOT EXISTS (SELECT 1 FROM jobs j"
                "                 WHERE j.subscriber_id = s.id AND j.kind = ?)",
                (kind, kind)).fetchall()]
            if not dry_run:
                conn.executemany("INSERT INTO jobs (kind, subscriber_id, created_at, next_at)"
                                 " VALUES (?, ?, ?, ?)", [(kind, i, now, now) for i in ids])
        return len(ids)

    def forget_unsub(self, raw: str) -> None:
        """The mail carrying this link never left."""
        with closing(self._connect()) as conn, conn:
            conn.execute("DELETE FROM unsub_tokens WHERE hash = ?", (hash_token(raw),))

    def job_sent(self, job_id: int) -> None:
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT subscriber_id, kind FROM jobs WHERE id = ?",
                               (job_id,)).fetchone()
            if row and row["kind"] != "confirm":
                conn.execute("INSERT OR IGNORE INTO announcements (subscriber_id, kind, at)"
                             " VALUES (?, ?, ?)", (row["subscriber_id"], row["kind"], self.clock()))
            conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))

    def job_failed(self, job_id: int, error: str, retry_in: float) -> None:
        with closing(self._connect()) as conn, conn:
            conn.execute("UPDATE jobs SET attempts = attempts + 1, next_at = ?, last_error = ?"
                         " WHERE id = ?", (self.clock() + retry_in, error[:300], job_id))

    def job_dropped(self, job_id: int) -> None:
        """The address was refused for good: forget the job and the pending entry."""
        with closing(self._connect()) as conn, conn:
            row = conn.execute("SELECT subscriber_id FROM jobs WHERE id = ?", (job_id,)).fetchone()
            conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
            if row:
                conn.execute("DELETE FROM subscribers WHERE id = ? AND confirmed_at IS NULL",
                             (row[0],))

    # links

    def _by_confirm(self, conn, raw):
        if not well_formed(raw):
            return None
        return conn.execute("SELECT * FROM subscribers WHERE confirm_hash = ?",
                            (hash_token(raw),)).fetchone()

    def _confirm_state(self, row) -> str:
        if row["confirmed_at"] is not None:
            return "already"
        if row["confirm_expires_at"] is None or row["confirm_expires_at"] < self.clock():
            return "expired"
        return "pending"

    def check_confirm(self, raw) -> tuple[str, str | None]:
        with closing(self._connect()) as conn:
            row = self._by_confirm(conn, raw)
            if row is None or row["unsubscribed_at"] is not None:
                return "invalid", None
            return self._confirm_state(row), row["lang"]

    def confirm(self, raw, news: bool = False) -> tuple[str, str | None]:
        """Confirm the address. news is the optional "occasional news" box of
        the confirmation page, the only place that choice is made."""
        with closing(self._connect()) as conn, conn:
            conn.execute("BEGIN IMMEDIATE")
            row = self._by_confirm(conn, raw)
            if row is None or row["unsubscribed_at"] is not None:
                return "invalid", None
            state = self._confirm_state(row)
            if state != "pending":
                return state, row["lang"]
            conn.execute("UPDATE subscribers SET confirmed_at = ?, news = ? WHERE id = ?",
                         (self.clock(), int(bool(news)), row["id"]))
            conn.execute("DELETE FROM jobs WHERE subscriber_id = ?", (row["id"],))
            return "confirmed", row["lang"]

    def _by_unsub(self, conn, raw):
        if not well_formed(raw):
            return None
        return conn.execute(
            "SELECT s.* FROM unsub_tokens u JOIN subscribers s ON s.id = u.subscriber_id"
            " WHERE u.hash = ?", (hash_token(raw),)).fetchone()

    def _unsub_state(self, row) -> str:
        return "already" if row["unsubscribed_at"] is not None else "active"

    def check_unsubscribe(self, raw) -> tuple[str, str | None]:
        with closing(self._connect()) as conn:
            row = self._by_unsub(conn, raw)
            if row is None:
                return "invalid", None
            return self._unsub_state(row), row["lang"]

    def unsubscribe(self, raw) -> tuple[str, str | None]:
        with closing(self._connect()) as conn, conn:
            conn.execute("BEGIN IMMEDIATE")
            row = self._by_unsub(conn, raw)
            if row is None:
                return "invalid", None
            if row["unsubscribed_at"] is not None:
                return "already", row["lang"]
            conn.execute("UPDATE subscribers SET unsubscribed_at = ?, confirmed_at = NULL,"
                         " news = 0, confirm_hash = NULL, confirm_expires_at = NULL WHERE id = ?",
                         (self.clock(), row["id"]))
            conn.execute("DELETE FROM jobs WHERE subscriber_id = ?", (row["id"],))
            return "done", row["lang"]

    # housekeeping and launch day

    def purge(self) -> dict:
        now = self.clock()
        out = {}
        with closing(self._connect()) as conn, conn:
            stale = [r[0] for r in conn.execute(
                "SELECT subscriber_id FROM jobs WHERE created_at < ?", (now - JOB_MAX_AGE,))]
            conn.execute("DELETE FROM jobs WHERE created_at < ?", (now - JOB_MAX_AGE,))
            out["stale_jobs"] = len(stale)
            for sid in stale:
                conn.execute("DELETE FROM subscribers WHERE id = ? AND confirmed_at IS NULL",
                             (sid,))
            out["expired_pending"] = conn.execute(
                "DELETE FROM subscribers WHERE confirmed_at IS NULL AND unsubscribed_at IS NULL"
                " AND NOT EXISTS (SELECT 1 FROM jobs WHERE jobs.subscriber_id = subscribers.id)"
                " AND coalesce(confirm_expires_at, created_at + ?) < ?",
                (CONFIRM_TTL, now)).rowcount
            out["unsubscribed"] = conn.execute(
                "DELETE FROM subscribers WHERE unsubscribed_at < ?",
                (now - KEEP_UNSUBSCRIBED,)).rowcount
            conn.execute("DELETE FROM confirm_log WHERE at < ?", (now - 24 * 3600,))
        return out

    def counts(self) -> dict:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT"
                " sum(confirmed_at IS NULL AND unsubscribed_at IS NULL),"
                " sum(confirmed_at IS NOT NULL),"
                " sum(unsubscribed_at IS NOT NULL) FROM subscribers").fetchone()
        return {"pending": row[0] or 0, "confirmed": row[1] or 0, "unsubscribed": row[2] or 0}

    def confirmed(self) -> list[dict]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                "SELECT email, lang, news, confirmed_at FROM subscribers"
                " WHERE confirmed_at IS NOT NULL ORDER BY confirmed_at").fetchall()
        return [{"email": r["email"], "lang": r["lang"], "news": bool(r["news"]),
                 "confirmed_at": r["confirmed_at"]} for r in rows]

    def delete(self, email: str) -> bool:
        email = normalise_email(email)
        if email is None:
            return False
        with closing(self._connect()) as conn, conn:
            return conn.execute("DELETE FROM subscribers WHERE email = ?", (email,)).rowcount > 0
