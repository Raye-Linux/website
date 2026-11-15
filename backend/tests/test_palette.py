# SPDX-License-Identifier: GPL-3.0-or-later
"""The site wears the Raye Night of the desktop: neutral greys, the violet
only on buttons and links, no magenta."""
import os
import re
import unittest

SITE = os.path.join(os.path.dirname(__file__), "..", "..", "site")
CSS = open(os.path.join(SITE, "assets", "site.css"), encoding="utf-8").read()

# the violet greys and the magenta of the 0.2 palette
OLD = ("130E1F", "0F0B19", "1A1028", "0E0A17", "F3EAFF", "B9A8D6", "9889B1", "8D7FA8", "C040FF")


def var(name):
    return re.search(r"--%s:\s*([^;]+);" % name, CSS).group(1).strip()


class Palette(unittest.TestCase):
    def test_tokens_match_raye_night(self):
        self.assertEqual(var("bg-base"), "#141318")
        self.assertEqual(var("text-primary"), "#F1F0F4")
        self.assertEqual(var("text-secondary"), "#B5B3BC")

    def test_old_greys_are_gone(self):
        for root, _dirs, files in os.walk(SITE):
            for name in files:
                # the eye's own colours (assets/*.svg) are the brand's
                if not name.endswith((".css", ".html")):
                    continue
                text = open(os.path.join(root, name), encoding="utf-8").read().upper()
                with self.subTest(file=name):
                    self.assertEqual([c for c in OLD if "#" + c in text], [])
                    self.assertNotIn("RGBA(192, 64, 255", text)


if __name__ == "__main__":
    unittest.main()
