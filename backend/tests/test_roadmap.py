"""The roadmap page: the same list as #roadmap on the Discord, from
tools/roadmap.json, in both languages. A new item with no French stops the
build, so the French page never shows an English line."""

import copy
import json
import os
import re
import unittest

from test_site import BASE_PHRASE, DISCORD, ROOT, TOOLS, builder, parse, read

PAGES = {"en": "en/roadmap/index.html", "fr": "fr/feuille-de-route/index.html"}
HOMES = {"en": "en/index.html", "fr": "fr/index.html"}

# The coming-soon rule, except that Windows may be named: the roadmap is
# about what Raye does for people who come from it (the V1 site says the
# same). "Arch" is out too: no other system is named on the site.
NAMES = re.compile(
    r"\b(microsoft|ubuntu|kubuntu|debian|fedora|arch|mint|macos|apple|android|"
    r"chrome ?os|wine|ia|ai|intelligence artificielle|artificial intelligence|"
    r"chatgpt|claude|gpt|copilot)\b", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")


def roadmap():
    with open(os.path.join(TOOLS, "roadmap.json"), encoding="utf-8") as f:
        return json.load(f)


def visible(rel):
    c = parse(read(rel))
    return " ".join(c.text)


def norm(text):
    return re.sub(r"\s+", " ", text.replace(" ", " ")).strip()


class RoadmapTests(unittest.TestCase):
    def test_page_exists_in_both_languages(self):
        b = builder()
        self.assertEqual(b.PATHS["en"]["roadmap"], "/en/roadmap/")
        self.assertEqual(b.PATHS["fr"]["roadmap"], "/fr/feuille-de-route/")
        for lang, rel in PAGES.items():
            text = read(rel)
            self.assertIn('<html lang="%s">' % lang, text)
            self.assertIn("<h1>", text)

    def test_copy_is_the_discord_list(self):
        # update.sh copies the Discord roadmap here; check it is the same shape
        data = roadmap()
        self.assertTrue(data["sections"])
        for section in data["sections"]:
            self.assertTrue(section["title"])
            for state, text in section["items"]:
                self.assertIn(state, ("done", "doing", "planned"))
                self.assertTrue(text)

    def test_every_item_is_on_both_pages(self):
        b = builder()
        for lang, rel in PAGES.items():
            page = norm(visible(rel))
            sections = b.roadmap_sections(roadmap(), lang)
            self.assertEqual(len(sections), len(roadmap()["sections"]))
            for title, _, _, items in sections:
                name, note = b.roadmap_heading(title)
                with self.subTest(lang=lang, title=title):
                    self.assertIn(norm(name), page)
                    self.assertIn(norm(note), page)
                for state, text in items:
                    with self.subTest(lang=lang, item=text):
                        self.assertIn(norm(text), page)
            self.assertEqual(len(re.findall(r'class="rm-item ', read(rel))),
                             sum(len(s["items"]) for s in roadmap()["sections"]))

    def test_order_follows_the_json(self):
        b = builder()
        for lang, rel in PAGES.items():
            page = norm(visible(rel))
            at = -1
            for title, _, _, items in b.roadmap_sections(roadmap(), lang):
                for text in [b.roadmap_heading(title)[0]] + [t for _, t in items]:
                    found = page.find(norm(text), at + 1)
                    with self.subTest(lang=lang, text=text):
                        self.assertGreater(found, at)
                    at = found

    def test_english_items_stay_off_the_french_page(self):
        b = builder()
        page = norm(visible(PAGES["fr"]))
        renamed = set(b.roadmap_text.RENAMED)
        for section in roadmap()["sections"]:
            for _, text in section["items"]:
                english = b.roadmap_clean(text)
                if english in renamed or english == b.roadmap_text.FR.get(english):
                    continue
                with self.subTest(item=english):
                    self.assertNotIn(norm(english), page)

    def test_a_new_item_without_french_stops_the_build(self):
        b = builder()
        data = copy.deepcopy(roadmap())
        data["sections"][0]["items"].append(["planned", "A brand new thing nobody translated"])
        for lang in ("en", "fr"):
            with self.subTest(lang=lang):
                with self.assertRaises(SystemExit) as cm:
                    b.roadmap_sections(data, lang)
                self.assertIn("A brand new thing nobody translated", str(cm.exception))

    def test_a_new_section_without_french_stops_the_build(self):
        b = builder()
        data = copy.deepcopy(roadmap())
        data["sections"].append({"title": "🕒 V4", "color": "8a8f98",
                                 "items": [["planned", "More languages"]]})
        with self.assertRaises(SystemExit) as cm:
            b.roadmap_sections(data, "fr")
        self.assertIn("V4", str(cm.exception))

    def test_an_unknown_state_stops_the_build(self):
        b = builder()
        data = copy.deepcopy(roadmap())
        data["sections"][0]["items"][0][0] = "maybe"
        with self.assertRaises(SystemExit):
            b.roadmap_sections(data, "en")

    def test_states_are_shown(self):
        b = builder()
        for lang, rel in PAGES.items():
            text = read(rel)
            labels = b.roadmap_text.STATES[lang]
            for section in roadmap()["sections"]:
                for state, _ in section["items"]:
                    self.assertIn('class="rm-item rm-%s"' % state, text)
            for state in ("done", "doing", "planned"):
                with self.subTest(lang=lang, state=state):
                    self.assertIn(labels[state], visible(rel))

    def test_no_emoji_and_no_forbidden_name(self):
        for lang, rel in PAGES.items():
            text = BASE_PHRASE.sub("", visible(rel))
            with self.subTest(lang=lang):
                self.assertIsNone(NAMES.search(text), NAMES.search(text))
                self.assertIsNone(EMOJI.search(read(rel)))

    def test_the_names_rule_can_fail(self):
        for sample in ("Arch edition", "Android apps", "the Ubuntu edition", "j'ai fait"):
            self.assertTrue(NAMES.search(sample), sample)
        self.assertIsNone(NAMES.search("A real Windows 10 Start menu"))

    def test_intro_points_to_the_ideas_on_discord(self):
        for lang, rel in PAGES.items():
            text = read(rel)
            intro = text[text.index("<main"):text.index('class="rm-list"')]
            with self.subTest(lang=lang):
                self.assertIn("#ideas", intro)
                self.assertIn('href="%s"' % DISCORD, intro)

    def test_nav_footer_and_home_link_the_roadmap(self):
        b = builder()
        for lang, home in HOMES.items():
            path = b.PATHS[lang]["roadmap"]
            for rel in (home, PAGES[lang], "%s" % b.PATHS[lang]["privacy"].lstrip("/") + "index.html"):
                text = read(rel)
                nav = text[text.index('<nav class="nav"'):text.index("</nav>")]
                foot = text[text.index('<footer class="footer"'):]
                with self.subTest(page=rel):
                    self.assertIn('href="%s"' % path, nav)
                    self.assertIn('href="%s"' % path, foot)
            text = read(home)
            faq = text[text.index('id="questions"'):text.index("</section>", text.index('id="questions"'))]
            self.assertIn('href="%s"' % path, faq, lang)

    def test_the_roadmap_page_marks_itself_in_the_nav(self):
        for lang, rel in PAGES.items():
            text = read(rel)
            nav = text[text.index('<nav class="nav"'):text.index("</nav>")]
            self.assertEqual(nav.count('aria-current="page"'), 1, lang)

    def test_language_switch_leads_to_the_twin(self):
        b = builder()
        for lang, rel in PAGES.items():
            other = "en" if lang == "fr" else "fr"
            self.assertIn('class="lang-switch" href="%s"' % b.PATHS[other]["roadmap"], read(rel))

    def test_layout_is_plain_headings_and_lists(self):
        # no cards, badges, legend or icons: a version heading, one status
        # line, then a plain list
        b = builder()
        for lang, rel in PAGES.items():
            text = read(rel)
            main = text[text.index("<main"):text.index("</main>")]
            with self.subTest(lang=lang):
                for word in ('class="card', "rm-badge", "rm-legend", "<svg", "btn"):
                    self.assertNotIn(word, main)
                levels = re.findall(r"<h([1-6])", main)
                self.assertEqual(levels[0], "1")
                self.assertEqual(set(levels[1:]), {"2"})
                self.assertEqual(levels.count("2"), len(roadmap()["sections"]))
                sections = b.roadmap_sections(roadmap(), lang)
                self.assertEqual(main.count('class="rm-status"'),
                                 sum(1 for t, _, s, _ in sections
                                     if b.roadmap_status(t, s, b.roadmap_text.STATES[lang])[1]))

    def test_headings_keep_the_version_and_the_status_line_the_rest(self):
        b = builder()
        labels = b.roadmap_text.STATES["en"]
        self.assertEqual(b.roadmap_heading("V1 Beta 1 · out November 19"),
                         ("V1 Beta 1", "out November 19"))
        self.assertEqual(b.roadmap_heading("V1 Beta 2 (next big update)"),
                         ("V1 Beta 2", "next big update"))
        self.assertEqual(b.roadmap_status("V1 Beta 2 (next big update)", "doing", labels),
                         ("V1 Beta 2", "In progress · next big update"))
        self.assertEqual(b.roadmap_status("V2", "planned", labels), ("V2", "Planned"))
        # a heading that already says its state does not repeat it
        self.assertEqual(b.roadmap_status("Recently done", "done", labels),
                         ("Recently done", ""))

    def test_an_item_unlike_its_version_says_its_state_in_words(self):
        b = builder()
        data = copy.deepcopy(roadmap())
        section = next(s for s in data["sections"] if s["items"][0][0] == "planned")
        section["items"][0][0] = "done"
        load = b.roadmap_load
        b.roadmap_load = lambda: data
        try:
            page = b.roadmap("en")
        finally:
            b.roadmap_load = load
        self.assertIn('class="rm-item rm-done"', page)
        self.assertIn('<span class="rm-tag">(done)</span>', page)

    def test_the_style_stays_plain(self):
        with open(os.path.join(ROOT, "assets", "site.css"), encoding="utf-8") as f:
            css = f.read()
        block = css[css.index("/* roadmap"):css.index(".changes-next")]
        for word in ("box-shadow", "gradient", "line-through", "border-radius", "glow",
                     "text-align: center"):
            with self.subTest(word=word):
                self.assertNotIn(word, block)

    def test_the_short_addresses_redirect(self):
        with open(os.path.join(ROOT, "..", "deploy", "nginx", "raye-site.conf"),
                  encoding="utf-8") as f:
            conf = f.read()
        self.assertRegex(conf, r"location ~ \^/roadmap/\?\$ \{ return 301 /en/roadmap/")


if __name__ == "__main__":
    unittest.main()
