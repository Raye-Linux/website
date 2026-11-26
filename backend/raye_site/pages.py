"""Small result pages served by the backend (signup without script,
confirmation, unsubscribe). Same look as the static site, no script."""

import html

OTHER = {"fr": "en", "en": "fr"}

MESSAGES = {
    "subscribed": {
        "fr": ("Vérifiez votre boîte de réception",
               "Si l'adresse est valide, un courriel de confirmation est en route. "
               "Cliquez sur le lien qu'il contient pour finaliser l'inscription. "
               "Rien reçu d'ici quelques minutes ? Regardez dans les indésirables."),
        "en": ("Check your inbox",
               "If the address is valid, a confirmation email is on its way. "
               "Click the link inside to finish signing up. Nothing after a few "
               "minutes? Have a look in your spam folder."),
    },
    "bad_email": {
        "fr": ("Cette adresse ne semble pas valide",
               "Vérifiez l'adresse courriel saisie, puis réessayez."),
        "en": ("That address doesn't look right",
               "Check the email address you typed, then try again."),
    },
    "no_consent": {
        "fr": ("Il manque votre accord",
               "Cochez la case pour accepter de recevoir un courriel au lancement, "
               "puis réessayez."),
        "en": ("We need your consent",
               "Tick the box to agree to get an email at launch, then try again."),
    },
    "rate": {
        "fr": ("Un instant",
               "Trop de demandes en peu de temps. Réessayez un peu plus tard."),
        "en": ("Hold on",
               "Too many requests in a short time. Please try again a little later."),
    },
    "confirm_ask": {
        "fr": ("Confirmez votre inscription",
               "En confirmant, vous acceptez de recevoir un seul courriel, au lancement "
               "de Raye Linux. Vous pourrez vous désabonner en un clic."),
        "en": ("Confirm your signup",
               "By confirming, you agree to get one email, when Raye Linux launches. "
               "You can unsubscribe in one click."),
    },
    "confirmed": {
        "fr": ("C'est confirmé, vous êtes sur la liste",
               "Merci ! Nous vous écrirons quand Raye Linux sera prêt. Chaque "
               "courriel contient un lien pour vous désabonner."),
        "en": ("You're on the list",
               "Thank you! We'll write to you when Raye Linux is ready. Every "
               "email has a link to unsubscribe."),
    },
    "confirm_already": {
        "fr": ("Adresse déjà confirmée",
               "Votre adresse est déjà sur la liste. Rien d'autre à faire."),
        "en": ("Address already confirmed",
               "Your address is already on the list. Nothing else to do."),
    },
    "confirm_expired": {
        "fr": ("Ce lien a expiré",
               "Les liens de confirmation sont valables 48 heures. Inscrivez-vous "
               "de nouveau pour en recevoir un autre."),
        "en": ("This link has expired",
               "Confirmation links work for 48 hours. Sign up again to get a new one."),
    },
    "invalid": {
        "fr": ("Ce lien ne fonctionne pas",
               "Il est incomplet, expiré ou a déjà été remplacé par un plus récent. "
               "Copiez le lien en entier depuis le courriel, ou inscrivez-vous de nouveau."),
        "en": ("This link doesn't work",
               "It is incomplete, expired or was replaced by a newer one. Copy the "
               "whole link from the email, or sign up again."),
    },
    "unsub_ask": {
        "fr": ("Se désabonner",
               "Vous ne recevrez plus aucun courriel de Raye Linux."),
        "en": ("Unsubscribe",
               "You will not get any more emails from Raye Linux."),
    },
    "unsub_done": {
        "fr": ("Vous êtes désabonné",
               "C'est fait : vous ne recevrez plus de courriels de Raye Linux. "
               "Votre adresse sera effacée sous 30 jours."),
        "en": ("You're unsubscribed",
               "Done: you won't get any more emails from Raye Linux. Your address "
               "will be deleted within 30 days."),
    },
    "unsub_already": {
        "fr": ("Vous êtes déjà désabonné",
               "Cette adresse ne reçoit plus de courriels de Raye Linux."),
        "en": ("You're already unsubscribed",
               "This address no longer gets emails from Raye Linux."),
    },
    "join_ok": {
        "fr": ("Candidature envoyée",
               "Merci ! La Raye Team lit chaque candidature et vous répond sur Discord ou par "
               "courriel. Rien d'autre à faire pour l'instant."),
        "en": ("Application sent",
               "Thank you! The Raye Team reads every application and answers you on Discord "
               "or by email. Nothing else to do for now."),
    },
    "join_error": {
        "fr": ("Il manque quelque chose",
               "Revenez au formulaire et vérifiez l'adresse courriel, le nom Discord, le texte "
               "(30 caractères au moins) et la case d'accord."),
        "en": ("Something is missing",
               "Go back to the form and check the email address, the Discord name, the text "
               "(30 characters at least) and the consent box."),
    },
    "join_rate": {
        "fr": ("Un instant",
               "Trop de candidatures en peu de temps. Réessayez dans une heure."),
        "en": ("Hold on",
               "Too many applications in a short time. Please try again in an hour."),
    },
    "not_found": {
        "fr": ("Page introuvable", "Cette adresse n'existe pas sur le site."),
        "en": ("Page not found", "This address does not exist on the site."),
    },
}

BUTTONS = {
    "confirm_ask": {"fr": "Confirmer mon adresse", "en": "Confirm my address"},
    "unsub_ask": {"fr": "Me désabonner", "en": "Unsubscribe me"},
}

NEWS = {
    "fr": "Envoyez-moi aussi, de temps en temps, quelques nouvelles du projet (facultatif).",
    "en": "Also send me a bit of project news now and then (optional).",
}

# the V1 site has its French home at the root
HOME = {"fr": ("/", "Retour à l'accueil"), "en": ("/en/", "Back to the home page")}
BRAND_ALT = {"fr": "Raye Linux, accueil", "en": "Raye Linux, home"}


def _t(text: str) -> str:
    """Escape for a text node; apostrophes stay readable."""
    return html.escape(text, quote=False)


def _block(kind: str, lang: str, form_action: str | None, token: str | None) -> str:
    title, text = MESSAGES[kind][lang]
    parts = [f'<section class="result-block" lang="{lang}">',
             f"<h1>{_t(title)}</h1>", f"<p>{_t(text)}</p>"]
    if form_action and token:
        parts.append(f'<form method="post" action="{html.escape(form_action)}">'
                     f'<input type="hidden" name="t" value="{html.escape(token)}">')
        if kind == "confirm_ask":
            # the only place the news choice is made, unticked to start with
            parts.append('<label class="check"><input type="checkbox" name="news" value="on">'
                         f"<span>{_t(NEWS[lang])}</span></label>")
        parts.append(f'<button class="btn btn-accent" type="submit">'
                     f"{_t(BUTTONS[kind][lang])}</button></form>")
    href, label = HOME[lang]
    parts.append(f'<p class="result-home"><a href="{href}">{_t(label)}</a></p>')
    parts.append("</section>")
    return "".join(parts)


def render(kind: str, lang: str | None, form_action: str | None = None,
           token: str | None = None) -> str:
    """A page in the visitor's language. Without a known language (a link we
    could not match) both languages are shown, French first."""
    langs = [lang] if lang in OTHER else ["fr", "en"]
    main_lang = langs[0]
    title = MESSAGES[kind][main_lang][0]
    blocks = "\n".join(_block(kind, l, form_action, token) for l in langs)
    home, _ = HOME[main_lang]
    return f"""<!DOCTYPE html>
<html lang="{main_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#141318">
<title>{_t(title)} · Raye Linux</title>
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body class="page-result">
<header class="topbar"><a class="brand" href="{home}" aria-label="{BRAND_ALT[main_lang]}">
<img src="/assets/raye-mark.svg" alt="" width="28" height="28"><span>Raye Linux</span></a></header>
<main id="main" class="result card">
{blocks}
</main>
</body>
</html>
"""
