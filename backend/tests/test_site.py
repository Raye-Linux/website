"""Checks on the static site and everything a visitor can read: the strict
CSP holds (no inline script or style), nothing is loaded from elsewhere,
both languages match, and no forbidden name slips into visible text."""

import base64
import datetime
import hashlib
import html.parser
import importlib.machinery
import importlib.util
import io
import json
import os
import re
import sys
import unittest

from raye_site import emails, pages

# raye-tests promises to leave no bytecode under the repositories and runs
# everything with -B. The two modules this file loads by path below are
# loaded by us, not by the launcher, so the promise is ours to keep here.
sys.dont_write_bytecode = True

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "site")
TOOLS = os.path.join(os.path.dirname(__file__), "..", "..", "tools")
RELEASE_JSON = os.path.join(TOOLS, "release.json")
# the iso repository, checked out next to this one in /srv/raye
PUBLISH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "iso", "tools")
PUBLISH_CONF = os.path.join(PUBLISH, "release.conf")
PUBLISH_FILES = os.path.join(PUBLISH, "release-files")
# the archive public key, as the page tells the reader to import it
ARCHIVE_KEY = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                           "iso", "packages", "raye-base", "keyring",
                           "raye-archive.asc")

# The whole geste, because a barrier whose message names half of it
# costs an hour on the one day it goes off. Measured 2026-11-06: step 2
# alone has nothing to read -- $STAGE (/srv/publish) does not exist
# until step 1 has run once.
REMEDY = (
    "The geste that closes this, in this order:\n"
    "  1. iso/tools/release-files -- it reads the built image and writes "
    "release.json (with SHA256SUMS, its signature, the key and the parts) "
    "into $STAGE/release/$RELEASE/, both names coming from "
    "iso/tools/release.conf. It needs the signing key, and that staging "
    "folder does not exist until it has run once.\n"
    "  2. website/tools/build_pages.py --release <that release.json> -- it "
    "COPIES release, title, date, iso, size, sha256, urls and parts into "
    "website/tools/release.json and rewrites the pages from it, in the "
    "same run.\n"
    "Step 2 on its own refreshes nothing: no image is read in it."
)


def load_by_path(name, path):
    """A module of this tree loaded by its path, extension or not.

    tools/build_pages.py and iso/tools/release-files are the authorities
    on the formats this file checks. Re-spelling those formats here would
    be a second copy that goes stale without a word the day one of them
    changes -- which is exactly the trap the cached release.json below
    exists to catch.
    """
    loader = importlib.machinery.SourceFileLoader(name, path)
    spec = importlib.util.spec_from_file_location(name, path, loader=loader)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def builder():
    return load_by_path("raye_build_pages", os.path.join(TOOLS, "build_pages.py"))


def primary_fingerprint(path):
    """The v4 fingerprint of the first key in an armoured OpenPGP file.

    ⚠️ Computed here rather than asked of gpg, on purpose. This tree's
    launcher says it plainly: a test whose tool is missing can print
    "skipped" and exit 0, which looks like a verdict and is not one. gpg
    is not among this suite's declared needs, so a skip for want of it
    would be a hole exactly where a wrong fingerprint hurts most.

    RFC 4880 §12.2: SHA-1 over 0x99, the two-byte packet length, and the
    public-key packet body. Checked against gpg --show-keys on
    2026-11-06: both give EA7369D4...5DDE161E.
    """
    raw = io.open(path, encoding="utf-8").read()
    armour = raw.split("-----")[2]
    b64 = "".join(l for l in armour.splitlines()
                  if l and ":" not in l and not l.startswith("="))
    data = base64.b64decode(b64)
    head = data[0]
    if not head & 0x80:
        raise ValueError("%s does not begin with an OpenPGP packet" % path)
    if head & 0x40:                                  # new format
        tag, at = head & 0x3F, 1
        first = data[at]
        if first < 192:
            size, at = first, at + 1
        elif first < 224:
            size, at = ((first - 192) << 8) + data[at + 1] + 192, at + 2
        else:
            raise ValueError("%s: partial or five-octet length" % path)
    else:                                            # old format
        tag = (head >> 2) & 0x0F
        at = 1 + {0: 1, 1: 2, 2: 4}[head & 0x03]
        size = int.from_bytes(data[1:at], "big")
    if tag != 6:
        raise ValueError("%s: first packet is tag %d, not a public key" % (path, tag))
    packet = data[at:at + size]
    if packet[0] != 4:
        raise ValueError("%s: key version %d, only v4 is handled" % (path, packet[0]))
    digest = hashlib.sha1(b"\x99" + size.to_bytes(2, "big") + packet).hexdigest()
    return digest.upper()


def gpg_grouping(fpr):
    """The 40 hex digits as gpg prints them: ten groups of four, two
    spaces in the middle. That is the shape the reader compares against
    what `gpg --show-keys` shows them, so it is the shape the page uses."""
    half = lambda a, b: " ".join(fpr[i:i + 4] for i in range(a, b, 4))
    return half(0, 20) + "  " + half(20, 40)


def release_json():
    with open(RELEASE_JSON, encoding="utf-8") as f:
        return json.load(f)
PAGES = ["index.html", "fr/index.html", "en/index.html", "fr/confidentialite/index.html",
         "en/privacy/index.html", "fr/telecharger/index.html", "en/download/index.html",
         "404.html", "fr/conditions/index.html", "en/terms/index.html",
         "fr/mentions-legales/index.html", "en/legal/index.html",
         "fr/licences/index.html", "en/licenses/index.html",
         "fr/feuille-de-route/index.html", "en/roadmap/index.html"]
# Windows may be named on the roadmap; test_roadmap checks its words
ROADMAP_PAGES = ("fr/feuille-de-route/index.html", "en/roadmap/index.html")
# the bare rayelinux.com: no language, only the way on to /fr/ or /en/
CHOOSER = "index.html"
LICENSE_PAGES = {"fr/licences/index.html": "fr", "en/licenses/index.html": "en"}
DOWNLOAD_PAGES = ("fr/telecharger/index.html", "en/download/index.html")
DOWNLOAD_LANG = {"fr/telecharger/index.html": "fr", "en/download/index.html": "en"}
# the download pages link to the files, which live on the mirrors
MIRRORS = ("https://dl.rayelinux.com/", "https://github.com/Raye-Linux/")
# the only outside link allowed on every page: the community server invite
DISCORD = builder().DISCORD
FORBIDDEN = re.compile(
    r"\b(windows|microsoft|ubuntu|kubuntu|debian|fedora|arch linux|mint|macos|apple|"
    r"android|chrome ?os|wine|ia|ai|intelligence artificielle|artificial intelligence|"
    r"chatgpt|claude|gpt|copilot)\b", re.I)


# "based on Ubuntu" is the one exception to the names above (the legal
# mention of the base system); it is allowed in exactly this form
BASE_PHRASE = re.compile(r"\b(?:based on|basé sur) Ubuntu 26\.04 LTS\b", re.I)
HOMES = {"fr": "fr/index.html", "en": "en/index.html"}
TEXT_ASSETS = (".css", ".js", ".svg")


def trademark():
    """The notice as the page prints it (French typography applied)."""
    tm = load_by_path("raye_legal_text", os.path.join(TOOLS, "legal_text.py")).TRADEMARK
    return {"fr": builder().french(tm["fr"]), "en": tm["en"]}


def text_assets():
    """Every text file under site/assets (the screenshots are binary)."""
    found = []
    for folder, _, names in os.walk(os.path.join(ROOT, "assets")):
        for name in names:
            if name.endswith(TEXT_ASSETS):
                found.append(os.path.relpath(os.path.join(folder, name),
                                             os.path.join(ROOT, "assets")))
    return sorted(found)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


class Collector(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.tags, self._skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag in ("script", "style", "title"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "title"):
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            self.text.append(data)


def parse(text):
    c = Collector()
    c.feed(text)
    return c


class SiteTests(unittest.TestCase):
    def test_no_inline_script_or_style(self):
        for rel in PAGES:
            c = parse(read(rel))
            for tag, attrs in c.tags:
                with self.subTest(page=rel, tag=tag):
                    self.assertNotIn("style", attrs)
                    self.assertFalse(any(k.startswith("on") for k in attrs))
                    if tag == "script":
                        self.assertTrue(attrs.get("src", "").startswith("/assets/"))
                    self.assertNotEqual(tag, "style")

    def test_nothing_from_elsewhere(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                for key in ("src", "href", "action"):
                    value = attrs.get(key)
                    if value is None or tag == "link" and attrs.get("rel") in (
                            "canonical", "alternate"):
                        continue
                    allowed = ("/", "#", "mailto:bonjour@")
                    if rel in DOWNLOAD_PAGES and tag == "a":
                        allowed += MIRRORS
                    # the one outside link on every page: the community server
                    if tag == "a" and value == DISCORD:
                        allowed += (DISCORD,)
                    with self.subTest(page=rel, value=value):
                        self.assertTrue(value.startswith(allowed), value)
        for name in text_assets():
            text = read("assets/" + name)
            urls = re.findall(r"https?://[^\s\"')]+", text)
            self.assertEqual([u for u in urls if "www.w3.org" not in u], [], name)

    def test_local_links_exist(self):
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                value = attrs.get("src") or (attrs.get("href") if tag in ("a", "link") else None)
                if not value or not value.startswith("/") or value.startswith("/api/"):
                    continue
                target = value.split("#")[0].split("?")[0]
                path = os.path.join(ROOT, target.lstrip("/"))
                if target.endswith("/"):
                    path = os.path.join(path, "index.html")
                with self.subTest(page=rel, link=value):
                    self.assertTrue(os.path.isfile(path), path)

    def test_assets_are_versioned(self):
        # a changed script must get a new address, or a browser or Cloudflare
        # keeps serving the old one with the new page (it broke the signup once)
        import hashlib
        for rel in PAGES:
            for tag, attrs in parse(read(rel)).tags:
                value = attrs.get("src") or (attrs.get("href") if tag == "link" else None)
                if not value or not value.startswith("/assets/"):
                    continue
                name, _, query = value[len("/assets/"):].partition("?")
                with open(os.path.join(ROOT, "assets", name), "rb") as f:
                    want = "v=" + hashlib.sha256(f.read()).hexdigest()[:10]
                with self.subTest(page=rel, asset=value):
                    self.assertEqual(query, want)

    def test_submit_falls_back_to_a_normal_post(self):
        # if the script hits an error, the form must still be sent the plain way
        js = read("assets/app.js")
        self.assertIn("form.submit()", js)
        self.assertRegex(js, r"catch \(err\)")

    def test_visible_text_is_clean(self):
        # what a reader sees includes the alt text of the pictures; the base
        # system may be named, once, in the words the law asks for
        texts = {}
        for rel in PAGES:
            if rel in ROADMAP_PAGES:
                continue
            c = parse(read(rel))
            alts = [a.get("alt", "") for t, a in c.tags if t == "img"]
            text = " ".join(c.text + alts)
            if rel in LICENSE_PAGES:
                # the one place the site names those companies: the trademark
                # notice, exactly as written in tools/legal_text.py
                text = text.replace(trademark()[LICENSE_PAGES[rel]], "")
            texts[rel] = BASE_PHRASE.sub("", text)
        for kind in pages.MESSAGES:
            texts["page:" + kind] = " ".join(parse(pages.render(kind, None)).text)
        for lang in ("fr", "en"):
            msg = emails.build_confirmation("a@x.ca", lang, "https://rayelinux.com/c",
                                            "https://rayelinux.com/u",
                                            "Raye Linux <bonjour@rayelinux.com>")
            texts["mail:" + lang] = (msg["Subject"] + msg.get_body(("plain",)).get_content())
        texts["app.js"] = " ".join(re.findall(r'"([^"]*)"', read("assets/app.js")))
        for name, text in texts.items():
            with self.subTest(source=name):
                self.assertIsNone(FORBIDDEN.search(text), FORBIDDEN.search(text))

    def test_the_trademark_notice_is_on_the_licenses_pages_only(self):
        for rel in PAGES:
            text = " ".join(parse(read(rel)).text)
            for lang, notice in trademark().items():
                with self.subTest(page=rel, lang=lang):
                    want = 1 if LICENSE_PAGES.get(rel) == lang else 0
                    self.assertEqual(text.count(notice), want)

    def test_every_page_links_the_legal_pages(self):
        for rel in PAGES:
            if rel in ("404.html", CHOOSER):
                continue   # no language of their own, no footer: they only lead home
            hrefs = {a.get("href") for t, a in parse(read(rel)).tags if t == "a"}
            lang = rel.split("/")[0]
            paths = builder().PATHS[lang]
            for page in ("privacy", "terms", "notice", "licenses"):
                with self.subTest(page=rel, link=page):
                    self.assertIn(paths[page], hrefs)

    def test_the_download_agreement_links_the_terms(self):
        for rel, lang in DOWNLOAD_LANG.items():
            text = read(rel)
            box = text[text.index('id="accept"'):text.index("</section>", text.index('id="accept"'))]
            self.assertIn('href="%s"' % builder().PATHS[lang]["terms"], box)

    def test_the_help_bubble_names_nothing_but_says_what_answers(self):
        # the one exception to the forbidden words: the bubble has to say
        # its answers come from an AI, in its header line and in the notice.
        # Exactly these sentences, once each.
        js = read("assets/support.js")
        notice = ("Réponses écrites par une IA sur notre propre serveur.",
                  "Answers are written by an AI on our own server.",
                  "IA locale sur nos propres serveurs.",
                  "Local AI on our own servers.")
        strings = re.findall(r'"([^"]*)"', js)
        for sentence in notice:
            self.assertEqual(js.count(sentence), 1, sentence)
        text = " ".join(strings)
        for sentence in notice:
            text = text.replace(sentence, "")
        self.assertIsNone(FORBIDDEN.search(text), FORBIDDEN.search(text))
        for rel in PAGES:
            if rel != CHOOSER:
                self.assertIn("/assets/support.js?v=", read(rel), rel)

    def test_languages_match(self):
        for fr, en in (("fr/index.html", "en/index.html"),
                       ("fr/confidentialite/index.html", "en/privacy/index.html"),
                       ("fr/conditions/index.html", "en/terms/index.html"),
                       ("fr/mentions-legales/index.html", "en/legal/index.html"),
                       ("fr/licences/index.html", "en/licenses/index.html"),
                       ROADMAP_PAGES, DOWNLOAD_PAGES):
            a, b = parse(read(fr)), parse(read(en))
            self.assertEqual([t for t, _ in a.tags], [t for t, _ in b.tags], fr)
        fr, en = read("fr/index.html"), read("en/index.html")
        self.assertIn('<html lang="fr">', fr)
        self.assertIn('<html lang="en">', en)
        self.assertIn('name="lang" value="fr"', fr)
        self.assertIn('name="lang" value="en"', en)

    def test_download_pages_show_the_release(self):
        """🚨 The size and the date are checked too, and that is not padding.

        Measured 2026-11-06: with tools/release.json refreshed to the real
        image (2 960 349 184 bytes, 2026-11-06) and the pages NOT rebuilt,
        this test was GREEN while both pages still read "2,9 Go ... 1er
        novembre 2026". Only the checksum was compared, so the two facts a
        reader can actually check against their own download -- how big it
        is and how old it is -- were covered by nothing.

        It is the same trap as the cached release.json one level up: a page
        agreeing with nothing in particular. The expected strings come from
        the builder's own size_text()/date_text(), never re-spelled here.
        """
        info = release_json()
        bp = builder()
        for rel in DOWNLOAD_PAGES:
            page = read(rel)
            lang = DOWNLOAD_LANG[rel]
            hrefs = [a.get("href") for t, a in parse(page).tags if t == "a"]
            with self.subTest(page=rel):
                self.assertIn(info["sha256"], page)
                self.assertIn(
                    bp.size_text(lang, info["size"]), page,
                    "%s does not print the size tools/release.json gives "
                    "(%d bytes -> %r): rebuild it with "
                    "tools/build_pages.py" % (rel, info["size"],
                                              bp.size_text(lang, info["size"])))
                self.assertIn(
                    bp.date_text(lang, info["date"]), page,
                    "%s does not print the date tools/release.json gives "
                    "(%s -> %r): rebuild it with tools/build_pages.py"
                    % (rel, info["date"], bp.date_text(lang, info["date"])))
                self.assertIn(info["urls"]["r2"], hrefs)
                if builder().GITHUB_MIRROR:
                    self.assertIn(info["urls"]["github"], hrefs)
                else:  # the mirror is hidden until Raye-Linux/releases is public
                    self.assertNotIn(info["urls"]["github"], hrefs)
                for name in ("SHA256SUMS", "SHA256SUMS.asc", "raye-archive.asc"):
                    self.assertIn(info["urls"]["r2_folder"] + name, hrefs)
                for part in info["parts"] if builder().GITHUB_MIRROR else ():
                    self.assertIn(part, page)
                self.assertIn(info["iso"], page)
        # "in two parts" / "en deux morceaux" is prose, and it is the
        # last hard-coded count on the page. The cat and copy /b commands
        # are built from info["parts"], so they can never list the wrong
        # ones -- but the sentence above them cannot count. Measured
        # 2026-11-06: the image makes exactly 2 parts (2 960 349 184 bytes
        # against release-files' 1900 MiB), leaving about 1 GB before a
        # third appears and the sentence starts lying next to a command
        # that is right.
        self.assertEqual(
            len(info["parts"]), 2,
            "tools/release.json has %d parts, and both download pages say "
            "the image comes in two. The commands are generated and are "
            "fine; it is the sentence above them (DOWNLOAD[lang]"
            "['mirror_note'] in tools/build_pages.py) that has to change, "
            "in both languages." % len(info["parts"]))

    def test_release_json_describes_the_iso_it_will_publish(self):
        """🚨 The check above proves the PAGE matches tools/release.json.
        It proves nothing about release.json matching the image.

        Both can be stale together, and on 2026-11-06 they were. The
        download page carried

            sha256  5673b7af…0c406d      size  2 910 941 184

        while the image people would have been handed was

            sha256  b52f3431…1cdb65      size  2 960 349 184

        -- 49 MB and a completely different checksum. The suite was
        GREEN, because page and cache agreed with each other. A page that
        is consistent with a stale cache still lies to the reader, and a
        wrong checksum is worse than none: it tells someone their good
        download is corrupt, or their corrupt one is good.

        release.json is a copy that `tools/build_pages.py --release`
        refreshes from release-files. Nothing made anyone refresh it.

        ⚠️ The file name is deliberately NOT compared. The built image is
        dated (raye-0.1-beta-20261106-amd64.iso) and publication drops
        the date; the bytes are what must agree.

        🚨 THE DATE IS COMPARED, and it was not. release-files takes it
        from the image's mtime and the download page prints it in words.
        Measured 2026-11-06: with size and sha256 set to the real image
        and the date left at 2026-11-01, this test was GREEN -- a page
        that hands out the 6 November image while telling the reader it
        is the one from 1 November. The same single geste fixes it, so
        there was no reason to leave it out.

        ⚠️ The date is the image file's mtime, which is release-files'
        own definition of it. Copying the ISO about changes it, and then
        the page's date is the date of the copy.

        All three are reported at once rather than one per run: on the
        day this goes off, what is wanted is the whole list.
        """
        iso = os.environ.get("RAYE_ISO")
        if not iso or iso == "None":
            self.skipTest("RAYE_ISO is not set: nothing to compare "
                          "tools/release.json against")
        if not os.path.isfile(iso):
            self.skipTest("RAYE_ISO points at %s, which is not a file" % iso)
        info = release_json()
        wrong = []
        size = os.path.getsize(iso)
        if info["size"] != size:
            wrong.append("size:   release.json %d, the image %d (%+d bytes)"
                         % (info["size"], size, size - info["size"]))
        date = datetime.date.fromtimestamp(os.stat(iso).st_mtime).isoformat()
        if info["date"] != date:
            wrong.append("date:   release.json %s, the image %s"
                         % (info["date"], date))
        h = hashlib.sha256()
        with open(iso, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        if info["sha256"] != h.hexdigest():
            wrong.append("sha256: release.json %s, the image %s"
                         % (info["sha256"], h.hexdigest()))
        if wrong:
            self.fail("tools/release.json does not describe %s, so the "
                      "download page does not either:\n  %s\n%s"
                      % (iso, "\n  ".join(wrong), REMEDY))

    def test_release_json_remedy_names_a_geste_that_exists(self):
        """The barrier above is red by design until publication day, so its
        message is the only instruction anyone will have at that moment.

        ⚠️ It used to say "run tools/build_pages.py --release
        <release.json>" and stop there. Measured 2026-11-06: that step
        alone CANNOT work -- it only copies out of a file that
        iso/tools/release-files has to write first, and $STAGE
        (/srv/publish) did not exist at all. A remedy that names half
        the geste sends the reader looking for a file nobody made.

        This holds the message to naming both halves. It is not a
        tautology: it also re-asks whether the two tools it names are
        still there under those names, which a rename would otherwise
        break in silence until the day it matters.
        """
        for named in ("iso/tools/release-files",
                      "website/tools/build_pages.py --release"):
            self.assertIn(named, REMEDY,
                          "the barrier's remedy no longer names %s" % named)
        bp = builder()
        self.assertTrue(callable(getattr(bp, "take_release", None)),
                        "tools/build_pages.py has no take_release(): the "
                        "--release flag the remedy names is gone")
        self.assertIn("--release", bp.__doc__ or "",
                      "tools/build_pages.py no longer documents --release")
        if not os.path.isfile(PUBLISH_CONF):
            return      # the iso repository is not here; the half-check stands
        self.assertTrue(os.path.isfile(PUBLISH_FILES),
                        "%s is gone, and the remedy still names it"
                        % PUBLISH_FILES)

    def test_the_publish_geste_produces_what_the_download_page_needs(self):
        """Runs the real publication geste on a 4 KB stand-in image.

        The barrier above compares tools/release.json with the image. That
        is only worth something if the geste that refreshes it really
        produces the keys this page reads -- and nothing checked that: the
        two tools live in two repositories and agree only by habit.

        So: iso/tools/release-files --no-sign into a temporary folder, its
        release.json through build_pages.take_release() with RELEASE
        redirected, and then the keys the download page actually uses.
        ⚠️ RELEASE is redirected on purpose: take_release writes
        website/tools/release.json, and a test has no business touching the
        published cache.

        A red here means the publication geste is broken -- missing release
        notes, a renamed key -- and it is worth knowing before release day
        rather than on it. Measured 2026-11-06: green, with every key
        take_release keeps present in what release-files writes.
        """
        if not os.path.isfile(PUBLISH_FILES):
            self.skipTest("the iso repository is not checked out next to "
                          "this one: %s" % PUBLISH_FILES)
        import contextlib
        import tempfile
        rf = load_by_path("raye_release_files", PUBLISH_FILES)
        bp = builder()
        with tempfile.TemporaryDirectory() as tmp:
            iso = os.path.join(tmp, "stand-in.iso")
            with open(iso, "wb") as f:
                f.write(os.urandom(4096))
            out = os.path.join(tmp, "release")
            # release-files reports what it wrote on stdout, and the
            # launcher reads a suite's output to count what ran. A tool's
            # progress lines have no business in that.
            said = io.StringIO()
            with contextlib.redirect_stdout(said):
                code = rf.main(["--iso", iso, "--out", out, "--no-sign"])
            self.assertEqual(code, 0, "iso/tools/release-files refused to "
                             "run: %s" % said.getvalue().strip())
            made = os.path.join(out, "release.json")
            self.assertTrue(os.path.isfile(made), made)
            bp.RELEASE = os.path.join(tmp, "copied.json")
            bp.take_release(made)
            with open(bp.RELEASE, encoding="utf-8") as f:
                got = json.load(f)
            for key in ("release", "title", "date", "iso", "size", "sha256",
                        "urls", "parts"):
                self.assertIn(key, got, key)
            for key in ("r2", "r2_folder", "github", "github_download",
                        "issues"):
                self.assertIn(key, got["urls"], key)
            self.assertEqual(got["size"], os.path.getsize(iso))
            h = hashlib.sha256()
            with open(iso, "rb") as f:
                h.update(f.read())
            self.assertEqual(got["sha256"], h.hexdigest())
            self.assertEqual(
                got["date"],
                datetime.date.fromtimestamp(os.stat(iso).st_mtime).isoformat(),
                "release-files no longer dates the release by the image's "
                "mtime, which is what the barrier above compares")
            self.assertTrue(got["parts"] and all(isinstance(p, str)
                                                 for p in got["parts"]),
                            "the page prints the part names as strings: %r"
                            % (got["parts"],))
            # The release-notes link is the one address on the page whose
            # file name is spelled in two places -- build_pages.py builds
            # "release-notes-<release>[.fr].md", release-files copies
            # whatever iso/docs happens to call them. Measured 2026-11-06:
            # nothing compared the two, so a rename there would have left a
            # 404 behind the page's own "Notes de version" link, and the
            # suite green. Every other link on the page comes from
            # release.json; this one did not.
            made = set(os.listdir(out))
            for rel in DOWNLOAD_PAGES:
                links = [a.get("href") for t, a in parse(read(rel)).tags
                         if t == "a" and (a.get("href") or "").endswith(".md")]
                with self.subTest(page=rel):
                    self.assertTrue(links, "%s links to no release notes" % rel)
                    for href in links:
                        self.assertIn(
                            href.rsplit("/", 1)[-1], made,
                            "%s links to %s, which iso/tools/release-files "
                            "does not put next to the image (it wrote %s)"
                            % (rel, href, ", ".join(sorted(
                                n for n in made if n.endswith(".md")))))

    def test_the_key_fingerprint_on_the_page_is_the_archive_key(self):
        """🚨 The one fact on the download page that comes from nowhere.

        Measured 2026-11-06: the file name, size, checksum, date, parts
        and every address are generated from tools/release.json, but the
        fingerprint is the literal FINGERPRINT in tools/build_pages.py,
        derived from nothing and compared with nothing. It happens to be
        right.

        It is in the same family as the stale checksum, and it bites
        harder: the page tells the reader to run `gpg --show-keys
        raye-archive.asc` and check it. A fingerprint left behind after
        the archive key is rotated tells someone the genuine key is the
        wrong one -- and the honest reader is the one who stops.

        ⚠️ The ARCHIVE key, not the signing subkey. The page shows the
        primary (EA73...161E); release.conf's SIGNING_KEY is the subkey
        (E005...0DA0) that signs SHA256SUMS. Comparing against the wrong
        one of the two would be a green that proves nothing.
        """
        if not os.path.isfile(ARCHIVE_KEY):
            self.skipTest("the iso repository is not checked out next to "
                          "this one: %s" % ARCHIVE_KEY)
        bp = builder()
        want = gpg_grouping(primary_fingerprint(ARCHIVE_KEY))
        self.assertEqual(
            bp.FINGERPRINT, want,
            "tools/build_pages.py prints %r on the download page, but "
            "%s is %r. Fix FINGERPRINT and rebuild the pages with "
            "tools/build_pages.py." % (bp.FINGERPRINT, ARCHIVE_KEY, want))
        for rel in DOWNLOAD_PAGES:
            with self.subTest(page=rel):
                self.assertIn(want, read(rel),
                              "%s does not carry the archive fingerprint: "
                              "rebuild it with tools/build_pages.py" % rel)

    def test_release_json_addresses_still_match_the_publish_config(self):
        """Where the files will be is the owner's decision, and it is
        written down once: iso/tools/release.conf.

        website/tools/release.json holds a COPY of the addresses
        release-files builds from it, and the download page links to that
        copy. Nothing compared the two, so the day R2_PUBLIC, the GitHub
        organisation or the release number changes, the page would go on
        pointing at the old place -- a cache agreeing with itself again,
        and this time with every download link on it.

        The expected addresses are built by release-files' own urls() and
        iso_name(), never re-spelled here, and the config is read by its
        own settings(). ⚠️ So a red here is never "the page is wrong"
        alone: it is "the page and release.conf disagree", and release.conf
        is the side that decides.
        """
        if not os.path.isfile(PUBLISH_FILES):
            self.skipTest("the iso repository is not checked out next to "
                          "this one: %s" % PUBLISH_FILES)
        rf = load_by_path("raye_release_files", PUBLISH_FILES)
        conf = rf.rp.settings(PUBLISH_CONF)
        info = release_json()
        self.assertEqual(
            info["urls"], rf.urls(conf),
            "the addresses in website/tools/release.json are not the ones "
            "iso/tools/release.conf gives.\n%s" % REMEDY)
        self.assertEqual(info["release"], conf["RELEASE"], REMEDY)
        self.assertEqual(info["title"], conf["RELEASE_TITLE"], REMEDY)
        self.assertEqual(info["iso"], rf.iso_name(conf), REMEDY)

    def test_the_bare_name_picks_a_language_and_only_there(self):
        js = read("assets/lang.js")
        self.assertIn('fr: "/fr/", en: "/en/"', js)
        self.assertIn("HOMES.en", js)                  # English when nothing matches
        for rel in PAGES:
            with self.subTest(page=rel):
                self.assertEqual("/assets/lang.js?v=" in read(rel), rel == CHOOSER)
        tags = parse(read(CHOOSER)).tags
        hrefs = [a.get("href") for t, a in tags if t == "a"]
        self.assertIn("/fr/", hrefs)
        self.assertIn("/en/", hrefs)
        text = read(CHOOSER)
        links = text[text.index("<noscript>"):text.index("</noscript>")]
        self.assertIn('href="/fr/"', links)
        self.assertIn('href="/en/"', links)

    def test_every_page_says_where_its_twin_is(self):
        b = builder()
        for lang in ("fr", "en"):
            other = "en" if lang == "fr" else "fr"
            for page, path in b.PATHS[lang].items():
                text = read(path.lstrip("/") + "index.html")
                with self.subTest(lang=lang, page=page):
                    self.assertTrue(path.startswith("/%s/" % lang), path)
                    self.assertIn('<link rel="canonical" href="%s%s">' % (b.URL, path), text)
                    self.assertIn('hreflang="%s" href="%s%s"' % (other, b.URL, b.PATHS[other][page]),
                                  text)
                    want = "/" if page == "home" else b.PATHS["en"][page]
                    self.assertIn('hreflang="x-default" href="%s%s"' % (b.URL, want), text)

    def test_legal_pages_open_with_a_summary_and_contents(self):
        b = builder()
        for lang in ("fr", "en"):
            for page in ("privacy", "terms", "notice", "licenses"):
                text = read(b.PATHS[lang][page].lstrip("/") + "index.html")
                with self.subTest(lang=lang, page=page):
                    self.assertIn('class="legal-summary"', text)
                    self.assertLess(text.index('class="legal-summary"'), text.index('class="toc"'))
                    toc = text[text.index('class="toc"'):text.index("</nav>", text.index('class="toc"'))]
                    targets = re.findall(r'href="#([a-z-]+)"', toc)
                    self.assertGreaterEqual(len(targets), 3)
                    sections = re.findall(r'<section id="([a-z-]+)"', text)
                    self.assertEqual(targets, sections)

    def test_old_french_addresses_move_to_their_fr_page(self):
        conf = open(os.path.join(ROOT, "..", "deploy", "nginx", "raye-site.conf"),
                    encoding="utf-8").read()
        rule = re.search(r"location ~ \^/\(([a-z|-]+)\)\S* \{\s*return 301 /fr/\$1/", conf)
        self.assertIsNotNone(rule)
        old = set(rule.group(1).split("|"))
        b = builder()
        moved = {p.strip("/").split("/", 1)[1] for k, p in b.PATHS["fr"].items() if k != "home"}
        self.assertEqual(old, moved)
        self.assertIn("absolute_redirect off;", conf)
        self.assertRegex(conf, r"location ~ \^/download/\?\$ \{ return 301 /en/download/")
        for name in moved:
            self.assertFalse(os.path.exists(os.path.join(ROOT, name)), name)

    def test_form_fields(self):
        tags = parse(read("fr/index.html")).tags
        form = [a for t, a in tags if t == "form"][0]
        self.assertEqual((form["method"], form["action"]), ("post", "/api/subscribe"))
        names = {a.get("name") for t, a in tags if t == "input"}
        self.assertEqual(names, {"lang", "email", "consent", "website"})
        labels = {a.get("for") for t, a in tags if t == "label"}
        self.assertIn("email", labels)
        imgs = [a for t, a in tags if t == "img"]
        self.assertTrue(all("alt" in a and "width" in a and "height" in a for a in imgs))


# the installer repository, checked out next to this one in /srv/raye. Its
# welcomeq.conf is the ONLY place the figure is enforced: Calamares refuses
# to go on below it.
WELCOMEQ = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        "installer", "etc", "calamares", "modules",
                        "welcomeq.conf")


class FreeSpaceFigureTests(unittest.TestCase):
    """The free-space figure the download page prints must be the one the
    installer demands.

    🚨 Measured 2026-11-06: it was not. The page said 32 GB / 32 Go under a
    heading that reads "What you need" / "Configuration minimale", while
    welcomeq.conf says requiredStorage: 25 -- and the release notes and the
    handbook both say 25 too, in both languages. The website was the only
    one of the four that disagreed, and it disagreed in the direction that
    costs users: someone with 28 GB free reads that they cannot install and
    leaves, on a machine the installer would have accepted.

    The handbook has had this exact check since before this one existed
    (handbook/tests/test_promises.py). The website had none, which is
    precisely why it was the one that drifted.

    ⚠️ The figure is READ from welcomeq.conf, never written here. A test
    that hard-codes 25 freezes today's answer and goes green the day the
    installer asks for 30 -- it would guard the number instead of the
    agreement, which is the only thing worth guarding.
    """

    def setUp(self):
        if not os.path.exists(WELCOMEQ):
            self.skipTest("the installer repository is not checked out next to this one")
        with open(WELCOMEQ, encoding="utf-8") as f:
            m = re.search(r"^\s*requiredStorage:\s*([0-9.]+)\s*$", f.read(), re.M)
        self.assertTrue(m, "welcomeq.conf no longer declares requiredStorage")
        self.gb = str(int(float(m.group(1))))

    def _page(self, *parts):
        with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
            return f.read()

    def test_both_download_pages_print_the_enforced_figure(self):
        for parts, unit in ((("fr", "telecharger", "index.html"), "Go"),
                            (("en", "download", "index.html"), "GB")):
            page = self._page(*parts)
            self.assertIn(
                f"{self.gb} {unit}", page,
                f"{'/'.join(parts)} never says {self.gb} {unit}, which is what "
                f"the installer enforces (requiredStorage: {self.gb})")

    def test_no_download_page_prints_a_different_free_space_figure(self):
        """⚠️ The half that the check above cannot catch.

        Printing the right figure somewhere does not stop a second, wrong
        one sitting next to it -- and a page that gives two numbers for the
        same requirement is worse than one that gives the wrong number,
        because the reader cannot tell which to trust. So every figure that
        is followed by the words for free disk space has to be THE figure.
        """
        patterns = ((("fr", "telecharger", "index.html"),
                     r"(\d+)\s*Go\s*d'espace disque libre"),
                    (("en", "download", "index.html"),
                     r"(\d+)\s*GB\s*of free disk space"))
        for parts, pattern in patterns:
            found = re.findall(pattern, self._page(*parts))
            # Not just "every match equals gb": an EMPTY list would make
            # that assertion vacuously true, and a page that stopped
            # mentioning free space at all would pass a test named after
            # free space. unittest reports a loop over nothing as a plain
            # success -- zero items, zero assertions, green.
            self.assertTrue(
                found,
                f"{'/'.join(parts)} no longer states a free-disk-space figure at "
                "all, so this check was about to pass by having nothing to read")
            self.assertEqual(
                sorted(set(found)), [self.gb],
                f"{'/'.join(parts)} states {sorted(set(found))} for free disk "
                f"space; the installer enforces {self.gb}")


if __name__ == "__main__":
    unittest.main()


class HomePageTests(unittest.TestCase):
    """The home page keeps its promises: the screenshots it shows are on
    disk, every one of them is described, the two languages carry the same
    sections, and the signup form is the one the server expects."""

    SHOTS = os.path.join(ROOT, "assets", "shots")

    def tags(self, lang):
        return parse(read(HOMES[lang])).tags

    def image_addresses(self, lang):
        """Every picture address of the page: src, srcset and the full-size links."""
        found = []
        for tag, attrs in self.tags(lang):
            if tag in ("img", "source"):
                if attrs.get("src"):
                    found.append(attrs["src"])
                for part in (attrs.get("srcset") or "").split(","):
                    if part.strip():
                        found.append(part.split()[0])
            if tag == "a" and attrs.get("href", "").startswith("/assets/shots/"):
                found.append(attrs["href"])
        return found

    def test_every_picture_the_page_cites_exists(self):
        for lang in HOMES:
            addresses = self.image_addresses(lang)
            self.assertGreaterEqual(len([a for a in addresses if "/shots/" in a]), 15, lang)
            for value in addresses:
                path = os.path.join(ROOT, value.split("?")[0].lstrip("/"))
                with self.subTest(lang=lang, picture=value):
                    self.assertTrue(os.path.isfile(path), path)

    def test_srcset_entries_are_versioned_like_the_rest(self):
        import hashlib
        for lang in HOMES:
            for value in self.image_addresses(lang):
                name, _, query = value[len("/assets/"):].partition("?")
                with open(os.path.join(ROOT, "assets", name), "rb") as f:
                    want = "v=" + hashlib.sha256(f.read()).hexdigest()[:10]
                with self.subTest(lang=lang, picture=value):
                    self.assertEqual(query, want)

    def test_every_screenshot_is_described(self):
        for lang in HOMES:
            alts = []
            for tag, attrs in self.tags(lang):
                if tag != "img":
                    continue
                with self.subTest(lang=lang, img=attrs.get("src")):
                    self.assertIn("alt", attrs)
                    if "/shots/" in attrs["src"]:
                        # a real description, not a file name or a word
                        self.assertGreaterEqual(len(attrs["alt"].split()), 8, attrs["alt"])
                        alts.append(attrs["alt"])
                    else:
                        # only the decorative eye may be silent
                        self.assertIn("raye-mark.svg", attrs["src"])
            self.assertEqual(len(alts), len(set(alts)), lang)
            self.assertEqual(len(alts), 5, lang)

    def test_screenshots_match_the_page_language(self):
        for lang in HOMES:
            for value in self.image_addresses(lang):
                if "/shots/" in value:
                    with self.subTest(lang=lang, picture=value):
                        self.assertIn("-%s-" % lang, value)

    def test_screenshot_files_are_what_they_claim(self):
        names = sorted(os.listdir(self.SHOTS))
        cited = {v.split("?")[0].rsplit("/", 1)[1]
                 for lang in HOMES for v in self.image_addresses(lang)}
        total = 0
        for name in names:
            with open(os.path.join(self.SHOTS, name), "rb") as f:
                head = f.read(12)
            total += os.path.getsize(os.path.join(self.SHOTS, name))
            with self.subTest(file=name):
                self.assertIn(name, cited, "a screenshot no page uses")
                if name.endswith(".webp"):
                    self.assertEqual((head[:4], head[8:12]), (b"RIFF", b"WEBP"))
                else:
                    self.assertTrue(name.endswith(".jpg"), name)
                    self.assertEqual(head[:3], b"\xff\xd8\xff")
        # what the server holds; a visitor downloads a fraction of it
        self.assertLess(total, 2_000_000)

    def ids(self, lang):
        return [a["id"] for t, a in self.tags(lang) if t in ("section", "figure") and "id" in a]

    def test_both_languages_have_the_same_sections(self):
        self.assertEqual(self.ids("fr"), self.ids("en"))
        for wanted in ("captures", "nouveautes", "questions", "signup"):
            self.assertIn(wanted, self.ids("en"))

    def test_header_links_lead_somewhere_on_the_page(self):
        for lang in HOMES:
            text = read(HOMES[lang])
            nav = text[text.index('<nav class="nav"'):text.index("</nav>")]
            anchors = re.findall(r'href="#([a-z-]+)"', nav)
            self.assertEqual(len(anchors), 3, lang)
            for anchor in anchors + ["signup"]:
                with self.subTest(lang=lang, anchor=anchor):
                    self.assertIn('id="%s"' % anchor, text)

    def test_the_tabs_point_at_their_panels(self):
        for lang in HOMES:
            tags = self.tags(lang)
            tabs = [a["href"][1:] for t, a in tags if t == "a" and "data-tab" in a]
            panels = [a["id"] for t, a in tags if t == "figure" and "data-panel" in a]
            self.assertEqual(tabs, panels, lang)

    def test_the_form_is_the_one_the_server_reads(self):
        for lang in HOMES:
            tags = self.tags(lang)
            form = [a for t, a in tags if t == "form"]
            self.assertEqual(len(form), 1, lang)
            self.assertEqual((form[0]["method"], form[0]["action"], form[0]["id"]),
                             ("post", "/api/subscribe", "signup-form"))
            inputs = {a.get("name"): a for t, a in tags if t == "input"}
            self.assertEqual(set(inputs), {"lang", "email", "consent", "website"})
            self.assertEqual(inputs["lang"].get("value"), lang)
            self.assertEqual(inputs["email"].get("type"), "email")
            self.assertIn("required", inputs["email"])
            self.assertEqual(inputs["consent"].get("type"), "checkbox")
            self.assertIn("required", inputs["consent"])
            self.assertEqual(inputs["website"].get("tabindex"), "-1")
            buttons = [a for t, a in tags if t == "button"]
            self.assertEqual([b.get("type") for b in buttons], ["submit"])
            privacy = "/fr/confidentialite/" if lang == "fr" else "/en/privacy/"
            form_html = read(HOMES[lang])
            form_html = form_html[form_html.index("<form"):form_html.index("</form>")]
            self.assertIn('href="%s"' % privacy, form_html)

    def changelog(self, lang):
        """(datetime attribute, visible date, text) for each latest-changes line."""
        text = read(HOMES[lang])
        start = text.index('<ol class="changelog"')
        block = text[start:text.index("</ol>", start)]
        return re.findall(r'<li>\s*<time datetime="([^"]*)">([^<]*)</time>\s*<p>([^<]*)</p>',
                          block)

    def test_the_latest_changes_are_dated_and_not_empty(self):
        import datetime
        months = {"fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                         "août", "septembre", "octobre", "novembre", "décembre"],
                  "en": ["January", "February", "March", "April", "May", "June", "July",
                         "August", "September", "October", "November", "December"]}
        counts = {}
        for lang in HOMES:
            entries = self.changelog(lang)
            counts[lang] = [d for d, _, _ in entries]
            self.assertGreaterEqual(len(entries), 3, lang)
            self.assertLessEqual(len(entries), 6, lang)
            days = []
            for attr, shown, line in entries:
                with self.subTest(lang=lang, date=attr):
                    self.assertRegex(attr, r"^\d{4}-\d{2}-\d{2}$")
                    day = datetime.date.fromisoformat(attr)
                    days.append(day)
                    if lang == "fr":
                        first = "1er" if day.day == 1 else str(day.day)
                        want = "%s %s %d" % (first, months["fr"][day.month - 1], day.year)
                    else:
                        want = "%s %d, %d" % (months["en"][day.month - 1], day.day, day.year)
                    self.assertEqual(shown.replace("\u00a0", " "), want)
                    # a real sentence, not a placeholder
                    self.assertGreaterEqual(len(line.split()), 8, line)
            self.assertEqual(days, sorted(days, reverse=True), "newest first")
            # a change cannot be dated after the page was built
            self.assertLessEqual(days[0], datetime.date.today())
        self.assertEqual(counts["fr"], counts["en"])

    def test_the_note_is_signed(self):
        for lang in HOMES:
            text = read(HOMES[lang])
            note = text[text.index('class="author-note"'):text.index('class="changes"')]
            self.assertIn('<p class="signature">techoraye</p>', note, lang)
            self.assertGreaterEqual(note.count("<p>"), 2, lang)

    def test_the_base_system_is_named_once_and_only_in_the_faq(self):
        for lang in HOMES:
            text = read(HOMES[lang])
            self.assertEqual(len(re.findall("Ubuntu", text)), 1, lang)
            self.assertEqual(len(BASE_PHRASE.findall(text)), 1, lang)
            faq = text[text.index('id="questions"'):]
            self.assertTrue(BASE_PHRASE.search(faq), lang)

    def test_faq_memory_matches_the_download_page(self):
        # the idle figure is a measurement; the minimum is the download page's
        idle = {"fr": "environ 1,2 Go", "en": "about 1.2 GB"}
        minimum = {"fr": "4 Go de mémoire", "en": "4 GB of memory"}
        pages_ = builder().DOWNLOAD
        for lang in HOMES:
            faq = read(HOMES[lang])
            faq = faq[faq.index('id="questions"'):]
            self.assertIn(idle[lang], faq, lang)
            self.assertIn(minimum[lang], faq, lang)
            self.assertTrue(any(item.startswith(minimum[lang])
                                for item in pages_[lang]["needs_items"]), lang)

    def test_updates_are_said_to_install_while_you_work(self):
        # Raye Update installs whatever needs no restart right away
        update = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                              "update", "src", "raye_update.py")
        if os.path.exists(update):
            with open(update, encoding="utf-8") as f:
                self.assertIn("raye-update-live@", f.read())
        said = {"fr": "pendant que vous travaillez", "en": "while you work"}
        stale = ("au redémarrage", "que vous redémarrez", "on restart",
                 "next time you restart")
        for lang in HOMES:
            text = read(HOMES[lang])
            coming = text[text.index('id="nouveautes"'):text.index('id="questions"')]
            self.assertIn(said[lang], coming, lang)
            for rel in (HOMES[lang],) + DOWNLOAD_PAGES:
                for phrase in stale:
                    self.assertNotIn(phrase, read(rel), (rel, phrase))

    def test_the_full_list_sentence_follows_the_download_flag(self):
        b = builder()
        for live in (False, True):
            b.DOWNLOAD_LIVE = live
            for lang in HOMES:
                faq = b.home(lang)
                faq = faq[faq.index('id="questions"'):]
                self.assertIn(b.HOME[lang]["full_list"][live], faq, (lang, live))
                self.assertNotIn(b.HOME[lang]["full_list"][not live], faq, (lang, live))
        flag = builder().DOWNLOAD_LIVE
        for lang in HOMES:
            self.assertIn(b.HOME[lang]["full_list"][flag].replace(" :", "\u00a0:"),
                          read(HOMES[lang]), lang)


class NotYetPublicTests(unittest.TestCase):
    """The download pages are built ahead of the image. Until they go live,
    deploy.sh keeps them off the server, so no published page may link to
    them: a visitor would land on a 404."""

    def setUp(self):
        self.live = builder().DOWNLOAD_LIVE
        with open(os.path.join(ROOT, "..", "deploy", "not-yet-public"), encoding="utf-8") as f:
            self.held = [l.strip() for l in f if l.strip().startswith("/")]

    def test_the_held_list_follows_the_flag(self):
        want = [] if self.live else ["/fr/telecharger/", "/en/download/"]
        self.assertEqual(self.held, want)

    def test_no_published_page_links_to_a_held_one(self):
        for rel in PAGES:
            if rel in DOWNLOAD_PAGES:
                continue
            for tag, attrs in parse(read(rel)).tags:
                href = attrs.get("href", "")
                with self.subTest(page=rel, href=href):
                    self.assertFalse(any(href.startswith(h) for h in self.held), href)

    def test_deploy_reads_the_held_list(self):
        with open(os.path.join(ROOT, "..", "deploy", "deploy.sh"), encoding="utf-8") as f:
            script = f.read()
        self.assertIn("deploy/not-yet-public", script)
        self.assertIn('--exclude-from="$EXCLUDES"', script)
