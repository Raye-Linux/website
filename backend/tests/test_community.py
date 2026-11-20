"""The live Discord numbers of the Community page: only three facts pass,
the answer is kept ten minutes, and an outage shows the last numbers."""

import http.client
import json
import threading
import unittest

from raye_site import community
from raye_site import server as srv
from raye_site.store import Store

from helpers import Clock, TempDir, make_config
from test_applications import FakeOpener

INVITE = json.dumps({
    "code": "TrxhUkabyB", "inviter": {"id": "1", "username": "someone", "avatar": "abc"},
    "guild": {"id": "1570836408745074770", "name": "Raye Linux", "icon": "deadbeef"},
    "approximate_member_count": 68, "approximate_presence_count": 13}).encode()


class CommunityTests(unittest.TestCase):
    def test_only_name_and_counts_pass(self):
        c = community.Community("TrxhUkabyB", Clock(), FakeOpener(body=INVITE))
        status, data = c.status()
        self.assertEqual(status, 200)
        self.assertEqual(data, {"ok": True, "name": "Raye Linux", "members": 68, "online": 13,
                                "invite": "https://discord.gg/TrxhUkabyB"})
        self.assertNotIn("someone", json.dumps(data))
        self.assertIn("with_counts=true", c.opener.requests[0].full_url)

    def test_kept_ten_minutes(self):
        clock = Clock()
        c = community.Community("TrxhUkabyB", clock, FakeOpener(body=INVITE))
        c.status()
        c.status()
        self.assertEqual(len(c.opener.requests), 1)
        clock.advance(community.TTL + 1)
        c.status()
        self.assertEqual(len(c.opener.requests), 2)

    def test_an_outage_shows_the_last_numbers(self):
        clock = Clock()
        c = community.Community("TrxhUkabyB", clock, FakeOpener(body=INVITE))
        c.status()
        clock.advance(community.TTL + 1)
        c.opener = FakeOpener(fail="net")
        self.assertEqual(c.status()[1]["members"], 68)

    def test_no_numbers_ever(self):
        c = community.Community("TrxhUkabyB", Clock(), FakeOpener(fail="http"))
        self.assertEqual(c.status(), (502, {"ok": False, "error": "unavailable"}))
        bad = community.Community("TrxhUkabyB", Clock(), FakeOpener(body=b'{"guild": 1}'))
        self.assertEqual(bad.status()[0], 502)

    def test_not_configured_or_odd_code(self):
        for code in (None, "", "../etc", "a b"):
            with self.subTest(code=code):
                self.assertEqual(community.Community(code).status()[0], 503)


class CommunityEndpointTests(unittest.TestCase):
    def test_endpoint(self):
        with TempDir() as tmp:
            config = make_config(tmp, discord_invite="TrxhUkabyB")
            store = Store(config.db_path)
            store.init()
            httpd = srv.make_server(config, store, None, clock=Clock())
            httpd.app.community.opener = FakeOpener(body=INVITE)
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            try:
                conn = http.client.HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=5)
                conn.request("GET", "/api/community")
                r = conn.getresponse()
                data = json.loads(r.read())
                conn.close()
            finally:
                httpd.shutdown()
                httpd.server_close()
        self.assertEqual(r.status, 200)
        self.assertEqual(data["online"], 13)
        self.assertIn("max-age=300", r.getheader("Cache-Control"))


if __name__ == "__main__":
    unittest.main()
