"""The "What's missing" part of the Windows programs page is the target of
the link in the Windows layer's crash message (#missing). It has to say what
the layer really lacks: Direct3D to Vulkan and fonts that stand in for the
Windows ones are shipped, so they must not be listed as missing."""

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


def section(rel, anchor="missing"):
    with open(os.path.join(v1_root(), rel, "index.html"), encoding="utf-8") as f:
        html = f.read()
    start = html.index('id="%s"' % anchor)
    end = html.find("<h2", start + 1)
    text = re.sub(r"<[^>]+>", " ", html[start:end if end > 0 else None])
    return re.sub(r"\s+", " ", text.replace(" ", " "))


class WindowsMissingTests(unittest.TestCase):
    def test_the_crash_link_target_exists_in_both_languages(self):
        self.assertTrue(section("en/windows-programs"))
        self.assertTrue(section("programmes-windows"))

    def test_direct3d_to_vulkan_is_said_to_be_in_raye(self):
        en, fr = section("en/windows-programs"), section("programmes-windows")
        self.assertNotIn("I haven't started a single game", en)
        self.assertNotIn("not in Raye today", en)
        self.assertIn("DXVK", en)
        self.assertIn("DXVK", fr)
        self.assertNotIn("ne sont pas dans Raye aujourd'hui", fr)

    def test_fonts_are_said_to_stand_in_not_to_be_missing(self):
        en, fr = section("en/windows-programs"), section("programmes-windows")
        self.assertIn("same size", en)
        self.assertIn("même taille", fr)
        self.assertNotIn("gets another font", en)

    def test_what_is_really_missing_is_named(self):
        en, fr = section("en/windows-programs"), section("programmes-windows")
        self.assertIn("WebView2", en)
        self.assertIn("WebView2", fr)


if __name__ == "__main__":
    unittest.main()
