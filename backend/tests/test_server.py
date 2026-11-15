import http.client
import json
import threading
import unittest
import urllib.parse

from raye_site import server as srv
from raye_site.ratelimit import RateLimiter
from raye_site.store import Store

from helpers import Clock, TempDir, make_config


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.config = make_config(self.tmp)
        self.store = Store(self.config.db_path, clock=self.clock)
        self.store.init()
        self.woken = 0

        class FakeWorker:
            def wake(inner):
                self.woken += 1

        self.httpd = srv.make_server(self.config, self.store, FakeWorker(), clock=self.clock)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.tmpctx.__exit__(None, None, None)

    def request(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(method, path, body=body, headers=headers or {})
        r = conn.getresponse()
        data = r.read()
        conn.close()
        return r, data

    def subscribe(self, email="a@x.ca", lang="fr", consent=True, ip="203.0.113.5", **extra):
        payload = {"email": email, "lang": lang, "consent": consent, **extra}
        return self.request("POST", "/api/subscribe", json.dumps(payload),
                            {"Content-Type": "application/json", "X-Real-IP": ip})

    def token_for(self, email):
        job = [j for j in self.store.jobs_due() if j.email == email][0]
        confirm, unsub = self.store.issue_tokens(job.subscriber_id)
        self.store.job_sent(job.id)
        return confirm, unsub

    # subscribe

    def test_same_answer_for_new_pending_and_confirmed(self):
        r1, b1 = self.subscribe()
        self.assertEqual(r1.status, 200)
        self.assertEqual(json.loads(b1)["ok"], True)
        self.assertEqual(self.woken, 1)
        r2, b2 = self.subscribe()
        confirm, _ = self.token_for("a@x.ca")
        self.store.confirm(confirm)
        r3, b3 = self.subscribe()
        self.assertEqual((r2.status, r3.status), (200, 200))
        self.assertEqual(b1, b2)
        self.assertEqual(b1, b3)
        self.assertEqual(r1.getheader("Cache-Control"), "no-store")

    def test_english_answer(self):
        _, body = self.subscribe(lang="en")
        self.assertIn("inbox", json.loads(body)["message"])

    def test_form_post_returns_page(self):
        body = urllib.parse.urlencode({"email": "b@x.ca", "lang": "en", "consent": "on",
                                       "news": "on", "website": ""})
        r, data = self.request("POST", "/api/subscribe", body,
                               {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 200)
        self.assertIn("text/html", r.getheader("Content-Type"))
        page = data.decode()
        self.assertIn('lang="en"', page)
        self.assertIn("Check your inbox", page)
        self.assertNotIn("<script", page)
        self.assertEqual(self.store.jobs_due()[0].email, "b@x.ca")
        # "news" is only asked at confirmation, never taken from the signup
        confirm, _ = self.token_for("b@x.ca")
        self.store.confirm(confirm)
        self.assertFalse(self.store.confirmed()[0]["news"])

    def test_validation_errors(self):
        r, body = self.subscribe(consent=False)
        self.assertEqual(r.status, 400)
        self.assertEqual(json.loads(body)["error"], "consent")
        r, body = self.subscribe(email="nope")
        self.assertEqual(r.status, 400)
        self.assertEqual(json.loads(body)["error"], "email")
        self.assertEqual(self.store.queue_size(), 0)

    def test_form_validation_error_page(self):
        body = urllib.parse.urlencode({"email": "bad", "lang": "fr"})
        r, data = self.request("POST", "/api/subscribe", body,
                               {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 400)
        self.assertIn("adresse", data.decode())

    def test_honeypot_looks_like_success(self):
        r, body = self.subscribe(website="http://spam.example")
        self.assertEqual(r.status, 200)
        self.assertTrue(json.loads(body)["ok"])
        self.assertEqual(self.store.queue_size(), 0)

    def test_body_limits_and_types(self):
        r, _ = self.request("POST", "/api/subscribe", "x" * 5000,
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 413)
        r, _ = self.request("POST", "/api/subscribe", "{not json",
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 400)
        r, _ = self.request("POST", "/api/subscribe", "[1,2]",
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 400)
        r, _ = self.request("POST", "/api/subscribe", "a=b",
                            {"Content-Type": "text/plain"})
        self.assertEqual(r.status, 415)
        r, _ = self.request("POST", "/api/subscribe", b"\xff\xfe",
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 400)

    def test_hostile_shapes_get_400(self):
        r, _ = self.request("POST", "/api/subscribe", "[" * 3000,
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 400)
        self.assertEqual(r.getheader("Connection"), "close")
        r, _ = self.request("GET", "/api/confirm?" + "&".join(f"a{i}=1" for i in range(30)))
        self.assertEqual(r.status, 400)
        r, _ = self.request("POST", "/api/subscribe", "x=1",
                            {"Content-Type": "application/x-www-form-urlencoded",
                             "Content-Length": "-5"})
        self.assertEqual(r.status, 400)
        r, _ = self.request("POST", "/api/subscribe", "x=1",
                            {"Content-Type": "application/x-www-form-urlencoded",
                             "Content-Length": "abc"})
        self.assertEqual(r.status, 400)
        r, _ = self.request("POST", "/api/subscribe", None,
                            {"Content-Type": "application/json",
                             "Transfer-Encoding": "chunked"})
        self.assertEqual(r.status, 411)
        r, body = self.request("POST", "/api/subscribe",
                               json.dumps({"email": ["a@x.ca"], "lang": {"x": 1},
                                           "consent": True}),
                               {"Content-Type": "application/json"})
        self.assertEqual((r.status, json.loads(body)["error"]), (400, "email"))
        r, _ = self.request("POST", "/api/confirm", json.dumps({"t": ["x"]}),
                            {"Content-Type": "application/json"})
        self.assertEqual(r.status, 404)

    def test_get_with_a_body_closes_the_connection(self):
        r, _ = self.request("GET", "/api/health", "junk", {"Content-Length": "4"})
        self.assertEqual(r.status, 200)
        self.assertEqual(r.getheader("Connection"), "close")

    def test_rate_limit_shared_by_an_ipv6_64(self):
        for i in range(5):
            r, _ = self.subscribe(email=f"v{i}@x.ca", ip=f"2001:db8:1:2::{i + 1:x}")
            self.assertEqual(r.status, 200)
        r, _ = self.subscribe(email="v9@x.ca", ip="2001:db8:1:2:ffff:ffff:ffff:ffff")
        self.assertEqual(r.status, 429)
        r, _ = self.subscribe(email="v9@x.ca", ip="2001:db8:1:3::1")
        self.assertEqual(r.status, 200)

    def test_connection_cap(self):
        import socket
        import time
        self.httpd.set_max_connections(1)
        idle = socket.create_connection(("127.0.0.1", self.port))
        try:
            time.sleep(0.3)
            r, _ = self.request("GET", "/api/health")
            self.assertEqual(r.status, 503)
        finally:
            idle.close()
        time.sleep(0.3)
        r, _ = self.request("GET", "/api/health")
        self.assertEqual(r.status, 200)

    def test_head(self):
        r, body = self.request("HEAD", "/api/health")
        self.assertEqual((r.status, body), (200, b""))

    def test_missing_length(self):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.putrequest("POST", "/api/subscribe")
        conn.putheader("Content-Type", "application/json")
        conn.endheaders()
        r = conn.getresponse()
        self.assertEqual(r.status, 411)
        conn.close()

    def test_rate_limit_per_ip(self):
        for i in range(5):
            r, _ = self.subscribe(email=f"u{i}@x.ca")
            self.assertEqual(r.status, 200)
        r, body = self.subscribe(email="u9@x.ca")
        self.assertEqual(r.status, 429)
        self.assertEqual(json.loads(body)["error"], "rate")
        self.assertTrue(r.getheader("Retry-After"))
        # another client is not affected
        r, _ = self.subscribe(email="u9@x.ca", ip="203.0.113.6")
        self.assertEqual(r.status, 200)
        self.clock.advance(3601)
        r, _ = self.subscribe(email="u10@x.ca")
        self.assertEqual(r.status, 200)

    def test_global_hourly_cap(self):
        self.httpd.app.global_cap = 2
        self.subscribe(email="a1@x.ca", ip="198.51.100.1")
        self.subscribe(email="a2@x.ca", ip="198.51.100.2")
        r, _ = self.subscribe(email="a3@x.ca", ip="198.51.100.3")
        self.assertEqual(r.status, 429)

    # confirm and unsubscribe

    def test_confirm_two_steps(self):
        self.subscribe(lang="en")
        confirm, _ = self.token_for("a@x.ca")
        r, page = self.request("GET", "/api/confirm?t=" + confirm)
        self.assertEqual(r.status, 200)
        page = page.decode()
        self.assertIn('method="post"', page)
        self.assertIn(f'value="{confirm}"', page)
        self.assertIn('type="checkbox" name="news"', page)
        self.assertNotIn("checked", page)
        self.assertIn("By confirming", page)
        self.assertEqual(self.store.confirmed(), [])  # a GET never confirms
        r, page = self.request("POST", "/api/confirm",
                               urllib.parse.urlencode({"t": confirm, "news": "on"}),
                               {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 200)
        self.assertIn("You're on the list", page.decode())
        self.assertEqual(len(self.store.confirmed()), 1)
        self.assertTrue(self.store.confirmed()[0]["news"])
        r, page = self.request("GET", "/api/confirm?t=" + confirm)
        self.assertIn("already", page.decode())

    def test_confirm_invalid(self):
        r, page = self.request("GET", "/api/confirm?t=nope")
        self.assertEqual(r.status, 404)
        text = page.decode()
        self.assertIn("lien", text)  # both languages on an unknown token
        self.assertIn("link", text)
        r, _ = self.request("GET", "/api/confirm")
        self.assertEqual(r.status, 404)
        r, _ = self.request("POST", "/api/confirm", "t=nope",
                            {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 404)

    def test_confirm_expired(self):
        self.subscribe()
        confirm, _ = self.token_for("a@x.ca")
        self.clock.advance(49 * 3600)
        r, page = self.request("GET", "/api/confirm?t=" + confirm)
        self.assertEqual(r.status, 410)
        self.assertIn("expiré", page.decode())

    def test_unsubscribe_page_and_one_click(self):
        self.subscribe()
        confirm, unsub = self.token_for("a@x.ca")
        self.store.confirm(confirm)
        r, page = self.request("GET", "/api/unsubscribe?t=" + unsub)
        self.assertEqual(r.status, 200)
        self.assertIn('method="post"', page.decode())
        self.assertEqual(len(self.store.confirmed()), 1)
        # RFC 8058 one-click: token in the URL, fixed body
        r, page = self.request("POST", "/api/unsubscribe?t=" + unsub,
                               "List-Unsubscribe=One-Click",
                               {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 200)
        self.assertEqual(self.store.confirmed(), [])
        r, page = self.request("GET", "/api/unsubscribe?t=" + unsub)
        self.assertIn("déjà", page.decode())

    def test_unsubscribe_form_post(self):
        self.subscribe(lang="en")
        _, unsub = self.token_for("a@x.ca")
        r, page = self.request("POST", "/api/unsubscribe", "t=" + unsub,
                               {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 200)
        self.assertIn("unsubscribed", page.decode())
        r, _ = self.request("POST", "/api/unsubscribe", "t=bad",
                            {"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(r.status, 404)

    def test_token_brute_force_is_limited(self):
        statuses = set()
        for _ in range(40):
            r, _ = self.request("GET", "/api/confirm?t=guess", headers={"X-Real-IP": "192.0.2.9"})
            statuses.add(r.status)
        self.assertIn(429, statuses)

    # plumbing

    def test_other_routes(self):
        r, body = self.request("GET", "/api/health")
        self.assertEqual((r.status, body), (200, b"ok\n"))
        r, _ = self.request("GET", "/api/../etc/passwd")
        self.assertEqual(r.status, 404)
        r, _ = self.request("GET", "/api/subscribe")
        self.assertEqual(r.status, 405)
        r, _ = self.request("PUT", "/api/subscribe", "{}")
        self.assertEqual(r.status, 405)
        r, _ = self.request("DELETE", "/api/confirm")
        self.assertEqual(r.status, 405)
        r, _ = self.request("POST", "/nope", "{}", {"Content-Type": "application/json"})
        self.assertEqual(r.status, 404)

    def test_headers_on_pages(self):
        r, _ = self.request("GET", "/api/confirm?t=nope")
        self.assertIn("default-src 'none'", r.getheader("Content-Security-Policy"))
        self.assertEqual(r.getheader("X-Content-Type-Options"), "nosniff")
        self.assertEqual(r.getheader("Referrer-Policy"), "no-referrer")
        self.assertNotIn("Python", r.getheader("Server") or "")

    def test_tokens_never_logged(self):
        with self.assertLogs("raye_site.server", level="INFO") as logs:
            self.request("GET", "/api/confirm?t=SECRETTOKENVALUE")
        joined = "\n".join(logs.output)
        self.assertIn("/api/confirm", joined)
        self.assertNotIn("SECRETTOKENVALUE", joined)


class ClientIpTests(unittest.TestCase):
    def test_header_trusted_only_from_loopback(self):
        trusted = ("127.0.0.1", "::1")
        self.assertEqual(srv.client_ip("127.0.0.1", "203.0.113.4", trusted), "203.0.113.4")
        self.assertEqual(srv.client_ip("192.168.50.50", "203.0.113.4", trusted), "192.168.50.50")
        self.assertEqual(srv.client_ip("127.0.0.1", "not-an-ip", trusted), "127.0.0.1")
        self.assertEqual(srv.client_ip("127.0.0.1", None, trusted), "127.0.0.1")
        # IPv6 visitors are counted per /64: one home or one server, many addresses
        self.assertEqual(srv.client_ip("127.0.0.1", " 2001:db8::1 ", trusted), "2001:db8::/64")
        self.assertEqual(srv.client_ip("127.0.0.1", "2001:db8:0:0:ffff::9", trusted),
                         "2001:db8::/64")
        self.assertEqual(srv.client_ip("::1", None, trusted), "::/64")
        self.assertEqual(srv.client_ip("2001:db8:5:6:7::1", None, trusted), "2001:db8:5:6::/64")
        self.assertEqual(srv.client_ip("127.0.0.1", "::ffff:203.0.113.4", trusted), "203.0.113.4")


class RateLimiterTests(unittest.TestCase):
    def test_window(self):
        clock = Clock()
        rl = RateLimiter(limit=2, window=10, clock=clock)
        self.assertTrue(rl.hit("k"))
        self.assertTrue(rl.hit("k"))
        self.assertFalse(rl.hit("k"))
        self.assertGreater(rl.retry_after("k"), 0)
        clock.advance(11)
        self.assertTrue(rl.hit("k"))
        self.assertEqual(rl.retry_after("other"), 0)

    def test_memory_is_bounded(self):
        clock = Clock()
        rl = RateLimiter(limit=1, window=10, clock=clock, max_keys=100)
        for i in range(1000):
            rl.hit(f"ip{i}")
        self.assertLessEqual(len(rl.hits), 100)


if __name__ == "__main__":
    unittest.main()
