"""Renders the V1 site from tools/site_v1_text.py.

Called by build_pages.py. While build_pages.V1_LIVE is False the V1 site
is written to site-v1/ (the coming-soon page in site/ stays what is
online); at launch it is written to site/ itself. Same rules as the rest of
the site: no inline script or style, nothing loaded from elsewhere, French
and English with the same structure.

A screenshot block shows the real picture once shots/<id>-<lang>-1600.webp
exists at the top of the repository, and a labelled placeholder until then
-- never a stand-in picture. shots/ is the only place V1 screenshots come
from: the build copies it into <site>/assets/shots and removes whatever
else is there, so the coming-soon page's 0.2 pictures, which carry some of
the same names, can never stand in for a 1.0 one."""

import hashlib
import html
import os
import re
import shutil

import site_v1_people as people
import site_v1_text as V

TOOLS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(TOOLS, "..")
# where the V1 screenshots are dropped, and their manifest (version, date)
SHOTS_SRC = os.path.join(REPO, "shots")
SHOT_FILE = re.compile(r"^[a-z0-9-]+-(fr|en)-(1600|800)\.(webp|jpg)$")
NBSP = " "
# copied as they are from the coming-soon site's assets
SHARED_ASSETS = ("support.js", "site.css", "app.js", "favicon.svg", "raye-mark.svg", "raye-eye.svg")


class Site:
    """One build of the V1 site: where it goes and what is switched on."""

    def __init__(self, builder):
        self.b = builder
        self.root = builder.ROOT if builder.V1_LIVE else os.path.join(REPO, "site-v1")
        self.download_live = builder.DOWNLOAD_LIVE

    # ---------------------------------------------------------- text

    def path(self, key, lang):
        return V.PAGES[key]["path"][lang]

    def name(self, key, lang):
        return V.PAGES[key]["name"][lang]

    def fill(self, text, lang):
        """{p:key}, {m:key}, {v} and {free} in a text."""
        text = re.sub(r"\{p:([a-z]+)\}", lambda m: self.path(m.group(1), lang), text)
        text = re.sub(r"\{m:([a-z]+)\}",
                      lambda m: V.MEASURES[m.group(1)]["value"][lang].replace(" ", NBSP), text)
        text = text.replace("{v}", V.VERSION).replace("{free}", str(V.FREE_GB))
        # a number and its unit stay on one line, and so do a name and its number
        text = re.sub(r"(\d) (Go|Mo|GB|MB|Mo/s|MB/s|ms|s|min|h|%)(?![\w/])", r"\1" + NBSP + r"\2",
                      text)
        text = text.replace("free -m", "free" + NBSP + "-m")
        return text.replace("Windows 11", "Windows" + NBSP + "11")

    def t(self, pair, lang):
        return self.fill(pair[lang], lang)

    def shot_file(self, shot_id, lang, width, ext):
        return os.path.join(SHOTS_SRC, f"{shot_id}-{lang}-{width}.{ext}")

    def has_shot(self, shot_id, lang):
        return all(os.path.isfile(self.shot_file(shot_id, lang, w, e))
                   for w, e in ((1600, "webp"), (800, "webp"), (1600, "jpg")))

    # ---------------------------------------------------------- shell

    def head(self, lang, key, title, description, scripts=()):
        other = "en" if lang == "fr" else "fr"
        here, there = self.path(key, lang), self.path(key, other)
        url = self.b.URL
        extra = "".join(f'\n<script src="/assets/{name}" defer></script>' for name in scripts)
        og = ""
        if self.has_shot("desktop", lang):
            og = (f'\n<meta property="og:image" content="{url}/assets/shots/desktop-{lang}-1600.jpg">'
                  '\n<meta property="og:image:width" content="1600">'
                  '\n<meta property="og:image:height" content="900">')
        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(description)}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141318">
<link rel="canonical" href="{url}{here}">
<link rel="alternate" hreflang="{lang}" href="{url}{here}">
<link rel="alternate" hreflang="{other}" href="{url}{there}">
<link rel="alternate" hreflang="x-default" href="{url}{self.path(key, 'fr')}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/v1.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Raye Linux">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}{here}">
<meta property="og:locale" content="{'fr_CA' if lang == 'fr' else 'en_CA'}">{og}
<script src="/assets/lang.js"></script>
<script src="/assets/app.js" defer></script>
<script src="/assets/support.js" defer></script>{extra}
</head>"""

    def download_button(self, lang, small=False):
        ui = V.UI[lang]
        size = " btn-small" if small else ""
        if self.download_live:
            return (f'<a class="btn btn-accent{size}" href="{self.path("download", lang)}">'
                    f'{ui["download"]}</a>')
        return f'<span class="btn btn-held{size}">{ui["download_held"]}</span>'

    def topbar(self, lang, key):
        ui = V.UI[lang]
        other = ui["switch_lang"]
        items = []
        for page in V.NAV:
            current = ' aria-current="page"' if page == key else ""
            items.append(f'<li><a href="{self.path(page, lang)}"{current}>'
                         f'{self.name(page, lang)}</a></li>')
        links = "\n".join(items)
        return f"""<header class="topbar">
<div class="topbar-in">
<a class="brand" href="{self.path('home', lang)}" aria-label="{ui['brand_label']}">
<img src="/assets/raye-mark.svg" alt="" width="28" height="28"><span>Raye Linux</span></a>
<nav class="nav" aria-label="{ui['nav_label']}">
<ul>
{links}
</ul>
</nav>
<div class="topbar-end">
<a class="lang-switch" href="{self.path(key, other)}" hreflang="{other}" lang="{other}"
   data-set-lang="{other}" aria-label="{ui['switch_label']}">{self.b.GLOBE}<span>{ui['switch']}</span></a>
{self.download_button(lang, small=True)}
</div>
</div>
</header>"""

    def footer(self, lang):
        ui = V.UI[lang]
        cols = []
        for title, keys in V.FOOTER:
            links = "\n".join(f'<li><a href="{self.path(k, lang)}">{self.name(k, lang)}</a></li>'
                              for k in keys if k != "download" or self.download_live)
            cols.append(f'<div>\n<h2>{title[lang]}</h2>\n<ul>\n{links}\n</ul>\n</div>')
        cols = "\n".join(cols)
        return f"""<footer class="footer v1-footer">
<div class="wrap">
<div class="footer-cols">
<div class="footer-brand">
<img src="/assets/raye-mark.svg" alt="" width="28" height="28">
<p>{ui['rights']}<br><a href="mailto:{ui['mail']}">{ui['mail']}</a></p>
<p><a class="btn btn-quiet btn-small" href="{self.b.DISCORD}" rel="noopener">Discord</a></p>
</div>
{cols}
</div>
</div>
</footer>"""

    def page(self, lang, key, title, description, main, body_class="", scripts=()):
        ui = V.UI[lang]
        return f"""{self.head(lang, key, title, description, scripts)}
<body class="v1 page-{key}{' ' + body_class if body_class else ''}">
<a class="skip-link" href="#main">{ui['skip']}</a>
{self.topbar(lang, key)}
<main id="main">
{main}
</main>
{self.footer(lang)}
</body>
</html>
"""

    # ---------------------------------------------------------- blocks

    def shot(self, shot_id, lang, hero=False):
        text = self.t(V.SHOTS[shot_id], lang)
        # an alt attribute takes plain text: no tag, and quotes escaped
        alt = html.escape(re.sub(r"<[^>]+>", "", text), quote=True)
        ui = V.UI[lang]
        cls = "shot shot-hero" if hero else "shot"
        if self.has_shot(shot_id, lang):
            base = f"/assets/shots/{shot_id}-{lang}"
            # the picture at the top of the home page is the first thing seen:
            # fetched at once, and as wide as the hero column
            load = ('loading="eager" fetchpriority="high"' if hero
                    else 'loading="lazy"')
            sizes = "(min-width: 76rem) 72rem, 94vw" if hero else "(min-width: 60rem) 56rem, 94vw"
            return (f'<figure class="{cls}">\n<a class="shot-frame" href="{base}-1600.webp">\n'
                    f'<picture>\n<source type="image/webp" srcset="{base}-800.webp 800w, '
                    f'{base}-1600.webp 1600w" sizes="{sizes}">\n'
                    f'<img src="{base}-1600.jpg" alt="{alt}" width="1600" height="900" '
                    f'{load} decoding="async">\n</picture>\n</a>\n</figure>')
        note = ui["shot_note"].format(v=V.VERSION)
        return (f'<figure class="{cls}">\n<div class="shot-todo" data-shot="{shot_id}">\n'
                f'<p class="todo-label">{ui["shot_todo"]} · <code>{shot_id}</code></p>\n'
                f'<p class="todo-what">{text}</p>\n<p class="todo-note">{note}</p>\n'
                f'</div>\n</figure>')

    def measures(self, keys, lang):
        """A table of measurements. When every row comes from the same
        machine, date and version, that is said once under the table."""
        ui = V.UI[lang]
        ms = [V.MEASURES[k] for k in keys]
        origin = lambda m: (m["machine"], m["date"], m["version"])
        shared = len({origin(m) for m in ms}) == 1

        def where(m):
            return ui["measured"].format(date=self.b.date_text(lang, m["date"]),
                                         version=m["version"],
                                         machine=V.MACHINES[m["machine"]][lang])
        rows = []
        for m in ms:
            cell = "" if shared else f'\n<td>{where(m)}</td>'
            rows.append(f'<tr>\n<th scope="row">{self.t(m["name"], lang)}'
                        f'<span class="how">{self.t(m["how"], lang)}</span></th>\n'
                        f'<td class="num">{m["value"][lang].replace(" ", NBSP)}</td>{cell}\n</tr>')
        head_where = "" if shared else f'<th scope="col">{ui["col_where"]}</th>'
        note = f'\n<p class="table-note">{where(ms[0])}</p>' if shared else ""
        return (f'<div class="table-scroll">\n<table class="measures">\n<thead>\n<tr>'
                f'<th scope="col">{ui["col_measure"]}</th><th scope="col">{ui["col_value"]}</th>'
                f'{head_where}</tr>\n</thead>\n<tbody>\n' + "\n".join(rows) +
                f'\n</tbody>\n</table>{note}\n</div>')

    _section = ""

    def block(self, b, lang):
        kind = b[0]
        if kind == "h2":
            self._section = b[1]
            return f'<h2 id="{b[1]}">{self.t(b[2], lang)}</h2>'
        if kind == "p":
            return f"<p>{self.t(b[1], lang)}</p>"
        if kind == "shot":
            return self.shot(b[1], lang)
        if kind == "limits":
            # each box is named after its section ("What is still missing" +
            # "Task Manager"): a screen reader lists them apart, not as six
            # identical asides
            items = "\n".join(f"<li>{self.t(x, lang)}</li>" for x in b[1])
            own = f"limits-{self._section or 'page'}"
            label = f"{own} {self._section}" if self._section else own
            return (f'<aside class="limits" aria-labelledby="{label}">\n'
                    f'<p class="limits-title" id="{own}">{V.UI[lang]["limits"]}</p>\n'
                    f'<ul>\n{items}\n</ul>\n</aside>')
        if kind == "list":
            items = "\n".join(f"<li>{self.t(x, lang)}</li>" for x in b[1])
            return f'<ul class="text-list">\n{items}\n</ul>'
        if kind == "keys":
            rows = "\n".join(f"<div>\n<dt>{self.t(k, lang)}</dt>\n<dd>{self.t(d, lang)}</dd>\n</div>"
                             for k, d in b[1])
            return f'<dl class="keys">\n{rows}\n</dl>'
        if kind == "measures":
            return self.measures(b[1], lang)
        if kind == "steps":
            items = "\n".join(f"<li>\n<h3>{self.t(h, lang)}</h3>\n<p>{self.t(p, lang)}</p>\n</li>"
                              for h, p in b[1])
            return f'<ol class="step-list">\n{items}\n</ol>'
        if kind == "qa":
            # open, not folded: an honest answer should not need a click to be read
            items = "\n".join(f'<div class="qa-open">\n<h2 id="q{i}">{self.t(q, lang)}</h2>\n'
                              f"<p>{self.t(a, lang)}</p>\n</div>"
                              for i, (q, a) in enumerate(b[1], 1))
            return f'<div class="v1-qa">\n{items}\n</div>'
        if kind == "timeline":
            return self.timeline(b[1], lang)
        if kind == "pair":
            return self.pair(b, lang)
        if kind == "path":
            items = "\n".join(
                f'<li>\n<a href="{self.path(k, lang)}">{self.name(k, lang)}</a>\n'
                f"<p>{self.t(x, lang)}</p>\n</li>" for k, x in b[1])
            return f'<ol class="path">\n{items}\n</ol>'
        if kind == "note":
            paras = "\n".join(f"<p>{self.t(x, lang)}</p>" for x in b[2])
            return (f'<div class="author-note v1-note">\n<h2 id="note">{b[1][lang]}</h2>\n'
                    f'{paras}\n<p class="signature">techoraye</p>\n</div>')
        raise ValueError(f"unknown block {kind}")

    def pair(self, b, lang):
        _, t1, items1, t2, items2 = b
        cols = []
        for title, items in ((t1, items1), (t2, items2)):
            lis = "\n".join(f"<li>{self.t(x, lang)}</li>" for x in items)
            cols.append(f'<div>\n<h3>{title[lang]}</h3>\n<ul>\n{lis}\n</ul>\n</div>')
        return '<div class="pair">\n' + "\n".join(cols) + "\n</div>"

    def timeline(self, entries, lang):
        ui = V.UI[lang]
        items = []
        for date, version, text in entries:
            if date:
                when = f'<time datetime="{date}">{self.b.date_text(lang, date)}</time>'
            else:
                when = f'<span class="tl-later">{ui["to_come"]}</span>'
            items.append(f'<li>\n<div class="tl-head">\n<h2>{self.t(version, lang)}</h2>\n'
                         f'{when}\n</div>\n<p>{self.t(text, lang)}</p>\n</li>')
        return '<ol class="timeline">\n' + "\n".join(items) + "\n</ol>"

    def blocks(self, blocks, lang):
        self._section = ""
        return "\n".join(self.block(b, lang) for b in blocks)

    def next_link(self, key, lang):
        if key == "download" and not self.download_live:
            key = "questions"
        return (f'<nav class="next wrap" aria-label="{V.UI[lang]["next"]}">\n'
                f'<a href="{self.path(key, lang)}"><span>{V.UI[lang]["next"]}</span>'
                f'<strong>{self.name(key, lang)}</strong></a>\n</nav>')

    # ---------------------------------------------------------- pages

    def home(self, lang):
        h = V.HOME
        meta = h["meta"][lang].format(v=V.VERSION)
        main = f"""<section class="v1-hero wrap" aria-labelledby="title">
<div class="v1-hero-text">
<h1 id="title">{self.t(h['h1'], lang)}</h1>
<p class="lede">{self.t(h['lede'], lang)}</p>
<div class="hero-actions">
{self.download_button(lang)}
<a class="btn btn-quiet" href="#changes">{h['more'][lang]}</a>
</div>
<p class="hero-meta">{meta}</p>
{self.b.site_stats(lang)}
</div>
{self.shot(h['hero_shot'], lang, hero=True)}
</section>
<div class="article">
{self.blocks(h['blocks'], lang)}
</div>
{people.people_band(self, lang)}"""
        return self.page(lang, "home", h["title"][lang], h["description"][lang], main, "home-v1")

    def content_page(self, lang, key):
        c = V.CONTENT[key]
        h1 = self.t(c["h1"], lang)
        title = f"{re.sub('<[^>]+>', '', h1)} · Raye Linux"
        main = f"""<header class="page-head">
<p class="eyebrow">{c['eyebrow'][lang]}</p>
<h1>{h1}</h1>
<p class="lede">{self.t(c['lede'], lang)}</p>
</header>
<div class="article">
{self.blocks(c['blocks'], lang)}
</div>
{self.next_link(c['next'], lang)}"""
        return self.page(lang, key, title, self.t(c["description"], lang), main)

    def not_found(self):
        """One page for both languages, in the V1 shell: nginx cannot know
        which language was meant, so the top bar is the French one and the
        page says it in both."""
        nf = V.NOT_FOUND
        blocks = []
        for lang, tag in (("fr", "h1"), ("en", "h2")):
            links = "\n".join(f'<li><a href="{self.path(k, lang)}">{self.name(k, lang)}</a></li>'
                              for k in ("home", "desktop", "windows", "questions"))
            blocks.append(f'<section class="result-v1" lang="{lang}">\n'
                          f'<{tag}>{nf["h1"][lang]}</{tag}>\n<p>{nf["text"][lang]}</p>\n'
                          f'<ul class="text-list">\n{links}\n</ul>\n</section>')
        main = '<div class="article not-found">\n' + "\n".join(blocks) + "\n</div>"
        text = self.page("fr", "home", nf["title"], nf["description"], main, "page-404")
        text = text.replace('<meta name="viewport"',
                            '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
        return text.replace('<script src="/assets/lang.js"></script>\n', "")

    # ---------------------------------------------------------- output

    def versioned(self, text):
        def tag(m):
            name = m.group(1)
            with open(os.path.join(self.root, "assets", name), "rb") as f:
                return "/assets/%s?v=%s" % (name, hashlib.sha256(f.read()).hexdigest()[:10])
        return re.sub(r'/assets/([A-Za-z0-9._/-]+)(?:\?v=[0-9a-f]+)?(?=[" ])', tag, text)

    def write(self, rel, text, lang):
        if lang == "fr":
            text = french(text)
        text = self.versioned(text)
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def rel(self, key, lang):
        return self.path(key, lang).lstrip("/") + "index.html"

    def shots(self, dest):
        """<site>/assets/shots becomes exactly the screenshots of shots/."""
        os.makedirs(dest, exist_ok=True)
        wanted = sorted(n for n in (os.listdir(SHOTS_SRC) if os.path.isdir(SHOTS_SRC) else ())
                        if SHOT_FILE.match(n))
        for name in os.listdir(dest):
            if name not in wanted:
                os.remove(os.path.join(dest, name))
        for name in wanted:
            src, dst = os.path.join(SHOTS_SRC, name), os.path.join(dest, name)
            if not os.path.isfile(dst) or open(src, "rb").read() != open(dst, "rb").read():
                shutil.copyfile(src, dst)

    def assets(self):
        dest = os.path.join(self.root, "assets")
        self.shots(os.path.join(dest, "shots"))
        if self.root != self.b.ROOT:
            for name in SHARED_ASSETS:
                shutil.copyfile(os.path.join(self.b.ROOT, "assets", name),
                                os.path.join(dest, name))
        shutil.copyfile(os.path.join(TOOLS, "site_v1.css"), os.path.join(dest, "v1.css"))
        shutil.copyfile(os.path.join(TOOLS, "site_v1.js"), os.path.join(dest, "v1.js"))
        with open(os.path.join(dest, "lang.js"), "w", encoding="utf-8") as f:
            f.write(lang_js())

    def build(self):
        self.assets()
        for lang in ("fr", "en"):
            self.write(self.rel("home", lang), self.home(lang), lang)
            for key in V.CONTENT:
                self.write(self.rel(key, lang), self.content_page(lang, key), lang)
            self.write(self.rel("download", lang), self.b.download(lang, shell=self), lang)
            for key in ("privacy", "terms", "betaterms", "notice", "licenses"):
                self.write(self.rel(key, lang), people.legal(self, lang, key), lang)
            self.write(self.rel("join", lang), people.join_index(self, lang), lang)
            for role, r in people.J.ROLES.items():
                self.write(self.rel(r["page"], lang), people.role_page(self, lang, role), lang)
            self.write(self.rel("community", lang), people.community(self, lang), lang)
            self.write(self.rel("rules", lang), people.rules(self, lang), lang)
            # the roadmap and source lists are built once, by build_pages.py
            rm = self.b.roadmap_text.PAGE[lang]
            self.write(self.rel("roadmap", lang),
                       people.borrowed(self, lang, "roadmap",
                                       people.roadmap_words(self.b.roadmap(lang), lang),
                                       rm["description"]), lang)
            self.write(self.rel("source", lang),
                       people.borrowed(self, lang, "source", self.b.source(lang),
                                       self.b.SOURCE[lang]["lead"][:150].rsplit(" ", 1)[0] + "…"),
                       lang)
        self.write("404.html", self.b.strip_links(self.not_found()), "fr")

def lang_js():
    """The coming-soon lang.js, with every V1 page in its map."""
    pairs = ",\n    ".join(f'"{p["path"]["fr"]}": "{p["path"]["en"]}"' for p in V.PAGES.values())
    return f"""// Runs before the page draws: send visitors whose browser is not in French
// to the English page, unless they already picked a language with the switch.
// Written by tools/site_v1.py from the list of pages.
(function () {{
  "use strict";
  var MAP = {{
    {pairs}
  }};
  var target = MAP[window.location.pathname];
  if (!target) return;
  var choice = null;
  try {{ choice = window.localStorage.getItem("raye-lang"); }} catch (e) {{ /* storage off */ }}
  if (choice === "fr") return;
  if (choice !== "en") {{
    var langs = navigator.languages && navigator.languages.length
      ? navigator.languages : [navigator.language || "fr"];
    for (var i = 0; i < langs.length; i++) {{
      if (/^fr\\b/i.test(String(langs[i]))) return;
    }}
  }}
  window.location.replace(target + window.location.search + window.location.hash);
}})();
"""


def french(text):
    """French spacing: a no-break space before : ? ! ; and inside « ».

    Only in text, never inside a tag (an address, an attribute)."""
    def fix(part):
        if part.startswith("<"):
            return part
        part = re.sub(r" ([:?!;])", NBSP + r"\1", part)
        return part.replace("« ", "«" + NBSP).replace(" »", NBSP + "»")
    return "".join(fix(p) for p in re.split(r"(<[^>]*>)", text))


def build(builder):
    Site(builder).build()
