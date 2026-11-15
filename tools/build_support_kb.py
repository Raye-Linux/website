#!/usr/bin/env python3
"""Builds what the help bubble on rayelinux.com may answer from.

Only real sources go in: the handbook, the questions and the download page
of the site as a visitor reads them, the release notes of the published
release, and the help texts of the Discord server. The result is
backend/raye_site/support_kb.json, committed and deployed with the backend.

    tools/build_support_kb.py           # rewrite the file
    tools/build_support_kb.py --check   # exit 1 if the file is stale

deploy.sh runs --check before anything is copied: a page or a handbook
change that is not in the file stops the deploy instead of shipping old
answers. Every path can be moved with an environment variable."""

import ast
import hashlib
import html.parser
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEBSITE = os.path.normpath(os.path.join(HERE, ".."))
SITE = os.path.join(WEBSITE, "site")
OUT = os.path.join(WEBSITE, "backend", "raye_site", "support_kb.json")
RELEASE = os.path.join(HERE, "release.json")

# the values for one machine live in deploy/site.env (not in git), like for deploy.sh
_LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deploy", "site.env")
if os.path.isfile(_LOCAL):
    for _line in open(_LOCAL, encoding="utf-8"):
        _key, _sep, _value = _line.strip().partition("=")
        if _sep and _key.startswith("RAYE_") and not _line.lstrip().startswith("#"):
            os.environ.setdefault(_key, _value.strip().strip('"').strip("'"))
HANDBOOK = os.environ.get("RAYE_HANDBOOK", os.path.join(WEBSITE, "..", "handbook"))
PUBLISH = os.environ.get("RAYE_PUBLISH", "/srv/publish/release")
DISCORD_TEXTS = os.environ.get("RAYE_DISCORD_TEXTS", "discord-texts.py")

# one piece of text the model sees at once; longer sections are cut at a
# paragraph break
CHUNK_MAX = 1800

PAGES = {
    "fr": {"home": "/fr/", "download": "/fr/telecharger/", "file": "fr/index.html",
           "dl_file": "fr/telecharger/index.html"},
    "en": {"home": "/en/", "download": "/en/download/", "file": "en/index.html",
           "dl_file": "en/download/index.html"},
}


class Missing(Exception):
    pass


def read(path):
    if not os.path.isfile(path):
        raise Missing(path)
    with open(path, encoding="utf-8") as f:
        return f.read()


def clean(text):
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()


def split_long(title, text):
    """Pieces of at most CHUNK_MAX characters, cut between paragraphs."""
    out, cur = [], ""
    for para in text.split("\n\n"):
        if cur and len(cur) + len(para) + 2 > CHUNK_MAX:
            out.append(cur)
            cur = para
        else:
            cur = f"{cur}\n\n{para}" if cur else para
    if cur:
        out.append(cur)
    return [(title if i == 0 else f"{title} ({i + 1})", t) for i, t in enumerate(out)]


def markdown_chunks(text, page_title):
    """(title, text) per ## or ### section; links keep their words only."""
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    sections, title, lines = [], page_title, []
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.*)", line)
        if m:
            if "\n".join(lines).strip():
                sections.append((title, "\n".join(lines)))
            level, head = len(m.group(1)), m.group(2).strip()
            title = head if level == 1 else f"{page_title} › {head}"
            if level == 1:
                page_title = head
            lines = []
        else:
            lines.append(line)
    if "\n".join(lines).strip():
        sections.append((title, "\n".join(lines)))
    out = []
    for t, body in sections:
        out += split_long(t, clean(body))
    return out


class Text(html.parser.HTMLParser):
    """The visible text of a page, with its headings and questions marked."""

    BLOCK = {"p", "li", "pre", "tr", "div", "section", "details", "h3", "dd", "dt"}

    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "title", "nav", "header", "footer", "svg"):
            self.skip += 1
        elif tag in ("h2", "summary"):
            self.parts.append("\n\n\x00")
        elif tag in self.BLOCK:
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "title", "nav", "header", "footer", "svg"):
            self.skip -= 1
        elif tag in ("h2", "summary"):
            self.parts.append("\x01\n\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data.replace("\xa0", " "))


def page_sections(html_text):
    """(heading, text) for each h2 or summary of a page."""
    p = Text()
    p.feed(html_text)
    raw = "".join(p.parts)
    out = []
    for piece in raw.split("\x00")[1:]:
        head, _, body = piece.partition("\x01")
        head, body = clean(head), clean(re.sub(r"\n\s*\n", "\n\n", body))
        if head and body:
            out.append((head, body))
    return out


def site_chunks():
    chunks = []
    for lang, p in PAGES.items():
        home = read(os.path.join(SITE, p["file"]))
        start = home.index('id="questions"')
        faq = home[start:home.index("</section>", start)]
        questions = [(q, a) for q, a in page_sections(faq) if q != "Questions"]
        for i, (q, a) in enumerate(questions):
            chunks.append({"id": f"faq:{lang}:{i}", "lang": lang, "title": q,
                           "url": p["home"] + "#questions", "text": a})
        dl = read(os.path.join(SITE, p["dl_file"]))
        main = dl[dl.index("<main"):dl.index("</main>")]
        for i, (h, body) in enumerate(page_sections(main)):
            for j, (t, text) in enumerate(split_long(h, body)):
                chunks.append({"id": f"download:{lang}:{i}.{j}", "lang": lang, "title": t,
                               "url": p["download"], "text": text})
    return chunks


def handbook_chunks():
    chunks = []
    for lang in ("fr", "en"):
        folder = os.path.join(HANDBOOK, lang)
        if not os.path.isdir(folder):
            raise Missing(folder)
        for name in sorted(os.listdir(folder)):
            if not name.endswith(".md"):
                continue
            text = read(os.path.join(folder, name))
            for i, (t, body) in enumerate(markdown_chunks(text, name[:-3])):
                chunks.append({"id": f"handbook:{lang}:{name[:-3]}:{i}", "lang": lang,
                               "title": t, "url": None, "text": body})
    return chunks


def notes_paths():
    with open(RELEASE, encoding="utf-8") as f:
        release = json.load(f)["release"]
    base = os.path.join(PUBLISH, release, f"release-notes-{release}")
    return {"en": base + ".md", "fr": base + ".fr.md"}


def notes_chunks():
    chunks = []
    for lang, path in notes_paths().items():
        for i, (t, body) in enumerate(markdown_chunks(read(path), "Notes")):
            chunks.append({"id": f"notes:{lang}:{i}", "lang": lang, "title": t,
                           "url": PAGES[lang]["download"], "text": body})
    return chunks


def discord_text(text):
    """Channel and role mentions as a reader of the site would say them."""
    text = re.sub(r"<#\{(\w+)\}>", lambda m: "#" + m.group(1).replace("_", "-"), text)
    text = re.sub(r"<@&\{(\w+)\}>", r"@\1", text)
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text).replace("**", "")


def discord_chunks():
    """The constants of texts.py, read without running the file."""
    tree = ast.parse(read(DISCORD_TEXTS))
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            try:
                values[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    chunks = []
    for lang, suffix in (("en", "EN"), ("fr", "FR")):
        for i, (q, a) in enumerate(values[f"FAQ_{suffix}"]):
            chunks.append({"id": f"faq:discord:{lang}:{i}", "lang": lang, "title": q,
                           "url": None, "text": discord_text(a)})
        title = "Discord rules" if lang == "en" else "Règles du serveur Discord"
        chunks.append({"id": f"discord:rules:{lang}", "lang": lang, "title": title,
                       "url": None, "text": discord_text(values[f"RULES_{suffix}"])})
    for key in ("HELP_GUIDE", "BUGS_GUIDE"):
        en, _, fr = values[key].partition("**Français**")
        chunks.append({"id": f"discord:{key.lower()}:en", "lang": "en",
                       "title": values[key + "_TITLE"].split(" / ")[0],
                       "url": None, "text": discord_text(en.replace("**English**", ""))})
        chunks.append({"id": f"discord:{key.lower()}:fr", "lang": "fr",
                       "title": values[key + "_TITLE"].split(" / ")[1],
                       "url": None, "text": discord_text(fr)})
    for c in chunks:
        c["text"] = clean(c["text"])
    return chunks


def source_files():
    files = [os.path.join(SITE, p[k]) for p in PAGES.values() for k in ("file", "dl_file")]
    for lang in ("fr", "en"):
        folder = os.path.join(HANDBOOK, lang)
        files += sorted(os.path.join(folder, n) for n in os.listdir(folder) if n.endswith(".md"))
    files += list(notes_paths().values()) + [DISCORD_TEXTS]
    return files


def build():
    chunks = site_chunks() + handbook_chunks() + notes_chunks() + discord_chunks()
    sources = {}
    for path in source_files():
        with open(path, "rb") as f:
            sources[os.path.basename(os.path.dirname(path)) + "/" + os.path.basename(path)] = \
                hashlib.sha256(f.read()).hexdigest()[:16]
    with open(RELEASE, encoding="utf-8") as f:
        title = json.load(f)["title"]
    return {"release": title, "site": "https://rayelinux.com", "sources": sources,
            "chunks": chunks}


def dump(kb):
    return json.dumps(kb, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def main(argv):
    check = "--check" in argv
    try:
        text = dump(build())
    except Missing as exc:
        print(f"support knowledge base: source missing: {exc}", file=sys.stderr)
        return 2
    if check:
        try:
            current = read(OUT)
        except Missing:
            current = ""
        if current != text:
            print("support knowledge base is stale: run tools/build_support_kb.py",
                  file=sys.stderr)
            return 1
        print("support knowledge base is current")
        return 0
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {OUT}: {len(json.loads(text)['chunks'])} pieces")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
