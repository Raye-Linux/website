"""The confirmation mail, in French or English. Plain text plus HTML with
inline styles and no remote images, so it reads the same everywhere."""

import html
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import formatdate, make_msgid

UNSUB_MAILTO = "mailto:bonjour@rayelinux.com?subject=unsubscribe"

TEXT = {
    "fr": {
        "subject": "Confirmez votre inscription à Raye Linux",
        "preheader": "Un clic pour être prévenu du lancement de Raye Linux.",
        "hello": "Bonjour,",
        "intro": "Merci de votre intérêt pour Raye Linux. Pour finaliser votre "
                 "inscription, confirmez votre adresse :",
        "consent": "En confirmant, vous acceptez de recevoir un seul courriel, au "
                   "lancement de Raye Linux. Sur la page de confirmation, vous pourrez "
                   "aussi choisir de recevoir, de temps en temps, quelques nouvelles du "
                   "projet : c'est facultatif et décoché au départ.",
        "button": "Confirmer mon adresse",
        "expires": "Ce lien est valable 48 heures. Sans confirmation, votre adresse "
                   "sera effacée.",
        "ignore": "Vous n'avez rien demandé ? Ignorez ce courriel : sans clic, "
                  "rien ne se passe.",
        "unsub": "Ne plus recevoir de courriels de Raye Linux",
        "sign": "L'équipe Raye Linux",
    },
    "en": {
        "subject": "Confirm your Raye Linux signup",
        "preheader": "One click to hear when Raye Linux launches.",
        "hello": "Hello,",
        "intro": "Thanks for your interest in Raye Linux. To finish signing up, "
                 "please confirm your address:",
        "consent": "By confirming, you agree to get one email, when Raye Linux "
                   "launches. On the confirmation page you can also choose to get a "
                   "bit of project news now and then: it is optional and unticked to "
                   "start with.",
        "button": "Confirm my address",
        "expires": "This link works for 48 hours. Without confirmation, your address "
                   "will be deleted.",
        "ignore": "Didn't ask for this? Just ignore this email: nothing happens "
                  "without a click.",
        "unsub": "Stop getting emails from Raye Linux",
        "sign": "The Raye Linux team",
    },
}


def _address(value: str) -> Address:
    """A single address, display name allowed. Refuses anything that could
    smuggle a header."""
    if any(c in value for c in "\r\n\x00"):
        raise ValueError("control character in address")
    if "<" in value:
        name, _, rest = value.partition("<")
        addr = rest.rstrip().rstrip(">").strip()
        name = name.strip().strip('"')
    else:
        name, addr = "", value.strip()
    if addr.count("@") != 1 or any(c in addr for c in " ,;<>\"\t"):
        raise ValueError("bad address")
    user, domain = addr.split("@")
    return Address(display_name=name, username=user, domain=domain)


def _html(lang: str, t: dict, confirm_url: str, unsub_url: str) -> str:
    c, u = html.escape(confirm_url), html.escape(unsub_url)
    e = {k: html.escape(v) for k, v in t.items()}
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<meta name="color-scheme" content="light only"><title>{e['subject']}</title></head>
<body style="margin:0;padding:0;background:#F5F4F7;">
<div style="display:none;max-height:0;overflow:hidden;">{e['preheader']}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F5F4F7;">
<tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;background:#FFFFFF;border:1px solid #E2E1E6;border-radius:12px;">
<tr><td style="padding:28px 32px 8px 32px;font-family:'Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;">
<div style="font-size:13px;letter-spacing:2px;font-weight:700;color:#6A2FE6;">RAYE LINUX</div>
</td></tr>
<tr><td style="padding:8px 32px 0 32px;font-family:'Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;color:#17151C;font-size:16px;line-height:1.55;">
<p style="margin:0 0 12px 0;">{e['hello']}</p>
<p style="margin:0 0 24px 0;">{e['intro']}</p>
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:8px;background:#7B3CFF;">
<a href="{c}" style="display:inline-block;padding:12px 24px;font-weight:600;color:#FFFFFF;text-decoration:none;border-radius:8px;">{e['button']}</a>
</td></tr></table>
<p style="margin:24px 0 12px 0;font-size:15px;color:#17151C;">{e['consent']}</p>
<p style="margin:0 0 8px 0;font-size:14px;color:#5B5963;">{e['expires']}</p>
<p style="margin:0 0 8px 0;font-size:14px;color:#5B5963;">{e['ignore']}</p>
<p style="margin:0 0 24px 0;font-size:13px;color:#5B5963;word-break:break-all;">{c}</p>
<p style="margin:0 0 28px 0;">{e['sign']}</p>
</td></tr>
<tr><td style="padding:16px 32px 24px 32px;border-top:1px solid #E2E1E6;font-family:'Segoe UI',system-ui,-apple-system,Roboto,Helvetica,Arial,sans-serif;font-size:12px;color:#5B5963;">
<a href="{u}" style="color:#6A2FE6;">{e['unsub']}</a> &middot; rayelinux.com
</td></tr>
</table></td></tr></table>
</body></html>
"""


def build_confirmation(to: str, lang: str, confirm_url: str, unsub_url: str,
                       sender: str) -> EmailMessage:
    t = TEXT.get(lang, TEXT["fr"])
    lang = lang if lang in TEXT else "fr"
    msg = EmailMessage()
    msg["Subject"] = t["subject"]
    msg["From"] = _address(sender)
    msg["To"] = _address(to)
    msg["Date"] = formatdate(localtime=False)
    msg["Message-ID"] = make_msgid(domain="rayelinux.com")
    msg["Content-Language"] = lang
    msg["Auto-Submitted"] = "auto-generated"
    msg["List-Unsubscribe"] = f"<{UNSUB_MAILTO}>, <{unsub_url}>"
    msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    text = (f"{t['hello']}\n\n{t['intro']}\n\n{confirm_url}\n\n{t['consent']}\n\n"
            f"{t['expires']}\n"
            f"{t['ignore']}\n\n{t['sign']}\n\n--\n{t['unsub']}"
            f"{' :' if lang == 'fr' else ':'}\n{unsub_url}\n")
    msg.set_content(text, cte="quoted-printable")
    msg.add_alternative(_html(lang, t, confirm_url, unsub_url), subtype="html",
                        cte="quoted-printable")
    return msg


# The one mail promised at signup ("one email, when Raye Linux launches").
LAUNCH = {
    "fr": {
        "subject": "Raye Linux est disponible en bêta publique",
        "hello": "Bonjour,",
        "intro": "Vous vous êtes inscrit pour être prévenu du lancement de Raye Linux : "
                 "c'est maintenant. La bêta publique, Raye Linux 0.5 Bêta Alpenglow, "
                 "se télécharge dès aujourd'hui.",
        "beta": "La bêta publique dure environ une à deux semaines, avant la version 1.0. "
                "Vous croiserez des bugs : dites-le-nous sur le serveur Discord, ça aide "
                "beaucoup.",
        "button": "Télécharger Raye Linux",
        "discord": "Le serveur Discord",
        "sign": "L'équipe Raye Linux",
        "unsub": "Ne plus recevoir de courriels de Raye Linux",
        "url": "https://www.rayelinux.com/fr/telecharger/",
    },
    "en": {
        "subject": "Raye Linux is out in public beta",
        "hello": "Hello,",
        "intro": "You signed up to hear when Raye Linux launches: it's now. The public "
                 "beta, Raye Linux 0.5 Beta Alpenglow, is ready to download today.",
        "beta": "The public beta runs for about one to two weeks, before version 1.0. "
                "You'll meet bugs: tell us on the Discord server, it helps a lot.",
        "button": "Download Raye Linux",
        "discord": "The Discord server",
        "sign": "The Raye Linux team",
        "unsub": "Stop getting emails from Raye Linux",
        "url": "https://www.rayelinux.com/en/download/",
    },
}
DISCORD = "https://discord.gg/TrxhUkabyB"


def build_launch(to: str, lang: str, unsub_url: str, sender: str) -> EmailMessage:
    lang = lang if lang in LAUNCH else "fr"
    t = LAUNCH[lang]
    msg = EmailMessage()
    msg["Subject"] = t["subject"]
    msg["From"] = _address(sender)
    msg["To"] = _address(to)
    msg["Date"] = formatdate(localtime=False)
    msg["Message-ID"] = make_msgid(domain="rayelinux.com")
    msg["Content-Language"] = lang
    msg["List-Unsubscribe"] = f"<{UNSUB_MAILTO}>, <{unsub_url}>"
    msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
    colon = " :" if lang == "fr" else ":"
    msg.set_content(f"{t['hello']}\n\n{t['intro']}\n\n{t['button']}{colon}\n{t['url']}\n\n"
                    f"{t['beta']}\n{t['discord']}{colon} {DISCORD}\n\n{t['sign']}\n\n--\n"
                    f"{t['unsub']}{colon}\n{unsub_url}\n", cte="quoted-printable")
    e = {k: html.escape(v) for k, v in t.items()}
    u = html.escape(unsub_url)
    msg.add_alternative(f"""<!DOCTYPE html>
<html lang="{lang}">
<body style="margin:0;padding:24px;background:#f4f2f8;font-family:Segoe UI,Arial,sans-serif;color:#1b1a1f;">
<div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:12px;padding:28px;">
<p style="margin:0 0 16px;">{e['hello']}</p>
<p style="margin:0 0 20px;line-height:1.5;">{e['intro']}</p>
<p style="margin:0 0 24px;"><a href="{e['url']}" style="display:inline-block;background:#6A2FE6;color:#ffffff;text-decoration:none;padding:12px 22px;border-radius:999px;font-weight:600;">{e['button']}</a></p>
<p style="margin:0 0 20px;line-height:1.5;">{e['beta']}<br><a href="{DISCORD}" style="color:#6A2FE6;">{e['discord']}</a></p>
<p style="margin:0;">{e['sign']}</p>
</div>
<p style="max-width:520px;margin:16px auto 0;font-size:12px;color:#6b6873;text-align:center;">
<a href="{u}" style="color:#6A2FE6;">{e['unsub']}</a> &middot; rayelinux.com</p>
</body>
</html>""", subtype="html", cte="quoted-printable")
    return msg
