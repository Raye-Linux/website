"""Checks on the V1 site (tools/site_v1.py), built in site-v1/ until the
1.0 image is out and in site/ after.

The same rules as the coming-soon page -- strict CSP, nothing from other
sites, both languages alike, no forbidden name -- plus what a longer site
can get wrong: a page the language script does not know, a screenshot
placeholder left at launch, a figure measured on an older version, a word
from an advertisement."""

import datetime
import hashlib
import os
import re
import sys
import unittest

from test_site import WELCOMEQ, builder, parse

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(REPO, "tools"))
import site_v1_text as V  # noqa: E402

B = builder()
LIVE = B.V1_LIVE
ROOT = os.path.join(REPO, "site") if LIVE else os.path.join(REPO, "site-v1")
MIRRORS = ("https://dl.rayelinux.com/", "https://github.com/Raye-Linux/")

# Windows may be named: the site is for people who come from it. The other
# names stay out of what a reader sees. AI / IA are matched in capitals only:
# the French "j'ai" is a word, not an acronym.
NAMES = re.compile(
    r"\b(microsoft|ubuntu|kubuntu|debian|fedora|arch linux|mint|macos|apple|android|"
    r"chrome ?os|wine|intelligence artificielle|artificial intelligence|chatgpt|claude|"
    r"gpt|copilot|onedrive|calamares|plasma|kde)\b", re.I)
CAPS = re.compile(r"\b(IA|AI)\b")


def forbidden(text):
    """The forbidden words left in a text once the allowed phrases are out."""
    text = ALLOWED.sub("", text)
    return [m.group(0) for m in NAMES.finditer(text)] + [m.group(0) for m in CAPS.finditer(text)]
# the two forms the law and the trademarks ask for, and nothing else
ALLOWED = re.compile(r"\b(?:based on|basé sur) Ubuntu 26\.04 LTS\b|"
                     r"marque de Microsoft Corporation|trademark of Microsoft Corporation")
# words from an advertisement, not from someone who made the thing
HOLLOW = re.compile(
    r"\b(seamless\w*|powerful|next[- ]generation|experience\w*|revolution\w*|unleash\w*|"
    r"elevate\w*|cutting[- ]edge|effortless\w*|game[- ]changer|blazing\w*|"
    r"révolutionnaire|puissant\w*|nouvelle génération|expérience|sans effort|élégant\w*|"
    r"fluide\w*|incroyable\w*)\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def rel_of(path):
    return path.lstrip("/") + "index.html"


PAIRS = [(rel_of(p["path"]["fr"]), rel_of(p["path"]["en"])) for p in V.PAGES.values()]
PAGES = [r for pair in PAIRS for r in pair] + ["404.html"]
DOWNLOAD = {rel_of(V.PAGES["download"]["path"][l]) for l in ("fr", "en")}
HELD = ("/telecharger/", "/en/download/")


def metadata(rel):
    """What a search engine or a shared link shows: the title and the
    descriptions. A word kept out of the page must stay out of these too."""
    text = read(rel)
    title = re.findall(r"<title>([^<]*)</title>", text)
    metas = [a.get("content", "") for t, a in parse(text).tags
             if t == "meta" and (a.get("name") == "description"
                                 or a.get("property", "").startswith("og:"))
             and not a.get("property", "").startswith("og:image")
             and a.get("property") not in ("og:url", "og:locale", "og:type")]
    return " ".join(title + metas)


def visible(rel):
    c = parse(read(rel))
    alts = [a.get("alt", "") for t, a in c.tags if t == "img"]
    return " ".join(c.text + alts) + " " + metadata(rel)


class V1Tests(unittest.TestCase):
    def test_every_page_is_built(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, rel)), rel)

    def test_no_inline_script_or_style(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                with self.subTest(page=rel, tag=tag):
                    self.assertNotIn("style", attrs)
                    self.assertNotEqual(tag, "style")
                    self.assertFalse(any(k.startswith("on") for k in attrs))
                    if tag == "script":
                        self.assertTrue(attrs.get("src", "").startswith("/assets/"))

    def test_nothing_from_elsewhere(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                for key in ("src", "href", "action", "srcset"):
                    value = attrs.get(key)
                    if value is None or tag == "link" and attrs.get("rel") in (
                            "canonical", "alternate"):
                        continue
                    allowed = ("/", "#", "mailto:bonjour@")
                    if rel in DOWNLOAD and tag == "a":
                        allowed += MIRRORS
                    # the community server, where bugs are reported
                    if tag == "a" and value == B.DISCORD:
                        allowed += (B.DISCORD,)
                    with self.subTest(page=rel, value=value):
                        self.assertTrue(value.startswith(allowed), value)
        for name in ("v1.css", "lang.js", "app.js", "site.css"):
            text = read("assets/" + name)
            urls = [u for u in re.findall(r"https?://[^\s\"')]+", text) if "w3.org" not in u]
            self.assertEqual(urls, [], name)

    def test_local_links_exist(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                value = attrs.get("src") or (attrs.get("href") if tag in ("a", "link") else None)
                if not value or not value.startswith("/"):
                    continue
                target = value.split("#")[0].split("?")[0]
                path = os.path.join(ROOT, target.lstrip("/"))
                if target.endswith("/"):
                    path = os.path.join(path, "index.html")
                with self.subTest(page=rel, link=value):
                    self.assertTrue(os.path.isfile(path), path)

    def test_anchors_on_the_page_exist(self):
        for rel in PAGES:
            text = read(rel)
            for anchor in re.findall(r'href="#([a-z0-9-]+)"', text):
                with self.subTest(page=rel, anchor=anchor):
                    self.assertIn(f'id="{anchor}"', text)

    def test_assets_are_versioned(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                value = attrs.get("src") or (attrs.get("href") if tag == "link" else None)
                if not value or not value.startswith("/assets/"):
                    continue
                name, _, query = value[len("/assets/"):].partition("?")
                with open(os.path.join(ROOT, "assets", name), "rb") as f:
                    want = "v=" + hashlib.sha256(f.read()).hexdigest()[:10]
                with self.subTest(page=rel, asset=value):
                    self.assertEqual(query, want)

    def test_visible_text_names_nothing_it_should_not(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                self.assertEqual(forbidden(visible(rel)), [])

    def test_the_forbidden_names_rule_can_fail(self):
        # a rule that never fires proves nothing: try it on what it is for
        for sample in ("lancé par Wine", "built with AI", "l'IA a écrit", "Microsoft Edge",
                       "based on Ubuntu"):
            with self.subTest(sample=sample):
                self.assertTrue(forbidden(sample), sample)
        for sample in ("j'ai mesuré", "basé sur Ubuntu 26.04 LTS",
                       "marque de Microsoft Corporation", "programmes Windows"):
            with self.subTest(sample=sample):
                self.assertEqual(forbidden(sample), [], sample)

    def test_no_word_from_an_advertisement(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                self.assertIsNone(HOLLOW.search(visible(rel)),
                                  HOLLOW.search(visible(rel)))
                self.assertIsNone(EMOJI.search(read(rel)))

    def test_languages_match(self):
        for fr, en in PAIRS:
            a, b = parse(read(fr)), parse(read(en))
            with self.subTest(page=fr):
                self.assertEqual([t for t, _ in a.tags], [t for t, _ in b.tags])
                self.assertIn('<html lang="fr">', read(fr))
                self.assertIn('<html lang="en">', read(en))

    def test_the_language_script_knows_every_page(self):
        js = read("assets/lang.js")
        for fr, en in PAIRS:
            with self.subTest(page=fr):
                self.assertIn(f'"/{fr[:-len("index.html")]}": "/{en[:-len("index.html")]}"', js)

    def test_every_screenshot_is_described_once(self):
        for rel in PAGES:
            tags = parse(read(rel)).tags
            descriptions = [a["alt"] for t, a in tags if t == "img" and "/shots/" in a.get("src", "")]
            text = read(rel)
            descriptions += re.findall(r'<p class="todo-what">([^<]*)</p>', text)
            with self.subTest(page=rel):
                self.assertEqual(len(descriptions), len(set(descriptions)))
                for d in descriptions:
                    self.assertGreaterEqual(len(d.split()), 8, d)

    def test_every_shot_id_is_declared(self):
        for block_list in [V.HOME["blocks"]] + [c["blocks"] for c in V.CONTENT.values()]:
            for b in block_list:
                if b[0] == "shot":
                    self.assertIn(b[1], V.SHOTS)
        # b21 and b22 of the 0.3 tests show the upstream name on screen
        self.assertFalse([s for s in V.SHOTS if re.match(r"b2[12]\b", s)])

    def test_measures_carry_their_origin(self):
        today = datetime.date.today()
        for key, m in V.MEASURES.items():
            with self.subTest(measure=key):
                self.assertIn(m["machine"], V.MACHINES)
                self.assertLessEqual(datetime.date.fromisoformat(m["date"]), today)
                self.assertRegex(m["version"], r"^\d+\.\d+")
                for lang in ("fr", "en"):
                    self.assertTrue(m["name"][lang] and m["value"][lang] and m["how"][lang])

    def test_a_printed_figure_says_where_it_comes_from(self):
        # every measurement table is followed by its machine and date
        for rel in PAGES:
            text = read(rel)
            for table in re.findall(r'<table class="measures">.*?</div>', text, re.S):
                with self.subTest(page=rel):
                    self.assertRegex(table, r"(Mesuré le|Measured on) .*\d{4}")

    def test_the_free_space_figure_is_the_installers(self):
        if not os.path.exists(WELCOMEQ):
            self.skipTest("the installer repository is not checked out next to this one")
        with open(WELCOMEQ, encoding="utf-8") as f:
            gb = re.search(r"^\s*requiredStorage:\s*([0-9.]+)\s*$", f.read(), re.M).group(1)
        self.assertEqual(V.FREE_GB, int(float(gb)))
        for lang, unit in (("fr", "Go"), ("en", "GB")):
            page = read(rel_of(V.PAGES["hardware"]["path"][lang]))
            self.assertIn(f"{V.FREE_GB} {unit}", page.replace(" ", " "))

    def test_the_metadata_rules_can_fail(self):
        # the coming-soon description ("élégant", "Inscrivez-vous") once sat
        # on the V1 privacy and 404 pages, unseen: the checks read only the text
        sample = ('<html><head><title>Raye</title><meta name="description" '
                  'content="un bureau élégant"></head><body><p>texte</p></body></html>')
        global read
        real = read
        read = lambda rel: sample
        try:
            self.assertTrue(HOLLOW.search(visible("x")))
        finally:
            read = real

    def test_descriptions_fit_a_search_result(self):
        for rel in PAGES:
            descriptions = [a.get("content", "") for t, a in parse(read(rel)).tags
                            if t == "meta" and a.get("name") == "description"]
            with self.subTest(page=rel):
                self.assertEqual(len(descriptions), 1)
                self.assertLessEqual(len(descriptions[0]), 160, descriptions[0])
            title = re.search(r"<title>([^<]*)</title>", read(rel)).group(1)
            with self.subTest(page=rel, title=title):
                self.assertLessEqual(title.count("Raye Linux"), 1, title)

    def test_every_limits_box_has_its_own_name(self):
        # six identical "complementary" landmarks tell a screen reader nothing
        for rel in PAGES:
            text = read(rel)
            ids = set(re.findall(r'\bid="([^"]+)"', text))
            labels = re.findall(r'<aside class="limits" aria-labelledby="([^"]+)">', text)
            with self.subTest(page=rel):
                self.assertEqual(len(labels), text.count('<aside class="limits"'))
                self.assertEqual(len(labels), len(set(labels)))
                for label in labels:
                    for ref in label.split():
                        self.assertIn(ref, ids, ref)

    def test_the_404_wears_the_v1_shell(self):
        text = read("404.html")
        for piece in ('class="skip-link"', '<header class="topbar">', 'class="footer v1-footer"',
                      "/assets/v1.css", 'name="robots" content="noindex"'):
            with self.subTest(piece=piece):
                self.assertIn(piece, text)
        self.assertNotIn("/assets/lang.js", text)
        self.assertEqual(text.count("<h1"), 1)

    def test_screenshots_come_only_from_shots(self):
        """The coming-soon page's 0.2 pictures share names with V1 shots
        (lock, settings, store): only shots/ may feed the V1 site, and what
        it holds is what the site's assets/shots holds."""
        sys.path.insert(0, os.path.join(REPO, "tools"))
        import site_v1
        src = site_v1.SHOTS_SRC
        want = sorted(n for n in (os.listdir(src) if os.path.isdir(src) else ())
                      if site_v1.SHOT_FILE.match(n))
        here = os.path.join(ROOT, "assets", "shots")
        have = sorted(os.listdir(here)) if os.path.isdir(here) else []
        self.assertEqual(have, want)
        for rel in PAGES:
            for shot in re.findall(r'/assets/shots/([^"?]+)', read(rel)):
                with self.subTest(page=rel, shot=shot):
                    self.assertIn(shot, want)

    def test_no_page_links_to_a_held_one(self):
        if B.DOWNLOAD_LIVE:
            self.skipTest("the download pages are live")
        for rel in PAGES:
            if rel in DOWNLOAD:
                continue
            for tag, attrs in parse(read(rel)).tags:
                href = attrs.get("href", "")
                with self.subTest(page=rel, href=href):
                    self.assertFalse(href.startswith(HELD), href)

    def test_at_launch_nothing_is_left_to_take_or_remeasure(self):
        """While the site is in site-v1/ the placeholders and the 0.3
        figures are expected. The day it takes site/ over, none may stay."""
        placeholders = [rel for rel in PAGES if 'class="shot-todo"' in read(rel)]
        old = [k for k, m in V.MEASURES.items() if m["version"] != V.VERSION]
        # every screenshot says, in shots/manifest.json, which version it shows
        manifest_path = os.path.join(REPO, "shots", "manifest.json")
        manifest = {}
        if os.path.isfile(manifest_path):
            import json
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
        taken = sorted({n.rsplit("-", 1)[0] for n in os.listdir(os.path.join(REPO, "shots"))
                        if re.match(r"^[a-z0-9-]+-(fr|en)-1600\.webp$", n)}) \
            if os.path.isdir(os.path.join(REPO, "shots")) else []
        stale = [k for k in taken if manifest.get(k, {}).get("version") != V.VERSION]
        if not LIVE:
            self.skipTest("preview: %d pages with placeholders, %d figures to remeasure, "
                          "%d screenshots not from %s" % (len(placeholders), len(old),
                                                          len(stale), V.VERSION))
        self.assertEqual(placeholders, [], "screenshots still to take")
        self.assertEqual(old, [], "figures not measured on %s" % V.VERSION)
        self.assertEqual(stale, [], "screenshots without a %s entry in shots/manifest.json"
                         % V.VERSION)


if __name__ == "__main__":
    unittest.main()
