"""The staff panel: closed to everyone but staff, every action logged, notes
and states, nothing personal in the list or the log, deletion takes the
notes away."""

import http.client
import json
import os
import sqlite3
import threading
import unittest

from raye_site import applications as apps
from raye_site import server as srv
from raye_site import staff as st
from raye_site.store import Store

from helpers import Clock, TempDir, make_config
from test_applications import FakeOpener, good

TOKEN = "t0ken-" + "x" * 30
NAME = "Ana Staff"


class PanelTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.tokfile = os.path.join(self.tmp, "staff-token")
        with open(self.tokfile, "w", encoding="utf-8") as f:
            f.write(TOKEN + "\n")
        self.config = make_config(self.tmp, staff_token_paths=(self.tokfile,))
        self.store = Store(self.config.db_path, clock=self.clock)
        self.store.init()

        class FakeWorker:
            def wake(inner):
                pass

        self.httpd = srv.make_server(self.config, self.store, FakeWorker(), clock=self.clock)
        self.join = self.httpd.app.join
        self.join.background = False
        self.join.opener = FakeOpener()
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.ref = self.join.submit(apps.validate(good()))

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmpctx.__exit__(None, None, None)

    def call(self, method, path, body=None, token=TOKEN, name=NAME, ip="198.51.100.7",
             ctype="application/json"):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        headers = {"X-Real-IP": ip}
        if token is not None:
            headers["Authorization"] = "Bearer " + token
        if name:
            headers["X-Staff-Name"] = name
        data = None
        if body is not None:
            data = json.dumps(body)
            headers["Content-Type"] = ctype
        conn.request(method, path, body=data, headers=headers)
        r = conn.getresponse()
        raw = r.read()
        conn.close()
        try:
            return r, json.loads(raw)
        except ValueError:
            return r, raw

    # ---- closed to the public

    def test_every_data_route_refuses_without_the_token(self):
        for method, path in [("GET", "/api/staff/me"), ("GET", "/api/staff/applications"),
                             ("GET", "/api/staff/applications/" + self.ref),
                             ("GET", "/api/staff/log"),
                             ("POST", "/api/staff/applications/%s/state" % self.ref),
                             ("POST", "/api/staff/applications/%s/note" % self.ref)]:
            with self.subTest(path=path):
                r, j = self.call(method, path, {"action": "accepted"} if method == "POST" else None,
                                 token=None, ip="198.51.100.%d" % (hash(path) % 200 + 1))
                self.assertEqual(r.status, 401)
                self.assertEqual(j["error"], "denied")
                self.assertNotIn(self.ref, json.dumps(j))

    def test_wrong_token_is_the_same_answer_and_gets_limited(self):
        for _ in range(st.FAILS_PER_10_MIN):
            r, j = self.call("GET", "/api/staff/me", token="nope")
            self.assertEqual(r.status, 401)
        r, j = self.call("GET", "/api/staff/me", token="nope")
        self.assertEqual((r.status, j["error"]), (429, "limited"))
        # even the right token waits: the limit is about the visitor
        r, _ = self.call("GET", "/api/staff/me")
        self.assertEqual(r.status, 429)
        self.clock.advance(601)
        r, _ = self.call("GET", "/api/staff/me")
        self.assertEqual(r.status, 200)

    def test_good_use_is_never_limited(self):
        for _ in range(30):
            r, _ = self.call("GET", "/api/staff/me")
            self.assertEqual(r.status, 200)

    def test_a_name_is_required_with_the_token(self):
        r, j = self.call("GET", "/api/staff/me", name="")
        self.assertEqual((r.status, j["error"]), (400, "name"))
        r, j = self.call("GET", "/api/staff/me", name="a/b;c")
        self.assertEqual(r.status, 400)

    def test_no_token_file_switches_the_panel_off(self):
        os.remove(self.tokfile)
        self.httpd.app.staff.token = None
        r, j = self.call("GET", "/api/staff/me")
        self.assertEqual((r.status, j["error"]), (503, "staff_off"))

    def test_a_short_token_is_refused_at_load(self):
        with open(self.tokfile, "w", encoding="utf-8") as f:
            f.write("short")
        self.assertIsNone(st.load_token([self.tokfile]))

    def test_the_page_holds_no_data_and_is_not_indexed(self):
        r, body = self.call("GET", "/api/staff/panel", token=None)
        self.assertEqual(r.status, 200)
        self.assertIn(b"noindex", body)
        self.assertEqual(r.getheader("X-Robots-Tag"), "noindex, nofollow, noarchive")
        self.assertEqual(r.getheader("Cache-Control"), "no-store")
        csp = r.getheader("Content-Security-Policy")
        self.assertIn("script-src 'self'", csp)
        self.assertEqual(len(r.msg.get_all("Content-Security-Policy")), 1)
        self.assertNotIn(b"<script>", body)
        r, js = self.call("GET", "/api/staff/panel.js", token=None)
        self.assertEqual(r.status, 200)
        self.assertNotIn(b"innerHTML", js)

    def test_posts_must_be_json(self):
        r, _ = self.call("POST", "/api/staff/applications/%s/note" % self.ref,
                         {"text": "x"}, ctype="text/plain")
        self.assertEqual(r.status, 415)

    # ---- lists and detail

    def test_the_list_has_no_email_and_the_detail_is_logged(self):
        r, j = self.call("GET", "/api/staff/applications")
        self.assertEqual(r.status, 200)
        self.assertEqual(j["applications"][0]["ref"], self.ref)
        self.assertNotIn("ana@example.org", json.dumps(j))
        self.assertNotIn("why", j["applications"][0])
        r, j = self.call("GET", "/api/staff/applications/" + self.ref)
        self.assertEqual(j["application"]["email"], "ana@example.org")
        r, log = self.call("GET", "/api/staff/log")
        self.assertEqual(log["log"][0]["action"], "view")
        self.assertEqual(log["log"][0]["staff"], NAME)
        self.assertNotIn("ana@example.org", json.dumps(log))

    def test_unknown_reference_and_bad_state(self):
        r, _ = self.call("GET", "/api/staff/applications/" + "0" * 16)
        self.assertEqual(r.status, 404)
        r, _ = self.call("GET", "/api/staff/applications?state=bogus")
        self.assertEqual(r.status, 400)

    # ---- states

    def test_new_to_in_review_to_accepted_and_the_role(self):
        def state():
            return self.call("GET", "/api/staff/applications/" + self.ref)[1]["application"]["state"]

        url = "/api/staff/applications/%s/state" % self.ref
        self.assertEqual(state(), "new")
        r, j = self.call("POST", url, {"action": "in_review"})
        self.assertEqual(j["state"], "in_review")
        self.assertEqual(self.call("GET", "/api/staff/applications?state=in_review")[1]
                         ["applications"][0]["ref"], self.ref)
        self.assertEqual(self.call("GET", "/api/staff/applications?state=new")[1]
                         ["applications"], [])
        r, j = self.call("POST", url, {"action": "accepted", "note": "welcome"})
        self.assertEqual(j["state"], "accepted")
        detail = self.call("GET", "/api/staff/applications/" + self.ref)[1]["application"]
        self.assertEqual((detail["decided_by"], detail["decision_note"]), (NAME, "welcome"))
        r, j = self.call("POST", url, {"action": "role_given"})
        self.assertEqual(j["state"], "accepted")
        # a decision is final: it cannot go back to review or be declined
        for action in ("in_review", "declined", "new"):
            r, j = self.call("POST", url, {"action": action})
            self.assertEqual((r.status, j["error"]), (409, "cannot"), action)
        counts = self.call("GET", "/api/staff/me")[1]["counts"]
        self.assertEqual((counts["accepted"], counts["new"]), (1, 0))

    def test_a_note_sent_with_a_move_to_review_is_kept(self):
        # the route takes a note with every action; a move that is not a
        # decision has no decision note, so it has to become an internal note
        url = "/api/staff/applications/%s/" % self.ref
        r, j = self.call("POST", url + "state", {"action": "in_review", "note": "ask the models"})
        self.assertEqual(j["state"], "in_review")
        notes = self.call("GET", "/api/staff/applications/" + self.ref)[1]["application"]["notes"]
        self.assertEqual([(n["staff"], n["text"]) for n in notes], [(NAME, "ask the models")])
        # a move that does not happen keeps nothing
        self.call("POST", url + "state", {"action": "declined"})
        r, j = self.call("POST", url + "state", {"action": "new", "note": "lost?"})
        self.assertEqual(r.status, 409)
        notes = self.call("GET", "/api/staff/applications/" + self.ref)[1]["application"]["notes"]
        self.assertEqual(len(notes), 1)

    def test_declined_and_unknown_action(self):
        url = "/api/staff/applications/%s/state" % self.ref
        self.assertEqual(self.call("POST", url, {"action": "declined"})[1]["state"], "declined")
        self.assertEqual(self.call("POST", url, {"action": "wipe"})[0].status, 400)
        self.assertEqual(self.call("POST", url, {"action": ["x"]})[0].status, 400)

    def test_every_action_is_in_the_log_with_who(self):
        url = "/api/staff/applications/%s/" % self.ref
        self.call("POST", url + "state", {"action": "in_review"}, name="Bob Mod")
        self.call("POST", url + "note", {"text": "ask for a link"})
        self.call("POST", url + "state", {"action": "declined"}, name="Cy Lead")
        log = self.call("GET", "/api/staff/log")[1]["log"]
        got = [(r["staff"], r["action"]) for r in reversed(log)]
        self.assertEqual(got, [("Bob Mod", "in_review"), (NAME, "note"), ("Cy Lead", "declined")])

    # ---- notes

    def test_notes_are_kept_in_order_and_bounded(self):
        url = "/api/staff/applications/%s/note" % self.ref
        self.call("POST", url, {"text": "first"})
        r, j = self.call("POST", url, {"text": "second\r\nline"})
        self.assertEqual([n["text"] for n in j["notes"]], ["first", "second\nline"])
        for bad in ("", "   ", "x" * (st.NOTE_MAX + 1), 5):
            r, _ = self.call("POST", url, {"text": bad})
            self.assertEqual(r.status, 400, bad)
        r, _ = self.call("POST", "/api/staff/applications/%s/note" % ("1" * 16), {"text": "a"})
        self.assertEqual(r.status, 404)

    def test_notes_leave_with_the_application(self):
        self.call("POST", "/api/staff/applications/%s/note" % self.ref, {"text": "private"})
        self.assertTrue(self.join.store.delete(self.ref))
        with sqlite3.connect(self.config.db_path) as c:
            self.assertEqual(c.execute("SELECT count(*) FROM staff_notes").fetchone()[0], 0)

    def test_notes_leave_with_a_person_forgotten_and_a_purge(self):
        url = "/api/staff/applications/%s/note" % self.ref
        self.call("POST", url, {"text": "private"})
        self.assertEqual(self.join.store.delete_person(email="ana@example.org"), 1)
        ref2 = self.join.submit(apps.validate(good(discord="bob_x", email="b@example.org")))
        self.call("POST", "/api/staff/applications/%s/note" % ref2, {"text": "later"})
        self.clock.advance(apps.KEEP_PENDING + 1)
        self.join.store.purge()
        with sqlite3.connect(self.config.db_path) as c:
            self.assertEqual(c.execute("SELECT count(*) FROM staff_notes").fetchone()[0], 0)

    def test_a_database_from_the_first_release_gets_the_column(self):
        path = os.path.join(self.tmp, "old.db")
        with sqlite3.connect(path) as c:
            c.executescript(apps.SCHEMA.split("-- the staff panel")[0])   # no staff tables
        for _ in range(2):                                              # and init can repeat
            apps.Store(path).init()
        with sqlite3.connect(path) as c:
            cols = [r[1] for r in c.execute("PRAGMA table_info(applications)")]
            tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master")]
        self.assertIn("in_review_at", cols)
        self.assertIn("staff_notes", tables)
        self.assertIn("staff_log", tables)

    # ---- accounts with the staff role

    def test_a_staff_account_gets_in_and_a_plain_one_does_not(self):
        def accounts(roles):
            me = json.dumps({"id": "abcdef12-3456", "email": "s@example.org",
                             "email_verified": True, "roles": roles})
            return apps.Accounts("https://account.example", FakeOpener(body=me.encode()))

        self.httpd.app.staff.accounts = accounts(["staff"])
        r, j = self.call("GET", "/api/staff/me", token="an-account-token", name="")
        self.assertEqual((r.status, j["staff"]), (200, "account:abcdef12-3456"))
        self.httpd.app.staff.accounts = accounts(["member"])
        r, _ = self.call("GET", "/api/staff/me", token="an-account-token", name="")
        self.assertEqual(r.status, 401)
        self.httpd.app.staff.accounts = accounts("staff")      # not a list
        r, _ = self.call("GET", "/api/staff/me", token="an-account-token", name="")
        self.assertEqual(r.status, 401)

    def test_nothing_staff_is_in_the_public_pages(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        for base, _, files in [w for sub in ("site", "site-v1")
                               for w in os.walk(os.path.join(root, sub))]:
            for f in files:
                if f.endswith((".html", ".xml", ".txt", ".js")):
                    with open(os.path.join(base, f), encoding="utf-8") as fh:
                        self.assertNotIn("/api/staff", fh.read(), f)
