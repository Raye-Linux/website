"""The V1 download page.

While tools/release-v1.json says "pending", the page is complete but holds no
size, no checksum and no download button: they are filled in when the image
is published (build_pages.py --release <release.json>, which also clears the
pending mark). The beta's checksum is never shown here: it would verify the
wrong file. The text comes from build_pages.DOWNLOAD (verify, USB and bug
sections, which do not change) with the V1 wording over it."""

import html
import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
PENDING_FILE = os.path.join(TOOLS, "release-v1.json")

V1_TEXT = {
    "fr": {
        "description": "Télécharger Raye Linux 1.0 : l'image ISO, comment la vérifier, l'écrire "
                       "sur une clé USB, et ce qu'il faut savoir avant.",
        "known": "Ce qu'il faut savoir",
        "status_pending": "En préparation",
        "status_live": "Version 1.0",
        "lede_pending": "L'image de Raye Linux 1.0 sera ici à la sortie. La taille et la somme "
                        "de contrôle seront inscrites le jour de la publication, pas avant : "
                        "celles d'une autre image ne vérifieraient rien. En attendant, lisez ce "
                        "qui suit.",
        "lede_live": "L'image de Raye Linux, à écrire sur une clé USB pour l'installer. Si "
                     "quelque chose ne marche pas, écrivez-moi.",
        "pending_size": "Taille : à renseigner à la publication",
        "pending_sha": "À renseigner à la publication",
        "pending_get": "Téléchargement à la sortie",
        "kind": "ISO 64 bits, démarrage UEFI ou BIOS",
        "accept_title": "Avant de télécharger",
        "accept_items": [
            "Sauvegardez vos fichiers importants avant d'installer : l'installation peut effacer "
            "tout le disque choisi.",
            "Le logiciel est fourni « tel quel », sans garantie, comme le prévoient ses licences "
            "libres. Dans toute la mesure permise par la loi, Raye Linux et ses contributeurs "
            "ne sont pas responsables des dommages ou pertes de données liés à son "
            "téléchargement, son installation ou son utilisation.",
            "Vous êtes responsable de l'ordinateur sur lequel vous l'installez.",
            "En téléchargeant, vous acceptez les "
            "<a href=\"/conditions/\">conditions d'utilisation</a>.",
        ],
        "accept_check": "Je confirme avoir lu ces avertissements et avoir sauvegardé mes données.",
        "accept_go": "J'accepte, télécharger l'ISO",
        "needs_items": [
            "Un processeur Intel ou AMD 64 bits et un PC qui démarre en mode UEFI ou dans "
            "l'ancien mode BIOS (disques MBR compris)",
            "8 Go de mémoire conseillés",
            "{free} Go d'espace disque libre",
            "Une clé USB de 8 Go ou plus",
            "Secure Boot et puce TPM pris en charge, sans être obligatoires",
        ],
        "known_items": [
            "Au premier démarrage sous Secure Boot, passer au noyau de Raye demande d'inscrire "
            "une clé sur un écran bleu, une seule fois : page Installer.",
            "Les cartes AMD RX 400 et 500 et les cartes NVIDIA à 144 Hz ont des correctifs que je "
            "n'ai pas pu essayer sur une vraie carte. Si l'écran reste noir, choisissez « Safe "
            "graphics » sur la clé.",
            "Les programmes .exe : le premier lancement prend quelques secondes, et tous ne "
            "fonctionnent pas.",
            "Hors ligne, les Paramètres indiquent que les mises à jour n'ont pas pu être "
            "vérifiées.",
        ],
    },
    "en": {
        "description": "Download Raye Linux 1.0: the ISO image, how to check it, write it to a "
                       "USB stick, and what to know first.",
        "known": "What to know",
        "status_pending": "In preparation",
        "status_live": "Version 1.0",
        "lede_pending": "The Raye Linux 1.0 image will be here at release. Its size and checksum "
                        "will be filled in on the day it is published, not before: another "
                        "image's checksum would verify nothing. Meanwhile, read what follows.",
        "lede_live": "The Raye Linux image, to write to a USB stick to install it. If something "
                     "doesn't work, write to me.",
        "pending_size": "Size: to be filled in at release",
        "pending_sha": "To be filled in at release",
        "pending_get": "Download at release",
        "kind": "64-bit ISO, UEFI or BIOS start",
        "accept_title": "Before you download",
        "accept_items": [
            "Back up your important files before you install: installing can erase the whole "
            "disk you pick.",
            "The software is provided “as is”, without warranty, as its free licenses say. To "
            "the fullest extent the law allows, Raye Linux and its contributors are not liable "
            "for any damage or data loss that comes from downloading, installing or using it.",
            "You are responsible for the computer you install it on.",
            "By downloading, you accept the <a href=\"/en/terms/\">terms of use</a>.",
        ],
        "accept_check": "I have read these warnings and backed up my data.",
        "accept_go": "I agree, download the ISO",
        "needs_items": [
            "A 64-bit Intel or AMD processor and a PC that starts in UEFI mode or the older "
            "BIOS mode (MBR disks too)",
            "8 GB of memory recommended",
            "{free} GB of free disk space",
            "A USB stick of 8 GB or more",
            "Secure Boot and a TPM chip are supported, not required",
        ],
        "known_items": [
            "On the first start under Secure Boot, moving to Raye's kernel asks you to enroll a "
            "key on a blue screen, once: Install page.",
            "The AMD RX 400 and 500 cards and NVIDIA cards at 144 Hz have fixes I couldn't try "
            "on a real card. If the screen stays black, pick “Safe graphics” on the stick.",
            ".exe programs: the first launch takes a few seconds, and not all of them work.",
            "Offline, Settings say that updates couldn't be checked.",
        ],
    },
}


def state():
    """The release the V1 pages talk about: the pending one until the real
    release.json has been taken, then that one."""
    try:
        with open(PENDING_FILE, encoding="utf-8") as f:
            pending = json.load(f)
    except (OSError, ValueError):
        pending = {"pending": False}
    return pending


def is_pending():
    return bool(state().get("pending"))


def page(site, lang):
    b = site.b
    import site_v1_text as V
    t = dict(b.DOWNLOAD[lang])
    t.update(V1_TEXT[lang])
    pending = is_pending()
    info = state() if pending else b.release_info()
    urls, iso = info["urls"], info["iso"]
    folder = urls["r2_folder"]
    free = str(V.FREE_GB)
    head = site.head(lang, "download", t["get_title"] + " Raye " + V.VERSION + " · Raye Linux",
                     t["description"])
    parts = " ".join(info.get("parts", []))
    commands = {
        "join": b.pre(f"cat {parts} &gt; {iso}") + f'<p class="small">{t["join_other"]}</p>'
                + b.pre(f"copy /b {' + '.join(info.get('parts', []))} {iso}"),
        "gpg": b.pre("gpg --import raye-archive.asc\ngpg --verify SHA256SUMS.asc SHA256SUMS"),
        "sum": b.pre("sha256sum --check --ignore-missing SHA256SUMS"),
    }
    steps = "\n".join(f"<li><p>{text}</p>\n{commands[key]}</li>"
                      for text, key in t["verify_steps"] if key != "join")
    usb = "\n".join((f"<li><strong>{n}</strong> : {x}</li>" if lang == "fr"
                     else f"<li><strong>{n}</strong>: {x}</li>") for n, x in t["usb_items"])
    li = lambda items: "\n".join(f"<li>{x.replace('{free}', free)}</li>" for x in items)
    if pending:
        status, lede = t["status_pending"], t["lede_pending"]
        meta = t["pending_size"]
        sha = f'<dd>{t["pending_sha"]}</dd>'
        action = f'<span class="btn btn-held">{t["pending_get"]}</span>'
        accept = ""
        links = ""
    else:
        status, lede = t["status_live"], t["lede_live"]
        meta = (f'{b.size_text(lang, info["size"])} · {t["kind"]} · '
                f'{b.date_text(lang, info["date"])}')
        sha = f'<dd><code class="hash">{info["sha256"]}</code></dd>'
        action = f'<a class="btn btn-accent" href="#accept" data-accept>{t["get"]}</a>'
        accept = f"""<section id="accept" class="card dl-card dl-accept" aria-labelledby="accept-title">
<h2 id="accept-title">{t['accept_title']}</h2>
<ul class="plain">
{li(t['accept_items'])}
</ul>
<label class="dl-check"><input type="checkbox" id="accept-check"> <span>{t['accept_check']}</span></label>
<p class="dl-accept-actions"><a class="btn btn-accent dl-go" href="{urls['r2']}">{t['accept_go']}</a>
<button type="button" class="btn btn-quiet dl-cancel" hidden>{t['accept_close']}</button></p>
</section>
"""
        notes = f"release-notes-{info['release']}{'.fr' if lang == 'fr' else ''}.md"
        links = f"""<ul class="dl-links">
<li><a href="{folder}SHA256SUMS">{t['sums']}</a></li>
<li><a href="{folder}SHA256SUMS.asc">{t['sig']}</a></li>
<li><a href="{folder}raye-archive.asc">{t['key']}</a></li>
<li><a href="{folder}{notes}">{t['notes']}</a></li>
</ul>"""
    skip = "Aller au contenu" if lang == "fr" else "Skip to content"
    return f"""{head}
<body class="v1 page-download">
<a class="skip-link" href="#main">{skip}</a>
{site.topbar(lang, 'download')}
<main id="main" class="download wrap">
<header class="dl-head">
<p class="status"><span class="dot" aria-hidden="true"></span>{status}</p>
<h1>{t['get_title']} Raye Linux {V.VERSION}</h1>
<p class="lede">{lede}</p>
</header>

<section class="dl-file card" aria-labelledby="file-title">
<div class="dl-file-top">
<div>
<h2 id="file-title">{html.escape(iso)}</h2>
<p class="dl-meta">{meta}</p>
</div>
<div class="dl-actions">
{action}
</div>
</div>
<dl class="dl-facts">
<div><dt>{t['sha']}</dt>{sha}</div>
<div><dt>{t['fingerprint']}</dt><dd><code>{b.FINGERPRINT}</code></dd></div>
</dl>
{links}
</section>

{accept}<div class="dl-grid">
<section class="card dl-card" aria-labelledby="verify-title">
<h2 id="verify-title">{t['verify']}</h2>
<ol class="steps">
{steps}
</ol>
</section>

<section class="card dl-card" aria-labelledby="usb-title">
<h2 id="usb-title">{t['usb']}</h2>
<ul class="plain">
{usb}
</ul>
{b.pre(f"sudo dd if={iso} of=/dev/sdX bs=4M conv=fsync status=progress")}
<p>{t['usb_boot']} <a href="{site.path('install', lang)}">{site.name('install', lang)}</a>.</p>
</section>

<section class="card dl-card" aria-labelledby="needs-title">
<h2 id="needs-title">{t['needs']}</h2>
<ul class="plain">
{li(t['needs_items'])}
</ul>
</section>

<section class="card dl-card" aria-labelledby="known-title">
<h2 id="known-title">{t['known']}</h2>
<ul class="plain">
{li(t['known_items'])}
</ul>
</section>

<section class="card dl-card dl-wide" aria-labelledby="bug-title">
<h2 id="bug-title">{t['bug']}</h2>
<p>{t['bug_text']}</p>
<p><a href="{b.DISCORD}" rel="noopener">{t['bug_issue']}</a> · {t['bug_mail']}
<a href="mailto:bonjour@rayelinux.com">bonjour@rayelinux.com</a></p>
</section>
</div>
</main>
{site.footer(lang)}
</body>
</html>
"""
