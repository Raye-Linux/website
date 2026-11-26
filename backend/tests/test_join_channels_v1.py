"""The Join pages name the update channel each role gets: the channels are
in Raye Update since the V1 (Raye Insider), so none is "planned"."""

import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.normpath(os.path.join(HERE, "..", ".."))


def text(rel):
    with open(os.path.join(WEBSITE, "site-v1", rel, "index.html"), encoding="utf-8") as f:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", f.read()))


class JoinChannelTests(unittest.TestCase):
    def test_no_channel_is_planned_any_more(self):
        for root, _, files in os.walk(os.path.join(WEBSITE, "site-v1")):
            if "index.html" not in files:
                continue
            rel = os.path.relpath(root, os.path.join(WEBSITE, "site-v1"))
            page = text(rel)
            with self.subTest(page=rel):
                self.assertNotRegex(page, r"(beta|dev|bêta publique|bêta) \((planned|prévu)\)")


if __name__ == "__main__":
    unittest.main()
