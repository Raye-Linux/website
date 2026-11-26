"""support_facts.md: what both Raye assistants (the help bubble and the
Discord bot) are told is always true. It is sent as is, so a stale or wrong
line becomes a wrong answer. These checks cover what can be checked
without a model: the links, the words, the figures the site also prints,
and the Settings names it gives."""

import glob
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.normpath(os.path.join(HERE, "..", ".."))
FACTS = os.path.join(WEBSITE, "backend", "raye_site", "support_facts.md")
SITE = os.path.join(WEBSITE, "site")
SETTINGS = os.path.normpath(os.path.join(WEBSITE, "..", "settings"))

# A path such as /en/download/, rayelinux.com/fr/feuille-de-route/ or, on the
# V1 site where French is at the root, /telecharger/ -- one or more lowercase
# segments, each closed by a slash
# (not a file path such as /root/tools/x.py: nothing may follow the slash)
PATH = re.compile(r"(?<![\w./-])(?:rayelinux\.com)?(/(?:[a-z0-9-]+/)+)(?![\w-]|\.\w)")

# Words the assistants must never write. "Wine" is the name the owner wants
# hidden everywhere (say "Windows programs support").
FORBIDDEN = re.compile(r"\bwine\b", re.I)

# Sentences that were true once and are not any more.
STALE = (
    "Until the next update",                  # Optional updates is in Settings since 0.5.5
    "not from sleep",                         # Clock alarms wake the PC since Beta 2
    "600-700", "600–700", "600 to 700",        # the RAM goal, never reached
    "2,881,132,544",                          # the size of the Beta 1 image
    "Chromebooks are not a good fit",         # Intel/AMD Chromebooks have a guide
)

# Settings names the facts give, with where Settings shows them. Each one must
# still exist in the Settings sources, or the assistant sends people to a
# page that is not there.
SETTINGS_NAMES = (
    "Files from Windows", "Desktop style", "Turn sleep back on", "Power & battery",
    "Device security", "Allow an app through the firewall", "DNS server assignment",
    "Add VPN", "Storage Sense", "Do not disturb", "Game Mode", "Optional updates",
    "Performance options", "NVIDIA Control Panel", "Other updates",
)


def facts():
    with open(FACTS, encoding="utf-8") as f:
        return f.read()


def settings_text():
    texts = []
    for pattern in ("src/qml/**/*.qml", "data/search/*.json", "src/**/*.cpp"):
        for name in glob.glob(os.path.join(SETTINGS, pattern), recursive=True):
            with open(name, encoding="utf-8", errors="replace") as f:
                texts.append(f.read())
    return "\n".join(texts)


def v1():
    import sys
    sys.path.insert(0, os.path.join(WEBSITE, "tools"))
    import build_pages
    import site_v1_text
    return build_pages.V1_LIVE, site_v1_text


def home_faq(lang):
    """The questions a visitor reads: the home page FAQ of the coming-soon
    site, the Questions page of the V1 site."""
    live, V = v1()
    rel = (V.PAGES["questions"]["path"][lang].strip("/") if live else lang)
    with open(os.path.join(SITE, rel, "index.html"), encoding="utf-8") as f:
        text = f.read()
    if live:
        return text[text.index("<main"):text.index("</main>")].replace("\u00a0", " ")
    return text[text.index('id="questions"'):]


class FactsTests(unittest.TestCase):
    def test_every_site_link_is_a_page_that_exists(self):
        paths = PATH.findall(facts())
        self.assertGreater(len(paths), 10)
        for path in paths:
            with self.subTest(path=path):
                self.assertTrue(os.path.isfile(os.path.join(SITE, path.strip("/"), "index.html")),
                                path)

    def test_every_page_of_the_site_is_listed(self):
        # the facts say "never give any other link": a page left out of the
        # list is a page the assistants refuse to name
        listed = set(PATH.findall(facts()))
        for name in glob.glob(os.path.join(SITE, "*", "**", "index.html"), recursive=True):
            rel = "/" + os.path.relpath(os.path.dirname(name), SITE) + "/"
            with self.subTest(page=rel):
                self.assertIn(rel, listed)

    def test_no_forbidden_word(self):
        self.assertIsNone(FORBIDDEN.search(facts()))

    def test_no_stale_sentence(self):
        text = facts()
        for sentence in STALE:
            with self.subTest(sentence=sentence):
                self.assertNotIn(sentence, text)

    def test_the_idle_memory_is_the_figure_the_site_prints(self):
        text = facts()
        live, V = v1()
        if live:
            # the figure the V1 site prints, from its measures table
            ram = V.MEASURES["ram"]["value"]
            self.assertIn("about " + ram["en"], text)
            self.assertIn(ram["en"], home_faq("en"))
            self.assertIn(ram["fr"], home_faq("fr"))
            return
        self.assertIn("about 850 MB", text)
        self.assertIn("about 850 MB", home_faq("en"))
        self.assertIn("environ 850 Mo", home_faq("fr"))

    def test_the_settings_names_exist_in_settings(self):
        if not os.path.isdir(os.path.join(SETTINGS, "src")):
            self.skipTest("the settings repository is not checked out next to this one")
        source = settings_text()
        text = facts()
        for name in SETTINGS_NAMES:
            with self.subTest(name=name):
                self.assertIn(name, text)
                self.assertIn(name, source)

    def test_the_checks_can_fail(self):
        self.assertTrue(FORBIDDEN.search("runs through Wine"))
        self.assertEqual(PATH.findall("see rayelinux.com/en/bugs/ or /fr/x/"), ["/en/bugs/", "/fr/x/"])
        self.assertFalse(os.path.isfile(os.path.join(SITE, "en", "bugs", "index.html")))


if __name__ == "__main__":
    unittest.main()
