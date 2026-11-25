"""What search engines read: one sitemap with every public page in both
languages, robots.txt pointing at it, a true title and description on every
page (no leftover "coming soon" text), the structured data of the home page,
and the IndexNow key file."""

import html.parser
import json
import os
import re
import sys
import unittest
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True

from test_site import FORBIDDEN, ROOT, TOOLS, builder, read  # noqa: E402

URL = "https://www.rayelinux.com"
SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
XHTML = "{http://www.w3.org/1999/xhtml}"
# every public page, both languages (not the chooser at / nor the 404)
PUBLIC = {lang: [p for p in builder().PATHS[lang].values()] for lang in ("fr", "en")}
# the coming-soon wording the pages wore before the beta came out
STALE = re.compile(r"(is coming|arrive\s*:|sign up|inscrivez|when it launches|du lancement)", re.I)


class Head(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.meta, self.ld, self._in = "", {}, [], None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in = "title"
        elif tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in = "ld"
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag in ("title", "script"):
            self._in = None

    def handle_data(self, data):
        if self._in == "title":
            self.title += data
        elif self._in == "ld":
            self.ld[-1] += data


def head(rel):
    h = Head()
    h.feed(read(rel))
    return h


def rel_of(path):
    return path.lstrip("/") + "index.html"


class SitemapTests(unittest.TestCase):
    def test_sitemap_lists_every_public_page_with_its_other_language(self):
        tree = ET.fromstring(read("sitemap.xml"))
        urls = {}
        for u in tree.findall(SM + "url"):
            loc = u.find(SM + "loc").text
            self.assertRegex(u.find(SM + "lastmod").text, r"^\d{4}-\d{2}-\d{2}$")
            urls[loc] = {l.get("hreflang"): l.get("href") for l in u.findall(XHTML + "link")}
        want = {URL + p for lang in PUBLIC for p in PUBLIC[lang]}
        self.assertEqual(set(urls), want)
        for loc, alts in urls.items():
            with self.subTest(loc=loc):
                self.assertEqual(set(alts), {"fr", "en", "x-default"})
                self.assertIn(loc, alts.values())
                for href in alts.values():
                    self.assertTrue(os.path.isfile(os.path.join(
                        ROOT, href[len(URL):].lstrip("/") or ".", "index.html")), href)

    def test_robots_txt_names_the_sitemap_and_allows_everything(self):
        text = read("robots.txt")
        self.assertIn(f"Sitemap: {URL}/sitemap.xml", text)
        self.assertNotRegex(text, r"(?m)^Disallow:\s*/\s*$")


class HeadTests(unittest.TestCase):
    def test_every_page_has_its_own_true_title_and_description(self):
        seen_titles, seen_desc = {}, {}
        for lang in PUBLIC:
            for path in PUBLIC[lang]:
                rel = rel_of(path)
                h = head(rel)
                desc = h.meta.get("description", "")
                with self.subTest(page=rel):
                    self.assertIn("Raye Linux", h.title)
                    self.assertGreaterEqual(len(desc), 50)
                    self.assertLessEqual(len(desc), 180)
                    self.assertIsNone(STALE.search(desc), desc)
                    self.assertIsNone(FORBIDDEN.search(h.title + " " + desc))
                    self.assertNotIn(h.title, seen_titles, seen_titles.get(h.title))
                    self.assertNotIn(desc, seen_desc, seen_desc.get(desc))
                    seen_titles[h.title], seen_desc[desc] = rel, rel
                    # the share cards say the same
                    self.assertEqual(h.meta.get("og:title"), h.title)
                    self.assertEqual(h.meta.get("og:description"), desc)
                    self.assertEqual(h.meta.get("twitter:card"), "summary_large_image")
                    self.assertEqual(h.meta.get("twitter:title"), h.title)
                    self.assertEqual(h.meta.get("twitter:description"), desc)
                    self.assertTrue(h.meta.get("twitter:image", "").startswith(URL + "/assets/"))

    def test_the_bare_address_has_a_true_description_too(self):
        desc = head("index.html").meta["description"]
        self.assertIsNone(STALE.search(desc), desc)
        self.assertIn("Raye Linux", head("index.html").title)

    def test_home_titles_say_what_raye_linux_is(self):
        self.assertTrue(head("en/index.html").title.startswith("Raye Linux — a free Linux desktop"))
        self.assertTrue(head("fr/index.html").title.startswith("Raye Linux — un bureau Linux gratuit"))
        for rel in ("en/index.html", "fr/index.html"):
            self.assertIn("1.0", head(rel).meta["description"])
            self.assertIn("Sundog", head(rel).meta["description"])


class StructuredDataTests(unittest.TestCase):
    def graph(self, rel):
        blocks = head(rel).ld
        self.assertEqual(len(blocks), 1, rel)
        data = json.loads(blocks[0])
        self.assertEqual(data["@context"], "https://schema.org")
        return {item["@type"]: item for item in data["@graph"]}

    def test_home_pages_describe_the_system_and_the_project(self):
        info = builder().release_info()
        for rel in ("en/index.html", "fr/index.html"):
            with self.subTest(page=rel):
                g = self.graph(rel)
                app, org = g["SoftwareApplication"], g["Organization"]
                self.assertEqual(app["name"], "Raye Linux")
                self.assertEqual(app["applicationCategory"], "OperatingSystem")
                self.assertEqual(app["operatingSystem"], "Linux")
                self.assertEqual(app["softwareVersion"], "1.0 Beta Sundog")
                self.assertEqual(app["offers"]["price"], "0")
                self.assertEqual(app["downloadUrl"], info["urls"]["r2"])
                self.assertTrue(app["url"].startswith(URL + "/"))
                self.assertTrue(app["screenshot"].startswith(URL + "/assets/shots/"))
                self.assertEqual(org["name"], "Raye Linux")
                self.assertEqual(org["url"], URL + "/")
                self.assertTrue(org["logo"].startswith(URL + "/assets/"))
                self.assertEqual(set(org["sameAs"]), {
                    "https://github.com/Raye-Linux", "https://codeberg.org/Raye-Linux",
                    "https://gitlab.com/raye-linux", builder().DISCORD})
                for url in (app["screenshot"], org["logo"]):
                    path = url[len(URL):].split("?")[0]
                    self.assertTrue(os.path.isfile(os.path.join(ROOT, path.lstrip("/"))), url)
                self.assertIsNone(FORBIDDEN.search(json.dumps(app["description"])))

    def test_no_other_page_carries_structured_data(self):
        for lang in PUBLIC:
            for path in PUBLIC[lang]:
                if path not in ("/fr/", "/en/"):
                    self.assertEqual(head(rel_of(path)).ld, [], path)


class IndexNowTests(unittest.TestCase):
    def test_the_key_file_is_published_and_holds_the_key(self):
        key = builder().INDEXNOW_KEY
        self.assertRegex(key, r"^[0-9a-f]{32}$")
        self.assertEqual(read(f"{key}.txt").strip(), key)

    def test_the_submit_tool_sends_every_sitemap_page_with_the_key(self):
        sys.path.insert(0, TOOLS)
        import indexnow
        body = indexnow.payload(indexnow.sitemap_urls())
        key = builder().INDEXNOW_KEY
        self.assertEqual(body["host"], "www.rayelinux.com")
        self.assertEqual(body["key"], key)
        self.assertEqual(body["keyLocation"], f"{URL}/{key}.txt")
        self.assertEqual(len(body["urlList"]), sum(len(v) for v in PUBLIC.values()))
        with self.assertRaises(SystemExit):
            indexnow.payload(["https://example.com/x"])


if __name__ == "__main__":
    unittest.main()
