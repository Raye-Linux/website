"""The Join pages name the update channel each role gets: the channels are
in Raye Update since the V1 (Raye Insider), so none is "planned"."""

import os
import re
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


def text(rel):
    with open(os.path.join(v1_root(), rel, "index.html"), encoding="utf-8") as f:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", f.read()))


class JoinChannelTests(unittest.TestCase):
    def test_no_channel_is_planned_any_more(self):
        for root, _, files in os.walk(v1_root()):
            if "index.html" not in files:
                continue
            rel = os.path.relpath(root, v1_root())
            page = text(rel)
            with self.subTest(page=rel):
                self.assertNotRegex(page, r"(beta|dev|bêta publique|bêta) \((planned|prévu)\)")


if __name__ == "__main__":
    unittest.main()
