"""The "Join the team" applications: what a form must hold, what is kept,
the limits, the staff channel, and that a Discord outage loses nothing."""

import http.client
import io
import json
import logging
import os
import sqlite3
import threading
import unittest
import urllib.error
import urllib.parse

from raye_site import applications as apps
from raye_site import server as srv
from raye_site.store import Store

from helpers import Clock, TempDir, make_config

HOOK = "https://discord.com/api/webhooks/123456789012345678/" + "S" * 68


def good(**over):
    fields = {"role": "beta", "lang": "en", "email": "Ana@Example.org", "discord": "@ana.tests",
              "languages": "English, French", "skills": "I test software on two laptops.",
              "why": "I have used Raye since the first beta and I want to help find bugs.",
              "consent": True}
    fields.update(over)
    return fields


class FakeResponse:
    def __init__(self, status, body=b"{}"):
        self.status = status
        self.body = body

    def read(self, n=-1):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeOpener:
    """Records the requests; answers with `status`, or raises."""

    def __init__(self, status=200, body=b"{}", fail=None):
        self.status, self.body, self.fail = status, body, fail
        self.requests = []

    def open(self, req, timeout=None):
        self.requests.append(req)
        if self.fail == "http":
            raise urllib.error.HTTPError(req.full_url, 500, "boom", {}, io.BytesIO(b"no"))
        if self.fail == "net":
            raise OSError("unreachable")
        return FakeResponse(self.status, self.body)


class ValidateTests(unittest.TestCase):
    def test_a_good_application_passes_and_is_cleaned(self):
        app = apps.validate(good())
        self.assertEqual(app["email"], "ana@example.org")
        self.assertEqual(app["discord"], "ana.tests")
        self.assertEqual(app["role"], "beta")
        self.assertIsNone(app["account_token"])

    def test_each_problem_has_its_own_code(self):
        cases = {
            "bad_role": good(role="admin"),
            "email": good(email="not an address"),
            "discord": good(discord="a"),
            "why_short": good(why="Because."),
            "consent": good(consent=False),
            "languages": good(role="translator", languages=""),
            "links": good(why="see http://a.example http://b.example http://c.example "
                              "and www.d.example for my work please"),
            "too_long": good(why="x" * (apps.WHY_MAX + 1)),
            "bad_request": good(skills=["not", "text"]),
        }
        for code, fields in cases.items():
            with self.subTest(code=code):
                with self.assertRaises(ValueError) as ctx:
                    apps.validate(fields)
                self.assertEqual(str(ctx.exception), code)

    def test_discord_names(self):
        ok = {"Ana.Tests": "ana.tests", "@bob_99": "bob_99", "Old Name#1234": "Old Name#1234"}
        for raw, want in ok.items():
            with self.subTest(raw=raw):
                self.assertEqual(apps.discord_name(raw), want)
        for raw in ("a", "two..dots", "x" * 33, "name#0000", "has space", "@everyone#12",
                    "<@123>", None, 5):
            with self.subTest(raw=raw):
                self.assertIsNone(apps.discord_name(raw))

    def test_text_cannot_ping_on_discord(self):
        app = apps.validate(good(why="@everyone look at me, I really want to help with tests"))
        self.assertNotIn("@everyone", app["why"])

    def test_every_role_maps_to_a_discord_role_key(self):
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "tools",
                               "site_v1_join_text.py"), encoding="utf-8") as f:
            text = f.read()
        for role in apps.DISCORD_ROLES:
            with self.subTest(role=role):
                self.assertIn(f'"{role}"', text)
                self.assertIn(role, apps.ROLE_NAMES)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.store = apps.Store(os.path.join(self.tmp, "site.db"), self.clock)
        self.store.init()

    def tearDown(self):
        self.tmpctx.__exit__(None, None, None)

    def test_no_ip_address_column(self):
        with sqlite3.connect(self.store.path) as conn:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(applications)")]
        self.assertFalse([c for c in cols if "ip" in c.split("_")])
        self.assertIn("consent_version", cols)

    def test_the_same_person_is_not_doubled(self):
        ref, created = self.store.add(apps.validate(good()))
        self.assertTrue(created)
        again, created = self.store.add(apps.validate(good(discord="other_name")))
        self.assertEqual((again, created), (ref, False))
        # another role is another application
        _, created = self.store.add(apps.validate(good(role="translator")))
        self.assertTrue(created)

    def test_decide_then_give_the_role(self):
        ref, _ = self.store.add(apps.validate(good()))
        self.assertFalse(self.store.role_given(ref))           # not approved yet
        with self.assertRaises(ValueError):
            self.store.decide(ref, "approved", "")              # who decided is required
        self.assertTrue(self.store.decide(ref, "approved", "techoraye", "welcome"))
        self.assertFalse(self.store.decide(ref, "declined", "techoraye"))  # only once
        self.assertTrue(self.store.role_given(ref))
        row = self.store.get(ref)
        self.assertEqual((row["status"], row["decided_by"]), ("approved", "techoraye"))
        self.assertEqual(apps.DISCORD_ROLES[row["role"]], "beta_tester")

    def test_purge_keeps_approved_and_drops_old_decisions(self):
        approved, _ = self.store.add(apps.validate(good()))
        declined, _ = self.store.add(apps.validate(good(role="translator")))
        pending, _ = self.store.add(apps.validate(good(role="developer")))
        self.store.decide(approved, "approved", "t")
        self.store.decide(declined, "declined", "t")
        self.clock.advance(apps.KEEP_DECIDED + 1)
        self.assertEqual(self.store.purge(), {"decided": 1, "stale_pending": 0})
        self.clock.advance(apps.KEEP_PENDING)
        self.assertEqual(self.store.purge(), {"decided": 0, "stale_pending": 1})
        self.assertIsNotNone(self.store.get(approved))
        self.assertIsNone(self.store.get(pending))

    def test_forget_a_person(self):
        self.store.add(apps.validate(good()))
        self.store.add(apps.validate(good(role="moderator")))
        self.assertEqual(self.store.delete_person(email="ANA@example.org"), 2)
        self.assertEqual(self.store.counts()["pending"], 0)

    def test_get_refuses_a_malformed_reference(self):
        self.assertIsNone(self.store.get("' OR 1=1 --"))


class StaffChannelTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.store = apps.Store(os.path.join(self.tmp, "site.db"), self.clock)
        self.store.init()
        self.hookfile = os.path.join(self.tmp, "join-webhook")
        with open(self.hookfile, "w") as f:
            f.write(HOOK + "\n")

    def tearDown(self):
        self.tmpctx.__exit__(None, None, None)

    def make(self, opener):
        return apps.Applications(self.store, (self.hookfile,), self.clock, opener=opener,
                                 background=False)

    def test_message_has_no_email_and_cannot_ping(self):
        j = self.make(FakeOpener())
        j.submit(apps.validate(good(why="@here please read, I want to help with the beta")))
        body = j.opener.requests[0].data.decode()
        self.assertNotIn("ana@example.org", body)
        self.assertIn('"parse": []', body)
        self.assertNotIn("@here", body)
        self.assertIn("ana.tests", body)

    def test_discord_down_loses_nothing_and_is_retried(self):
        down = FakeOpener(fail="net")
        j = self.make(down)
        ref = j.submit(apps.validate(good()))
        row = self.store.get(ref)
        self.assertIsNotNone(row)                      # kept although Discord did not answer
        self.assertIsNone(row["notified_at"])
        self.assertEqual(row["notify_attempts"], 1)
        j.opener = FakeOpener()
        self.assertEqual(j.deliver_pending(), (0, 0))  # waits before trying again
        self.clock.advance(3600)
        self.assertEqual(j.deliver_pending(), (1, 0))
        self.assertIsNotNone(self.store.get(ref)["notified_at"])
        self.assertEqual(j.deliver_pending(), (0, 0))  # told once

    def test_an_http_error_is_a_failure_too(self):
        j = self.make(FakeOpener(fail="http"))
        ref = j.submit(apps.validate(good()))
        self.assertIsNone(self.store.get(ref)["notified_at"])

    def test_no_webhook_file_still_keeps_the_application(self):
        j = apps.Applications(self.store, (os.path.join(self.tmp, "missing"),), self.clock,
                              opener=FakeOpener(), background=False)
        ref = j.submit(apps.validate(good()))
        self.assertIsNotNone(self.store.get(ref))
        self.assertEqual(j.opener.requests, [])

    def test_a_file_that_is_not_a_webhook_is_ignored(self):
        with open(self.hookfile, "w") as f:
            f.write("https://evil.example/api/webhooks/1/abc\n")
        j = self.make(FakeOpener())
        j.submit(apps.validate(good()))
        self.assertEqual(j.opener.requests, [])

    def test_the_webhook_never_reaches_the_log(self):
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        root = logging.getLogger()
        root.addHandler(handler)
        old = root.level
        root.setLevel(logging.DEBUG)
        try:
            self.make(FakeOpener(fail="http")).submit(apps.validate(good()))
        finally:
            root.removeHandler(handler)
            root.setLevel(old)
        self.assertNotIn("S" * 20, stream.getvalue())
        self.assertNotIn("ana@example.org", stream.getvalue())
        self.assertIn("will retry", stream.getvalue())


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.store = apps.Store(os.path.join(self.tmp, "site.db"))
        self.store.init()

    def tearDown(self):
        self.tmpctx.__exit__(None, None, None)

    def test_accounts_off_means_email(self):
        j = apps.Applications(self.store, background=False)
        with self.assertRaises(ValueError) as ctx:
            j.submit(apps.validate(good(account_token="t" * 32, email=None)))
        self.assertEqual(str(ctx.exception), "account_unavailable")

    def test_a_signed_in_account_replaces_the_email(self):
        me = json.dumps({"id": "0b7f6f9e-1c1d-4a52-9c8e-3d8e2c9b0a11", "email": "ana@example.org",
                         "email_verified": True}).encode()
        opener = FakeOpener(body=me)
        j = apps.Applications(self.store, background=False,
                              accounts=apps.Accounts("https://account.example", opener))
        ref = j.submit(apps.validate(good(account_token="t" * 32, email=None)))
        row = self.store.get(ref)
        self.assertEqual(row["account_id"], "0b7f6f9e-1c1d-4a52-9c8e-3d8e2c9b0a11")
        self.assertIsNone(row["email"])
        self.assertEqual(opener.requests[0].get_header("Authorization"), "Bearer " + "t" * 32)

    def test_an_unconfirmed_account_is_refused(self):
        me = json.dumps({"id": "0b7f6f9e-1c1d", "email": "a@b.ca", "email_verified": False})
        j = apps.Applications(self.store, background=False, accounts=apps.Accounts(
            "https://account.example", FakeOpener(body=me.encode())))
        with self.assertRaises(ValueError) as ctx:
            j.submit(apps.validate(good(account_token="t" * 32, email=None)))
        self.assertEqual(str(ctx.exception), "account")


class JoinEndpointTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.config = make_config(self.tmp)
        self.store = Store(self.config.db_path, clock=self.clock)
        self.store.init()

        class FakeWorker:
            def wake(inner):
                pass

        self.httpd = srv.make_server(self.config, self.store, FakeWorker(), clock=self.clock)
        self.join = self.httpd.app.join
        self.join.background = False
        self.join.webhook = HOOK
        self.join.opener = FakeOpener()
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmpctx.__exit__(None, None, None)

    def post(self, fields, ip="203.0.113.9", form=False, raw=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        if form:
            body = urllib.parse.urlencode(fields)
            ctype = "application/x-www-form-urlencoded"
        else:
            body = raw if raw is not None else json.dumps(fields)
            ctype = "application/json"
        conn.request("POST", "/api/join", body=body,
                     headers={"Content-Type": ctype, "X-Real-IP": ip})
        r = conn.getresponse()
        data = r.read()
        conn.close()
        return r, data

    def test_an_application_is_stored_and_told(self):
        r, data = self.post(good())
        reply = json.loads(data)
        self.assertEqual(r.status, 200)
        self.assertTrue(reply["ok"])
        row = self.join.store.get(reply["reference"])
        self.assertEqual(row["discord"], "ana.tests")
        self.assertIsNotNone(row["notified_at"])
        self.assertNotIn(HOOK, data.decode())
        self.assertNotIn("S" * 20, data.decode())

    def test_errors_are_worded_in_the_page_language(self):
        r, data = self.post(good(lang="fr", discord="!"))
        reply = json.loads(data)
        self.assertEqual((r.status, reply["error"]), (400, "discord"))
        self.assertIn("Discord", reply["message"])
        self.assertIn("ne semble pas", reply["message"])

    def test_robots_get_the_same_answer_and_nothing_is_kept(self):
        r, data = self.post(good(website="http://spam.example"))
        self.assertEqual(r.status, 200)
        self.assertTrue(json.loads(data)["ok"])
        self.assertEqual(self.join.store.counts()["pending"], 0)
        self.assertEqual(self.join.opener.requests, [])

    def test_rate_limit_counts_only_real_applications(self):
        for _ in range(5):
            self.post(good(why="short"))                      # typos do not count
        for role in ("beta", "translator", "developer"):
            r, _ = self.post(good(role=role))
            self.assertEqual(r.status, 200)
        r, data = self.post(good(role="moderator"))
        self.assertEqual(r.status, 429)
        self.assertTrue(int(r.getheader("Retry-After")) > 0)
        self.assertEqual(json.loads(data)["error"], "rate")
        r, _ = self.post(good(role="moderator"), ip="198.51.100.4")   # someone else
        self.assertEqual(r.status, 200)

    def test_everyone_together_has_a_cap(self):
        self.join.everyone = apps.RateLimiter(2, 3600, self.clock)
        self.post(good(), ip="198.51.100.1")
        self.post(good(role="translator"), ip="198.51.100.2")
        r, _ = self.post(good(role="developer"), ip="198.51.100.3")
        self.assertEqual(r.status, 429)

    def test_webhook_failure_still_answers_ok_and_keeps_it(self):
        self.join.opener = FakeOpener(fail="http")
        r, data = self.post(good())
        self.assertEqual(r.status, 200)
        row = self.join.store.get(json.loads(data)["reference"])
        self.assertIsNone(row["notified_at"])

    def test_a_form_without_script_gets_a_page(self):
        r, data = self.post(good(consent="on"), form=True)
        self.assertEqual(r.status, 200)
        self.assertIn("text/html", r.getheader("Content-Type"))
        self.assertIn("Application sent", data.decode())
        r, data = self.post(good(consent=""), form=True)
        self.assertEqual(r.status, 400)
        self.assertIn("Something is missing", data.decode())

    def test_too_big_and_wrong_method(self):
        r, _ = self.post(None, raw="x" * (apps.MAX_BODY + 1))
        self.assertEqual(r.status, 413)
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request("GET", "/api/join")
        self.assertEqual(conn.getresponse().status, 405)
        conn.close()


if __name__ == "__main__":
    unittest.main()
