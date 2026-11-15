#!/usr/bin/env python3
"""Writes the static pages of rayelinux.com, French and English, from one
template so the two languages never drift apart.

    python3 tools/build_pages.py

    python3 tools/build_pages.py --release /srv/publish/release/0.1-beta/release.json

Output: site/fr/... and site/en/... (committed), plus site/index.html, the
bare name, which has no language and sends the visitor to /fr/ or /en/. The download pages take the
file name, size and checksum from tools/release.json; --release copies
them there from the release-files output of the iso repo first."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import legal_text  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
URL = "https://rayelinux.com"
# the community server; a permanent invite to #welcome
DISCORD = "https://discord.gg/TrxhUkabyB"
RELEASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "release.json")

# The download pages are built and tested, but they go online with the image:
# their mirrors do not answer yet. Until then deploy/not-yet-public keeps them
# off the server and no other page links to them. Flip both together.
DOWNLOAD_LIVE = True

# The V1 site (tools/site_v1.py, text in tools/site_v1_text.py) is built
# next to the coming-soon page, in site-v1/, until the 1.0 image is out.
# At launch it takes site/ over: flip this with DOWNLOAD_LIVE, after the
# steps of the site plan (measures redone, screenshots taken).
V1_LIVE = False

# The GitHub mirror needs the Raye-Linux/releases repository to be public.
# Until it is, the page offers dl.rayelinux.com only, and no step mentions parts.
GITHUB_MIRROR = False

PATHS = {
    "fr": {"home": "/fr/", "privacy": "/fr/confidentialite/", "download": "/fr/telecharger/",
           "terms": "/fr/conditions/", "notice": "/fr/mentions-legales/",
           "licenses": "/fr/licences/", "source": "/fr/code-source/"},
    "en": {"home": "/en/", "privacy": "/en/privacy/", "download": "/en/download/",
           "terms": "/en/terms/", "notice": "/en/legal/", "licenses": "/en/licenses/",
           "source": "/en/source/"},
}

GLOBE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
         'aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3c-2.6 2.6-2.6 15.4 0 18M12 3c2.6 2.6 2.6 15.4 0 18"/></svg>')

CHECK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
         'aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9.5"/>'
         '<path d="M7.8 12.3l2.8 2.8 5.6-5.8"/></svg>')

T = {
    "fr": {
        "description": "Raye Linux arrive : un bureau familier, élégant et sûr. "
                       "Inscrivez-vous pour être prévenu du lancement.",
        "skip": "Aller à l'inscription",
        "brand_label": "Raye Linux, accueil",
        "switch": "English",
        "switch_lang": "en",
        "switch_label": "Read this page in English",
        "signup_title": "Soyez prévenu du lancement",
        "signup_hint": "Un courriel au lancement, rien de plus. Pas de publicité, et votre "
                       "adresse n'est jamais vendue ni partagée.",
        "email_label": "Adresse courriel",
        "email_placeholder": "vous@exemple.com",
        "button": "M'inscrire",
        "consent": "J'accepte de recevoir un courriel au lancement de Raye Linux.",
        "required": "(obligatoire)",
        "hp": "Laissez ce champ vide",
        "small": "Vous recevrez d'abord un courriel pour confirmer votre adresse. Détails "
                 "dans la <a href=\"/fr/confidentialite/\">politique de confidentialité</a>.",
        "privacy": "Confidentialité",
        "download": "Télécharger",
        "rights": "© 2026 Raye Linux",
        "privacy_title": "Politique de confidentialité",
    },
    "en": {
        "description": "Raye Linux is coming: a familiar, polished and secure desktop. "
                       "Sign up to hear when it launches.",
        "skip": "Skip to signup",
        "brand_label": "Raye Linux, home",
        "switch": "Français",
        "switch_lang": "fr",
        "switch_label": "Lire cette page en français",
        "signup_title": "Hear about the launch",
        "signup_hint": "One email at launch, nothing more. No ads, and your address is "
                       "never sold or shared.",
        "email_label": "Email address",
        "email_placeholder": "you@example.com",
        "button": "Sign me up",
        "consent": "I agree to get an email when Raye Linux launches.",
        "required": "(required)",
        "hp": "Leave this field empty",
        "small": "You'll first get an email to confirm your address. Details in the "
                 "<a href=\"/en/privacy/\">privacy policy</a>.",
        "privacy": "Privacy",
        "download": "Download",
        "rights": "© 2026 Raye Linux",
        "privacy_title": "Privacy policy",
    },
}

# the privacy policy lives in legal_text.py with the other legal pages
PRIVACY = {lang: legal_text.body("privacy", lang, PATHS[lang]) for lang in PATHS}


DOWNLOAD = {
    "fr": {
        "title": "Télécharger Raye Linux",
        "description": "Téléchargez la bêta de Raye Linux : l'image ISO, sa somme de contrôle, "
                       "comment la vérifier et l'écrire sur une clé USB.",
        "accept_title": "Avant de télécharger : c'est une bêta publique",
        "accept_items": [
            "Raye Linux 0.5 est une version bêta. Elle peut contenir beaucoup de bugs, planter "
            "et, dans de rares cas, faire perdre des données.",
            "L'installation peut effacer tout le disque choisi. Sauvegardez vos fichiers "
            "importants avant d'installer, et préférez un PC de test ou une machine virtuelle.",
            "Le logiciel est fourni « tel quel », sans aucune garantie, comme le prévoient ses "
            "licences libres. Dans toute la mesure permise par la loi, Raye Linux et ses "
            "contributeurs ne sont pas responsables des dommages, pertes de données ou autres "
            "problèmes liés à son téléchargement, son installation ou son utilisation.",
            "Vous l'installez et l'utilisez à vos propres risques, et vous êtes responsable de "
            "l'ordinateur sur lequel vous le faites.",
            "La bêta publique dure environ une à deux semaines, avant la version 1.0.",
            "En téléchargeant, vous acceptez les "
            "<a href=\"/fr/conditions/\">conditions d'utilisation</a>.",
        ],
        "accept_check": "Je confirme avoir lu ces avertissements, avoir sauvegardé mes données "
                        "et accepter d'utiliser cette bêta à mes propres risques.",
        "accept_go": "J'accepte, télécharger l'ISO",
        "accept_close": "Annuler",
        "status": "Bêta publique",
        "get_title": "Télécharger",
        "lede": "L'image de Raye Linux, à écrire sur une clé USB pour l'essayer ou l'installer. "
                "Si quelque chose ne marche pas, écrivez-moi.",
        "file": "Image ISO",
        "kind": "ISO 64 bits, démarrage UEFI",
        "get": "Télécharger l'ISO",
        "mirror": "Miroir GitHub",
        "mirror_note": "Sur GitHub, l'image est coupée en deux morceaux (limite de 2 Go par "
                       "fichier). Recollez-les avant de la vérifier.",
        "sha": "SHA-256",
        "sums": "SHA256SUMS",
        "sig": "Signature",
        "key": "Clé publique",
        "fingerprint": "Empreinte de la clé",
        "notes": "Notes de version",
        "verify": "Vérifier le téléchargement",
        "verify_steps": [
            ("Recollez les morceaux, si vous avez pris le miroir GitHub :", "join"),
            ("Vérifiez que la liste des sommes vient bien de Raye Linux. "
             "La commande doit afficher « Good signature » :", "gpg"),
            ("Vérifiez l'image. La commande doit afficher « OK » :", "sum"),
        ],
        "join_other": "Dans une invite de commandes :",
        "usb": "Créer une clé USB",
        "usb_items": [
            ("Rufus", "choisissez l'ISO et, quand il le demande, écrivez-la en <strong>mode "
                      "image DD</strong>. Le mode ISO donne une clé qui ne démarre pas."),
            ("balenaEtcher", "choisissez l'ISO, puis la clé, puis Flash."),
            ("dd", "remplacez <code>sdX</code> par votre clé et vérifiez deux fois avec "
                   "<code>lsblk</code> : tout ce qu'elle contient sera effacé."),
        ],
        "usb_boot": "Démarrez ensuite l'ordinateur sur la clé, souvent avec F12, F11, F8 ou "
                    "Échap à l'allumage.",
        "needs": "Configuration minimale",
        "needs_items": [
            "Un processeur Intel ou AMD 64 bits, démarrage en mode UEFI",
            "4 Go de mémoire, 8 Go conseillés",
            "25 Go d'espace disque libre",
            "Une clé USB de 8 Go ou plus",
            "Démarrage sécurisé (Secure Boot) et puce TPM pris en charge, sans être obligatoires",
        ],
        "known": "Problèmes connus de la bêta",
        "known_items": [
            "Le terminal, l'outil de capture et quelques boîtes de dialogue sont aux couleurs "
            "de Raye, mais pas encore redessinés en applis Raye.",
            "Les programmes .exe : le premier lancement prend quelques secondes et tous ne fonctionnent pas.",
            "Hors ligne, les Paramètres indiquent que les mises à jour n'ont pas pu être vérifiées.",
        ],
        "bug": "Signaler un problème",
        "bug_text": "Dites-moi quel ordinateur vous avez, ce que vous avez fait, ce que vous "
                    "attendiez et ce qui s'est passé. Une photo de l'écran aide beaucoup.",
        "bug_issue": "Le signaler sur Discord, dans #bugs",
        "bug_mail": "Ou écrivez à",
    },
    "en": {
        "title": "Download Raye Linux",
        "description": "Download the Raye Linux beta: the ISO image, its checksum, how to "
                       "check it and write it to a USB stick.",
        "accept_title": "Before you download: this is a public beta",
        "accept_items": [
            "Raye Linux 0.5 is a beta. It can have many bugs, crash and, in rare cases, "
            "lose data.",
            "Installing can erase the whole disk you pick. Back up your important files "
            "before you install, and prefer a test PC or a virtual machine.",
            "The software is provided “as is”, without any warranty, as its free licenses "
            "say. To the fullest extent the law allows, Raye Linux and its contributors are "
            "not liable for any damage, data loss or other problem that comes from "
            "downloading, installing or using it.",
            "You install and use it at your own risk, and you are responsible for the "
            "computer you do it on.",
            "The public beta runs for about one to two weeks, before version 1.0.",
            "By downloading, you accept the "
            "<a href=\"/en/terms/\">terms of use</a>.",
        ],
        "accept_check": "I have read these warnings, backed up my data and agree to use this "
                        "beta at my own risk.",
        "accept_go": "I agree, download the ISO",
        "accept_close": "Cancel",
        "status": "Public beta",
        "get_title": "Download",
        "lede": "The Raye Linux image, to write to a USB stick to try it or install it. If "
                "something doesn't work, write to me.",
        "file": "ISO image",
        "kind": "64-bit ISO, UEFI start",
        "get": "Download the ISO",
        "mirror": "GitHub mirror",
        "mirror_note": "On GitHub the image comes in two parts (2 GB limit per file). Put "
                       "them back together before checking it.",
        "sha": "SHA-256",
        "sums": "SHA256SUMS",
        "sig": "Signature",
        "key": "Public key",
        "fingerprint": "Key fingerprint",
        "notes": "Release notes",
        "verify": "Check the download",
        "verify_steps": [
            ("Put the parts back together, if you took the GitHub mirror:", "join"),
            ("Check that the checksum list really comes from Raye Linux. "
             "It must say “Good signature”:", "gpg"),
            ("Check the image. It must say “OK”:", "sum"),
        ],
        "join_other": "In a Command Prompt:",
        "usb": "Make a USB stick",
        "usb_items": [
            ("Rufus", "choose the ISO and, when asked, write it in <strong>DD image "
                      "mode</strong>. ISO mode gives a stick that doesn't start."),
            ("balenaEtcher", "choose the ISO, then the stick, then Flash."),
            ("dd", "replace <code>sdX</code> with your stick and check twice with "
                   "<code>lsblk</code>: everything on it will be erased."),
        ],
        "usb_boot": "Then start the computer from the stick, often with F12, F11, F8 or Esc "
                    "at power on.",
        "needs": "What you need",
        "needs_items": [
            "A 64-bit Intel or AMD processor, starting in UEFI mode",
            "4 GB of memory, 8 GB recommended",
            "25 GB of free disk space",
            "A USB stick of 8 GB or more",
            "Secure Boot and the TPM chip are supported, not required",
        ],
        "known": "Known issues in the beta",
        "known_items": [
            "The terminal, the screenshot tool and a few dialogs wear Raye's colors but are "
            "not redrawn as Raye apps yet.",
            ".exe programs: the first start takes a few seconds, and not all of them run.",
            "Offline, Settings says updates could not be checked.",
        ],
        "bug": "Report a problem",
        "bug_text": "Tell me what computer you have, what you did, what you expected and what "
                    "happened. A photo of the screen helps a lot.",
        "bug_issue": "Report it on Discord, in #bugs",
        "bug_mail": "Or write to",
    },
}

FINGERPRINT = "EA73 69D4 C3A3 10B2 DF3D  FC16 D3AA 2E62 5DDE 161E"
MONTHS = {
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
           "septembre", "octobre", "novembre", "décembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}


def release_info():
    with open(RELEASE, encoding="utf-8") as f:
        return json.load(f)


def take_release(path):
    """Copies what the page needs from release-files' release.json."""
    with open(path, encoding="utf-8") as f:
        info = json.load(f)
    keep = {k: info[k] for k in ("release", "title", "date", "iso", "size", "sha256", "urls")}
    keep["parts"] = [p["name"] for p in info["parts"]]
    with open(RELEASE, "w", encoding="utf-8") as f:
        json.dump(keep, f, indent=2, ensure_ascii=False)
        f.write("\n")


def size_text(lang, size):
    text = f"{size / 1e9:.1f}"
    return (text.replace(".", ",") + " Go") if lang == "fr" else text + " GB"


def date_text(lang, iso_date):
    y, m, d = (int(x) for x in iso_date.split("-"))
    if lang == "fr":
        return f"{'1er' if d == 1 else d} {MONTHS['fr'][m - 1]} {y}"
    return f"{MONTHS['en'][m - 1]} {d}, {y}"


def pre(text):
    return f'<pre class="code"><code>{text}</code></pre>'


def download(lang, shell=None):
    """The download page. `shell` is the V1 site, which brings its own
    head, top bar and footer; without it the page wears the coming-soon ones."""
    t, d = T[lang], DOWNLOAD[lang]
    page_head = (shell.head if shell else head)(lang, 'download', d['get_title'] + ' · Raye Linux',
                                                 d['description'])
    page_top = shell.topbar(lang, 'download') if shell else topbar(lang, 'download')
    page_foot = shell.footer(lang) if shell else footer(lang)
    info = release_info()
    urls, iso = info["urls"], info["iso"]
    title = info["title"].replace("Beta", "Bêta") if lang == "fr" else info["title"]
    # the version and "Beta" stay on one line
    title = title.replace(" B", "\u00a0B")
    folder = urls["r2_folder"]
    parts = " ".join(info["parts"])
    commands = {
        "join": pre(f"cat {parts} &gt; {iso}")
                + f'<p class="small">{d["join_other"]}</p>'
                + pre(f"copy /b {' + '.join(info['parts'])} {iso}"),
        "gpg": pre("gpg --import raye-archive.asc\ngpg --verify SHA256SUMS.asc SHA256SUMS"),
        "sum": pre("sha256sum --check --ignore-missing SHA256SUMS"),
    }
    steps = "\n".join(f"<li><p>{text}</p>\n{commands[key]}</li>"
                      for text, key in d["verify_steps"]
                      if GITHUB_MIRROR or key != "join")
    mirror = (f'<a class="btn btn-quiet" href="{urls["github"]}">{d["mirror"]}</a>'
              if GITHUB_MIRROR else "")
    mirror_note = f'<p class="small">{d["mirror_note"]}</p>' if GITHUB_MIRROR else ""
    usb = "\n".join(f"<li><strong>{name}</strong> : {text}</li>" if lang == "fr"
                    else f"<li><strong>{name}</strong>: {text}</li>"
                    for name, text in d["usb_items"])
    needs = "\n".join(f"<li>{x}</li>" for x in d["needs_items"])
    known = "\n".join(f"<li>{x}</li>" for x in d["known_items"])
    accept_items = "\n".join(f"<li>{x}</li>" for x in d["accept_items"])
    notes = f"release-notes-{info['release']}{'.fr' if lang == 'fr' else ''}.md"
    return f"""{page_head}
<body{' class="v1"' if shell else ''}>
<a class="skip-link" href="#main">{'Aller au contenu' if lang == 'fr' else 'Skip to content'}</a>
{page_top}
<main id="main" class="download wrap">
<header class="dl-head">
<p class="status"><span class="dot" aria-hidden="true"></span>{d['status']}</p>
<h1>{d['get_title']} {title}</h1>
<p class="lede">{d['lede']}</p>
</header>

<section class="dl-file card" aria-labelledby="file-title">
<div class="dl-file-top">
<div>
<h2 id="file-title">{iso}</h2>
<p class="dl-meta">{size_text(lang, info['size'])} · {d['kind']} · {date_text(lang, info['date'])}</p>
</div>
<div class="dl-actions">
<a class="btn btn-accent" href="#accept" data-accept>{d['get']}</a>
{mirror}
</div>
</div>
{mirror_note}
<dl class="dl-facts">
<div><dt>{d['sha']}</dt><dd><code class="hash">{info['sha256']}</code></dd></div>
<div><dt>{d['fingerprint']}</dt><dd><code>{FINGERPRINT}</code></dd></div>
</dl>
<ul class="dl-links">
<li><a href="{folder}SHA256SUMS">{d['sums']}</a></li>
<li><a href="{folder}SHA256SUMS.asc">{d['sig']}</a></li>
<li><a href="{folder}raye-archive.asc">{d['key']}</a></li>
<li><a href="{folder}{notes}">{d['notes']}</a></li>
</ul>
</section>

<section id="accept" class="card dl-card dl-accept" aria-labelledby="accept-title">
<h2 id="accept-title">{d['accept_title']}</h2>
<ul class="plain">
{accept_items}
</ul>
<label class="dl-check"><input type="checkbox" id="accept-check"> <span>{d['accept_check']}</span></label>
<p class="dl-accept-actions"><a class="btn btn-accent dl-go" href="{urls['r2']}">{d['accept_go']}</a>
<button type="button" class="btn btn-quiet dl-cancel" hidden>{d['accept_close']}</button></p>
</section>

<div class="dl-grid">
<section class="card dl-card" aria-labelledby="verify-title">
<h2 id="verify-title">{d['verify']}</h2>
<ol class="steps">
{steps}
</ol>
</section>

<section class="card dl-card" aria-labelledby="usb-title">
<h2 id="usb-title">{d['usb']}</h2>
<ul class="plain">
{usb}
</ul>
{pre(f"sudo dd if={iso} of=/dev/sdX bs=4M conv=fsync status=progress")}
<p>{d['usb_boot']}</p>
</section>

<section class="card dl-card" aria-labelledby="needs-title">
<h2 id="needs-title">{d['needs']}</h2>
<ul class="plain">
{needs}
</ul>
</section>

<section class="card dl-card" aria-labelledby="known-title">
<h2 id="known-title">{d['known']}</h2>
<ul class="plain">
{known}
</ul>
</section>

<section class="card dl-card dl-wide" aria-labelledby="bug-title">
<h2 id="bug-title">{d['bug']}</h2>
<p>{d['bug_text']}</p>
<p><a href="{DISCORD}" rel="noopener">{d['bug_issue']}</a> · {d['bug_mail']}
<a href="mailto:bonjour@rayelinux.com">bonjour@rayelinux.com</a></p>
</section>
</div>
</main>
{page_foot}
</body>
</html>
"""


def x_default(page):
    """The address for a browser in neither language: the bare name, which
    picks one, for the home page; the English page for the others."""
    return "/" if page == "home" else PATHS["en"][page]


def head(lang, page, title, description):
    other = "en" if lang == "fr" else "fr"
    here, there = PATHS[lang][page], PATHS[other][page]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141318">
<link rel="canonical" href="{URL}{here}">
<link rel="alternate" hreflang="{lang}" href="{URL}{here}">
<link rel="alternate" hreflang="{other}" href="{URL}{there}">
<link rel="alternate" hreflang="x-default" href="{URL}{x_default(page)}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Raye Linux">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{URL}{here}">
<meta property="og:locale" content="{'fr_CA' if lang == 'fr' else 'en_CA'}">
<meta property="og:image" content="{URL}/assets/shots/start-{lang}-944.jpg">
<meta property="og:image:width" content="944">
<meta property="og:image:height" content="450">
<script src="/assets/app.js" defer></script>
<script src="/assets/support.js" defer></script>
</head>"""


def topbar(lang, page):
    t, h = T[lang], HOME[lang]
    other = t["switch_lang"]
    # on the home page the links stay on the page; elsewhere they lead back to it
    base = "" if page == "home" else PATHS[lang]["home"]
    links = "\n".join(f'<li><a href="{base}#{key}">{label}</a></li>'
                      for key, label in h["nav"])
    if DOWNLOAD_LIVE:
        cta = f'<a class="btn btn-accent btn-small" href="{PATHS[lang]["download"]}">{t["download"]}</a>'
    else:
        cta = f'<a class="btn btn-accent btn-small" href="{base}#signup">{h["nav_signup"]}</a>'
    return f"""<header class="topbar">
<div class="topbar-in">
<a class="brand" href="{PATHS[lang]['home']}" aria-label="{t['brand_label']}">
<img src="/assets/raye-mark.svg" alt="" width="36" height="16"><span>Raye Linux</span></a>
<nav class="nav" aria-label="{h['nav_label']}">
<ul>
{links}
</ul>
</nav>
<div class="topbar-end">
<a class="lang-switch" href="{PATHS[other][page]}" hreflang="{other}" lang="{other}"
   data-set-lang="{other}" aria-label="{t['switch_label']}">{GLOBE}<span>{t['switch']}</span></a>
<a class="btn btn-quiet btn-small" href="{DISCORD}" rel="noopener">Discord</a>
{cta}
</div>
</div>
</header>"""


FOOTER = {
    "fr": {"made": "Fait au Québec par une seule personne.", "site": "Raye Linux",
           "shots": "Captures", "inside": "Ce qu'il y a dedans", "questions": "Questions",
           "help": "Aide", "legal": "Légal", "licenses": "Licences"},
    "en": {"made": "Made in Québec by one person.", "site": "Raye Linux",
           "shots": "Screenshots", "inside": "What's in it", "questions": "Questions",
           "help": "Help", "legal": "Legal", "licenses": "Licenses"},
}


def footer(lang, note=""):
    t, f, p = T[lang], FOOTER[lang], PATHS[lang]
    note = f'\n<p class="footer-note">{note}</p>' if note else ""
    download = (f'<li><a href="{p["download"]}">{t["download"]}</a></li>\n'
                if DOWNLOAD_LIVE else "")
    return f"""<footer class="footer">
<div class="wrap">
<div class="footer-cols">
<div class="footer-brand">
<img src="/assets/raye-mark.svg" alt="" width="36" height="16">
<p>{t['rights']}<br>{f['made']}</p>
</div>
<div>
<h2>{f['site']}</h2>
<ul>
{download}<li><a href="{p['home']}#captures">{f['shots']}</a></li>
<li><a href="{p['home']}#nouveautes">{f['inside']}</a></li>
<li><a href="{p['home']}#questions">{f['questions']}</a></li>
</ul>
</div>
<div>
<h2>{f['help']}</h2>
<ul>
<li><a href="{DISCORD}" rel="noopener">Discord</a></li>
<li><a href="mailto:bonjour@rayelinux.com">bonjour@rayelinux.com</a></li>
</ul>
</div>
<div>
<h2>{f['legal']}</h2>
<ul>
<li><a href="{p['privacy']}">{t['privacy']}</a></li>
<li><a href="{p['terms']}">{legal_text.TITLES['terms'][lang]}</a></li>
<li><a href="{p['notice']}">{legal_text.TITLES['notice'][lang]}</a></li>
<li><a href="{p['licenses']}">{f['licenses']}</a></li>
<li><a href="{p['source']}">{SOURCE[lang]['title']}</a></li>
</ul>
</div>
</div>{note}
</div>
</footer>"""


# The screenshots were taken on the test PC (the test VM) with the beta of
# 2026-11-08, one session in English and one in French. Each one exists in
# assets/shots/ as <name>-<lang>-1600.webp, -800.webp and -1600.jpg; the hero
# is the French or English desktop cropped to the top of the Start menu
# (search box and pinned apps), 944x450 at actual size, nothing scaled up.
SHOT_DATE = {"fr": "8 novembre 2026", "en": "November 8, 2026"}

HOME = {
    "fr": {
        "title": "Raye Linux · Bêta publique",
        "nav_label": "Sur cette page",
        "nav": [("captures", "Captures"), ("nouveautes", "Dedans"),
                ("questions", "Questions")],
        "nav_signup": "M'inscrire",
        "status": "Bêta publique",
        "h1": "Un bureau que vous savez déjà utiliser.",
        "lede": "Raye Linux est un système gratuit pour votre PC. La barre des tâches, le "
                "menu Démarrer et les Paramètres sont là où vous les cherchez, donc pas "
                "besoin de tout réapprendre. La bêta publique vient de sortir et dure une "
                "à deux semaines avant la 1.0. Il reste des bugs, c'est le but de la bêta.",
        "cta": "Télécharger la bêta",
        "cta_more": "Voir les captures",
        "facts": ["Gratuit", "En français et en anglais", "Prévu pour Secure Boot et TPM"],
        "byline": "Fait par une seule personne, au Québec. Bêta publiée le {date}.",
        "hero_alt": "Le haut du menu Démarrer de Raye : la barre de recherche, puis onze "
                    "applications épinglées, dont Fichiers, Firefox, Store, Paramètres, "
                    "Terminal et Calculatrice.",
        "hero_caption": "Le haut du menu Démarrer. Toutes les images de cette page "
                        "sont des captures de Raye, prises sur un PC de test le "
                        "{date}.",
        "shots_title": "Faites le tour",
        "shots_lede": "Quatre écrans de la version de test, sans retouche. Cliquez sur "
                      "une image pour l'ouvrir en grand.",
        "shots_label": "Écrans",
        "shots": [
            ("settings", "Paramètres",
             "Tout est dans une seule fenêtre, rangé comme vous le chercheriez : Système, "
             "Réseau, Personnalisation, Comptes. La recherche trouve un réglage par son nom.",
             "La fenêtre Paramètres : le compte en haut, une barre de recherche et douze "
             "catégories comme Système, Réseau et Internet, Personnalisation, et "
             "Confidentialité et sécurité."),
            ("files", "Fichiers",
             "Vos dossiers à gauche, la vue détaillée par défaut, et une vue scindée quand "
             "il faut déplacer des fichiers d'un endroit à l'autre.",
             "L'application Fichiers ouverte sur le dossier personnel : Bureau, Documents, "
             "Téléchargements, Musique, Images et Vidéos, avec la liste des emplacements à "
             "gauche."),
            ("store", "Store",
             "Les applications s'installent en un clic et se mettent à jour avec le "
             "système. Beaucoup d'applications courantes y sont déjà.",
             "L'application Store : une application mise en avant en haut et une rangée "
             "d'applications gratuites populaires en dessous."),
            ("lock", "Verrouillage",
             "Une touche, votre mot de passe, et vous retrouvez vos fenêtres comme vous "
             "les aviez laissées. Sur cette capture, la date est encore en anglais : "
             "c'est noté, et ce sera corrigé avant la sortie.",
             "L'écran de verrouillage : une grande horloge et la date sur le fond violet "
             "de Raye."),
        ],
        "coming_title": "Ce qu'il y a dedans",
        "coming_lede": "Ce qui marche déjà dans la bêta. Le reste se peaufine d'ici la 1.0.",
        "coming": [
            ("Les programmes .exe",
             "Les installateurs .exe s'ouvrent d'un double-clic et le programme arrive dans "
             "le menu Démarrer comme n'importe quelle application. Tous ne fonctionnent pas "
             "encore, et le premier lancement prend quelques secondes."),
            ("Des mises à jour sans interruption",
             "La plupart s'installent pendant que vous travaillez, sans redémarrage. "
             "Celles qui touchent au système lui-même, comme le noyau ou les pilotes, "
             "attendent que vous choisissiez de redémarrer."),
            ("Secure Boot et chiffrement",
             "Raye démarre sur un PC où Secure Boot est activé. Si vous chiffrez le disque, la puce "
             "TPM le déverrouille au démarrage sur votre PC ; branché sur un autre, il "
             "reste illisible."),
            ("En français et en anglais",
             "Démarrer, les Paramètres, Fichiers et le Store sont déjà traduits. Vous "
             "choisissez la langue à l'installation."),
        ],
        "faq_title": "Questions",
        # The download page is online only with DOWNLOAD_LIVE.
        "full_list": {False: "La liste complète sera sur la page de téléchargement, au lancement.",
                      True: "La liste complète est sur la page de téléchargement."},
        "faq": [
            ("Qui fait Raye Linux ?",
             "Une seule personne, techoraye, au Québec. Raye a commencé en 2026 parce que "
             "je voulais un Linux qu'on prend en main sans tout réapprendre. La bêta publique "
             "est sortie le 14 novembre 2026. Pour me parler, le plus simple est le serveur "
             "Discord, ou bonjour@rayelinux.com."),
            ("C'est gratuit ?",
             "Oui. Raye Linux ne coûte rien à télécharger ni à utiliser, et il n'y a "
             "aucune publicité dedans."),
            ("Sur quoi c'est basé ?",
             "Raye Linux est basé sur Ubuntu 26.04 LTS. Cela lui donne des années de "
             "correctifs de sécurité et des pilotes pour la plupart des PC. Le bureau, les "
             "applications et les réglages par-dessus sont les nôtres."),
            ("Mes programmes vont-ils fonctionner ?",
             "Beaucoup de programmes .exe s'installent et s'ouvrent d'un double-clic, et le "
             "Store a une bonne partie des applications gratuites habituelles. Certains "
             "programmes ne fonctionnent pas encore. S'il vous en manque un, écrivez-moi "
             "son nom : c'est comme ça que je décide quoi régler en premier."),
            ("Quel PC faut-il ?",
             "Un PC Intel ou AMD 64 bits qui démarre en mode UEFI, avec au moins 4 Go de "
             "mémoire. Une fois démarré, sans rien d'ouvert, Raye en utilise environ "
             "1,2 Go (mesuré avec deux écrans) : le reste est pour vos applis, et 8 Go "
             "valent mieux pour beaucoup d'onglets ou les jeux. {full_list}"),
            ("Et la version 1.0 ?",
             "Elle arrive après la bêta, d'ici une à deux semaines. Laissez votre courriel "
             "si vous voulez que je vous écrive le jour de sa sortie."),
        ],
        "join_title": "La suite, si vous vous inscrivez",
        "join_steps": [
            "Vous recevez un courriel pour confirmer votre adresse.",
            "Le jour de la sortie de la 1.0, vous recevez un deuxième courriel.",
            "C'est tout. Chaque courriel a un lien pour vous désinscrire.",
        ],
        "shots_note": "Captures : version de test du {date}, sur un PC de test.",
        "note_title": "Un mot",
        "note": [
            "Je fais Raye pour qu'on puisse changer de système sans réapprendre son "
            "ordinateur. La barre des tâches, Démarrer et les Paramètres doivent être là "
            "où la main va déjà, et quand ce n'est pas le cas, c'est un bogue.",
            "La bêta publique est sortie le 14 novembre. Elle a encore des défauts, et "
            "c'est justement pour ça qu'elle existe. Si quelque chose cloche chez vous, "
            "dites-le sur le Discord, je lis tout.",
        ],
        "log_title": "Derniers changements",
        "log_lede": "Tirés de l'historique du code, du plus récent au plus ancien.",
    },
    "en": {
        "title": "Raye Linux · Public beta",
        "nav_label": "On this page",
        "nav": [("captures", "Screenshots"), ("nouveautes", "What's in it"),
                ("questions", "Questions")],
        "nav_signup": "Sign up",
        "status": "Public beta",
        "h1": "A desktop you already know how to use.",
        "lede": "Raye Linux is a free system for your PC. The taskbar, the Start menu and "
                "Settings sit where you expect them, so there's nothing to relearn. The "
                "public beta just came out and runs for one to two weeks before 1.0. "
                "There are still bugs, that's what the beta is for.",
        "cta": "Download the beta",
        "cta_more": "See the screenshots",
        "facts": ["Free", "In English and French", "Made for Secure Boot and TPM"],
        "byline": "Made by one person in Québec. Beta out on {date}.",
        "hero_alt": "The top of the Raye Start menu: the search box, then eleven pinned "
                    "apps, among them Files, Firefox, Store, Settings, Terminal and "
                    "Calculator.",
        "hero_caption": "The top of the Start menu. Every picture on this page is a "
                        "screenshot of Raye, taken on a test PC on {date}.",
        "shots_title": "Have a look around",
        "shots_lede": "Four screens from the test version, not touched up. Click a picture "
                      "to open it full size.",
        "shots_label": "Screens",
        "shots": [
            ("settings", "Settings",
             "Everything in one window, sorted the way you'd look for it: System, Network, "
             "Personalization, Accounts. The search box finds a setting by name.",
             "The Settings window: the account at the top, a search box, and twelve "
             "categories such as System, Network & internet, Personalization and "
             "Privacy & security."),
            ("files", "Files",
             "Your folders on the left, a details view by default, and a split view when "
             "you need to move things from one place to another.",
             "The Files app open on the home folder: Desktop, Documents, Downloads, Music, "
             "Pictures and Videos, with the list of places on the left."),
            ("store", "Store",
             "Apps install in one click and update along with the system. Plenty of the "
             "usual apps are already there.",
             "The Store app: a featured app at the top and a row of popular free apps "
             "below it."),
            ("lock", "Lock screen",
             "Press a key, type your password, and every open app is where you left "
             "it.",
             "The lock screen: a large clock and the date over the purple Raye "
             "background."),
        ],
        "coming_title": "What's in it",
        "coming_lede": "What already works in the beta. The rest gets polished before 1.0.",
        "coming": [
            (".exe programs",
             ".exe installers open with a double-click, and the program lands in the Start "
             "menu like any other app. Not all of them run yet, and the first start takes "
             "a few seconds."),
            ("Updates that don't interrupt you",
             "Most install while you work, with no restart. The ones that touch the "
             "system itself, like the kernel or drivers, wait until you choose to "
             "restart."),
            ("Secure Boot and encryption",
             "Raye starts on a PC with Secure Boot turned on. If you encrypt the disk, the TPM chip "
             "unlocks it at startup on your PC; put it in another one and it can't be "
             "read."),
            ("In English and French",
             "Start, Settings, Files and the Store are already translated. You pick the "
             "language when you install."),
        ],
        "faq_title": "Questions",
        "full_list": {False: "The full list will be on the download page at launch.",
                      True: "The full list is on the download page."},
        "faq": [
            ("Who makes Raye Linux?",
             "One person, techoraye, in Québec. I started Raye in 2026 because I wanted a "
             "Linux you can pick up without relearning everything. The public beta came out "
             "on November 14, 2026. The easiest way to reach me is the Discord server, or "
             "bonjour@rayelinux.com."),
            ("Is it free?",
             "Yes. Raye Linux costs nothing to download or use, and there are no ads in "
             "it."),
            ("What is it built on?",
             "Raye Linux is based on Ubuntu 26.04 LTS. That gives it years of security "
             "fixes and drivers for most PCs. The desktop, the apps and the settings on "
             "top are ours."),
            ("Will my programs still work?",
             "Many .exe programs install and open with a double-click, and the Store has "
             "a good share of the usual free apps. Some programs don't run yet. If one you "
             "need is missing, send me its name: that's how I decide what to fix first."),
            ("What kind of PC do I need?",
             "A 64-bit Intel or AMD PC that starts in UEFI mode, with at least 4 GB of "
             "memory. Once started, with nothing open, Raye uses about 1.2 GB of it "
             "(measured with two screens): the rest is for your apps, and 8 GB is better "
             "for lots of tabs or games. {full_list}"),
            ("What about 1.0?",
             "It comes after the beta, in one to two weeks. Leave your email if you want "
             "me to write you the day it's out."),
        ],
        "join_title": "What happens if you sign up",
        "join_steps": [
            "You get an email to confirm your address.",
            "When 1.0 comes out, you get a second email.",
            "That's it. Every email has a link to unsubscribe.",
        ],
        "shots_note": "Screenshots: test version of {date}, on a test PC.",
        "note_title": "A word",
        "note": [
            "I'm making Raye so that switching systems doesn't mean learning your "
            "computer all over again. The taskbar, Start and Settings should be where "
            "your hand already goes, and when they aren't, that's a bug.",
            "The public beta came out on November 14. It still has rough edges, and "
            "that's exactly why it exists. If something's off on your PC, say it on the "
            "Discord, I read everything.",
        ],
        "log_title": "Latest changes",
        "log_lede": "Taken from the code history, newest first.",
    },
}

# The "latest changes" list on the home page. Every line is a commit in one
# of the Raye repositories, dated by its author date; keep them newest first
# and rewrite the old ones out rather than letting the list grow.
CHANGES = [
    ("2026-11-08", "theme 1c0c19f",
     {"fr": "Le bouton des réglages rapides apparaît maintenant dans la barre des tâches "
            "dès la première connexion.",
      "en": "The quick settings button now shows on the taskbar at the very first "
            "sign-in."}),
    ("2026-11-07", "theme 6282497",
     {"fr": "Une fenêtre réduite perdait son bouton dans la barre, et un clic sur l'icône "
            "ouvrait une deuxième copie de l'appli. Elle le garde maintenant.",
      "en": "A minimized window lost its taskbar button, and clicking the icon started a "
            "second copy of the app. It keeps its button now."}),
    ("2026-11-07", "installer 29bd5f8",
     {"fr": "L'installateur a sa propre page Disque, et il relit le disque juste avant "
            "d'écrire : si quelque chose a changé, il s'arrête.",
      "en": "The installer has its own Disk page, and it reads the disk again just before "
            "writing: if anything changed, it stops."}),
    ("2026-11-07", "iso c88b083",
     {"fr": "Une session en français a enfin ses dossiers en français (Documents, "
            "Téléchargements, Images…) et Firefox en français.",
      "en": "A French session finally gets French folder names (Documents, "
            "Téléchargements, Images…) and Firefox in French."}),
]


# hero: up to ~760 px wide on a large screen, the full width on a phone
HERO_SIZES = "(min-width: 64rem) 944px, 94vw"
SHOT_SIZES = "(min-width: 64rem) 68vw, 94vw"


def picture(name, lang, alt, sizes, eager=False, size=(1600, 900)):
    """A screenshot as WebP in two widths, with a JPEG for older browsers."""
    base = f"/assets/shots/{name}-{lang}"
    w, h = size
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture>\n<source type="image/webp" srcset="{base}-{w // 2}.webp {w // 2}w, '
            f'{base}-{w}.webp {w}w" sizes="{sizes}">\n'
            f'<img src="{base}-{w}.jpg" alt="{alt}" width="{w}" height="{h}" '
            f'{load} decoding="async">\n</picture>')


def home(lang):
    t, h = T[lang], HOME[lang]
    date = SHOT_DATE[lang]
    facts = "\n".join(f"<li>{x}</li>" for x in h["facts"])
    tabs = "\n".join(
        f'<li><a class="shot-tab" href="#shot-{key}" id="tab-{key}" data-tab>{title}</a></li>'
        for key, title, _, _ in h["shots"])
    panels = "\n".join(f"""<figure class="shot-panel" id="shot-{key}" data-panel>
<a class="shot-frame" href="/assets/shots/{key}-{lang}-1600.webp">
{picture(key, lang, alt, SHOT_SIZES)}
</a>
<figcaption>
<h3>{title}</h3>
<p>{text}</p>
</figcaption>
</figure>""" for key, title, text, alt in h["shots"])
    coming = "\n".join(f"""<li>
<h3>{title}</h3>
<p>{text}</p>
</li>""" for title, text in h["coming"])
    faq = "\n".join(f"""<details class="qa">
<summary>{q}</summary>
<p>{a.replace("{full_list}", h["full_list"][DOWNLOAD_LIVE])}</p>
</details>""" for q, a in h["faq"])
    steps = "\n".join(f"<li>{x}</li>" for x in h["join_steps"])
    note = "\n".join(f"<p>{x}</p>" for x in h["note"])
    log = "\n".join(f"""<li>
<time datetime="{day}">{date_text(lang, day)}</time>
<p>{text[lang]}</p>
</li>""" for day, _, text in CHANGES)
    return f"""{head(lang, 'home', h['title'], t['description'])}
<body class="home">
<a class="skip-link" href="#signup">{t['skip']}</a>
{topbar(lang, 'home')}
<main id="main">
<section class="hero wrap" aria-labelledby="title">
<div class="hero-text">
<h1 id="title">{h['h1']}</h1>
<p class="lede">{h['lede']}</p>
<div class="hero-actions">
<a class="btn btn-accent" href="{PATHS[lang]['download'] if DOWNLOAD_LIVE else '#signup'}">{h['cta']}</a>
<a class="more-link" href="#captures">{h['cta_more']}</a>
</div>
<p class="byline"><strong>{release_info()['title'].replace('Raye Linux ', '')}</strong> · {h['byline'].format(date=date_text(lang, release_info()['date']))}</p>
</div>
<figure class="hero-shot">
<div class="screen">
{picture('start', lang, h['hero_alt'], HERO_SIZES, eager=True, size=(944, 450))}
</div>
<figcaption>{h['hero_caption'].format(date=date)}</figcaption>
</figure>
</section>

<section id="captures" class="band shots-band" aria-labelledby="shots-title" tabindex="-1">
<div class="wrap">
<div class="band-head">
<h2 id="shots-title">{h['shots_title']}</h2>
<p>{h['shots_lede']}</p>
</div>
<div class="shots" data-tabs>
<ul class="shot-tabs" aria-label="{h['shots_label']}">
{tabs}
</ul>
{panels}
</div>
</div>
</section>

<section id="nouveautes" class="band wrap" aria-labelledby="coming-title" tabindex="-1">
<div class="band-head">
<h2 id="coming-title">{h['coming_title']}</h2>
<p>{h['coming_lede']}</p>
</div>
<ul class="coming">
{coming}
</ul>
</section>

<section id="journal" class="band wrap journal" aria-labelledby="note-title" tabindex="-1">
<div class="author-note">
<h2 id="note-title">{h['note_title']}</h2>
{note}
<p class="signature">techoraye</p>
</div>
<div class="changes">
<h3 id="log-title">{h['log_title']}</h3>
<p class="changes-lede">{h['log_lede']}</p>
<ol class="changelog" aria-labelledby="log-title">
{log}
</ol>
</div>
</section>

<section id="questions" class="band wrap faq" aria-labelledby="faq-title" tabindex="-1">
<h2 id="faq-title">{h['faq_title']}</h2>
<div class="qa-list">
{faq}
</div>
</section>

<div class="band wrap join">
<section id="signup" class="signup card" aria-labelledby="signup-title" tabindex="-1">
<div class="signup-body">
<h2 id="signup-title">{t['signup_title']}</h2>
<p class="hint">{t['signup_hint']}</p>
<form id="signup-form" method="post" action="/api/subscribe" novalidate>
<input type="hidden" name="lang" value="{lang}">
<label class="field-label" for="email">{t['email_label']}</label>
<div class="row">
<input class="input" id="email" name="email" type="email" inputmode="email" autocomplete="email"
       required maxlength="254" spellcheck="false" autocapitalize="off"
       placeholder="{t['email_placeholder']}" aria-describedby="form-msg">
<button class="btn btn-accent" type="submit">{t['button']}</button>
</div>
<div class="checks">
<label class="check"><input type="checkbox" name="consent" value="on" required>
<span><span class="req">{t['consent']}</span> {t['required']}</span></label>
</div>
<div class="hp" aria-hidden="true"><label for="website">{t['hp']}</label>
<input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
<p id="form-msg" class="form-msg" role="status" aria-live="polite"></p>
<p class="small">{t['small']}</p>
</form>
</div>
</section>
<div class="join-next">
<h3>{h['join_title']}</h3>
<ol>
{steps}
</ol>
</div>
</div>
</main>
{footer(lang, h['shots_note'].format(date=date))}
</body>
</html>
"""


def privacy(lang):
    return legal(lang, "privacy")


def legal(lang, page):
    t = T[lang]
    title = legal_text.TITLES[page][lang]
    return f"""{head(lang, page, title + ' · Raye Linux', t['description'])}
<body>
<a class="skip-link" href="#main">{'Aller au contenu' if lang == 'fr' else 'Skip to content'}</a>
{topbar(lang, page)}
<main id="main">
<article class="prose card">
<h1>{title}</h1>
{legal_text.body(page, lang, PATHS[lang]).strip()}
</article>
</main>
{footer(lang)}
</body>
</html>
"""


# The source code page. Every repository is on GitHub and copied, commit for
# commit, to Codeberg, GitLab and our own server (plain git over HTTPS).
# GitLab reserves the names "files" and "update", so those two carry a prefix there.
REPOS = [
    ("iso", "The build of the installation image and the base packages.",
     "La fabrication de l'image d'installation et les paquets de base."),
    ("installer", "Everything from the USB stick to the first desktop.",
     "Tout ce qui se passe entre la clé USB et le premier bureau."),
    ("theme", "How Raye looks: colours, icons, taskbar, Start menu.",
     "L'apparence de Raye : couleurs, icônes, barre des tâches, menu Démarrer."),
    ("desktop", "Raye's builds of the desktop, with its patches.",
     "Les paquets du bureau, avec les correctifs de Raye."),
    ("files", "Raye Explorer, the file manager.", "L'Explorateur Raye, le gestionnaire de fichiers."),
    ("settings", "The Settings app.", "L'application Paramètres."),
    ("store", "Raye Store, for apps and games.", "Le Raye Store, pour les applis et les jeux."),
    ("update", "Raye Update, the system updates.", "Raye Update, les mises à jour du système."),
    ("apps", "Terminal, Notepad, Task Manager, Calculator and the other small apps.",
     "Terminal, Bloc-notes, Gestionnaire des tâches, Calculatrice et les autres petites applis."),
    ("archive", "Opening and extracting ZIP, 7z, RAR and other archives.",
     "L'ouverture et l'extraction des ZIP, 7z, RAR et autres archives."),
    # the Windows layer repo is left off this page until it is renamed (its
    # current name must not appear in what users read); it is public all the same
    ("account", "Raye accounts: the server and the client.", "Les comptes Raye : le serveur et le client."),
    ("kernel", "The kernel, with Raye's changes for PCs and laptops.",
     "Le noyau, avec les changements de Raye pour les PC et portables."),
    ("handbook", "The user guide.", "Le guide d'utilisation."),
    ("website", "This website.", "Ce site."),
]
GITLAB_NAME = {"files": "raye-files", "update": "raye-update"}
SOURCE = {
    "en": {"title": "Source code",
           "lead": "Raye Linux is free software. All of its code is public, mostly under the GPL; "
                   "each repository says which licence applies. It lives on GitHub and is copied to "
                   "three other places, so it stays available if one of them goes down.",
           "clone": "To get a copy, clone from any of the four, for example from our own server:",
           "where": "Where to find it", "repo": "Repository", "ours": "Raye server",
           "help": "Found a bug or want to suggest something? Tell us on "
                   "<a href=\"{discord}\" rel=\"noopener\">Discord</a> or at "
                   "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>."},
    "fr": {"title": "Code source",
           "lead": "Raye Linux est un logiciel libre. Tout son code est public, surtout sous licence GPL ; "
                   "chaque dépôt indique la sienne. Il est sur GitHub et copié à trois autres endroits, "
                   "pour rester disponible si l'un d'eux tombe.",
           "clone": "Pour en avoir une copie, clonez depuis n'importe lequel des quatre, par exemple depuis notre serveur :",
           "where": "Où le trouver", "repo": "Dépôt", "ours": "Serveur Raye",
           "help": "Un bogue, une idée ? Dites-le-nous sur "
                   "<a href=\"{discord}\" rel=\"noopener\">Discord</a> ou à "
                   "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>."},
}


def source(lang):
    t, s = T[lang], SOURCE[lang]
    rows = []
    for name, en, fr in REPOS:
        links = [("GitHub", f"https://github.com/Raye-Linux/{name}"),
                 ("Codeberg", f"https://codeberg.org/Raye-Linux/{name}"),
                 ("GitLab", f"https://gitlab.com/raye-linux/{GITLAB_NAME.get(name, name)}"),
                 (s["ours"], f"https://dl.rayelinux.com/git/{name}.git")]
        buttons = " · ".join(f'<a href="{url}" rel="noopener">{label}</a>' for label, url in links)
        rows.append(f'<tr><th scope="row">{name}</th><td>{fr if lang == "fr" else en}</td>'
                    f'<td class="source-links">{buttons}</td></tr>')
    return f"""{head(lang, 'source', s['title'] + ' · Raye Linux', s['lead'])}
<body>
<a class="skip-link" href="#main">{'Aller au contenu' if lang == 'fr' else 'Skip to content'}</a>
{topbar(lang, 'source')}
<main id="main">
<article class="prose card">
<h1>{s['title']}</h1>
<p>{s['lead']}</p>
<p>{s['clone']}</p>
{pre("git clone https://dl.rayelinux.com/git/iso.git")}
<h2>{s['where']}</h2>
<div class="table-wrap"><table class="source-table">
<thead><tr><th scope="col">{s['repo']}</th><th scope="col"></th><th scope="col"></th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table></div>
<p>{s['help'].format(discord=DISCORD)}</p>
</article>
</main>
{footer(lang)}
</body>
</html>
"""


def not_found():
    """One page for both languages: nginx cannot know which one was meant."""
    return f"""{head('fr', 'home', 'Page introuvable · Page not found', T['fr']['description'])}
<body class="page-result">
<header class="topbar"><a class="brand" href="/" aria-label="Raye Linux">
<img src="/assets/raye-mark.svg" alt="" width="36" height="16"><span>Raye Linux</span></a></header>
<main id="main" class="result card">
<section class="result-block" lang="fr"><h1>Page introuvable</h1>
<p>Cette adresse n'existe pas sur le site.</p>
<p class="result-home"><a href="/fr/">Retour à l'accueil</a></p></section>
<section class="result-block" lang="en"><h1>Page not found</h1>
<p>This address does not exist on the site.</p>
<p class="result-home"><a href="/en/">Back to the home page</a></p></section>
</main>
</body>
</html>
""".replace(
        '<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"')


def chooser():
    """The bare rayelinux.com: no language of its own. lang.js sends the
    visitor on to /fr/ or /en/ before the page draws; without scripts, the
    two links are all there is."""
    links = "\n".join(
        f'<li><a href="{PATHS[lang]["home"]}" hreflang="{lang}" lang="{lang}">{label}</a></li>'
        for lang, label in (("fr", "Français"), ("en", "English")))
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Raye Linux</title>
<meta name="description" content="{T['en']['description']}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141318">
<link rel="canonical" href="{URL}/">
<link rel="alternate" hreflang="fr" href="{URL}{PATHS['fr']['home']}">
<link rel="alternate" hreflang="en" href="{URL}{PATHS['en']['home']}">
<link rel="alternate" hreflang="x-default" href="{URL}/">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/lang.js"></script>
</head>
<body class="page-result">
<header class="topbar"><a class="brand" href="/" aria-label="Raye Linux">
<img src="/assets/raye-mark.svg" alt="" width="36" height="16"><span>Raye Linux</span></a></header>
<main id="main" class="result card">
<noscript>
<section class="result-block"><h1>Raye Linux</h1>
<ul class="lang-choice">
{links}
</ul></section>
</noscript>
</main>
</body>
</html>
"""


def strip_links(text):
    keep = ('rel="canonical"', 'rel="alternate"', 'property="og:')
    return "\n".join(l for l in text.split("\n") if not any(k in l for k in keep))


def versioned(text):
    """Give every /assets/ file a ?v=<content hash> address.

    A changed script then has a new URL, so no browser or Cloudflare cache can
    serve an old script with a new page (that once broke the signup button).
    """
    import hashlib, re as _re
    def tag(m):
        name = m.group(1)
        with open(os.path.join(ROOT, "assets", name), "rb") as f:
            return "/assets/%s?v=%s" % (name, hashlib.sha256(f.read()).hexdigest()[:10])
    return _re.sub(r'/assets/([A-Za-z0-9._/-]+)(?:\?v=[0-9a-f]+)?(?=[" ])', tag, text)


def write(rel, text):
    text = versioned(text)
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def french(text):
    # French typography: no line break before a colon
    return text.replace(" :", "\u00a0:")


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--release":
        take_release(sys.argv[2])
    elif len(sys.argv) > 1:
        sys.exit("usage: build_pages.py [--release release.json]")
    if not V1_LIVE:
        # the coming-soon site, which is what site/ holds until the launch
        write("index.html", chooser())
        write("fr/index.html", french(home("fr")))
        write("en/index.html", home("en"))
        write("fr/confidentialite/index.html", french(privacy("fr")))
        write("en/privacy/index.html", privacy("en"))
        for page in ("terms", "notice", "licenses"):
            for lang in ("fr", "en"):
                text = legal(lang, page)
                write(PATHS[lang][page].lstrip("/") + "index.html",
                      french(text) if lang == "fr" else text)
        write("fr/code-source/index.html", french(source("fr")))
        write("en/source/index.html", source("en"))
        write("fr/telecharger/index.html", french(download("fr")))
        write("en/download/index.html", download("en"))
        write("404.html", french(strip_links(not_found())))
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import site_v1
    site_v1.build(sys.modules[__name__])


if __name__ == "__main__":
    main()
