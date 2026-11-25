"""The V1 legal pages, the FAQ and the roadmap pages say what the code and the
roadmap do: cookies page, lawyer notice, staff panel retention, the data and
account questions, no V1.2 left."""

import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(WEBSITE, "tools"))

from raye_site import applications as apps  # noqa: E402


def page(rel):
    with open(os.path.join(WEBSITE, "site-v1", rel, "index.html"), encoding="utf-8") as f:
        text = re.sub(r"<[^>]+>", " ", f.read())
    return re.sub(r"\s+", " ", text.replace(" ", " "))


class LegalFaqTests(unittest.TestCase):
    def test_cookies_page_exists_in_both_languages_and_says_none(self):
        self.assertIn("uses no cookies", page("en/cookies"))
        self.assertIn("n'utilise aucun témoin", page("temoins"))

    def test_every_legal_page_carries_the_lawyer_notice(self):
        for rel, word in (("en/privacy", "lawyer"), ("en/terms", "lawyer"),
                          ("en/cookies", "lawyer"), ("en/beta-terms", "lawyer"),
                          ("confidentialite", "juriste"), ("conditions", "juriste"),
                          ("temoins", "juriste"), ("conditions-beta", "juriste")):
            with self.subTest(page=rel):
                self.assertIn(word, page(rel))

    def test_privacy_describes_the_staff_panel_as_the_code_keeps_it(self):
        en, fr = page("en/privacy"), page("confidentialite")
        self.assertIn("internal notes", en)
        self.assertIn("notes internes", fr)
        self.assertIn("deleted after one year", en)
        self.assertIn("effacé au bout d'un an", fr)
        self.assertEqual(apps.KEEP_LOG, 365 * 24 * 3600)

    def test_privacy_and_terms_say_raye_community_is_not_open(self):
        self.assertIn("not open yet", page("en/privacy"))
        self.assertIn("is not open yet", page("en/terms"))
        self.assertIn("pas encore ouverte", page("confidentialite"))

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
        self.assertIn("accounts are not open yet", facts.lower().replace("raye ", ""))

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
