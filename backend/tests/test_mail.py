import logging
import os
import unittest

from raye_site import mailer
from raye_site.emails import build_confirmation
from raye_site.mailer import Worker, load_smtp_settings
from raye_site.store import Store

from helpers import Clock, FakeSMTP, TempDir, make_certs, make_config, write_smtp_env

CONFIRM = "https://www.rayelinux.com/api/confirm?t=AAA"
UNSUB = "https://www.rayelinux.com/api/unsubscribe?t=BBB"
SENDER = "Raye Linux <bonjour@rayelinux.com>"


class EmailTests(unittest.TestCase):
    def test_french_mail(self):
        msg = build_confirmation("marie@x.ca", "fr", CONFIRM, UNSUB, SENDER)
        self.assertEqual(msg["To"], "marie@x.ca")
        self.assertEqual(msg["From"], SENDER)
        self.assertIn("Confirmez", msg["Subject"])
        self.assertEqual(msg["List-Unsubscribe-Post"], "List-Unsubscribe=One-Click")
        lu = msg["List-Unsubscribe"]
        self.assertIn("<mailto:bonjour@rayelinux.com?subject=unsubscribe>", lu)
        self.assertIn(f"<{UNSUB}>", lu)
        self.assertTrue(msg["Message-ID"].endswith("@rayelinux.com>"))
        self.assertTrue(msg.is_multipart())
        text = msg.get_body(("plain",)).get_content()
        html = msg.get_body(("html",)).get_content()
        self.assertIn(CONFIRM, text)
        self.assertIn(UNSUB, text)
        self.assertIn("48 heures", text)
        self.assertIn("En confirmant, vous acceptez de recevoir un seul courriel", text)
        self.assertIn("nouvelles", text)
        self.assertIn('href="https://www.rayelinux.com/api/confirm?t=AAA"', html)
        self.assertIn('lang="fr"', html)
        self.assertNotIn("<img", html)
        self.assertNotIn("http://", html)
        self.assertNotIn("<script", html.lower())

    def test_english_mail(self):
        msg = build_confirmation("joe@x.ca", "en", CONFIRM, UNSUB, SENDER)
        self.assertIn("Confirm", msg["Subject"])
        text = msg.get_body(("plain",)).get_content()
        self.assertIn("48 hours", text)
        self.assertIn("By confirming, you agree to get one email", text)
        self.assertIn('lang="en"', msg.get_body(("html",)).get_content())

    def test_urls_are_escaped_in_html(self):
        msg = build_confirmation("joe@x.ca", "en", 'https://x/"><b>', UNSUB, SENDER)
        html = msg.get_body(("html",)).get_content()
        self.assertNotIn('"><b>', html)
        self.assertIn("&quot;&gt;&lt;b&gt;", html)

    def test_header_injection_refused(self):
        with self.assertRaises(ValueError):
            build_confirmation("a@x.ca\r\nBcc: evil@y.ca", "fr", CONFIRM, UNSUB, SENDER)
        with self.assertRaises(ValueError):
            build_confirmation("a@x.ca", "fr", CONFIRM, UNSUB, "Raye <b@x.ca>\nBcc: e@y.ca")


class SettingsTests(unittest.TestCase):
    def test_load(self):
        with TempDir() as tmp:
            p = os.path.join(tmp, "smtp.env")
            self.assertIsNone(load_smtp_settings([p]))
            write_smtp_env(p, port=587)
            s = load_smtp_settings([os.path.join(tmp, "nope"), p])
            self.assertEqual((s.host, s.port, s.user), ("127.0.0.1", 587, "bonjour@rayelinux.com"))
            self.assertEqual(s.password, "s3cret-pass")
            self.assertEqual(s.sender, SENDER)
            self.assertNotIn("s3cret", repr(s))

    def test_incomplete_or_bad(self):
        with TempDir() as tmp:
            p = os.path.join(tmp, "smtp.env")
            with open(p, "w") as f:
                f.write("SMTP_HOST=x\nSMTP_PORT=587\n")
            self.assertIsNone(load_smtp_settings([p]))
            with open(p, "w") as f:
                f.write("SMTP_HOST=x\nSMTP_PORT=abc\nSMTP_USER=u\nSMTP_PASSWORD=p\n")
            self.assertIsNone(load_smtp_settings([p]))
            with open(p, "w") as f:
                f.write("export SMTP_HOST=x\nSMTP_PORT=587\nSMTP_USER=u\nSMTP_PASSWORD=p\n"
                        "garbage line\n")
            s = load_smtp_settings([p])
            self.assertEqual(s.host, "x")
            self.assertEqual(s.sender, "Raye Linux <bonjour@rayelinux.com>")


class WorkerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.certdir = TempDir()
        folder = cls.certdir.__enter__()
        cls.ca, cls.cert, cls.key = make_certs(folder)

    @classmethod
    def tearDownClass(cls):
        cls.certdir.__exit__(None, None, None)

    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.config = make_config(self.tmp, smtp_cafile=self.ca)
        self.store = Store(self.config.db_path, clock=self.clock)
        self.store.init()

    def tearDown(self):
        self.tmpctx.__exit__(None, None, None)

    def worker(self, **over):
        cfg = make_config(self.tmp, smtp_cafile=self.ca, **over)
        return Worker(self.store, cfg, clock=self.clock)

    def test_missing_credentials_keeps_mail_and_logs_retry(self):
        self.store.subscribe("a@x.ca", "fr")
        with self.assertLogs("raye_site.mailer", level="INFO") as logs:
            out = self.worker().process_once()
        self.assertEqual(out, {"sent": 0, "retry": 1, "dropped": 0})
        self.assertIn("retry in 300 s", "\n".join(logs.output))
        self.assertNotIn("a@x.ca", "\n".join(logs.output))
        self.assertEqual(self.store.queue_size(), 1)
        self.assertEqual(self.store.jobs_due(), [])

    def test_sends_over_starttls_after_credentials_arrive(self):
        self.store.subscribe("a@x.ca", "en")
        self.worker().process_once()
        with FakeSMTP(self.cert, self.key) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            self.clock.advance(301)
            out = self.worker().process_once()
        self.assertEqual(out["sent"], 1)
        self.assertEqual(self.store.queue_size(), 0)
        self.assertEqual(smtp.auth_ok, [("bonjour@rayelinux.com", True)])
        sent = smtp.messages[0]
        self.assertTrue(sent["tls"])
        self.assertEqual(sent["rcpts"], ["<a@x.ca>"])
        self.assertIn("bonjour@rayelinux.com", sent["from"])
        text = sent["msg"].get_body(("plain",)).get_content()
        token = text.split("/api/confirm?t=")[1].split()[0]
        self.assertEqual(self.store.confirm(token), ("confirmed", "en"))

    def test_wrong_certificate_name_is_refused(self):
        self.store.subscribe("a@x.ca", "fr")
        with FakeSMTP(self.cert, self.key) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            with self.assertLogs("raye_site.mailer", level="WARNING"):
                out = self.worker(smtp_tls_name="other.example").process_once()
        self.assertEqual(out["retry"], 1)
        self.assertEqual(smtp.auth_ok, [])
        self.assertEqual(self.store.queue_size(), 1)

    def test_no_starttls_means_no_password_in_clear(self):
        self.store.subscribe("a@x.ca", "fr")
        with FakeSMTP(offer_tls=False) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            with self.assertLogs("raye_site.mailer", level="WARNING"):
                out = self.worker().process_once()
        self.assertEqual(out["retry"], 1)
        self.assertEqual(smtp.auth_ok, [])

    def test_bad_password_retries_with_backoff(self):
        self.store.subscribe("a@x.ca", "fr")
        with FakeSMTP(self.cert, self.key, password="other") as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            with self.assertLogs("raye_site.mailer", level="WARNING") as logs:
                self.worker().process_once()
                self.clock.advance(61)
                self.worker().process_once()
        joined = "\n".join(logs.output)
        self.assertIn("retry in 60 s", joined)
        self.assertIn("retry in 120 s", joined)
        self.assertNotIn("s3cret", joined)
        self.assertEqual(smtp.messages, [])

    def test_refused_recipient_is_dropped(self):
        self.store.subscribe("a@x.ca", "fr")
        with FakeSMTP(self.cert, self.key, reject_rcpt=True) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            with self.assertLogs("raye_site.mailer", level="WARNING"):
                out = self.worker().process_once()
        self.assertEqual(out["dropped"], 1)
        self.assertEqual(self.store.counts()["pending"], 0)

    def test_backoff_is_capped(self):
        self.assertEqual(mailer.backoff(0), 60)
        self.assertEqual(mailer.backoff(3), 480)
        self.assertEqual(mailer.backoff(30), 3600)

    def test_thread_runs_and_stops(self):
        w = self.worker()
        w.poll_seconds = 0.05
        logging.getLogger("raye_site.mailer").setLevel(logging.ERROR)
        try:
            w.start()
            w.wake()
            w.stop()
        finally:
            logging.getLogger("raye_site.mailer").setLevel(logging.NOTSET)
        self.assertFalse(w.thread.is_alive())


if __name__ == "__main__":
    unittest.main()


class LaunchMailTests(WorkerTests):
    """The one launch email promised at signup."""

    def confirmed(self, email, lang):
        self.store.subscribe(email, lang)
        with FakeSMTP(self.cert, self.key) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            self.worker().process_once()
        text = smtp.messages[-1]["msg"].get_body(("plain",)).get_content()
        self.assertEqual(self.store.confirm(text.split("/api/confirm?t=")[1].split()[0])[0],
                         "confirmed")

    def test_queued_once_for_confirmed_only_and_sent_with_unsubscribe(self):
        self.confirmed("a@x.ca", "fr")
        self.store.subscribe("pending@x.ca", "en")        # never confirmed
        self.clock.advance(1)
        self.assertEqual(self.store.queue_announcement("launch", dry_run=True), 1)
        self.assertEqual(self.store.queue_announcement("launch"), 1)
        self.assertEqual(self.store.queue_announcement("launch"), 0)   # already waiting
        with FakeSMTP(self.cert, self.key) as smtp:
            write_smtp_env(os.path.join(self.tmp, "smtp.env"), port=smtp.port)
            self.worker().process_once()
        launch = [m for m in smtp.messages if "bêta publique" in str(m["msg"]["Subject"])]
        self.assertEqual([m["rcpts"] for m in launch], [["<a@x.ca>"]])
        text = launch[0]["msg"].get_body(("plain",)).get_content()
        self.assertIn("https://www.rayelinux.com/fr/telecharger/", text)
        self.assertNotIn("/api/confirm?t=", text)
        self.assertIn("List-Unsubscribe", launch[0]["msg"])
        token = text.split("/api/unsubscribe?t=")[1].split()[0]
        self.assertEqual(self.store.queue_announcement("launch"), 0)   # sent: never again
        self.assertEqual(self.store.unsubscribe(token)[0], "done")
