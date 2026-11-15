import contextlib
import csv
import io
import os
import unittest

from raye_site import admin
from raye_site.config import Config
from raye_site.store import Store

from helpers import Clock, TempDir


class AdminTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.db = os.path.join(self.tmp, "site.db")
        self.store = Store(self.db, clock=Clock())
        self.store.init()
        for email, lang in (("a@x.ca", "fr"), ("=cmd@x.ca", "en"), ("p@x.ca", "fr")):
            self.store.subscribe(email, lang)
        for job in self.store.jobs_due():
            confirm, _ = self.store.issue_tokens(job.subscriber_id)
            self.store.job_sent(job.id)
            if job.email != "p@x.ca":
                self.store.confirm(confirm, news=job.lang == "en")

    def tearDown(self):
        self.tmpctx.__exit__(None, None, None)

    def run_cli(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = admin.main(["--db", self.db, *args])
        return code, out.getvalue(), err.getvalue()

    def test_count(self):
        code, out, _ = self.run_cli("count")
        self.assertEqual(code, 0)
        self.assertIn("confirmed: 2", out)
        self.assertIn("pending: 1", out)
        self.assertIn("queued mails: 0", out)

    def test_list(self):
        code, out, _ = self.run_cli("list")
        self.assertEqual(code, 0)
        self.assertIn("a@x.ca", out)
        self.assertNotIn("p@x.ca", out)

    def test_export_csv_is_safe_for_spreadsheets(self):
        code, out, _ = self.run_cli("export")
        rows = list(csv.reader(io.StringIO(out)))
        self.assertEqual(rows[0], ["email", "lang", "news", "confirmed_at"])
        emails = sorted(r[0] for r in rows[1:])
        self.assertEqual(emails, ["'=cmd@x.ca", "a@x.ca"])
        news = {r[0]: r[2] for r in rows[1:]}
        self.assertEqual(news["'=cmd@x.ca"], "yes")

    def test_delete(self):
        code, out, _ = self.run_cli("delete", "A@x.ca")
        self.assertEqual(code, 0)
        self.assertIn("deleted", out)
        code, out, err = self.run_cli("delete", "a@x.ca")
        self.assertEqual(code, 1)
        self.assertIn("not found", err)

    def test_purge_command(self):
        code, out, _ = self.run_cli("purge")
        self.assertEqual(code, 0)
        self.assertIn("stale_jobs", out)

    def test_no_command(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                admin.main(["--db", self.db])


class ConfigTests(unittest.TestCase):
    def test_from_env(self):
        env = {
            "RAYE_SITE_DB": "/x/site.db",
            "RAYE_SITE_URL": "https://rayelinux.com/",
            "RAYE_SITE_PORT": "9000",
            "CREDENTIALS_DIRECTORY": "/run/creds",
        }
        cfg = Config.from_env(env)
        self.assertEqual(cfg.db_path, "/x/site.db")
        self.assertEqual(cfg.site_url, "https://rayelinux.com")
        self.assertEqual(cfg.listen_port, 9000)
        self.assertEqual(cfg.listen_host, "127.0.0.1")
        self.assertIn("/run/creds/smtp_smtp.env", cfg.smtp_env_paths)
        self.assertEqual(cfg.smtp_tls_name, "mail.example.org")

    def test_defaults_and_state_directory(self):
        cfg = Config.from_env({"STATE_DIRECTORY": "/var/lib/raye-site"})
        self.assertEqual(cfg.db_path, "/var/lib/raye-site/site.db")
        self.assertEqual(cfg.smtp_env_paths, ("/etc/raye-site/smtp.env",))

    def test_listen_host_must_be_loopback(self):
        with self.assertRaises(ValueError):
            Config.from_env({"RAYE_SITE_HOST": "0.0.0.0"})

    def test_site_url_must_be_https(self):
        with self.assertRaises(ValueError):
            Config.from_env({"RAYE_SITE_URL": "http://rayelinux.com"})


if __name__ == "__main__":
    unittest.main()
