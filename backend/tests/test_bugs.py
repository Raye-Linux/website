"""Bug reports from the help box: what is accepted, what Discord receives,
and that the webhook address and the report text never reach the journal."""

import base64
import http.client
import http.server
import json
import logging
import os
import threading
import unittest

from raye_site import bugs
from raye_site import server as srv
from raye_site.store import Store

from helpers import Clock, TempDir, make_config

JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 200
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 200
SECRET_TEXT = "the quorvel panel 5521 froze when I opened it"
FIREFOX = "Mozilla/5.0 (X11; Linux x86_64; rv:160.0) Gecko/20100101 Firefox/160.0"


def data_url(raw, kind="jpeg"):
    return f"data:image/{kind};base64," + base64.b64encode(raw).decode()


class FakeWebhook:
    """Takes webhook posts and keeps them, the way Discord would."""

    def __init__(self, status=200):
        self.status, self.posts, self.answer = status, [], b"{}"
        self.needs_thread = False   # a forum channel: refuses posts without a title
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_POST(self):
                n = int(self.headers.get("Content-Length", 0))
                fake.posts.append((self.path, dict(self.headers), self.rfile.read(n)))
                status, answer = fake.status, fake.answer
                if fake.needs_thread and "thread_name" not in fake.payload():
                    status, answer = 400, b'{"code": 220001, "message": "needs thread_name"}'
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(answer)))
                self.end_headers()
                self.wfile.write(answer)

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d/api/webhooks/123456/tok" % self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()

    def payload(self, i=-1):
        body = self.posts[i][2]
        start = body.index(b"\r\n\r\n") + 4
        end = body.index(b"\r\n--", start)
        return json.loads(body[start:end])


class UnitTests(unittest.TestCase):
    def test_only_a_discord_webhook_address_is_used(self):
        with TempDir() as tmp:
            bad, good = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            with open(bad, "w") as f:
                f.write("https://evil.example/api/webhooks/1/x\n")
            url = "https://discord.com/api/webhooks/1234567890/" + "A" * 40
            with open(good, "w") as f:
                f.write(url + "\n")
            self.assertIsNone(bugs.load_webhook([bad, os.path.join(tmp, "missing")]))
            self.assertEqual(bugs.load_webhook([bad, good]), url)

    def test_validation(self):
        ok = bugs.validate({"lang": "en", "what": "It crashes on start", "page": "/en/"})
        self.assertEqual(ok["what"], "It crashes on start")
        self.assertIsNone(ok["image"])
        for fields, code in (({"what": "short"}, "too_short"),
                             ({"what": "x" * (bugs.WHAT_MAX + 1)}, "too_long"),
                             ({"what": "long enough text", "steps": "s" * 2000}, "too_long"),
                             ({"what": "long enough text", "image": "data:text/html,hi"}, "bad_image"),
                             ({"what": "long enough text", "image": data_url(b"GIF89a" + b"0" * 9)},
                              "bad_image"),
                             ({"what": "long enough text",
                               "image": data_url(b"\xff\xd8\xff" + b"0" * bugs.IMAGE_MAX)},
                              "image_too_large")):
            with self.assertRaises(ValueError) as ctx:
                bugs.validate(fields)
            self.assertEqual(str(ctx.exception), code)
        self.assertEqual(bugs.validate({"what": "x" * 20, "page": "https://x/"})["page"], "")
        self.assertEqual(bugs.validate({"what": "x" * 20, "image": data_url(PNG, "png")})["image"][1],
                         "png")

    def test_mentions_and_hidden_characters_are_neutralised(self):
        text = bugs.clean("ping @everyone and @here and <@123>‮\x07 mail a@b.ca", 200)
        self.assertNotIn("@everyone", text)
        self.assertNotIn("@here", text)
        self.assertNotIn("<@", text)
        self.assertNotIn("‮", text)
        self.assertIn("a@b.ca", text)

    def test_the_forum_post(self):
        report = bugs.validate({"lang": "fr", "what": "le bureau gèle quand j'ouvre Fichiers... "
                                "Ensuite plus rien.", "steps": "1. ouvrir Fichiers\n2) brancher la clé",
                                "contact": "me@x.ca", "page": "/telecharger/",
                                "agent": FIREFOX, "image": data_url(JPEG)})
        msg = bugs.message(report)
        self.assertEqual(msg["thread_name"], "Le bureau gèle quand j'ouvre Fichiers")
        self.assertEqual(msg["allowed_mentions"], {"parse": []})
        embed = msg["embeds"][0]
        self.assertEqual(embed["color"], 0x7B3CFF)
        self.assertEqual(embed["image"]["url"], "attachment://screenshot.jpg")
        self.assertEqual([f["name"] for f in embed["fields"]],
                         ["What happened", "Steps to reproduce"])
        self.assertEqual(embed["fields"][1]["value"], "1. ouvrir Fichiers\n2. brancher la clé")
        self.assertEqual(embed["footer"]["text"],
                         "Sent from rayelinux.com · Firefox 160 on Linux · French")
        dumped = json.dumps(msg)
        self.assertNotIn("me@x.ca", dumped)
        self.assertNotIn("Gecko", dumped)
        self.assertNotIn("telecharger", dumped)

    def test_no_empty_fields(self):
        embed = bugs.message(bugs.validate({"what": "The menu does not open at all"}))["embeds"][0]
        self.assertEqual([f["name"] for f in embed["fields"]], ["What happened"])
        self.assertNotIn("image", embed)
        self.assertEqual(embed["footer"]["text"], "Sent from rayelinux.com · French")

    def test_titles(self):
        for what, title in (("the panel freezes!!!", "The panel freezes"),
                            ("Files crashes. It happens every time.", "Files crashes"),
                            ("- wifi drops after sleep ...", "Wifi drops after sleep"),
                            ("ok. The dock vanishes after login", "Ok. The dock vanishes after login")):
            self.assertEqual(bugs.thread_name(what), title)
        long = bugs.thread_name("word " * 60)
        self.assertLessEqual(len(long), bugs.THREAD_NAME_MAX)
        self.assertTrue(long.endswith("word…"))

    def test_one_step_is_not_numbered(self):
        self.assertEqual(bugs.numbered("just open it"), "just open it")
        self.assertEqual(bugs.numbered("- a\n\n- b\n- c"), "1. a\n2. b\n3. c")

    def test_browser_names(self):
        for agent, short in (
                (FIREFOX, "Firefox 160 on Linux"),
                ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/142.0.0.0 Safari/537.36", "Chrome 142 on Windows"),
                ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0", "Edge 142 on Windows"),
                ("Mozilla/5.0 (iPhone; CPU iPhone OS 26_1 like Mac OS X) AppleWebKit/605.1.15 "
                 "(KHTML, like Gecko) Version/26.1 Mobile/15E148 Safari/604.1", "Safari 26 on iOS"),
                ("Mozilla/5.0 (Linux; Android 16; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/142.0.0.0 Mobile Safari/537.36", "Chrome 142 on Android"),
                ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like "
                 "Gecko) Version/26.0 Safari/605.1.15", "Safari 26 on macOS"),
                ("curl/8.5", ""), ("", "")):
            self.assertEqual(bugs.short_agent(agent), short, agent)

    def test_review_post_keeps_the_contact_and_the_reason(self):
        report = bugs.validate({"lang": "en", "what": "test test test", "contact": "me@x.ca",
                                "page": "/en/"})
        msg = bugs.review_message(report, "too little real content")
        embed = msg["embeds"][0]
        self.assertEqual(embed["title"], "Held: too little real content")
        self.assertIn({"name": "Contact (private)", "value": "me@x.ca"}, embed["fields"])
        self.assertNotIn("thread_name", msg)


class FakeClassifier:
    def __init__(self, label="bug"):
        self.value, self.calls = label, 0

    def label(self, report):
        self.calls += 1
        return self.value


class EndpointTests(unittest.TestCase):
    def setUp(self):
        self.tmpctx = TempDir()
        self.tmp = self.tmpctx.__enter__()
        self.clock = Clock()
        self.hook = FakeWebhook()
        self.review = FakeWebhook()
        self.ai = FakeClassifier()

    def tearDown(self):
        if hasattr(self, "httpd"):
            self.httpd.shutdown()
            self.httpd.server_close()
        self.hook.close()
        self.review.close()
        self.tmpctx.__exit__(None, None, None)

    def start(self, url="hook", review="hook"):
        config = make_config(self.tmp)
        store = Store(config.db_path, clock=self.clock)
        store.init()

        class W:
            def wake(self):
                pass

        self.httpd = srv.make_server(config, store, W(), clock=self.clock)
        self.httpd.app.bugs = bugs.Bugs(self.hook.url if url == "hook" else url, self.clock,
                                        review_url=self.review.url if review == "hook" else review,
                                        classifier=self.ai)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def post(self, payload, ip="203.0.113.9"):
        conn = http.client.HTTPConnection("127.0.0.1", self.httpd.server_address[1], timeout=10)
        conn.request("POST", "/api/support/bug", body=json.dumps(payload),
                     headers={"Content-Type": "application/json", "X-Real-IP": ip})
        r = conn.getresponse()
        data = json.loads(r.read().decode())
        conn.close()
        return r.status, data

    def test_a_good_report_goes_public_without_its_contact(self):
        self.start()
        status, data = self.post({"lang": "en", "what": "Files freezes when I open a folder",
                                  "contact": "ann@example.ca", "agent": FIREFOX})
        self.assertEqual((status, data), (200, {"ok": True, "error": None}))
        self.assertEqual(len(self.hook.posts), 1)
        self.assertEqual(self.review.posts, [])
        path, headers, body = self.hook.posts[0]
        self.assertTrue(path.endswith("?wait=true"))
        self.assertIn("DiscordBot", headers["User-Agent"])
        self.assertNotIn(b"ann@example.ca", body)
        self.assertNotIn(b"Gecko", body)
        self.assertEqual(self.hook.payload()["thread_name"], "Files freezes when I open a folder")

    def test_held_reports_go_to_review_with_the_same_answer(self):
        self.start()
        cases = [({"what": "test test test", "contact": "ann@example.ca"}, "too little"),
                 ({"what": "asdfghjkl qwerty zxcvbnm"}, "too little"),
                 ({"what": "The menu breaks, see https://evil.example/x"}, "link"),
                 ({"what": "Join discord.gg/abcdef the menu breaks here"}, "link"),
                 ({"what": "The menu breaks, ask @someone about the panel"}, "mention"),
                 ({"what": "The menu breaks every single time, fuck"}, "swearing")]
        for i, (fields, reason) in enumerate(cases):
            status, data = self.post(dict(fields, lang="en"), ip="203.0.113.%d" % (20 + i))
            self.assertEqual((status, data), (200, {"ok": True, "error": None}), fields)
            title = self.review.payload()["embeds"][0]["title"]
            self.assertIn(reason, title, fields)
        self.assertEqual(self.hook.posts, [])
        self.assertIn(b"ann@example.ca", self.review.posts[0][2])
        self.assertEqual(self.ai.calls, 0)  # the filters decided before the model

    def test_screenshot_and_model_verdicts_go_to_review(self):
        self.start()
        self.post({"what": "Files freezes when I open a folder", "image": data_url(JPEG)})
        body = self.review.posts[-1][2]
        self.assertIn(b'filename="screenshot.jpg"', body)
        self.assertIn(JPEG, body)
        self.assertIn("screenshot", self.review.payload()["embeds"][0]["title"])
        self.ai.value = "question"
        self.post({"what": "How do I install Steam on this thing"}, ip="203.0.113.30")
        self.assertIn("question", self.review.payload()["embeds"][0]["title"])
        self.ai.value = None  # the model is down or too slow
        self.post({"what": "The panel goes black after waking up"}, ip="203.0.113.31")
        self.assertIn("did not answer", self.review.payload()["embeds"][0]["title"])
        self.assertEqual(self.hook.posts, [])

    def test_abuse_and_duplicates_are_dropped_quietly(self):
        self.start()
        self.assertEqual(self.post({"what": "your installer sucks, kill yourself"}),
                         (200, {"ok": True, "error": None}))
        self.assertEqual(self.post({"what": "F4GG0T devs broke the menu again"}, ip="203.0.113.2")[0],
                         200)
        self.assertEqual(self.hook.posts + self.review.posts, [])
        self.post({"what": "Files freezes when I open a folder"}, ip="203.0.113.3")
        status, data = self.post({"what": "files FREEZES when I open a folder!"}, ip="203.0.113.4")
        self.assertEqual((status, data), (200, {"ok": True, "error": None}))
        self.assertEqual(len(self.hook.posts), 1)
        self.clock.advance(24 * 3600 + 1)
        self.post({"what": "Files freezes when I open a folder"}, ip="203.0.113.5")
        self.assertEqual(len(self.hook.posts), 2)

    def test_a_failed_send_can_be_tried_again(self):
        self.start()
        self.hook.status = 500
        self.assertEqual(self.post({"what": "Files freezes when I open a folder"})[1]["error"],
                         "not_sent")
        self.hook.status = 200
        self.assertEqual(self.post({"what": "Files freezes when I open a folder"})[0], 200)
        self.assertEqual(len(self.hook.posts), 2)

    def test_a_forum_review_channel_gets_a_title(self):
        self.review.needs_thread = True
        self.start()
        self.assertEqual(self.post({"what": "test test test"})[0], 200)
        self.assertEqual(len(self.review.posts), 2)
        self.assertNotIn("thread_name", self.review.payload(0))
        self.assertEqual(self.review.payload(1)["thread_name"], "Test test test")

    def test_nothing_but_counters_reaches_the_journal(self):
        self.start()
        with self.assertLogs("raye_site", level=logging.DEBUG) as logs:
            self.post({"what": SECRET_TEXT, "contact": "ann@example.ca"})
            self.hook.status = 500
            status, data = self.post({"what": SECRET_TEXT + " again"}, ip="203.0.113.10")
        self.assertEqual((status, data["error"]), (502, "not_sent"))
        journal = "\n".join(logs.output)
        for secret in ("quorvel", "ann@example", "webhooks", "/tok"):
            self.assertNotIn(secret, journal)
        self.assertIn("public=1 review=0 drop=0 failed=1", journal)

    def test_rate_limit_per_visitor(self):
        self.start()
        for i in range(bugs.REPORTS_PER_HOUR):
            self.assertEqual(self.post({"what": "a real problem here number %d" % i})[0], 200)
        status, data = self.post({"what": "a real problem here"})
        self.assertEqual((status, data["error"]), (429, "rate_limited"))
        self.assertEqual(self.post({"what": "a real problem here"}, ip="198.51.100.4")[0], 200)
        self.clock.advance(3601)
        self.assertEqual(self.post({"what": "another real problem here"})[0], 200)

    def test_refusals(self):
        self.start()
        self.assertEqual(self.post({"what": "hi"}), (400, {"ok": False, "error": "too_short"}))
        self.assertEqual(self.post({"what": "a real problem", "website": "x"})[0], 200)
        self.assertEqual(self.hook.posts + self.review.posts, [])

    def test_not_configured_is_a_503(self):
        for url, review in ((None, "hook"), ("hook", None)):
            self.start(url=url, review=review)
            self.assertEqual(self.post({"what": "a real problem here"}),
                             (503, {"ok": False, "error": "not_configured"}))
            self.httpd.shutdown()
            self.httpd.server_close()
            del self.httpd


class FakeRiven:
    """The Discord bot's API, as far as the site reads it."""

    def __init__(self):
        self.calls, self.status = [], 200
        fake = self

        class H(http.server.BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def do_GET(self):
                fake.calls.append(self.path)
                if fake.status != 200:
                    body, code = b'{"ok":false}', fake.status
                elif self.path == "/api/public/raye/bugs":
                    body, code = json.dumps({"ok": True, "tags": ["Open", "Solved"], "bugs": [
                        {"id": "123", "title": "<b>Freeze</b>", "tags": ["Open"], "replies": 2,
                         "created": "2026-11-14T10:00:00Z", "archived": False, "secret": "x"},
                        {"id": "../9", "title": "bad"}]}).encode(), 200
                elif self.path == "/api/public/raye/bugs/123":
                    body, code = json.dumps({"ok": True, "id": "123", "title": "Freeze",
                                             "tags": [], "replies": 1, "messages": [
                        {"author": "Ann", "text": "It froze", "date": "2026-11-14T10:00:00Z",
                         "attachments": [{"name": "a.png", "url": "https://cdn.example/a.png"}],
                         "id": "999"}]}).encode(), 200
                else:
                    body, code = b'{"ok":false}', 404
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.url = "http://127.0.0.1:%d" % self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


class FeedTests(unittest.TestCase):
    def setUp(self):
        self.riven, self.clock = FakeRiven(), Clock()
        self.feed = bugs.Feed(self.riven.url, "1570836408745074770", self.clock)

    def tearDown(self):
        self.riven.close()

    def test_only_the_shown_fields_pass_and_bad_ids_are_dropped(self):
        status, data = self.feed.topics()
        self.assertEqual(status, 200)
        self.assertEqual([b["id"] for b in data["bugs"]], ["123"])
        self.assertNotIn("secret", data["bugs"][0])
        self.assertEqual(data["bugs"][0]["title"], "<b>Freeze</b>")  # escaped by the page

    def test_a_topic_keeps_names_not_links_and_points_to_discord(self):
        status, data = self.feed.topic("123")
        self.assertEqual(status, 200)
        msg = data["messages"][0]
        self.assertEqual(msg["files"], ["a.png"])
        self.assertNotIn("id", msg)
        self.assertEqual(data["discord"],
                         "https://discord.com/channels/1570836408745074770/123")

    def test_answers_are_kept_a_minute_and_errors_fall_back(self):
        self.feed.topics()
        self.feed.topics()
        self.assertEqual(len(self.riven.calls), 1)
        self.clock.advance(61)
        self.riven.status = 500
        self.assertEqual(self.feed.topics()[0], 200)  # the older list beats an error
        self.assertEqual(self.feed.topic("124")[0], 502)

    def test_ids_are_checked_before_asking(self):
        for bad in ("", "abc", "1/2", "1" * 21):
            self.assertEqual(self.feed.topic(bad)[0], 404)
        self.assertEqual(self.riven.calls, [])
        self.assertEqual(bugs.Feed(None).topics()[0], 503)


if __name__ == "__main__":
    unittest.main()
