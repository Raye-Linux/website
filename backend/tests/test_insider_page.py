"""The Raye Insider page of the V1 site: both languages, the four channels
with their Settings names, the way in for each one, and leaving without a
downgrade -- and every link on it leads to a page the site builds."""

import os
import re
import sys
import unittest

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..", "..")
sys.path.insert(0, os.path.join(REPO, "tools"))
import site_v1_text as V  # noqa: E402
from test_site_v1 import ROOT, visible  # noqa: E402


def page(lang):
    rel = V.PAGES["insider"]["path"][lang].lstrip("/") + "index.html"
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class InsiderPageTests(unittest.TestCase):
    def test_both_languages_name_the_four_channels(self):
        for lang, names in (("en", ("Stable", "Public Beta", "Beta", "Dev")),
                            ("fr", ("Stable", "Bêta publique", "Bêta", "Dev"))):
            text = page(lang)
            for name in names:
                self.assertIn(f"<dt>{name}</dt>", text, (lang, name))
            self.assertIn("Raye Insider", text)

    def test_it_says_where_to_pick_and_that_leaving_never_downgrades(self):
        self.assertIn("Settings › Raye Update › Raye Insider", page("en"))
        self.assertIn("Paramètres › Raye Update › Raye Insider", page("fr"))
        self.assertIn("stay until Stable catches up", page("en"))
        self.assertIn("restent jusqu'à ce que Stable les rattrape", page("fr"))

    def test_beta_and_dev_go_through_the_account_applications(self):
        for lang in ("en", "fr"):
            text = page(lang)
            for key in ("jpublic", "jbeta", "jdev"):
                self.assertIn(f'href="{V.PAGES[key]["path"][lang]}"', text, (lang, key))

    def test_every_page_of_the_site_links_to_it(self):
        for lang in ("en", "fr"):
            home = V.PAGES["home"]["path"][lang].lstrip("/") + "index.html"
            with open(os.path.join(ROOT, home), encoding="utf-8") as f:
                self.assertIn(f'href="{V.PAGES["insider"]["path"][lang]}"', f.read())

    def test_the_language_switch_knows_it(self):
        with open(os.path.join(ROOT, "assets", "lang.js"), encoding="utf-8") as f:
            self.assertIn('"/insider/": "/en/insider/"', f.read())


if __name__ == "__main__":
    unittest.main()
