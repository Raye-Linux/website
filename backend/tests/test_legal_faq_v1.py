"""The V1 legal pages, the FAQ and the roadmap pages say what the code and the
roadmap do: cookies page, lawyer notice, staff panel retention, the data and
account questions, no V1.2 left."""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.normpath(os.path.join(HERE, "..", ".."))


def v1_root():
    """Where the V1 site is: site/ since the launch (build_pages.V1_LIVE),
    site-v1/ before. Reading site-v1/ after the launch would check a stale copy."""
    import sys
    sys.path.insert(0, os.path.join(WEBSITE, "tools"))
    import build_pages
    return os.path.join(WEBSITE, "site" if build_pages.V1_LIVE else "site-v1")
sys.path.insert(0, os.path.join(WEBSITE, "tools"))

from raye_site import applications as apps  # noqa: E402


def page(rel):
    with open(os.path.join(v1_root(), rel, "index.html"), encoding="utf-8") as f:
        text = re.sub(r"<[^>]+>", " ", f.read())
    return re.sub(r"\s+", " ", text.replace(" ", " "))


class LegalFaqTests(unittest.TestCase):
    def test_cookies_page_exists_in_both_languages_and_says_none(self):
        self.assertIn("uses no cookies", page("en/cookies"))
        self.assertIn("n'utilise aucun témoin", page("temoins"))

    def test_every_legal_page_carries_the_honest_lawyer_notice(self):
        # Decision of the project: no lawyer reads these pages. They say who
        # wrote them and that no lawyer reviewed them, never that one will.
        for rel, notice, promise in (
                ("en/privacy", "not reviewed by a lawyer", "has to be read by a lawyer"),
                ("en/terms", "not reviewed by a lawyer", "has to be read by a lawyer"),
                ("en/cookies", "not reviewed by a lawyer", "has to be read by a lawyer"),
                ("en/beta-terms", "not reviewed by a lawyer", "has to be read by a lawyer"),
                ("confidentialite", "pas été relues par un avocat", "faire relire par un juriste"),
                ("conditions", "pas été relues par un avocat", "faire relire par un juriste"),
                ("temoins", "pas été relues par un avocat", "faire relire par un juriste"),
                ("conditions-beta", "pas été relues par un avocat", "faire relire par un juriste")):
            with self.subTest(page=rel):
                text = page(rel)
                self.assertIn(notice, text)
                self.assertIn("Raye" , text)
                self.assertNotIn(promise, text)

    def test_privacy_describes_the_staff_panel_as_the_code_keeps_it(self):
        en, fr = page("en/privacy"), page("confidentialite")
        self.assertIn("internal notes", en)
        self.assertIn("notes internes", fr)
        self.assertIn("deleted after one year", en)
        self.assertIn("effacé au bout d'un an", fr)
        self.assertEqual(apps.KEEP_LOG, 365 * 24 * 3600)

    def test_privacy_and_terms_say_raye_community_is_open_as_a_beta(self):
        # open since 1.0: the pages say what it keeps now, not what it will
        for rel in ("en/privacy", "en/terms", "confidentialite", "conditions",
                    "en/community", "communaute"):
            text = page(rel)
            with self.subTest(page=rel):
                self.assertRegex(text, r"(open as a beta|ouverte en bêta)")
                self.assertNotRegex(text, r"(not open yet|pas encore ouvert|once it opens|"
                                          r"quand elle ouvrira)")
        self.assertIn("moderation log", page("en/privacy"))
        self.assertIn("journal de modération", page("confidentialite"))

    def test_accounts_and_insider_are_described_as_open(self):
        for rel in ("en/privacy", "confidentialite", "en/cookies", "temoins", "en/questions",
                    "questions", "en/beta-terms", "conditions-beta", "en/insider", "insider"):
            text = page(rel)
            with self.subTest(page=rel):
                self.assertNotRegex(text, r"(not open yet|pas encore ouverts?|once they open|"
                                          r"quand ils ouvriront|planned and not open|"
                                          r"sont prévus|not built yet|pas encore construit)")
        self.assertIn("Settings › Raye Update › Raye Insider", page("en/beta-terms"))
        self.assertIn("account.rayelinux.com", page("en/privacy"))

    def test_the_faq_answers_data_and_accounts(self):
        en, fr = page("en/questions"), page("questions")
        self.assertIn("Does Raye send data about me?", en)
        self.assertIn("Do I need a Raye account?", en)
        self.assertIn("Raye envoie-t-il des données sur moi ?", fr)
        self.assertIn("Faut-il un compte Raye ?", fr)

    def test_the_assistant_facts_match_the_faq_on_data(self):
        with open(os.path.join(WEBSITE, "backend", "raye_site", "support_facts.md"),
                  encoding="utf-8") as f:
            facts = f.read()
        self.assertIn("DATA AND PRIVACY", facts)
        self.assertIn("no usage reports and no crash reports", facts)
        self.assertNotIn("not open yet", facts)
        self.assertIn("account.rayelinux.com", facts)
        self.assertIn("community.rayelinux.com", facts)

    def test_nothing_after_v1_is_called_1_2(self):
        for rel in ("en/whats-next", "ensuite"):
            text = page(rel)
            with self.subTest(page=rel):
                self.assertNotRegex(text, r"\b1\.2\b")
                self.assertRegex(text, r"1\.1")
        for rel in ("en/roadmap", "feuille-de-route"):
            self.assertNotIn("V1.2", page(rel))


if __name__ == "__main__":
    unittest.main()
