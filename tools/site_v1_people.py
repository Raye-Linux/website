"""The V1 pages about people and rules, in the V1 shell of site_v1.py:
Join the team (overview and one page per role, each with its form), the
Community page with the live Discord numbers, the community rules, the
legal pages (privacy, terms, beta program terms, legal notice, licenses),
and the roadmap and source pages of the live site, re-dressed.

Text: site_v1_join_text.py and legal_v1_text.py."""

import re

import legal_text
import legal_v1_text as LV
import site_v1_join_text as J

ARROW = ('<svg class="arrow" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
         '<path d="M3 8h9M8.5 4.5 12 8l-3.5 3.5" fill="none" stroke="currentColor" '
         'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ROLE_ORDER = ["beta", "public-beta", "beta-dev", "moderator", "translator", "developer", "other"]


def t(site, pair, lang):
    return site.fill(pair[lang], lang)


def head_block(site, eyebrow, h1, lede, lang, crumbs=None, wide=False, here=None):
    """The page header. A page under another one shows the way back to it
    (breadcrumb) where the other pages show their eyebrow."""
    cls = "page-head wide" if wide else "page-head"
    if crumbs:
        links = "".join(f'<li><a href="{site.path(k, lang)}">{site.name(k, lang)}</a></li>'
                        for k in crumbs)
        if here:
            links += f'<li aria-current="page">{site.name(here, lang)}</li>'
        label = "Fil d'Ariane" if lang == "fr" else "Breadcrumb"
        top = f'<nav class="crumbs" aria-label="{label}">\n<ol>{links}</ol>\n</nav>'
    else:
        top = f'<p class="eyebrow">{eyebrow}</p>'
    return (f'<header class="{cls}">\n{top}\n'
            f'<h1>{h1}</h1>\n<p class="lede">{lede}</p>\n</header>')


# ---------------------------------------------------------------- join

def join_index(site, lang):
    j = J.JOIN
    cards = []
    for role in ROLE_ORDER:
        r = J.ROLES[role]
        key = r["page"]
        cards.append(f'<li class="role-card">\n<h3><a href="{site.path(key, lang)}">'
                     f'{site.name(key, lang)}</a></h3>\n<p>{t(site, r["summary"], lang)}</p>\n'
                     f'<span class="role-more" aria-hidden="true">{j["open"][lang]}{ARROW}</span>'
                     f'\n</li>')
    steps = "\n".join(f"<li>\n<h3>{t(site, h, lang)}</h3>\n<p>{t(site, p, lang)}</p>\n</li>"
                      for h, p in j["how"])
    why = "\n".join(f"<li>{t(site, x, lang)}</li>" for x in j["why"])
    main = f"""{head_block(site, j['eyebrow'][lang], j['h1'][lang], t(site, j['lede'], lang), lang,
            wide=True)}
<div class="article wide">
<h2 id="roles">{j['roles_title'][lang]}</h2>
<ul class="role-grid">
{chr(10).join(cards)}
</ul>
<div class="split">
<section aria-labelledby="how">
<h2 id="how">{j['how_title'][lang]}</h2>
<ol class="step-list">
{steps}
</ol>
</section>
<section aria-labelledby="why">
<h2 id="why">{j['why_title'][lang]}</h2>
<ul class="text-list">
{why}
</ul>
</section>
</div>
</div>"""
    title = f"{J.PAGES['join']['name'][lang]} · Raye Linux"
    return site.page(lang, "join", title, t(site, j["description"], lang), main)


def field(name, label, hint, lang, kind="input", required=False, attrs="", hint_id=None):
    req = (f' <span class="req-mark" aria-hidden="true">*</span>'
           f'<span class="visually-hidden"> {J.FORM["required"][lang]}</span>') if required else ""
    hid = hint_id or f"{name}-hint"
    described = f' aria-describedby="{hid} {name}-err"'
    need = " required" if required else ""
    if kind == "textarea":
        control = (f'<textarea class="input textarea" id="{name}" name="{name}"{need}'
                   f'{described} {attrs}></textarea>')
    else:
        control = f'<input class="input" id="{name}" name="{name}"{need}{described} {attrs}>'
    return (f'<div class="field">\n<label class="field-label" for="{name}">{label}{req}</label>\n'
            f'<p class="field-hint" id="{hid}">{hint}</p>\n{control}\n'
            f'<p class="field-err" id="{name}-err" data-err-for="{name}"></p>\n</div>')


def apply_form(site, lang, role):
    f = J.FORM
    privacy = (f'<a href="{site.path("privacy", lang)}#applications">'
               f'{f["privacy_link"][lang]}</a>')
    langs_label = f["languages_tr"][lang] if role == "translator" else f["languages"][lang]
    parts = [
        f'<input type="hidden" name="role" value="{role}">',
        f'<input type="hidden" name="lang" value="{lang}">',
        field("email", f["email"][lang], f["email_hint"][lang], lang, required=True,
              attrs='type="email" inputmode="email" autocomplete="email" maxlength="254" '
                    'spellcheck="false" autocapitalize="off"'),
        f'<p class="form-note">{f["accounts"][lang]}</p>',
        field("discord", f["discord"][lang], f["discord_hint"][lang], lang, required=True,
              attrs='type="text" autocomplete="off" maxlength="37" spellcheck="false" '
                    'autocapitalize="off"'),
        field("languages", langs_label, f["languages_hint"][lang], lang,
              required=role == "translator", attrs='type="text" maxlength="120"'),
        field("skills", f["skills"][lang], f["skills_hint"][lang], lang, kind="textarea",
              attrs='rows="3" maxlength="600"'),
        field("why", f["why"][lang], f["why_hint"][lang], lang, kind="textarea", required=True,
              attrs='rows="5" minlength="30" maxlength="1500"'),
        f'<div class="checks">\n<label class="check"><input type="checkbox" name="consent" '
        f'value="on" required aria-describedby="consent-err">\n<span><span class="req">'
        f'{f["consent"][lang].format(privacy=privacy)}</span> {f["required"][lang]}</span>'
        f'</label>\n<p class="field-err" id="consent-err" data-err-for="consent"></p>\n</div>',
        f'<div class="hp" aria-hidden="true"><label for="website">{f["hp"][lang]}</label>\n'
        f'<input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>',
        f'<div class="form-actions">\n<button class="btn btn-accent" type="submit" '
        f'data-sending="{f["sending"][lang]}">{f["send"][lang]}</button>\n</div>',
        f'<p class="form-msg" id="join-msg" role="status" aria-live="polite" '
        f'data-failed="{f["failed"][lang]}" data-ref="{f["reference"][lang]}"></p>',
    ]
    body = "\n".join(parts)
    return (f'<section class="apply card" id="apply" aria-labelledby="apply-title" '
            f'tabindex="-1">\n<h2 id="apply-title">{f["title"][lang]}</h2>\n'
            f'<p class="hint">{f["intro"][lang]}</p>\n'
            f'<form class="join-form" id="join-form" method="post" action="/api/join" '
            f'novalidate data-done="{f["done"][lang]}">\n{body}\n</form>\n</section>')


def role_page(site, lang, role):
    r, ui = J.ROLES[role], J.ROLE_UI
    key = r["page"]
    glance = "\n".join(f"<div>\n<dt>{t(site, k, lang)}</dt>\n<dd>{t(site, v, lang)}</dd>\n</div>"
                       for k, v in r["at"])
    means = "\n".join(f"<li>{t(site, x, lang)}</li>" for x in r["means"])
    expect = "\n".join(f"<li>{t(site, x, lang)}</li>" for x in r["expect"])
    main = f"""{head_block(site, J.JOIN['eyebrow'][lang], site.name(key, lang),
                           t(site, r['lede'], lang), lang, crumbs=['join'], here=key)}
<div class="article">
<dl class="glance" aria-label="{ui['at'][lang]}">
{glance}
</dl>
<p class="hero-actions"><a class="btn btn-accent" href="#apply">{ui['apply'][lang]}</a></p>
<h2 id="means">{ui['means'][lang]}</h2>
<ul class="text-list">
{means}
</ul>
<h2 id="expect">{ui['expect'][lang]}</h2>
<ul class="text-list">
{expect}
</ul>
<p class="approval">{ui['approval'][lang]}</p>
{apply_form(site, lang, role)}
</div>
<nav class="next wrap" aria-label="{ui['all_roles'][lang]}">
<a href="{site.path('join', lang)}"><span>{J.JOIN['eyebrow'][lang]}</span><strong>{ui['all_roles'][lang]}</strong></a>
</nav>"""
    title = f"{site.name(key, lang)} · Raye Linux"
    return site.page(lang, key, title, t(site, r["summary"], lang), main, scripts=("v1.js",))


# ---------------------------------------------------------------- community

def community(site, lang):
    c = J.COMMUNITY
    there = "\n".join(f"<div>\n<dt>{t(site, k, lang)}</dt>\n<dd>{t(site, v, lang)}</dd>\n</div>"
                      for k, v in c["there"])
    words = {"rules": f'<a href="{site.path("rules", lang)}">{c["rules_word"][lang]}</a>',
             "join": f'<a href="{site.path("join", lang)}">{c["join_word"][lang]}</a>'}
    main = f"""{head_block(site, c['eyebrow'][lang], c['h1'][lang], t(site, c['lede'], lang), lang)}
<div class="article">
<section class="live card" aria-labelledby="live-title" data-community>
<div class="live-head">
<img src="/assets/raye-mark.svg" alt="" width="44" height="44">
<div>
<p class="live-label" id="live-title">{c['live_label'][lang]}</p>
<p class="live-name">Raye Linux</p>
</div>
</div>
<p class="live-numbers" aria-live="polite">
<span class="live-wait" data-live-wait>{c['live_wait'][lang]}</span>
<span class="live-count" data-live-count hidden><strong data-members></strong> {c['members'][lang]}</span>
<span class="live-count live-online" data-live-count hidden><span class="dot" aria-hidden="true"></span><strong data-online></strong> {c['online'][lang]}</span>
</p>
<p><a class="btn btn-accent" href="{site.b.DISCORD}" rel="noopener">{c['join'][lang]}</a></p>
<p class="small">{c['privacy'][lang]}</p>
</section>
<h2 id="there">{c['there_title'][lang]}</h2>
<dl class="keys feature-keys">
{there}
</dl>
<h2 id="further">{c['help_title'][lang]}</h2>
<p>{c['help'][lang].format(**words)}</p>
</div>"""
    title = f"{site.name('community', lang)} · Raye Linux"
    return site.page(lang, "community", title, t(site, c["description"], lang), main,
                     scripts=("v1.js",))


def rules(site, lang):
    r = J.RULES
    items = "\n".join(f"<li>\n<h3>{t(site, h, lang)}</h3>\n<p>{t(site, p, lang)}</p>\n</li>"
                      for h, p in r["rules"])
    mod = "\n".join(f"<li>{t(site, x, lang)}</li>" for x in r["mod"])
    main = f"""{head_block(site, r['eyebrow'][lang], r['h1'][lang], t(site, r['lede'], lang), lang,
                           crumbs=['community'], here='rules')}
<div class="article">
<ol class="step-list rules-list">
{items}
</ol>
<h2 id="moderators">{r['mod_title'][lang]}</h2>
<ul class="text-list">
{mod}
</ul>
<h2 id="appeal">{r['appeal_title'][lang]}</h2>
<p>{r['appeal'][lang]}</p>
</div>"""
    title = f"{r['h1'][lang]} · Raye Linux"
    return site.page(lang, "rules", title, t(site, r["description"], lang), main)


def people_band(site, lang):
    """The end of the home page: the community and the open roles."""
    c, j = J.COMMUNITY, J.JOIN
    return f"""<section class="people wrap" aria-labelledby="people-title">
<h2 id="people-title" class="visually-hidden">{c['eyebrow'][lang]}</h2>
<div class="people-grid">
<a class="people-card" href="{site.path('community', lang)}">
<span class="eyebrow">{c['eyebrow'][lang]}</span>
<strong>{c['h1'][lang]}</strong>
<span>{t(site, c['lede'], lang)}</span>
<span class="role-more">{site.name('community', lang)}{ARROW}</span>
</a>
<a class="people-card" href="{site.path('join', lang)}">
<span class="eyebrow">{j['eyebrow'][lang]}</span>
<strong>{j['h1'][lang]}</strong>
<span>{t(site, j['lede'], lang)}</span>
<span class="role-more">{site.name('join', lang)}{ARROW}</span>
</a>
</div>
</section>"""


# ---------------------------------------------------------------- legal

LEGAL_EYEBROW = {"fr": "Légal", "en": "Legal"}
LEGAL_DESCRIPTION = {
    "privacy": {"fr": "Ce que rayelinux.com et Raye Linux gardent sur vous : candidatures, liste "
                      "de courriels, rapports de bogue. Combien de temps, et vos droits.",
                "en": "What rayelinux.com and Raye Linux keep about you: applications, mailing "
                      "list, bug reports. How long, and your rights."},
    "terms": {"fr": "Les conditions d'utilisation du site, du logiciel Raye Linux, de la "
                    "communauté et des rôles de l'équipe.",
              "en": "The terms of use of the site, the Raye Linux software, the community and "
                    "the team roles."},
    "cookies": {"fr": "Les témoins (cookies) et le stockage local de rayelinux.com : aucun "
                      "aujourd'hui, sauf votre langue si vous la choisissez.",
                "en": "The cookies and local storage of rayelinux.com: none today, except "
                      "your language if you pick one."},
    "betaterms": {"fr": "Les conditions pour tester les bêtas de Raye Linux : ce qu'une bêta "
                        "peut faire, ce que nous demandons, et comment partir.",
                  "en": "The terms for testing Raye Linux betas: what a beta can do, what we "
                        "ask, and how to leave."},
    "notice": {"fr": "Qui publie rayelinux.com, où il est hébergé et comment signaler un "
                     "problème.",
               "en": "Who publishes rayelinux.com, where it is hosted and how to report a "
                     "problem."},
    "licenses": {"fr": "Les licences des composants de Raye Linux, et les marques.",
                 "en": "The licenses of Raye Linux's parts, and the trademarks."},
}


def legal_paths(site, lang):
    keys = ("privacy", "terms", "cookies", "notice", "licenses", "download", "betaterms", "rules", "join",
            "community")
    return {k: site.path(k, lang) for k in keys}


def legal(site, lang, key):
    paths = legal_paths(site, lang)
    if key in LV.PAGES:
        sections, summary = LV.PAGES[key]
        inner = legal_text.render(sections, summary, lang, paths, updated=LV.UPDATED,
                                  version=LV.VERSION, words=LV.WORDS, note=LV.DRAFT)
        title = (LV.TITLES.get(key) or legal_text.TITLES[key])[lang]
    else:
        inner = legal_text.body(key, lang, paths)
        title = legal_text.TITLES[key][lang]
    main = f"""<header class="page-head">
<p class="eyebrow">{LEGAL_EYEBROW[lang]}</p>
<h1>{title}</h1>
</header>
<div class="article prose-v1 legal-v1">
{inner.strip()}
</div>"""
    return site.page(lang, key, f"{title} · Raye Linux", LEGAL_DESCRIPTION[key][lang], main)


# ---------------------------------------------------------------- shared pages

def roadmap_words(page, lang):
    for old, new in J.ROADMAP_V1_WORDS[lang]:
        if old not in page:
            raise SystemExit("site_v1_join_text.ROADMAP_V1_WORDS: %r is no longer on the "
                             "roadmap; remove or update it" % old)
        page = page.replace(old, new)
    return page


def borrowed(site, lang, key, html_page, description):
    """A live-site page (roadmap, source) in the V1 shell: its <main> is
    taken as it is, so the list it shows is built in one place only."""
    m = re.search(r'<main id="main"( class="[^"]*")?>\n(.*)\n</main>', html_page, re.S)
    inner = m.group(2)
    # the live pages carry their own heading levels and classes; the V1 shell
    # gives them a reading width instead of a card
    inner = inner.replace('<article class="prose card">', '<article class="prose-v1 borrowed">')
    cls = m.group(1) or ""
    title = re.search(r"<title>([^<]*)</title>", html_page).group(1)
    main = f'<div class="borrowed-wrap"><div{cls}>\n{inner}\n</div></div>'
    return site.page(lang, key, title, description, main)
