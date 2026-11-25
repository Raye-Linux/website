"""The site carries the cut-triangle logo, not the old eye."""
import hashlib
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parents[2]
OLD = {
    "site/assets/favicon.svg": "f2f36e0fd35afe425a16b2cc6e82a67bb44e54b7ecd228fc0d5dedf66c280028",
    "site/assets/raye-mark.svg": "a16854605f0e9e99205d725aa1f54c86fdc16a59995b375960a5679001702b94",
    "site/assets/raye-eye.svg": "b1e5dff4999d3abdac3e35dd9c4fa736af4d3d1b3174236e12433ed7de722476"
}


def test_logo_svgs_embed_the_new_logo_not_the_old_eye_drawing():
    for sub in ("site", "site-v1"):
        for name in ("favicon.svg", "raye-mark.svg", "raye-eye.svg"):
            text = (SITE / sub / "assets" / name).read_text()
            assert "data:image/png;base64," in text, (sub, name)
            # the old eye was drawn with scanline gradients and an almond clip path
            assert "clipPath" not in text and "linearGradient" not in text, (sub, name)


def test_the_old_eye_files_are_gone():
    for rel, digest in OLD.items():
        assert hashlib.sha256((SITE / rel).read_bytes()).hexdigest() != digest, rel


def test_header_logo_is_square():
    for page in (SITE / "site").rglob("index.html"):
        for w, h in re.findall(r'raye-mark\.svg[^"]*" alt="" width="(\d+)" height="(\d+)"', page.read_text()):
            assert w == h, page
