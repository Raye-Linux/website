import os
import sqlite3
import unittest

from raye_site import store as st
from raye_site.store import Store
from raye_site.tokens import hash_token

from helpers import Clock, TempDir

HOUR = 3600
DAY = 24 * HOUR


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TempDir()
        path = self.tmp.__enter__()
        self.clock = Clock()
        self.db = os.path.join(path, "site.db")
        self.store = Store(self.db, clock=self.clock)
        self.store.init()

    def tearDown(self):
        self.tmp.__exit__(None, None, None)

    def rows(self, sql, *args):
        with sqlite3.connect(self.db) as c:
            return c.execute(sql, args).fetchall()

    def send_first(self):
        job = self.store.jobs_due()[0]
        confirm, unsub = self.store.issue_tokens(job.subscriber_id)
        self.store.job_sent(job.id)
        return job, confirm, unsub

    # signup and queue

    def test_new_signup_is_queued_once(self):
        self.assertTrue(self.store.subscribe("a@x.ca", "fr"))
        # a second signup while the first mail is still waiting adds nothing,
        # and someone else typing the address cannot change its choices
        self.assertFalse(self.store.subscribe("a@x.ca", "en"))
        jobs = self.store.jobs_due()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].email, "a@x.ca")
        self.assertEqual(jobs[0].lang, "fr")
        row = self.rows("SELECT lang, news, consent_version, confirmed_at FROM subscribers")[0]
        self.assertEqual(row, ("fr", 0, st.CONSENT_VERSION, None))

    def test_no_ip_and_no_raw_token_stored(self):
        self.store.subscribe("a@x.ca", "fr")
        job, confirm, unsub = self.send_first()
        cols = [r[1] for r in self.rows("PRAGMA table_info(subscribers)")]
        self.assertNotIn("ip", cols)
        dump = "\n".join(sqlite3.connect(self.db).iterdump())
        self.assertNotIn(confirm, dump)
        self.assertNotIn(unsub, dump)
        self.assertIn(hash_token(confirm), dump)

    def test_confirm_flow(self):
        self.store.subscribe("a@x.ca", "en")
        _, confirm, _ = self.send_first()
        self.assertEqual(self.store.check_confirm(confirm), ("pending", "en"))
        self.assertEqual(self.store.confirm(confirm, news=True), ("confirmed", "en"))
        self.assertEqual(self.store.confirm(confirm, news=False), ("already", "en"))
        self.assertEqual(self.store.check_confirm(confirm), ("already", "en"))
        confirmed = self.store.confirmed()
        self.assertEqual([r["email"] for r in confirmed], ["a@x.ca"])
        self.assertTrue(confirmed[0]["news"])  # a second click does not change it

    def test_news_is_off_unless_asked_at_confirmation(self):
        self.store.subscribe("a@x.ca", "fr")
        _, confirm, _ = self.send_first()
        self.store.confirm(confirm)
        self.assertFalse(self.store.confirmed()[0]["news"])

    def test_bad_tokens(self):
        for bad in ("", "x", "a" * 400, None, "../../etc"):
            self.assertEqual(self.store.check_confirm(bad), ("invalid", None))
            self.assertEqual(self.store.confirm(bad), ("invalid", None))
            self.assertEqual(self.store.check_unsubscribe(bad), ("invalid", None))
            self.assertEqual(self.store.unsubscribe(bad), ("invalid", None))

    def test_confirmation_link_expires_after_48h(self):
        self.store.subscribe("a@x.ca", "fr")
        _, confirm, _ = self.send_first()
        self.clock.advance(48 * HOUR + 1)
        self.assertEqual(self.store.check_confirm(confirm), ("expired", "fr"))
        self.assertEqual(self.store.confirm(confirm), ("expired", "fr"))
        self.assertEqual(self.store.confirmed(), [])

    def test_resend_limit_three_per_day(self):
        self.store.subscribe("a@x.ca", "fr")
        self.send_first()
        self.assertTrue(self.store.subscribe("a@x.ca", "fr"))
        self.send_first()
        self.assertTrue(self.store.subscribe("a@x.ca", "fr"))
        self.send_first()
        # fourth request in 24 h: silently nothing
        self.assertFalse(self.store.subscribe("a@x.ca", "fr"))
        self.assertEqual(self.store.jobs_due(), [])
        self.clock.advance(DAY + 1)
        self.store.purge()
        # a day later the address may ask again
        self.assertTrue(self.store.subscribe("a@x.ca", "fr"))

    def test_new_token_replaces_old(self):
        self.store.subscribe("a@x.ca", "fr")
        _, first, _ = self.send_first()
        self.store.subscribe("a@x.ca", "fr")
        _, second, _ = self.send_first()
        self.assertEqual(self.store.check_confirm(first), ("invalid", None))
        self.assertEqual(self.store.confirm(second), ("confirmed", "fr"))

    def test_confirmed_address_is_not_mailed_again(self):
        self.store.subscribe("a@x.ca", "fr")
        _, confirm, _ = self.send_first()
        self.store.confirm(confirm)
        self.assertFalse(self.store.subscribe("a@x.ca", "en"))
        self.assertEqual(self.store.jobs_due(), [])
        # and its choices are not changed by an unverified request
        row = self.rows("SELECT lang, news FROM subscribers")[0]
        self.assertEqual(row, ("fr", 0))

    def test_unsubscribe_then_resubscribe(self):
        self.store.subscribe("a@x.ca", "fr")
        _, confirm, unsub = self.send_first()
        self.store.confirm(confirm, news=True)
        self.assertEqual(self.store.check_unsubscribe(unsub), ("active", "fr"))
        self.assertEqual(self.store.unsubscribe(unsub), ("done", "fr"))
        self.assertEqual(self.store.unsubscribe(unsub), ("already", "fr"))
        self.assertEqual(self.store.confirmed(), [])
        self.assertEqual(self.store.counts()["unsubscribed"], 1)
        # coming back means a fresh double opt-in; the language stays, news is off
        self.assertTrue(self.store.subscribe("a@x.ca", "en"))
        self.assertEqual(self.store.counts(), {"pending": 1, "confirmed": 0, "unsubscribed": 0})
        self.assertEqual(self.rows("SELECT lang, news FROM subscribers")[0], ("fr", 0))
        self.assertEqual(self.store.check_unsubscribe(unsub)[0], "invalid")

    def test_unsubscribe_from_confirmation_mail_while_pending(self):
        self.store.subscribe("a@x.ca", "fr")
        _, confirm, unsub = self.send_first()
        self.assertEqual(self.store.unsubscribe(unsub), ("done", "fr"))
        self.assertEqual(self.store.confirm(confirm), ("invalid", None))

    def test_job_failure_backoff(self):
        self.store.subscribe("a@x.ca", "fr")
        job = self.store.jobs_due()[0]
        self.store.job_failed(job.id, "boom", retry_in=600)
        self.assertEqual(self.store.jobs_due(), [])
        self.clock.advance(601)
        again = self.store.jobs_due()
        self.assertEqual(again[0].attempts, 1)
        self.assertEqual(self.store.queue_size(), 1)

    def test_job_dropped_removes_pending(self):
        self.store.subscribe("a@x.ca", "fr")
        job = self.store.jobs_due()[0]
        self.store.job_dropped(job.id)
        self.assertEqual(self.store.counts()["pending"], 0)
        self.assertEqual(self.store.queue_size(), 0)

    def test_job_for_confirmed_or_gone_subscriber_is_skipped(self):
        self.store.subscribe("a@x.ca", "fr")
        self.store.delete("a@x.ca")
        self.assertEqual(self.store.jobs_due(), [])

    def test_failed_issue_cleanup(self):
        self.store.subscribe("a@x.ca", "fr")
        job = self.store.jobs_due()[0]
        confirm, unsub = self.store.issue_tokens(job.subscriber_id)
        self.store.forget_unsub(unsub)
        self.assertEqual(self.store.check_unsubscribe(unsub), ("invalid", None))

    def test_purge(self):
        # old unsent job: dropped with its pending entry after 7 days
        self.store.subscribe("old@x.ca", "fr")
        # unsubscribed: kept 30 days then gone
        self.store.subscribe("gone@x.ca", "fr")
        jobs = {j.email: j for j in self.store.jobs_due()}
        confirm, unsub = self.store.issue_tokens(jobs["gone@x.ca"].subscriber_id)
        self.store.job_sent(jobs["gone@x.ca"].id)
        self.store.confirm(confirm)
        self.store.unsubscribe(unsub)
        # confirmed: kept
        self.store.subscribe("keep@x.ca", "fr")
        job = [j for j in self.store.jobs_due() if j.email == "keep@x.ca"][0]
        c2, _ = self.store.issue_tokens(job.subscriber_id)
        self.store.job_sent(job.id)
        self.store.confirm(c2)

        self.clock.advance(8 * DAY)
        out = self.store.purge()
        self.assertEqual(out["stale_jobs"], 1)
        self.assertEqual(self.store.counts(), {"pending": 0, "confirmed": 1, "unsubscribed": 1})
        self.clock.advance(31 * DAY)
        self.store.purge()
        self.assertEqual(self.store.counts(), {"pending": 0, "confirmed": 1, "unsubscribed": 0})
        self.assertEqual(self.rows("SELECT count(*) FROM unsub_tokens")[0][0], 1)

    def test_orphan_pending_without_job_purged(self):
        self.store.subscribe("a@x.ca", "fr")
        job = self.store.jobs_due()[0]
        self.store.issue_tokens(job.subscriber_id)
        self.store.job_sent(job.id)
        self.clock.advance(49 * HOUR)
        self.assertEqual(self.store.purge()["expired_pending"], 1)

    def test_delete(self):
        self.store.subscribe("a@x.ca", "fr")
        self.assertTrue(self.store.delete(" A@X.ca "))
        self.assertFalse(self.store.delete("a@x.ca"))
        self.assertFalse(self.store.delete("not an email"))
        self.assertEqual(self.store.queue_size(), 0)

    def test_hourly_queue_count(self):
        for i in range(3):
            self.store.subscribe(f"a{i}@x.ca", "fr")
        self.assertEqual(self.store.queued_last_hour(), 3)
        self.clock.advance(HOUR + 1)
        self.assertEqual(self.store.queued_last_hour(), 0)

    def test_init_is_idempotent_and_private(self):
        self.store.init()
        mode = os.stat(self.db).st_mode & 0o777
        self.assertEqual(mode & 0o077, 0)


if __name__ == "__main__":
    unittest.main()
