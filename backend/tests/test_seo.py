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

from test_site import (FORBIDDEN, ROOT, TOOLS, V1_LIVE, V1_DOWNLOAD, V1_TEXT,  # noqa: E402
                       builder, coming_soon_only, read)

URL = "https://www.rayelinux.com"
SM = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
XHTML = "{http://www.w3.org/1999/xhtml}"
# every public page, both languages (not the chooser at / nor the 404)
PUBLIC = {lang: [p for p in builder().PATHS[lang].values()] for lang in ("fr", "en")}
if V1_LIVE:
    # the V1 site: every page of tools/site_v1_text.PAGES, French home at /
    PUBLIC = {lang: [p["path"][lang] for p in V1_TEXT.PAGES.values()] for lang in ("fr", "en")}
HOME_FILES = (("en/index.html", "index.html") if V1_LIVE else ("en/index.html", "fr/index.html"))
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
    def test_every_v1_page_has_its_own_true_title_and_description(self):
        """The V1 head: the same promises, with the V1 site's own rules --
        Windows may be named (test_site_v1's rule), descriptions fit a search
        result (160), and the share card is the Open Graph one (X reads it
        when there is no twitter:title)."""
        if not V1_LIVE:
            self.skipTest("the coming-soon site is what site/ holds")
        from test_site_v1 import forbidden
        same = lambda text: (text or "").replace("\u00a0", " ")   # French typography
        for lang in PUBLIC:
            # a page and its twin may share a title ("Questions · Raye Linux")
            seen_titles, seen_desc = {}, {}
            for path in PUBLIC[lang]:
                rel = rel_of(path)
                h = head(rel)
                desc = h.meta.get("description", "")
                with self.subTest(page=rel):
                    self.assertIn("Raye Linux", h.title)
                    self.assertGreaterEqual(len(desc), 50)
                    self.assertLessEqual(len(desc), 160)
                    self.assertIsNone(STALE.search(h.title + " " + desc), desc)
                    self.assertEqual(forbidden(h.title + " " + desc), [])
                    self.assertNotIn(h.title, seen_titles, seen_titles.get(h.title))
                    self.assertNotIn(desc, seen_desc, seen_desc.get(desc))
                    seen_titles[h.title], seen_desc[desc] = rel, rel
                    self.assertEqual(same(h.meta.get("og:title")), same(h.title))
                    self.assertEqual(same(h.meta.get("og:description")), same(desc))
                    self.assertEqual(h.meta.get("og:url"), URL + path)
                    self.assertIn(h.meta.get("twitter:card"), ("summary", "summary_large_image"))
                    image = h.meta.get("og:image")
                    if image:
                        self.assertEqual(h.meta.get("twitter:card"), "summary_large_image")
                        self.assertTrue(image.startswith(URL + "/assets/shots/"), image)
                        self.assertTrue(os.path.isfile(os.path.join(
                            ROOT, image[len(URL):].split("?")[0].lstrip("/"))), image)

    @coming_soon_only
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

    @coming_soon_only
    def test_home_titles_say_what_raye_linux_is(self):
        self.assertTrue(head("en/index.html").title.startswith("Raye Linux — a free Linux desktop"))
        self.assertTrue(head("fr/index.html").title.startswith("Raye Linux — un bureau Linux gratuit"))
        for rel in ("en/index.html", "fr/index.html"):
            self.assertIn("1.0", head(rel).meta["description"])
            self.assertIn("Sundog", head(rel).meta["description"])


class StructuredDataTests(unittest.TestCase):
    def test_v1_home_pages_describe_the_system_and_the_project(self):
        if not V1_LIVE:
            self.skipTest("the coming-soon site is what site/ holds")
        info = builder().release_info()
        for rel in HOME_FILES:
            with self.subTest(page=rel):
                g = self.graph(rel)
                app, org = g["SoftwareApplication"], g["Organization"]
                self.assertEqual(app["name"], "Raye Linux")
                self.assertEqual(app["applicationCategory"], "OperatingSystem")
                self.assertEqual(app["operatingSystem"], "Linux")
                self.assertEqual(app["softwareVersion"], V1_TEXT.VERSION)
                self.assertEqual(app["offers"]["price"], "0")
                if V1_DOWNLOAD.is_pending():
                    self.assertNotIn("downloadUrl", app)
                else:
                    self.assertEqual(app["downloadUrl"], info["urls"]["r2"])
                    self.assertEqual(app["datePublished"], info["date"])
                self.assertTrue(app["url"].startswith(URL + "/"))
                self.assertEqual(org["url"], URL + "/")
                self.assertEqual(set(org["sameAs"]), {
                    "https://github.com/Raye-Linux", "https://codeberg.org/Raye-Linux",
                    "https://gitlab.com/raye-linux", builder().DISCORD})
                for url in (app.get("screenshot"), org["logo"]):
                    if url:
                        path = url[len(URL):].split("?")[0]
                        self.assertTrue(os.path.isfile(os.path.join(ROOT, path.lstrip("/"))), url)

    def test_v1_other_pages_carry_only_their_breadcrumb(self):
        if not V1_LIVE:
            self.skipTest("the coming-soon site is what site/ holds")
        homes = {V1_TEXT.PAGES["home"]["path"][l] for l in ("fr", "en")}
        for lang in PUBLIC:
            for path in PUBLIC[lang]:
                if path in homes:
                    continue
                blocks = head(rel_of(path)).ld
                with self.subTest(page=path):
                    self.assertEqual(len(blocks), 1)
                    data = json.loads(blocks[0])
                    self.assertEqual(data["@type"], "BreadcrumbList")
                    self.assertEqual(data["itemListElement"][-1]["item"], URL + path)
        self.assertEqual(head("404.html").ld, [])
        self.assertNotIn('rel="canonical"', read("404.html"))

    def graph(self, rel):
        blocks = head(rel).ld
        self.assertEqual(len(blocks), 1, rel)
        data = json.loads(blocks[0])
        self.assertEqual(data["@context"], "https://schema.org")
        return {item["@type"]: item for item in data["@graph"]}

    @coming_soon_only
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

    @coming_soon_only
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
