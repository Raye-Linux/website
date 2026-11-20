"""The legal pages of rayelinux.com: privacy, terms of use, legal notice,
licenses. Every claim is something measured on the servers or read in the
code; when the code or a server changes, change the page the same day and
add a line to CHANGES.

Each page is a list of sections, and each piece of text is a (French,
English) pair, so the two languages always have the same headings, lists
and tables. body() renders one page in one language.

The trademark notice is the one place the site names the companies whose
products Raye resembles. tests/test_site.py allows exactly TRADEMARK[lang],
on the licenses page only."""

UPDATED = {"fr": "14 novembre 2026", "en": "November 14, 2026"}
ISO_UPDATED = "2026-11-14"
VERSION = "3.0"

TRADEMARK = {
    "fr": "Windows et Microsoft sont des marques de Microsoft Corporation. Ubuntu est une "
          "marque de Canonical Ltd. Raye Linux n'est affilié à aucune de ces entreprises, "
          "ni approuvé ou soutenu par elles. Toute ressemblance de mise en page sert "
          "seulement à rendre Raye familier : les images, les icônes et le code sont les "
          "nôtres.",
    "en": "Windows and Microsoft are trademarks of Microsoft Corporation. Ubuntu is a "
          "trademark of Canonical Ltd. Raye Linux is not affiliated with, endorsed or "
          "sponsored by any of these companies. Any likeness in layout is only there to make "
          "Raye familiar: the pictures, icons and code are our own.",
}

CONTACT = '<a href="mailto:bonjour@rayelinux.com">bonjour@rayelinux.com</a>'

UI = {
    "fr": {"updated": "Dernière mise à jour", "version": "version", "summary": "En bref",
           "toc": "Sommaire", "top": "Haut de la page"},
    "en": {"updated": "Last updated", "version": "version", "summary": "In short",
           "toc": "Contents", "top": "Back to the top"},
}


# --- a small way of writing both languages side by side ---------------------

def P(fr, en):
    return ("p", (fr, en))


def H(fr, en):
    return ("h3", (fr, en))


def L(*items):
    return ("ul", items)


def OL(*items):
    return ("ol", items)


def T(head, *rows):
    return ("table", (head, rows))


def S(ident, fr, en, *blocks):
    return {"id": ident, "title": (fr, en), "blocks": blocks}


# --- privacy policy ----------------------------------------------------------

PRIVACY_SUMMARY = [
    ("Je garde le moins possible, je ne vends rien, il n'y a ni publicité, ni pistage, ni "
     "témoin (cookie).",
     "I keep as little as I can, I sell nothing, and there are no ads, no tracking and no "
     "cookies."),
    ("Le site, la bulle d'aide et la liste de courriels tournent sur mes propres serveurs, "
     "au Québec. Les connexions passent par Cloudflare (États-Unis).",
     "The site, the help bubble and the mailing list run on my own servers in Québec. "
     "Connections go through Cloudflare (United States)."),
    ("La liste de courriels garde votre adresse, votre langue et la preuve de votre "
     "consentement, jusqu'à votre désabonnement.",
     "The mailing list keeps your address, your language and the proof of your consent, "
     "until you unsubscribe."),
    ("Les questions de la bulle d'aide ne sont pas gardées. Les rapports de bogue publiés vont "
     "sur notre serveur Discord ; le moyen de vous joindre n'y est jamais publié.",
     "Help bubble questions are not kept. Published bug reports go to our Discord server; "
     "how to reach you is never posted there."),
    ("Raye Linux n'envoie aucun rapport d'utilisation ni de plantage depuis votre PC.",
     "Raye Linux sends no usage reports and no crash reports from your PC."),
    ("Vous pouvez tout consulter, corriger ou faire effacer : écrivez à bonjour@rayelinux.com, "
     "réponse sous 30 jours.",
     "You can see, correct or delete everything: write to bonjour@rayelinux.com, answer "
     "within 30 days."),
]

PRIVACY = [
    S("scope", "À quoi sert cette politique", "What this policy covers",
      P("Cette politique dit quels renseignements personnels sont recueillis quand vous "
        "utilisez le site rayelinux.com, sa bulle d'aide, son formulaire de rapport de bogue, "
        "sa liste de courriels, notre serveur Discord et le logiciel Raye Linux, pourquoi ils "
        "le sont, où ils vont, combien de temps ils restent et comment exercer vos droits. "
        "Elle est écrite à partir du code et des serveurs tels qu'ils fonctionnent "
        "réellement, et elle dit aussi ce qui n'est pas encore parfait.",
        "This policy says what personal information is collected when you use the "
        "rayelinux.com website, its help bubble, its bug report form, its mailing list, our "
        "Discord server and the Raye Linux software, why, where it goes, how long it stays and "
        "how to use your rights. It is written from the code and the servers as they really "
        "work, and it also says what isn't right yet."),
      P("Elle suit la Loi sur la protection des renseignements personnels dans le secteur "
        "privé du Québec (la « Loi 25 ») et, pour les personnes qui se trouvent dans l'Union "
        "européenne, le Règlement général sur la protection des données (RGPD). Si une loi de "
        "votre pays vous donne plus de droits, ces droits s'appliquent aussi.",
        "It follows Québec's Act respecting the protection of personal information in the "
        "private sector (\"Law 25\") and, for people in the European Union, the General Data "
        "Protection Regulation (GDPR). If a law of your country gives you more rights, those "
        "rights apply too.")),
    S("definitions", "Les mots utilisés ici", "Words used here",
      L(("<strong>Renseignement personnel</strong> : toute information qui concerne une "
         "personne et permet de l'identifier, directement ou non (une adresse courriel, une "
         "adresse IP, un pseudonyme Discord).",
         "<strong>Personal information</strong>: any information about a person that "
         "identifies them, directly or not (an email address, an IP address, a Discord "
         "name)."),
        ("<strong>Je</strong>, <strong>moi</strong> : la personne qui fait Raye Linux et "
         "ce site, présentée plus bas. <strong>Nous</strong>, <strong>l'équipe</strong> : "
         "cette personne et les personnes qui modèrent le serveur Discord avec elle.",
         "<strong>I</strong>, <strong>me</strong>: the person who makes Raye Linux and this "
         "site, introduced below. <strong>We</strong>, <strong>the team</strong>: that person "
         "and the people who moderate the Discord server with them."),
        ("<strong>Le site</strong> : rayelinux.com et ses pages, en français sous /fr/ et en "
         "anglais sous /en/.",
         "<strong>The site</strong>: rayelinux.com and its pages, in French under /fr/ and in "
         "English under /en/."),
        ("<strong>La bulle d'aide</strong> : le bouton « Aide » en bas des pages, qui répond "
         "aux questions et contient le formulaire « Signaler un bogue ».",
         "<strong>The help bubble</strong>: the \"Help\" button at the bottom of the pages, "
         "which answers questions and holds the \"Report a bug\" form."),
        ("<strong>Raye</strong> ou <strong>le logiciel</strong> : le système Raye Linux, "
         "tel que vous le téléchargez et l'installez.",
         "<strong>Raye</strong> or <strong>the software</strong>: the Raye Linux system, as "
         "you download and install it."),
        ("<strong>Sous-traitant</strong> : une entreprise qui traite des renseignements pour "
         "moi ou sur le chemin de vos données (Cloudflare, Contabo, Discord).",
         "<strong>Service provider</strong>: a company that handles information for me or on "
         "the path of your data (Cloudflare, Contabo, Discord)."))),
    S("who", "Qui est responsable et comment me joindre",
      "Who is responsible and how to reach me",
      P("Raye Linux et ce site sont faits par une seule personne, au Québec, sous le "
        "pseudonyme « techoraye ». C'est elle qui décide de ce qui est recueilli et pourquoi, "
        "et c'est aussi la personne responsable de la protection des renseignements "
        "personnels au sens de la Loi 25.",
        "Raye Linux and this site are made by one person in Québec, under the pseudonym "
        "\"techoraye\". That person decides what is collected and why, and is also the "
        "person in charge of protecting personal information under Law 25."),
      P("Pour toute question, demande ou plainte sur vos renseignements : {contact}. Écrivez "
        "en français ou en anglais. Aucun représentant n'est désigné dans l'Union européenne.",
        "For any question, request or complaint about your information: {contact}. Write in "
        "French or English. No representative is appointed in the European Union.")),
    S("overview", "Ce qui est recueilli, en un tableau", "What is collected, in one table",
      P("Le tableau donne la durée de conservation de chaque renseignement. Les sections qui "
        "suivent donnent le détail.",
        "The table gives how long each piece of information is kept. The sections after it "
        "give the details."),
      T([("Quoi", "What"), ("Où", "Where"), ("Combien de temps", "How long")],
        [("Inscription à la liste (adresse, langue, choix des nouvelles, dates, version du "
          "consentement)", "Mailing list signup (address, language, news choice, dates, "
          "consent version)"),
         ("mon serveur, au Québec", "my server, in Québec"),
         ("jusqu'au désabonnement, puis effacée sous 30 jours ; non confirmée : 48 heures",
          "until you unsubscribe, then deleted within 30 days; unconfirmed: 48 hours")],
        [("Questions et réponses de la bulle d'aide", "Help bubble questions and answers"),
         ("en mémoire, le temps de répondre", "in memory, while answering"),
         ("rien n'est gardé", "nothing is kept")],
        [("Rapport de bogue publié (texte, étapes, capture, langue, navigateur)",
          "Published bug report (text, steps, screenshot, language, browser)"),
         ("Discord, États-Unis", "Discord, United States"),
         ("jusqu'à sa suppression", "until it is deleted")],
        [("Moyen de vous joindre, rapport retenu pour relecture",
          "How to reach you, report held for review"),
         ("salon privé Discord, États-Unis", "private Discord channel, United States"),
         ("jusqu'à sa suppression", "until it is deleted")],
        [("Empreinte du texte d'un rapport", "Fingerprint of a report's text"),
         ("mémoire de mon serveur", "my server's memory"),
         ("24 heures", "24 hours")],
        [("Adresse IP pour limiter les abus", "IP address to limit abuse"),
         ("mémoire de mon serveur", "my server's memory"),
         ("10 minutes à 1 heure", "10 minutes to 1 hour")],
        [("Journal du serveur d'entrée (IP, date, page, navigateur)",
          "Front server log (IP, date, page, browser)"),
         ("mon serveur, au Québec", "my server, in Québec"),
         ("sans limite pour l'instant (à corriger : 14 jours)",
          "no limit for now (to fix: 14 days)")],
        [("Courriels que vous m'écrivez", "Emails you write to me"),
         ("mon serveur de courrier, au Québec", "my mail server, in Québec"),
         ("le temps de vous répondre et de suivre la demande",
          "while I answer and follow up your request")],
        [("Choix de langue", "Language choice"),
         ("votre navigateur", "your browser"),
         ("jusqu'à ce que vous l'effaciez", "until you clear it")])),
    S("mailing-list", "La liste de courriels", "The mailing list",
      H("Ce qui est gardé", "What is kept"),
      P("Si vous vous inscrivez, je garde votre <strong>adresse courriel</strong>, la "
        "<strong>langue</strong> choisie, votre choix de recevoir ou non de rares nouvelles, "
        "la date de votre inscription et de votre confirmation, et la version du texte de "
        "consentement accepté. Pour envoyer les courriels, le serveur garde aussi, le temps de "
        "l'envoi, une file des messages à partir et, sous forme d'empreinte seulement, les "
        "jetons des liens de confirmation et de désabonnement : ces liens ne sont jamais "
        "gardés lisibles.",
        "If you sign up, I keep your <strong>email address</strong>, the "
        "<strong>language</strong> you chose, whether you want occasional news, the date you "
        "signed up and confirmed, and the version of the consent text you agreed to. To send "
        "the emails, the server also keeps, while sending, a queue of messages to go out and, "
        "only as a hash, the tokens of the confirmation and unsubscribe links: those links are "
        "never stored in a readable form."),
      P("Votre adresse IP n'est pas enregistrée avec l'inscription : elle sert seulement, en "
        "mémoire et pendant au plus une heure, à bloquer les abus (5 inscriptions par heure "
        "et par adresse au plus).",
        "Your IP address is not stored with the signup: it is only used, in memory and for an "
        "hour at most, to block abuse (5 signups per hour per address at most)."),
      H("Pourquoi, et sur quelle base", "Why, and on what basis"),
      P("Pour vous écrire au lancement et, seulement si vous l'avez demandé, de rares nouvelles "
        "du projet. La base est votre <strong>consentement exprès</strong>, donné en cochant "
        "la case et confirmé par le lien reçu par courriel (double confirmation). Vous pouvez "
        "le retirer à tout moment.",
        "To write to you at launch and, only if you asked for it, a bit of occasional project "
        "news. The basis is your <strong>express consent</strong>, given by ticking the box "
        "and confirmed by the link I email you (double opt-in). You can withdraw it at any "
        "time."),
      H("Combien de temps", "How long"),
      L(("Une inscription non confirmée est effacée 48 heures après l'envoi du courriel de "
         "confirmation (au plus 7 jours si ce courriel n'a pas pu partir).",
         "An unconfirmed signup is deleted 48 hours after the confirmation email is sent "
         "(7 days at most if that email could not go out)."),
        ("Une adresse confirmée est gardée jusqu'à votre désabonnement ou votre demande "
         "d'effacement.",
         "A confirmed address is kept until you unsubscribe or ask me to delete it."),
        ("Une adresse désabonnée est effacée sous 30 jours. Ce délai sert seulement à ne pas "
         "vous réinscrire par erreur.",
         "An unsubscribed address is deleted within 30 days. The delay is only there so you "
         "aren't signed up again by mistake."),
        ("La liste n'existe qu'à un seul endroit : il n'en existe aucune copie de sauvegarde.",
         "The list exists in one place only: there is no backup copy of it.")),
      H("Comment les courriels partent", "How the emails go out"),
      P("Les courriels partent de mon propre serveur de courrier, au Québec, et sortent sur "
        "Internet par un serveur que je loue chez Contabo, en Allemagne, relié à la maison par "
        "un tunnel chiffré : le message y transite, il n'y est pas gardé. Votre fournisseur de "
        "courrier reçoit ensuite le message, selon ses propres règles.",
        "Emails leave from my own mail server in Québec and go out to the Internet through a "
        "server I rent from Contabo, in Germany, linked to my home by an encrypted tunnel: the "
        "message passes through it and is not kept there. Your email provider then receives "
        "the message, under its own rules."),
      P("Chaque courriel contient un lien de désabonnement en un clic. Aucun courriel ne "
        "contient de pixel espion ni de lien de suivi.",
        "Every email has a one-click unsubscribe link. No email holds a tracking pixel or a "
        "tracked link.")),
    S("help", "La bulle d'aide", "The help bubble",
      P("Les questions posées dans la bulle d'aide sont envoyées à un modèle de langue qui "
        "tourne sur mon propre serveur, au Québec. Il répond à partir du manuel de Raye, des "
        "pages du site et des notes de version. Les questions ne sont envoyées à aucune autre "
        "entreprise, et ne servent pas à entraîner un modèle.",
        "Questions asked in the help bubble go to a language model running on my own server "
        "in Québec. It answers from the Raye handbook, the site's pages and the release notes. "
        "The questions are not sent to any other company, and are not used to train a "
        "model."),
      P("Ni vos questions ni les réponses ne sont gardées : pas sur le disque, pas dans les "
        "journaux. Le serveur ne compte que le nombre de questions. La conversation vit dans "
        "la page ouverte et disparaît quand vous la fermez ou rechargez la page. Votre adresse "
        "IP sert, en mémoire et pendant au plus 10 minutes, à limiter le nombre de questions "
        "(20 par période de 10 minutes).",
        "Neither your questions nor the answers are kept: not on disk, not in the logs. The "
        "server only counts how many questions it got. The conversation lives in the open "
        "page and is gone when you close it or reload the page. Your IP address is used, in "
        "memory and for 10 minutes at most, to limit the number of questions (20 in any "
        "10 minutes)."),
      P("La base : vous demandez une réponse, et je vous la donne (votre demande ; au sens du "
        "RGPD, l'exécution du service demandé). Les réponses sont produites automatiquement "
        "et peuvent être fausses : en cas de doute, demandez à une personne sur Discord. "
        "<strong>N'écrivez pas de renseignements personnels dans vos questions</strong> : "
        "elles traversent Cloudflare comme le reste du site.",
        "The basis: you ask for an answer and I give it (your request; under the GDPR, "
        "performing the service you asked for). The answers are produced automatically and "
        "can be wrong: when in doubt, ask a person on Discord. <strong>Don't put personal "
        "information in your questions</strong>: they pass through Cloudflare like the rest "
        "of the site.")),
    S("bugs", "Signaler un bogue", "Reporting a bug",
      H("Ce que le formulaire envoie", "What the form sends"),
      P("Le formulaire « Signaler un bogue » de la bulle d'aide envoie à mon serveur ce que "
        "vous y écrivez (ce qui s'est passé, comment le refaire, et le moyen de vous joindre "
        "si vous en donnez un), la capture d'écran si vous en ajoutez une, l'adresse de la "
        "page, la langue de la page et le nom de votre navigateur. La capture est réduite dans "
        "votre navigateur avant l'envoi. Tous les champs sauf « ce qui s'est passé » sont "
        "facultatifs.",
        "The \"Report a bug\" form in the help bubble sends my server what you write in it "
        "(what happened, how to make it happen again, and how to reach you if you give that), "
        "the screenshot if you add one, the address of the page, the page's language and the "
        "name of your browser. The screenshot is shrunk in your browser before it is sent. "
        "Every field except \"what happened\" is optional."),
      H("La vérification avant publication", "The check before posting"),
      P("Avant toute publication, le rapport est vérifié par des filtres et par le modèle de "
        "langue de la bulle d'aide, sur mon propre serveur ; rien n'est envoyé à un tiers pour "
        "cette vérification. Selon le résultat, le rapport est :",
        "Before anything is posted, the report is checked by filters and by the help bubble's "
        "language model, on my own server; nothing is sent to a third party for this check. "
        "Depending on the result, the report is:"),
      L(("<strong>publié</strong> dans le forum #bugs de notre serveur Discord, si c'est "
         "clairement un bogue ;",
         "<strong>posted</strong> in the #bugs forum of our Discord server, if it is clearly "
         "a bug;"),
        ("<strong>retenu</strong> pour qu'une personne le relise, dans un salon privé de "
         "l'équipe : texte trop court, coordonnées dans le texte, lien, mention, gros mots, "
         "capture d'écran, doute du modèle, ou modèle indisponible ;",
         "<strong>held</strong> for a person to read, in a private staff channel: text too "
         "short, contact details in the text, a link, a mention, swearing, a screenshot, a "
         "doubt from the model, or the model not answering;"),
        ("<strong>écarté</strong> sans être envoyé nulle part, s'il contient des insultes "
         "haineuses ou des menaces, ou s'il répète un rapport déjà reçu dans les 24 heures.",
         "<strong>dropped</strong> without being sent anywhere, if it holds hateful slurs or "
         "threats, or repeats a report already received within 24 hours.")),
      P("C'est une décision prise automatiquement. Vous pouvez demander à une personne de la "
        "revoir, et savoir quels renseignements et quelles raisons l'ont menée : écrivez à "
        "{contact}.",
        "This is a decision made automatically. You can ask a person to look at it again, "
        "and learn what information and which reasons led to it: write to {contact}."),
      H("Ce qui est publié, et ce qui ne l'est jamais", "What is posted, and what never is"),
      P("Un rapport publié contient ce qui s'est passé, les étapes, la langue et un nom court "
        "du navigateur et du système (par exemple « Firefox 160 sur Linux »). Les membres du "
        "serveur Discord peuvent le lire et y répondre. <strong>Le moyen de vous joindre "
        "n'est jamais publié</strong> : il va seulement dans le salon privé de l'équipe. "
        "L'adresse de la page et la chaîne complète du navigateur ne sont jamais publiées non "
        "plus.",
        "A published report holds what happened, the steps, the language and a short name of "
        "the browser and system (for example \"Firefox 160 on Linux\"). Members of the Discord "
        "server can read it and reply. <strong>How to reach you is never posted</strong>: it "
        "only goes to the private staff channel. The page address and the full browser string "
        "are never posted either."),
      H("Où, combien de temps, sur quelle base", "Where, how long, on what basis"),
      P("Mon serveur ne garde rien de tout ça, sauf, en mémoire et pendant 24 heures, une "
        "empreinte du texte pour repérer les doublons (le texte lui-même ne peut pas en être "
        "retrouvé). Votre adresse IP sert, en mémoire et pendant au plus une heure, à limiter "
        "le nombre de rapports (3 par heure). C'est mon serveur qui envoie le rapport à "
        "Discord : Discord ne voit pas votre adresse IP. Discord est une entreprise des "
        "États-Unis : le rapport, publié ou retenu, est donc gardé hors du Québec, chez "
        "Discord, jusqu'à ce qu'on le supprime.",
        "My server keeps none of it, except, in memory and for 24 hours, a fingerprint of the "
        "text to spot duplicates (the text itself can't be recovered from it). Your IP address "
        "is used, in memory and for one hour at most, to limit the number of reports (3 per "
        "hour). My server is the one that sends the report to Discord: Discord does not see "
        "your IP address. Discord is a company in the United States, so the report, posted or "
        "held, is kept outside Québec, at Discord, until it is deleted."),
      P("La base : votre consentement, donné en envoyant le formulaire, pour publier le "
        "rapport et vous joindre ; et mon intérêt légitime à garder le forum lisible et sans "
        "abus, pour la vérification. Pour faire retirer un rapport ou vos coordonnées, "
        "écrivez à {contact}.",
        "The basis: your consent, given by sending the form, to post the report and reach "
        "you; and my legitimate interest in keeping the forum readable and free of abuse, for "
        "the check. To have a report or your contact details removed, write to {contact}.")),
    S("logs", "Les journaux des serveurs", "Server logs",
      P("Le serveur qui reçoit les visites (un serveur que j'héberge chez moi, au Québec) "
        "note pour chaque demande l'adresse IP, la date, la page demandée, la page d'où vous "
        "venez et le navigateur. Le serveur du site lui-même note seulement la page, le "
        "résultat et la durée, sans adresse et sans le reste de l'adresse de la page (où "
        "voyagent les jetons des liens de courriel). Le service du site note des compteurs "
        "(questions reçues, rapports envoyés), jamais un texte, une adresse courriel ou une "
        "adresse IP.",
        "The server that receives visits (one I host at home, in Québec) writes down, for each "
        "request, the IP address, the date, the page asked for, the page you came from and the "
        "browser. The site's own server writes only the page, the result and the time taken, "
        "with no address and without the rest of the page address (where email link tokens "
        "travel). The site's service writes counters (questions received, reports sent), never "
        "a text, an email address or an IP address."),
      P("Ces journaux servent à la sécurité et au dépannage (intérêt légitime). Le serveur "
        "d'entrée est copié chaque nuit, et ces copies sont gardées 7 jours sur un disque chez "
        "moi.",
        "These logs are for security and troubleshooting (legitimate interest). The front "
        "server is copied every night, and those copies are kept for 7 days on a disk at "
        "home."),
      P("<strong>À corriger :</strong> aujourd'hui, les journaux du serveur d'entrée ne sont "
        "pas encore effacés automatiquement ; ils existent depuis le 30 octobre 2026. Je mets "
        "en place leur effacement après 14 jours. En attendant, vous pouvez me demander "
        "d'effacer les lignes qui concernent votre adresse.",
        "<strong>Still to fix:</strong> today the front server's logs are not deleted "
        "automatically yet; they go back to October 30, 2026. I am setting up their deletion "
        "after 14 days. Until then, you can ask me to delete the lines about your address.")),
    S("cloudflare", "Cloudflare et les téléchargements", "Cloudflare and downloads",
      P("Toutes les connexions au site passent par Cloudflare, Inc., une entreprise des "
        "États-Unis, qui les chiffre et protège le site des attaques. Cloudflare déchiffre la "
        "connexion sur ses serveurs puis la transmet à mon serveur par un tunnel chiffré : ce "
        "que vous envoyez au site, y compris dans la bulle d'aide et le formulaire de bogue, "
        "passe donc par les serveurs de Cloudflare.",
        "Every connection to the site goes through Cloudflare, Inc., a company in the United "
        "States, which encrypts it and shields the site from attacks. Cloudflare decrypts the "
        "connection on its servers, then passes it to my server through an encrypted tunnel: "
        "what you send to the site, including in the help bubble and the bug form, therefore "
        "passes through Cloudflare's servers."),
      P("Le fichier ISO est servi par le stockage de Cloudflare (dl.rayelinux.com). Cloudflare "
        "voit donc votre adresse IP et les pages et fichiers demandés, et ces renseignements "
        "peuvent être traités hors du Québec et du Canada, selon sa propre politique de "
        "confidentialité. Cloudflare essaie d'ajouter un script de mesure d'audience aux "
        "pages ; la politique de sécurité du site le bloque, il ne s'exécute pas.",
        "The ISO file is served from Cloudflare's storage (dl.rayelinux.com). Cloudflare "
        "therefore sees your IP address and the pages and files you ask for, and this can be "
        "processed outside Québec and Canada, under its own privacy policy. Cloudflare tries "
        "to add an audience measurement script to the pages; the site's security policy blocks "
        "it, so it never runs."),
      P("La base : mon intérêt légitime à servir le site de façon sûre et rapide.",
        "The basis: my legitimate interest in serving the site safely and fast.")),
    S("browser", "Témoins et stockage dans votre navigateur", "Cookies and browser storage",
      P("Le site n'utilise <strong>aucun témoin (cookie)</strong>, aucun pixel, aucune police "
        "ni aucun script d'un tiers. Il ne mesure pas l'audience.",
        "The site uses <strong>no cookies</strong>, no pixels, and no third-party fonts or "
        "scripts. It does not measure its audience."),
      P("Une seule chose peut rester dans votre navigateur : si vous choisissez une langue "
        "avec le bouton de langue, ce choix est gardé dans le stockage local (clé "
        "« raye-lang », valeur « fr » ou « en »), sur votre appareil seulement. L'adresse "
        "rayelinux.com le lit pour vous ouvrir la bonne langue. Il n'est jamais envoyé au "
        "serveur. Pour l'effacer, videz les données du site dans votre navigateur.",
        "One thing only can stay in your browser: if you pick a language with the language "
        "button, that choice is kept in local storage (key \"raye-lang\", value \"fr\" or "
        "\"en\"), on your device only. The rayelinux.com address reads it to open the right "
        "language for you. It is never sent to the server. To clear it, clear the site's data "
        "in your browser."),
      P("La bulle d'aide et la case à cocher de la page de téléchargement ne gardent rien : "
        "tout disparaît quand vous fermez la page.",
        "The help bubble and the download page's tick box keep nothing: everything is gone "
        "when you close the page.")),
    S("discord", "Le serveur Discord", "The Discord server",
      P("La communauté se retrouve sur un serveur Discord. Discord est un service tiers, avec "
        "ses propres conditions et sa propre politique de confidentialité, et il faut avoir "
        "l'âge qu'il exige pour y aller. Ce que vous y écrivez est vu par les membres du "
        "serveur et par Discord. Les annonces y sont publiées par RivenBot, un robot Discord "
        "que je fais aussi ; ce qu'il garde est décrit dans sa propre politique, sur "
        "rivenbot.ca.",
        "The community meets on a Discord server. Discord is a third-party service with its "
        "own terms and privacy policy, and you must be the age it requires to join. What you "
        "write there is seen by the server's members and by Discord. Announcements are posted "
        "there by RivenBot, a Discord bot I also make; what it keeps is described in its own "
        "policy, on rivenbot.ca."),
      P("Les modérateurs peuvent supprimer des messages et exclure des membres selon les "
        "règles du serveur. Vous pouvez supprimer vos propres messages à tout moment.",
        "Moderators can delete messages and remove members under the server's rules. You can "
        "delete your own messages at any time.")),
    S("email", "Quand vous m'écrivez", "When you write to me",
      P("Un courriel envoyé à bonjour@rayelinux.com arrive sur mon serveur de courrier, au "
        "Québec, qui est copié chaque nuit sur un disque chez moi. Je le garde le temps de vous "
        "répondre et de suivre votre demande ; vous pouvez me demander de l'effacer ensuite. "
        "Pour une demande sur vos droits, je garde une trace de la demande et de ma réponse, "
        "parce que la loi peut me demander de prouver ma réponse.",
        "An email sent to bonjour@rayelinux.com arrives on my mail server in Québec, which is "
        "copied every night to a disk at home. I keep it while I answer and follow up your "
        "request; you can ask me to delete it afterwards. For a request about your rights, I "
        "keep a record of the request and my answer, because the law can ask me to show that I "
        "answered.")),
    S("accounts", "Les comptes Raye (quand ils ouvriront)", "Raye accounts (once they open)",
      P("Les comptes Raye ne sont <strong>pas encore ouverts</strong> : aucun serveur de "
        "comptes ne tourne. Ce qui suit décrit ce que le compte gardera, d'après son code. "
        "Raye fonctionne pareil sans compte, et rien dans le système n'en exige un.",
        "Raye accounts are <strong>not open yet</strong>: no account server is running. What "
        "follows describes what an account will keep, from its code. Raye works the same "
        "without an account, and nothing in the system needs one."),
      L(("Gardé : votre courriel, votre nom, votre photo (refaite en image de 256 pixels, ce "
         "qui retire sa position GPS et ses autres données), une liste fermée de 153 réglages "
         "de Raye (apparence, barre des tâches, langue et région, accessibilité et quelques "
         "autres), votre bibliothèque d'applications du Store et une ligne par PC.",
         "Kept: your email, your name, your picture (redrawn as a 256-pixel image, which "
         "removes its GPS location and other data), a closed list of 153 Raye settings "
         "(appearance, taskbar, language and region, accessibility and a few more), your Store "
         "app library and one row per PC."),
        ("Jamais lisibles : votre mot de passe, vos jetons et vos codes de secours ne sont "
         "gardés que sous forme d'empreinte ; votre secret de validation en deux étapes est "
         "scellé par une clé qui n'est pas dans la base.",
         "Never readable: your password, tokens and recovery codes are only kept as hashes; "
         "your two-step secret is sealed with a key that is not in the database."),
        ("Pas gardé : votre adresse IP, ce que vous naviguez, vos fichiers, ce que vous "
         "lancez, quand vous utilisez votre PC. Le serveur ne tient aucun journal des "
         "demandes. Mots de passe Wi-Fi et autres mots de passe : pas synchronisés.",
         "Not kept: your IP address, what you browse, your files, what you run, when you use "
         "your PC. The server keeps no request log. Wi-Fi and other passwords: not "
         "synced."),
        ("Le site des comptes utilisera un témoin de session et, si vous choisissez une "
         "langue, un témoin qui la retient ; aucun autre.",
         "The accounts site will set one session cookie and, if you pick a language, one "
         "cookie that remembers it; no other."),
        ("Vous pourrez tout exporter en un fichier et supprimer le compte en une fois, avec "
         "votre mot de passe. La base sera alors l'exécution du service que vous demandez.",
         "You will be able to export everything as one file and delete the account in one go, "
         "with your password. The basis will then be performing the service you ask for.")),
      P("Avant l'ouverture, cette section sera complétée (où tourne le serveur, durée des "
        "sauvegardes après une suppression) et datée dans l'historique plus bas.",
        "Before they open, this section will be completed (where the server runs, how long "
        "backups last after a deletion) and dated in the history below.")),
    S("software", "Ce que Raye Linux contacte depuis votre PC", "What Raye Linux contacts from your PC",
      L(("<strong>Raye Update</strong> télécharge les mises à jour de Raye depuis "
         "dl.rayelinux.com (Cloudflare) et raye-linux.github.io (GitHub), et celles du "
         "système de base depuis ses serveurs officiels, puisque Raye est basé sur Ubuntu "
         "26.04 LTS.",
         "<strong>Raye Update</strong> downloads Raye's updates from dl.rayelinux.com "
         "(Cloudflare) and raye-linux.github.io (GitHub), and the base system's updates from "
         "its official servers, since Raye is based on Ubuntu 26.04 LTS."),
        ("Les mises à jour de micrologiciel viennent du service public LVFS, quand vous les "
         "acceptez.",
         "Firmware updates come from the public LVFS service, when you accept them."),
        ("Le Store contacte Flathub pour les applications et odrs.gnome.org pour les avis.",
         "The Store contacts Flathub for apps and odrs.gnome.org for reviews."),
        ("Firefox se met à jour depuis le dépôt de Mozilla.",
         "Firefox updates from Mozilla's repository.")),
      P("Comme tout téléchargement, ces serveurs voient l'adresse IP de votre PC et ce qui "
        "est téléchargé, selon leurs propres règles. Raye n'envoie <strong>aucun rapport "
        "d'utilisation ni rapport de plantage</strong> : les outils qui le faisaient sont "
        "retirés de l'image. Ce que vous faites sur votre PC reste sur votre PC.",
        "Like any download, these servers see your PC's IP address and what is downloaded, "
        "under their own rules. Raye sends <strong>no usage reports and no crash "
        "reports</strong>: the tools that did are removed from the image. What you do on your "
        "PC stays on your PC.")),
    S("bases", "Pourquoi et sur quelle base, en résumé", "Purposes and legal bases, in short",
      P("Je n'utilise vos renseignements que pour ces fins. Je ne les vends pas, je ne les "
        "loue pas, je ne les utilise pas pour de la publicité ni pour établir un profil.",
        "I only use your information for these purposes. I don't sell it, rent it out, or use "
        "it for advertising or profiling."),
      T([("Traitement", "Processing"), ("Fin", "Purpose"), ("Base", "Basis")],
        [("Liste de courriels", "Mailing list"),
         ("vous prévenir du lancement, nouvelles si demandées",
          "tell you about the launch, news if asked"),
         ("consentement exprès", "express consent")],
        [("Bulle d'aide", "Help bubble"),
         ("répondre à votre question", "answer your question"),
         ("votre demande", "your request")],
        [("Rapport de bogue", "Bug report"),
         ("corriger Raye, vous recontacter", "fix Raye, get back to you"),
         ("consentement", "consent")],
        [("Vérification des rapports", "Checking reports"),
         ("forum lisible, sans abus", "a readable forum, free of abuse"),
         ("intérêt légitime", "legitimate interest")],
        [("Limites par adresse IP", "Per-address limits"),
         ("bloquer les abus", "block abuse"),
         ("intérêt légitime", "legitimate interest")],
        [("Journaux, Cloudflare", "Logs, Cloudflare"),
         ("sécurité, dépannage, service du site", "security, troubleshooting, serving the site"),
         ("intérêt légitime", "legitimate interest")],
        [("Vos courriels", "Your emails"),
         ("vous répondre, prouver une réponse", "answer you, show an answer was given"),
         ("votre demande, obligation légale", "your request, legal duty")])),
    S("recipients", "Qui reçoit vos renseignements, et hors du Québec",
      "Who receives your information, and outside Québec",
      P("Personne d'autre que moi n'a accès à la liste de courriels, aux journaux et à mes "
        "serveurs. Les seules entreprises sur le chemin de vos renseignements sont :",
        "Nobody but me has access to the mailing list, the logs and my servers. The only "
        "companies on the path of your information are:"),
      T([("Entreprise", "Company"), ("Rôle", "Role"), ("Pays", "Country")],
        [("Cloudflare, Inc.", "Cloudflare, Inc."),
         ("connexions au site, protection, fichiers à télécharger",
          "site connections, protection, downloads"),
         ("États-Unis", "United States")],
        [("Contabo GmbH", "Contabo GmbH"),
         ("passage des courriels sortants", "outgoing emails pass through"),
         ("Allemagne", "Germany")],
        [("Discord, Inc.", "Discord, Inc."),
         ("forum #bugs, salon privé de l'équipe, communauté",
          "#bugs forum, private staff channel, community"),
         ("États-Unis", "United States")]),
      P("Ces pays n'ont pas les mêmes lois que le Québec : un gouvernement étranger peut, "
        "selon ses lois, demander l'accès aux renseignements qu'une entreprise y garde. Je "
        "limite ce qui y va au strict nécessaire : rien de la liste de courriels ni de la "
        "bulle d'aide n'est gardé chez ces entreprises, et un rapport de bogue n'y va que si "
        "vous l'envoyez.",
        "These countries don't have the same laws as Québec: a foreign government can, under "
        "its laws, ask for access to information a company keeps there. I keep what goes "
        "there to what is needed: nothing from the mailing list or the help bubble is kept by "
        "these companies, and a bug report only goes there if you send it."),
      P("Je ne communiquerai vos renseignements à une autorité que si une loi m'y oblige, et "
        "je vous en préviendrai si la loi me le permet.",
        "I will only give your information to an authority if a law requires it, and I will "
        "tell you if the law allows me to.")),
    S("security", "Comment vos renseignements sont protégés", "How your information is protected",
      L(("Chaque service tourne dans sa propre machine, derrière son propre pare-feu ; le "
         "serveur du site n'accepte que le serveur d'entrée, et toute connexion "
         "d'administration passe par une passerelle qui la trace.",
         "Each service runs in its own machine, behind its own firewall; the site's server only "
         "accepts the front server, and every administration connection goes through a "
         "gateway that records it."),
        ("La base de la liste de courriels n'est lisible que par le service du site ; les "
         "réglages du courrier sont lus comme des secrets, jamais écrits dans les journaux.",
         "The mailing list database is only readable by the site's service; the mail settings "
         "are read as secrets and never written to logs."),
        ("Les jetons des liens de courriel ne sont gardés que sous forme d'empreinte, et "
         "expirent.",
         "Email link tokens are only kept as hashes, and expire."),
        ("Le site interdit tout script, police ou image d'ailleurs, et ses pages ne peuvent "
         "pas être affichées dans un autre site.",
         "The site forbids any script, font or image from elsewhere, and its pages can't be "
         "shown inside another site."),
        ("Les connexions sont chiffrées de votre navigateur jusqu'à chez moi.",
         "Connections are encrypted from your browser to my home.")),
      P("Aucune mesure n'est parfaite. Si vous trouvez une faille, écrivez-moi à {contact} "
        "avant d'en parler publiquement, pour que je puisse la corriger.",
        "No measure is perfect. If you find a security hole, write to me at {contact} before "
        "talking about it publicly, so I can fix it.")),
    S("rights", "Vos droits, et comment les exercer", "Your rights, and how to use them",
      P("Vous pouvez, à tout moment et sans frais :",
        "You can, at any time and at no cost:"),
      L(("<strong>savoir</strong> si je garde des renseignements sur vous, et les "
         "<strong>consulter</strong> ;",
         "<strong>know</strong> whether I keep information about you, and "
         "<strong>see</strong> it;"),
        ("les faire <strong>corriger</strong> s'ils sont inexacts, incomplets ou "
         "équivoques ;",
         "have it <strong>corrected</strong> if it is wrong, incomplete or unclear;"),
        ("les faire <strong>effacer</strong>, et faire cesser leur diffusion (par exemple un "
         "rapport publié) ;",
         "have it <strong>deleted</strong>, and its spread stopped (a posted report, for "
         "example);"),
        ("en recevoir une <strong>copie</strong> dans un format courant et lisible par "
         "ordinateur ;",
         "get a <strong>copy</strong> of it in a common, machine-readable format;"),
        ("<strong>retirer votre consentement</strong> (chaque courriel a un lien de "
         "désabonnement en un clic) ;",
         "<strong>withdraw your consent</strong> (every email has a one-click unsubscribe "
         "link);"),
        ("être informé d'une décision prise automatiquement à votre sujet, de ses raisons, "
         "et demander qu'une personne la revoie ;",
         "be told about a decision made automatically about you, its reasons, and ask a "
         "person to look at it again;"),
        ("dans l'Union européenne, aussi vous <strong>opposer</strong> à un traitement fondé "
         "sur l'intérêt légitime et en demander la <strong>limitation</strong>.",
         "in the European Union, also <strong>object</strong> to processing based on "
         "legitimate interest and ask for it to be <strong>restricted</strong>.")),
      H("Comment faire", "How to do it"),
      OL(("Écrivez à {contact}, de préférence depuis l'adresse concernée.",
          "Write to {contact}, preferably from the address concerned."),
         ("Dites ce que vous voulez : consulter, corriger, effacer, recevoir une copie. Pour "
          "un rapport de bogue, donnez son titre ou la date.",
          "Say what you want: see, correct, delete, get a copy. For a bug report, give its "
          "title or date."),
         ("Je peux vous demander de prouver que l'adresse ou le rapport est le vôtre, et "
          "rien de plus.",
          "I may ask you to show that the address or the report is yours, and nothing "
          "more."),
         ("Je réponds par écrit dans un délai de <strong>30 jours</strong>. Si je refuse, je "
          "vous dis pourquoi et quels recours vous avez.",
          "I answer in writing within <strong>30 days</strong>. If I refuse, I tell you why and "
          "what you can do about it.")),
      P("Pour la liste de courriels, le lien de désabonnement suffit : il ne demande rien "
        "d'autre et l'effet est immédiat.",
        "For the mailing list, the unsubscribe link is enough: it asks for nothing else and "
        "works at once."),
      H("Si ma réponse ne vous satisfait pas", "If my answer doesn't satisfy you"),
      P("Vous pouvez porter plainte auprès de la Commission d'accès à l'information du Québec "
        "(cai.gouv.qc.ca). Ailleurs au Canada, vous pouvez vous adresser au Commissariat à la "
        "protection de la vie privée du Canada. Dans l'Union européenne, vous pouvez porter "
        "plainte auprès de l'autorité de protection des données de votre pays.",
        "You can complain to the Commission d'accès à l'information du Québec "
        "(cai.gouv.qc.ca). Elsewhere in Canada, you can contact the Office of the Privacy "
        "Commissioner of Canada. In the European Union, you can complain to your country's "
        "data protection authority.")),
    S("incidents", "Incidents de sécurité", "Security incidents",
      P("Si un incident touche vos renseignements (un accès, une perte ou une fuite non "
        "autorisés), je prends tout de suite les mesures pour en réduire l'effet et éviter "
        "qu'il se reproduise. S'il présente un risque de préjudice sérieux, je vous préviens, "
        "ainsi que la Commission d'accès à l'information, sans attendre. Chaque incident, "
        "même sans risque sérieux, est noté dans un registre des incidents.",
        "If an incident affects your information (unauthorized access, loss or leak), I take "
        "steps at once to limit it and keep it from happening again. If it carries a risk of "
        "serious harm, I tell you and the Commission d'accès à l'information without delay. "
        "Every incident, even one with no serious risk, is written down in an incident "
        "register.")),
    S("minors", "Les mineurs", "Children",
      P("Le site ne s'adresse pas aux enfants et ne recueille rien sur eux à dessein. Si vous "
        "avez moins de 14 ans, un parent ou tuteur doit consentir pour vous avant que vous "
        "vous inscriviez à la liste ou envoyiez un rapport de bogue. Si vous pensez qu'un "
        "enfant m'a donné des renseignements sans ce consentement, écrivez-moi : je les "
        "efface.",
        "The site is not meant for children and does not knowingly collect anything about "
        "them. If you are under 14, a parent or guardian must consent for you before you join "
        "the mailing list or send a bug report. If you think a child gave me information "
        "without that consent, write to me: I delete it.")),
    S("changes", "Changements et historique", "Changes and history",
      P("Si cette politique change, la date et la version en haut de la page changent aussi, "
        "et la liste ci-dessous dit ce qui a changé. Si un changement touche ce que vous avez "
        "accepté (la liste de courriels, par exemple), je vous le demande de nouveau avant de "
        "l'appliquer à vos renseignements.",
        "If this policy changes, the date and version at the top change too, and the list "
        "below says what changed. If a change affects what you agreed to (the mailing list, "
        "for example), I ask you again before it applies to your information."),
      L(("<strong>3.0, 14 novembre 2026</strong> : politique réécrite en entier : mots "
         "utilisés, tableau des durées, bases de chaque traitement, entreprises et pays, "
         "mesures de sécurité, façon d'exercer vos droits, décision automatisée des rapports "
         "de bogue ; nombre de réglages des comptes corrigé (153) ; pages déplacées sous /fr/ "
         "et /en/.",
         "<strong>3.0, November 14, 2026</strong>: policy rewritten in full: words used, "
         "retention table, basis of each processing, companies and countries, security "
         "measures, how to use your rights, automated decision on bug reports; number of "
         "account settings corrected (153); pages moved under /fr/ and /en/."),
        ("<strong>2.1, 14 novembre 2026</strong> : vérification des rapports de bogue avant "
         "publication, moyen de vous joindre envoyé seulement à l'équipe.",
         "<strong>2.1, November 14, 2026</strong>: bug reports checked before they are "
         "posted, how to reach you sent to the team only."),
        ("<strong>2.0, 14 novembre 2026</strong> : politique réécrite à partir de ce que les "
         "serveurs gardent ; bulle d'aide, rapports de bogue, journaux, Cloudflare, comptes "
         "et logiciel.",
         "<strong>2.0, November 14, 2026</strong>: policy rewritten from what the servers "
         "keep; help bubble, bug reports, logs, Cloudflare, accounts and software."),
        ("<strong>1.0, 31 octobre 2026</strong> : première version, pour la liste de "
         "courriels (texte de consentement du 31 octobre 2026).",
         "<strong>1.0, October 31, 2026</strong>: first version, for the mailing list "
         "(consent text of October 31, 2026)."))),
]

# --- terms of use --------------------------------------------------------------

TERMS_SUMMARY = [
    ("Raye Linux est gratuit et libre (GPL et autres licences libres). Ces conditions "
     "n'enlèvent rien à ces licences.",
     "Raye Linux is free, as in price and in freedom (GPL and other free licenses). These "
     "terms take nothing away from those licenses."),
    ("C'est une bêta : sauvegardez vos fichiers avant d'installer. L'installation peut "
     "effacer le disque choisi.",
     "It is a beta: back up your files before you install. Installing can erase the disk "
     "you pick."),
    ("Le logiciel est fourni tel quel, sans garantie, dans la mesure permise par la loi. "
     "Vos droits de consommateur au Québec restent entiers.",
     "The software comes as is, with no warranty, to the extent the law allows. Your rights "
     "as a consumer in Québec stay whole."),
    ("Utilisez le site, la bulle d'aide et le formulaire de bogue de bonne foi : pas d'abus, "
     "pas d'attaque, pas de contenu illégal.",
     "Use the site, the help bubble and the bug form in good faith: no abuse, no attacks, no "
     "illegal content."),
    ("Ce que vous envoyez reste à vous ; vous me permettez de le publier dans le forum #bugs "
     "pour corriger Raye.",
     "What you send stays yours; you let me post it in the #bugs forum to fix Raye."),
    ("Lois du Québec, tribunaux du Québec, sans clause d'arbitrage.",
     "Québec law, Québec courts, no arbitration clause."),
]

TERMS = [
    S("about", "À propos de ces conditions", "About these terms",
      P("Ces conditions s'appliquent au site rayelinux.com (y compris sa bulle d'aide, son "
        "formulaire de bogue et sa liste de courriels), au logiciel Raye Linux et, quand ils "
        "ouvriront, aux comptes Raye. En les utilisant, vous acceptez ces conditions. Si vous "
        "ne les acceptez pas, n'utilisez pas le site ou le service concerné.",
        "These terms apply to the rayelinux.com website (including its help bubble, bug form "
        "and mailing list), to the Raye Linux software and, once they open, to Raye accounts. "
        "By using them, you accept these terms. If you don't accept them, don't use the site "
        "or service concerned."),
      P("La {privacy} dit comment vos renseignements sont traités ; elle fait partie de ces "
        "conditions. Les licences de chaque composant de Raye, présentées sur la page {licenses}, "
        "s'appliquent en plus et l'emportent en cas de conflit pour ce qui touche au logiciel.",
        "The {privacy} says how your information is handled; it is part of these terms. The "
        "licenses of each part of Raye, listed on the {licenses} page, apply on top and win if "
        "they disagree, for anything about the software."),
      P("Ces conditions existent en français et en anglais. En cas de différence, la version "
        "française l'emporte.",
        "These terms exist in French and English. If they differ, the French version "
        "prevails.")),
    S("definitions", "Les mots utilisés ici", "Words used here",
      L(("<strong>Je</strong>, <strong>moi</strong> : la personne qui fait Raye Linux, "
         "présentée dans les {notice}.",
         "<strong>I</strong>, <strong>me</strong>: the person who makes Raye Linux, introduced "
         "in the {notice}."),
        ("<strong>Vous</strong> : la personne qui utilise le site, le logiciel ou un compte.",
         "<strong>You</strong>: the person using the site, the software or an account."),
        ("<strong>Consommateur</strong> : une personne qui utilise Raye pour elle-même, et "
         "non pour une entreprise, au sens de la Loi sur la protection du consommateur.",
         "<strong>Consumer</strong>: a person who uses Raye for themselves, not for a "
         "business, as the Consumer Protection Act means it."),
        ("<strong>Contenu</strong> : ce que vous envoyez par le site : questions, rapports, "
         "étapes, captures d'écran, coordonnées.",
         "<strong>Content</strong>: what you send through the site: questions, reports, "
         "steps, screenshots, contact details."),
        ("<strong>Bêta</strong> : une version publiée avant la version finale, pour être "
         "essayée et corrigée.",
         "<strong>Beta</strong>: a version released before the final one, to be tried and "
         "fixed."))),
    S("who-can", "Qui peut utiliser le site et le logiciel", "Who can use the site and software",
      L(("Tout le monde peut lire le site et télécharger Raye.",
         "Anyone can read the site and download Raye."),
        ("Pour vous inscrire à la liste ou envoyer un rapport de bogue, vous devez avoir 14 "
         "ans ou plus, ou l'accord d'un parent ou tuteur.",
         "To join the mailing list or send a bug report, you must be 14 or older, or have a "
         "parent's or guardian's consent."),
        ("Pour le serveur Discord, vous devez avoir l'âge exigé par Discord.",
         "For the Discord server, you must be the age Discord requires."),
        ("Si vous utilisez Raye pour une entreprise ou un organisme, vous confirmez pouvoir "
         "accepter ces conditions en son nom.",
         "If you use Raye for a business or organization, you confirm you can accept these "
         "terms on its behalf."))),
    S("site", "Utiliser le site", "Using the site",
      P("Vous pouvez lire, partager et lier le site librement, et en citer de courts extraits "
        "avec un lien. En retour, vous vous engagez à ne pas :",
        "You can read, share and link to the site freely, and quote short extracts with a "
        "link. In return, you agree not to:"),
      L(("essayer de le perturber, de le surcharger ou de contourner ses limites (nombre de "
         "questions, de rapports, d'inscriptions) ;",
         "try to disrupt or overload it, or get around its limits (number of questions, "
         "reports, signups);"),
        ("chercher à accéder à ce qui n'est pas public, ou tester ses failles sans m'avoir "
         "prévenu ;",
         "try to reach what isn't public, or probe it for security holes without telling me "
         "first;"),
        ("l'interroger avec des robots en masse, ou en recopier le contenu pour le présenter "
         "comme le vôtre ;",
         "query it with bots in bulk, or copy its content to present it as your own;"),
        ("inscrire l'adresse courriel de quelqu'un d'autre à la liste ;",
         "sign up someone else's email address to the list;"),
        ("vous faire passer pour moi, pour l'équipe ou pour Raye Linux.",
         "pretend to be me, the team or Raye Linux.")),
      P("Le site peut être indisponible, changer ou fermer une partie de ses fonctions, "
        "notamment pendant la bêta.",
        "The site can be unavailable, change, or close some of its features, especially "
        "during the beta.")),
    S("help", "La bulle d'aide", "The help bubble",
      P("Les réponses de la bulle d'aide sont produites automatiquement par un modèle de "
        "langue, à partir du manuel et des pages du site. Elles peuvent être incomplètes ou "
        "fausses et ne remplacent ni le manuel, ni l'aide d'une personne, ni un conseil "
        "professionnel (juridique, financier, de sécurité). Vérifiez avant d'agir sur une "
        "réponse, surtout avant de toucher à vos disques.",
        "The help bubble's answers are produced automatically by a language model, from the "
        "handbook and the site's pages. They can be incomplete or wrong and don't replace the "
        "handbook, help from a person, or professional advice (legal, financial, security). "
        "Check before you act on an answer, especially before touching your disks."),
      P("N'y écrivez pas de renseignements personnels, de mots de passe ni de renseignements "
        "sur d'autres personnes.",
        "Don't write personal information, passwords or information about other people "
        "there.")),
    S("content", "Rapports de bogue et ce que vous envoyez", "Bug reports and what you send",
      P("Ce que vous envoyez reste à vous. En l'envoyant, vous me donnez le droit, gratuit et "
        "pour le monde entier, de le publier dans le forum #bugs de notre serveur Discord, "
        "de le raccourcir ou d'en retirer des renseignements personnels, d'y répondre, de le "
        "traduire et de m'en servir pour corriger et améliorer Raye. Ce droit prend fin quand "
        "le rapport est supprimé, sauf pour ce qui a déjà servi à corriger Raye.",
        "What you send stays yours. By sending it, you give me a free, worldwide right to post "
        "it in the #bugs forum of our Discord server, shorten it or remove personal "
        "information from it, reply to it, translate it, and use it to fix and improve Raye. "
        "That right ends when the report is deleted, except for what has already been used to "
        "fix Raye."),
      P("Vous confirmez avoir le droit d'envoyer ce contenu, en particulier la capture d'écran : "
        "elle ne doit pas montrer de renseignements sur d'autres personnes, de mots de passe, "
        "ni rien d'illégal. N'envoyez pas de rapport faux, injurieux, publicitaire ou qui "
        "n'a rien à voir avec Raye.",
        "You confirm you have the right to send this content, the screenshot in particular: it "
        "must not show information about other people, passwords, or anything illegal. Don't "
        "send false, abusive, promotional or unrelated reports."),
      P("Un rapport de bogue n'est pas une demande d'assistance garantie : je lis les "
        "rapports, mais je ne promets ni réponse ni délai de correction.",
        "A bug report is not a guaranteed support request: I read the reports, but I promise "
        "neither an answer nor a time to fix.")),
    S("moderation", "Modération", "Moderation",
      P("Avant d'être publié, chaque rapport est vérifié automatiquement, comme l'explique la "
        "{privacy}. Il peut être publié, retenu pour qu'une personne le relise, ou écarté. "
        "Même publié, un rapport peut être modifié, fermé ou supprimé par l'équipe s'il "
        "enfreint ces conditions, s'il contient des renseignements personnels, ou une fois le "
        "bogue corrigé.",
        "Before it is posted, every report is checked automatically, as the {privacy} "
        "explains. It can be posted, held for a person to read, or dropped. Even once posted, "
        "a report can be edited, closed or deleted by the team if it breaks these terms, holds "
        "personal information, or once the bug is fixed."),
      P("Si vous pensez qu'un rapport a été écarté ou retiré à tort, écrivez à {contact} : "
        "une personne le revoit et vous répond.",
        "If you think a report was dropped or removed by mistake, write to {contact}: a person "
        "looks at it again and answers you.")),
    S("community", "La communauté Discord", "The Discord community",
      P("Le serveur Discord suit les conditions de Discord et ses propres règles, affichées "
        "dans le serveur. Soyez respectueux : pas de harcèlement, de haine, de menace, de "
        "pourriel ni de contenu illégal. Les modérateurs peuvent supprimer des messages, "
        "rendre muet ou exclure un membre qui enfreint ces règles.",
        "The Discord server follows Discord's terms and its own rules, shown in the server. Be "
        "respectful: no harassment, hate, threats, spam or illegal content. Moderators can "
        "delete messages, mute or remove a member who breaks these rules.")),
    S("mailing-list", "La liste de courriels", "The mailing list",
      P("La liste sert à vous prévenir du lancement et, si vous l'avez demandé, à vous donner "
        "de rares nouvelles. Elle est gratuite. Vous pouvez vous désabonner en un clic depuis "
        "n'importe quel courriel.",
        "The list is there to tell you about the launch and, if you asked for it, to send "
        "occasional news. It is free. You can unsubscribe in one click from any email.")),
    S("license", "Le logiciel est libre", "The software is free",
      P("Raye Linux est un logiciel libre, fourni gratuitement. Chaque composant est sous sa "
        "propre licence, le plus souvent la GNU GPL : vous pouvez l'utiliser pour tout usage, "
        "l'étudier, le copier, le partager et le modifier selon cette licence. Ces conditions "
        "n'enlèvent aucun des droits que ces licences vous donnent. Le détail et la façon "
        "d'obtenir le code source sont sur la page {licenses}.",
        "Raye Linux is free software, given at no cost. Each part is under its own license, "
        "most often the GNU GPL: you can use it for any purpose, study, copy, share and change "
        "it under that license. These terms take away none of the rights those licenses give "
        "you. The details and how to get the source code are on the {licenses} page."),
      P("Les licences libres portent sur le code, pas sur le nom « Raye Linux » ni sur l'œil "
        "de Raye : si vous partagez une version modifiée, donnez-lui un autre nom et un autre "
        "logo, comme l'explique la page {licenses}.",
        "Free licenses cover the code, not the \"Raye Linux\" name or the Raye eye: if you "
        "share a changed version, give it another name and logo, as the {licenses} page "
        "explains.")),
    S("beta", "Raye est une bêta", "Raye is a beta",
      P("La version actuelle est une <strong>bêta publique</strong>. Elle peut contenir des "
        "bogues, planter, ne pas fonctionner avec votre matériel et, dans de rares cas, faire "
        "perdre des données. En particulier :",
        "The current version is a <strong>public beta</strong>. It can have bugs, crash, not "
        "work with your hardware and, in rare cases, lose data. In particular:"),
      L(("l'installation peut <strong>effacer tout le disque choisi</strong> ; installer à "
         "côté d'un autre système demande de redimensionner des partitions, ce qui comporte "
         "toujours un risque ;",
         "installing can <strong>erase the whole disk you pick</strong>; installing next to "
         "another system means resizing partitions, which always carries a risk;"),
        ("des mises à jour peuvent changer ou retirer des fonctions, et une mise à jour de "
         "bêta peut demander de réinstaller ;",
         "updates can change or remove features, and a beta update may require reinstalling;"),
        ("les applications d'autres systèmes peuvent ne pas toutes fonctionner.",
         "apps from other systems may not all work.")),
      P("<strong>Sauvegardez vos fichiers avant d'installer</strong>, vérifiez l'image "
        "téléchargée avec la somme de contrôle et la signature données sur la page "
        "{download}, et n'utilisez pas la bêta pour un usage où une panne pourrait blesser "
        "quelqu'un ou causer un dommage important (matériel médical, sécurité, contrôle "
        "industriel).",
        "<strong>Back up your files before you install</strong>, check the downloaded image "
        "with the checksum and signature given on the {download} page, and don't use the beta "
        "where a failure could hurt someone or cause serious damage (medical equipment, "
        "safety, industrial control)."),
      P("Le téléchargement de la bêta demande de cocher une case qui reprend ces "
        "avertissements ; elle ne remplace pas ces conditions, elle les rappelle.",
        "Downloading the beta asks you to tick a box that repeats these warnings; it doesn't "
        "replace these terms, it reminds you of them.")),
    S("accounts", "Les comptes Raye (quand ils ouvriront)", "Raye accounts (once they open)",
      L(("Un compte est personnel. Gardez votre mot de passe et vos codes de secours pour "
         "vous, et prévenez-moi si vous pensez qu'on y a accédé.",
         "An account is personal. Keep your password and recovery codes to yourself, and tell "
         "me if you think someone got in."),
        ("Donnez une adresse courriel qui est la vôtre et que vous lisez.",
         "Give an email address that is yours and that you read."),
        ("N'utilisez pas votre compte pour stocker ou diffuser du contenu illégal, attaquer le "
         "service ou nuire à d'autres personnes.",
         "Don't use your account to store or share illegal content, attack the service or "
         "harm other people."),
        ("Vous pouvez exporter vos données et supprimer votre compte à tout moment ; tout est "
         "effacé en une fois.",
         "You can export your data and delete your account at any time; everything goes at "
         "once."),
        ("Je peux suspendre ou fermer un compte qui enfreint ces règles ou met le service en "
         "danger. Sauf urgence, je vous préviens d'abord et vous dis pourquoi.",
         "I can suspend or close an account that breaks these rules or puts the service at "
         "risk. Except in an emergency, I tell you first and say why."))),
    S("warranty", "Garanties", "Warranties",
      P("Raye Linux et le site sont fournis gratuitement, <strong>tels quels, sans aucune "
        "garantie</strong>, expresse ou implicite, dans la mesure permise par la loi : je ne "
        "garantis pas qu'ils seront sans bogue, sans interruption, adaptés à un usage précis "
        "ou compatibles avec votre matériel. Les licences libres de Raye disent la même "
        "chose.",
        "Raye Linux and the site are given at no cost, <strong>as is, with no warranty</strong>, "
        "express or implied, to the extent the law allows: I don't promise they will be free "
        "of bugs or interruptions, fit for a given purpose or compatible with your hardware. "
        "Raye's free licenses say the same."),
      P("<strong>Si vous êtes un consommateur au Québec</strong>, rien dans ces conditions ne "
        "vous prive des garanties ni des droits que vous donnent la Loi sur la protection du "
        "consommateur et le Code civil du Québec, auxquels on ne peut pas renoncer. Ailleurs, "
        "les garanties que votre loi impose et qu'on ne peut pas exclure s'appliquent aussi.",
        "<strong>If you are a consumer in Québec</strong>, nothing in these terms takes away "
        "the warranties or rights you have under the Consumer Protection Act and the Civil "
        "Code of Québec, which can't be waived. Elsewhere, warranties your law imposes and "
        "that can't be excluded apply too.")),
    S("liability", "Responsabilité", "Liability",
      P("Dans la mesure permise par la loi, je ne suis pas responsable des dommages indirects "
        "causés par l'utilisation de Raye Linux ou du site, y compris la perte de données, de "
        "temps ou de revenus, ni des services d'autres entreprises (Discord, Cloudflare, "
        "Flathub, les applications que vous installez).",
        "To the extent the law allows, I am not liable for indirect damage caused by using "
        "Raye Linux or the site, including loss of data, time or income, nor for the services "
        "of other companies (Discord, Cloudflare, Flathub, the apps you install)."),
      P("Cette limite ne s'applique jamais à un préjudice corporel ou moral, ni à un dommage "
        "causé par ma faute intentionnelle ou ma faute lourde. Si vous êtes un consommateur "
        "au Québec, elle ne s'applique que dans la mesure où la Loi sur la protection du "
        "consommateur le permet. Si vous n'êtes pas un consommateur, ma responsabilité totale "
        "est limitée à 100 dollars canadiens, puisque Raye vous est donné gratuitement.",
        "This limit never applies to bodily or moral injury, nor to damage caused by my "
        "intentional or gross fault. If you are a consumer in Québec, it only applies to the "
        "extent the Consumer Protection Act allows. If you are not a consumer, my total "
        "liability is limited to 100 Canadian dollars, since Raye is given to you at no "
        "cost.")),
    S("indemnity", "Indemnisation", "Indemnity",
      P("Si vous n'êtes pas un consommateur, et dans la mesure permise par la loi, vous "
        "m'indemnisez des réclamations de tiers causées par votre violation de ces conditions "
        "ou par le contenu que vous avez envoyé. Cette section ne s'applique pas aux "
        "consommateurs.",
        "If you are not a consumer, and to the extent the law allows, you indemnify me against "
        "claims from others caused by your breach of these terms or by the content you sent. "
        "This section does not apply to consumers.")),
    S("termination", "Suspension et fin", "Suspension and termination",
      P("Vous pouvez arrêter d'utiliser le site et Raye quand vous voulez ; les licences "
        "libres continuent de s'appliquer aux copies que vous avez. Je peux bloquer l'accès à "
        "la bulle d'aide, au formulaire de bogue ou à la liste pour une adresse ou une "
        "personne qui en abuse, et retirer le contenu qui enfreint ces conditions. Les "
        "sections sur les licences, les garanties, la responsabilité et la loi applicable "
        "continuent de s'appliquer après la fin.",
        "You can stop using the site and Raye whenever you want; the free licenses keep "
        "applying to the copies you have. I can block access to the help bubble, the bug form "
        "or the list for an address or person who abuses it, and remove content that breaks "
        "these terms. The sections on licenses, warranties, liability and governing law keep "
        "applying afterwards.")),
    S("changes", "Changements", "Changes",
      P("Ces conditions peuvent changer, par exemple à l'ouverture des comptes. La date et la "
        "version en haut de la page changent avec elles. Un changement important est annoncé "
        "sur le site au moins 30 jours avant de s'appliquer, sauf s'il est exigé par la loi ou "
        "par la sécurité ; il ne s'applique jamais à ce que vous avez fait avant. Si vous "
        "n'êtes pas d'accord, vous pouvez cesser d'utiliser le service concerné.",
        "These terms can change, for example when accounts open. The date and version at the "
        "top change with them. An important change is announced on the site at least 30 days "
        "before it applies, unless the law or security requires it sooner; it never applies "
        "to what you did before. If you don't agree, you can stop using the service "
        "concerned."),
      L(("<strong>3.0, 14 novembre 2026</strong> : conditions complétées : mots utilisés, "
         "âge, usage permis, contenu envoyé et modération, communauté, bêta, garanties, "
         "responsabilité, indemnisation, fin, tribunaux.",
         "<strong>3.0, November 14, 2026</strong>: terms completed: words used, age, allowed "
         "use, content sent and moderation, community, beta, warranties, liability, "
         "indemnity, termination, courts."),
        ("<strong>1.0, 14 novembre 2026</strong> : première version, avec la bêta publique.",
         "<strong>1.0, November 14, 2026</strong>: first version, with the public beta."))),
    S("law", "Loi applicable et tribunaux", "Governing law and courts",
      P("Ces conditions sont régies par les lois du Québec et les lois du Canada qui s'y "
        "appliquent. Tout litige relève des tribunaux du Québec, sous réserve des droits que "
        "la loi vous garantit : un consommateur peut toujours s'adresser aux tribunaux de son "
        "lieu de résidence. Il n'y a aucune clause d'arbitrage obligatoire et aucune "
        "renonciation aux recours collectifs.",
        "These terms are governed by the laws of Québec and the federal laws of Canada that "
        "apply there. Any dispute goes to the courts of Québec, subject to the rights the law "
        "gives you: a consumer can always go to the courts where they live. There is no "
        "mandatory arbitration clause and no waiver of class actions."),
      P("Avant d'aller en justice, écrivez-moi : la plupart des problèmes se règlent par un "
        "courriel.",
        "Before going to court, write to me: most problems are solved with an email.")),
    S("general", "Dispositions générales", "General provisions",
      L(("<strong>Divisibilité</strong> : si une clause est jugée invalide, elle est "
         "appliquée dans la mesure permise et le reste des conditions continue de "
         "s'appliquer.",
         "<strong>Severability</strong>: if a clause is found invalid, it is applied to the "
         "extent allowed and the rest of the terms keep applying."),
        ("<strong>Non-renonciation</strong> : ne pas faire valoir un droit une fois ne veut "
         "pas dire y renoncer.",
         "<strong>No waiver</strong>: not enforcing a right once doesn't mean giving it up."),
        ("<strong>Ensemble des conditions</strong> : ces conditions, la politique de "
         "confidentialité et les licences forment tout l'accord entre nous pour le site et le "
         "logiciel.",
         "<strong>Entire agreement</strong>: these terms, the privacy policy and the licenses "
         "are the whole agreement between us for the site and the software."),
        ("<strong>Force majeure</strong> : je ne suis pas responsable d'une panne due à un "
         "événement hors de mon contrôle (coupure de courant ou d'Internet, panne d'un "
         "fournisseur).",
         "<strong>Force majeure</strong>: I am not liable for an outage due to an event "
         "beyond my control (power or Internet cut, a provider's outage)."),
        ("<strong>Transfert</strong> : si le projet change de mains, ces conditions suivent, "
         "et je vous préviens sur le site.",
         "<strong>Transfer</strong>: if the project changes hands, these terms follow, and I "
         "tell you on the site."))),
    S("contact", "Contact", "Contact",
      P("Pour toute question sur ces conditions, un avis ou une réclamation : {contact}.",
        "For any question about these terms, a notice or a claim: {contact}.")),
]

# --- legal notice --------------------------------------------------------------

NOTICE_SUMMARY = [
    ("Le site et Raye Linux sont édités par une personne, au Québec, sous le pseudonyme "
     "« techoraye ».",
     "The site and Raye Linux are published by one person in Québec, under the pseudonym "
     "\"techoraye\"."),
    ("Le site tourne sur mes propres serveurs, au Québec ; les connexions passent par "
     "Cloudflare.",
     "The site runs on my own servers in Québec; connections go through Cloudflare."),
    ("Contact : bonjour@rayelinux.com.", "Contact: bonjour@rayelinux.com."),
]

NOTICE = [
    S("publisher", "Éditeur", "Publisher",
      P("Le site rayelinux.com et Raye Linux sont édités par une personne physique, au "
        "Québec (Canada), sous le pseudonyme « techoraye ». Cette personne est aussi "
        "responsable de la publication et de la protection des renseignements personnels.",
        "The rayelinux.com website and Raye Linux are published by an individual in Québec "
        "(Canada), under the pseudonym \"techoraye\". That person is also responsible for "
        "what is published and for protecting personal information."),
      P("Contact : {contact}. Je réponds en français ou en anglais.",
        "Contact: {contact}. I answer in French or English.")),
    S("hosting", "Hébergement et prestataires", "Hosting and providers",
      T([("Quoi", "What"), ("Qui", "Who"), ("Où", "Where")],
        [("Site, bulle d'aide, liste de courriels", "Site, help bubble, mailing list"),
         ("mes propres serveurs", "my own servers"),
         ("Québec, Canada", "Québec, Canada")],
        [("Connexions, protection, fichiers à télécharger (dl.rayelinux.com)",
          "Connections, protection, downloads (dl.rayelinux.com)"),
         ("Cloudflare, Inc.", "Cloudflare, Inc."),
         ("San Francisco, États-Unis", "San Francisco, United States")],
        [("Passage des courriels sortants", "Outgoing emails pass through"),
         ("Contabo GmbH", "Contabo GmbH"),
         ("Munich, Allemagne", "Munich, Germany")],
        [("Communauté, forum #bugs", "Community, #bugs forum"),
         ("Discord, Inc.", "Discord, Inc."),
         ("San Francisco, États-Unis", "San Francisco, United States")])),
    S("ownership", "Propriété intellectuelle", "Intellectual property",
      P("Le code de Raye Linux est sous licence libre : voir {licenses}. Sauf licence "
        "contraire, les textes de ce site, les images de Raye et le logo sont protégés par le "
        "droit d'auteur ; vous pouvez en citer de courts extraits avec un lien vers la page "
        "d'origine. Les captures d'écran du site montrent Raye Linux tel qu'il est.",
        "Raye Linux's code is under free licenses: see {licenses}. Unless a license says "
        "otherwise, the texts of this site, the Raye pictures and the logo are protected by "
        "copyright; you may quote short extracts with a link to the original page. The site's "
        "screenshots show Raye Linux as it is.")),
    S("links", "Liens vers d'autres sites", "Links to other sites",
      P("Le site renvoie vers notre serveur Discord et vers les serveurs de téléchargement. "
        "Je ne contrôle pas les autres sites et ne réponds pas de leur contenu ni de leurs "
        "pratiques.",
        "The site links to our Discord server and to the download servers. I don't control "
        "other sites and am not responsible for their content or practices.")),
    S("report", "Signaler un contenu ou une faille", "Reporting content or a security hole",
      P("Pour signaler un contenu illégal ou qui vous concerne (sur le site ou dans le forum "
        "#bugs), une atteinte à vos droits ou une faille de sécurité, écrivez à {contact}. "
        "Je retire sans attendre ce qui est manifestement illégal.",
        "To report content that is illegal or about you (on the site or in the #bugs forum), "
        "an infringement of your rights or a security hole, write to {contact}. I remove "
        "anything plainly illegal without waiting.")),
    S("accessibility", "Accessibilité et langues", "Accessibility and languages",
      P("Le site est fait pour se lire au clavier, avec un lecteur d'écran, en grand texte et "
        "sans animation si vous le demandez à votre système. Il existe en français, sous /fr/, "
        "et en anglais, sous /en/ ; l'adresse rayelinux.com ouvre la langue de votre "
        "navigateur. Si une page vous pose problème, dites-le-moi.",
        "The site is made to work with a keyboard, a screen reader, large text, and no motion "
        "if you ask your system for that. It exists in French, under /fr/, and in English, "
        "under /en/; the rayelinux.com address opens your browser's language. If a page gives "
        "you trouble, tell me.")),
    S("related", "Pages liées", "Related pages",
      L(("{privacy}", "{privacy}"), ("{terms}", "{terms}"), ("{licenses}", "{licenses}"))),
]

# --- licenses and trademarks ---------------------------------------------------

LICENSES_SUMMARY = [
    ("Raye Linux est un logiciel libre : vous pouvez l'utiliser, l'étudier, le partager et le "
     "modifier.",
     "Raye Linux is free software: you may use, study, share and change it."),
    ("Les outils de Raye sont sous GNU GPL 3 ; le noyau, sous GNU GPL 2 ; le manuel, sous "
     "Creative Commons BY-SA 4.0.",
     "Raye's own tools are under the GNU GPL 3; the kernel, under the GNU GPL 2; the handbook, "
     "under Creative Commons BY-SA 4.0."),
    ("Le code source de chaque version s'obtient sur demande, à bonjour@rayelinux.com.",
     "The source code of each version is available on request, at bonjour@rayelinux.com."),
    ("Le nom « Raye Linux » et l'œil de Raye ne sont pas sous licence libre : une version "
     "modifiée porte un autre nom.",
     "The \"Raye Linux\" name and the Raye eye are not under a free license: a changed "
     "version takes another name."),
]

LICENSES = [
    S("free", "Raye Linux est un logiciel libre", "Raye Linux is free software",
      P("Vous pouvez l'utiliser pour tout usage, l'étudier, le partager et le modifier, selon "
        "les licences de ses composants. Ces licences vous donnent ces libertés directement : "
        "vous n'avez rien à me demander.",
        "You may use it for any purpose, study, share and change it, under the licenses of its "
        "parts. Those licenses give you these freedoms directly: you don't need to ask me "
        "anything.")),
    S("parts", "Les licences, composant par composant", "Licenses, part by part",
      T([("Composant", "Part"), ("Licence", "License")],
        [("Applications et outils de Raye : installation, Paramètres, Store, Raye Update, "
          "thème, compte Raye, outil d'archives, image d'installation",
          "Raye's own apps and tools: setup, Settings, Store, Raye Update, theme, Raye "
          "account, archive tool, install image"),
         ("GNU GPL version 3 ou plus récente", "GNU GPL version 3 or later")],
        [("Explorateur de fichiers et changements au bureau Plasma",
          "File Explorer and changes to the Plasma desktop"),
         ("GNU GPL version 2 ou plus récente, avec des parties sous GNU LGPL",
          "GNU GPL version 2 or later, with parts under the GNU LGPL")],
        [("Style des fenêtres et des contrôles", "Window and control style"),
         ("GNU GPL version 2 ou plus récente, quelques fichiers sous licence MIT",
          "GNU GPL version 2 or later, a few files under the MIT license")],
        [("Noyau Linux de Raye", "Raye's Linux kernel"),
         ("GNU GPL version 2", "GNU GPL version 2")],
        [("Manuel de Raye, images de l'installation", "Raye handbook, setup pictures"),
         ("Creative Commons BY-SA 4.0", "Creative Commons BY-SA 4.0")],
        [("Descriptions des applications (métadonnées)", "App descriptions (metadata)"),
         ("CC0 1.0", "CC0 1.0")],
        [("Polices Inter et Cascadia Mono, police du menu de démarrage",
          "Inter and Cascadia Mono fonts, boot menu font"),
         ("SIL Open Font License 1.1", "SIL Open Font License 1.1")],
        [("Bureau KDE Plasma et autres paquets du système",
          "KDE Plasma desktop and the system's other packages"),
         ("leur propre licence, libre", "their own free license")]),
      P("Sur votre PC, la licence exacte de chaque paquet se trouve dans "
        "<code>/usr/share/doc/&lt;paquet&gt;/copyright</code>. Quelques icônes "
        "d'applications montrées dans le Store appartiennent à leurs éditeurs.",
        "On your PC, the exact license of every package is in "
        "<code>/usr/share/doc/&lt;package&gt;/copyright</code>. A few app icons shown in the "
        "Store belong to their publishers.")),
    S("gpl", "Ce que la GPL vous permet, et vous demande", "What the GPL lets you do, and asks of you",
      L(("Vous pouvez exécuter le programme pour tout usage, privé ou commercial.",
         "You may run the program for any purpose, private or commercial."),
        ("Vous pouvez l'étudier et le modifier, ce qui suppose d'avoir son code source.",
         "You may study and change it, which means having its source code."),
        ("Vous pouvez en partager des copies, modifiées ou non, gratuitement ou contre "
         "paiement.",
         "You may share copies, changed or not, for free or for a fee."),
        ("Si vous partagez une copie, vous devez donner les mêmes libertés : la même licence "
         "et l'accès au code source correspondant.",
         "If you share a copy, you must pass on the same freedoms: the same license and "
         "access to the matching source code.")),
      P("Ces licences sont fournies <strong>sans garantie</strong> ; voir aussi les "
        "{terms}.",
        "These licenses come <strong>with no warranty</strong>; see also the {terms}.")),
    S("source", "Obtenir le code source", "Getting the source code",
      P("Pour obtenir le code source correspondant à la version de Raye que vous utilisez, "
        "écrivez à {contact} en donnant la version (elle est dans Paramètres, Système, "
        "Informations système). Je vous le fournis gratuitement par téléchargement, pendant au "
        "moins trois ans après la dernière diffusion de cette version. Le code des paquets du "
        "système de base est aussi publié par leurs auteurs.",
        "To get the source code that matches the version of Raye you use, write to {contact} "
        "with the version (it is in Settings, System, About). I give it to you at no cost as a "
        "download, for at least three years after that version was last distributed. The code "
        "of the base system's packages is also published by their authors.")),
    S("contributions", "Contributions", "Contributions",
      P("Un rapport de bogue, une idée ou un correctif que vous partagez reste à vous. Un "
        "correctif de code que vous m'envoyez pour qu'il entre dans Raye est accepté sous la "
        "licence du composant qu'il modifie.",
        "A bug report, idea or fix you share stays yours. A code fix you send me to go into "
        "Raye is accepted under the license of the part it changes.")),
    S("trademarks", "Marques", "Trademarks",
      P("« Raye Linux », « Raye » dans le nom de ses outils et l'œil de Raye sont les nôtres. "
        "Ils ne sont pas sous licence libre, pour que personne ne soit trompé sur ce qui vient "
        "de nous.",
        "\"Raye Linux\", \"Raye\" in the names of its tools, and the Raye eye are our own. They "
        "are not under a free license, so that nobody is misled about what comes from us."),
      H("Ce que vous pouvez faire sans demander", "What you can do without asking"),
      L(("Parler de Raye, en faire une critique, un tutoriel ou une vidéo, et montrer le "
         "logo pour l'illustrer.",
         "Talk about Raye, review it, make a tutorial or a video about it, and show the logo "
         "to illustrate it."),
        ("Partager des copies non modifiées de l'image officielle, sous son nom.",
         "Share unchanged copies of the official image, under its name."),
        ("Dire qu'un produit « fonctionne avec Raye Linux », si c'est vrai.",
         "Say a product \"works with Raye Linux\", if it is true.")),
      H("Ce qui demande mon accord", "What needs my consent"),
      L(("Partager une version modifiée sous le nom ou avec le logo de Raye : donnez-lui un "
         "autre nom et un autre logo, et vous pouvez dire qu'elle est « basée sur Raye "
         "Linux ».",
         "Sharing a changed version under Raye's name or logo: give it another name and logo, "
         "and you may say it is \"based on Raye Linux\"."),
        ("Utiliser le nom ou le logo d'une façon qui laisse croire que je vous approuve, ou "
         "dans un nom de domaine, d'application ou de compte qui pourrait être confondu avec "
         "le projet.",
         "Using the name or logo in a way that suggests I endorse you, or in a domain, app or "
         "account name that could be mistaken for the project."))),
    S("others", "Marques d'autres entreprises", "Other companies' trademarks",
      P("Linux est une marque de Linus Torvalds. KDE et Plasma sont des marques de KDE e.V. "
        "Firefox est une marque de la Fondation Mozilla. Discord est une marque de Discord, "
        "Inc. Les autres marques citées appartiennent à leurs propriétaires.",
        "Linux is a trademark of Linus Torvalds. KDE and Plasma are trademarks of KDE e.V. "
        "Firefox is a trademark of the Mozilla Foundation. Discord is a trademark of Discord, "
        "Inc. Other marks named belong to their owners."),
      ("tm", "")),
]

SUMMARIES = {"privacy": PRIVACY_SUMMARY, "terms": TERMS_SUMMARY, "notice": NOTICE_SUMMARY,
             "licenses": LICENSES_SUMMARY}
PAGES = {"privacy": PRIVACY, "terms": TERMS, "notice": NOTICE, "licenses": LICENSES}

TITLES = {
    "privacy": {"fr": "Politique de confidentialité", "en": "Privacy policy"},
    "terms": {"fr": "Conditions d'utilisation", "en": "Terms of use"},
    "notice": {"fr": "Mentions légales", "en": "Legal notice"},
    "licenses": {"fr": "Licences et marques", "en": "Licenses and trademarks"},
}

# how a page names another one inside a sentence
LINK_WORDS = {
    "fr": {"privacy": "politique de confidentialité", "terms": "conditions d'utilisation",
           "notice": "mentions légales", "licenses": "Licences",
           "download": "Télécharger"},
    "en": {"privacy": "privacy policy", "terms": "terms of use", "notice": "legal notice",
           "licenses": "Licenses", "download": "Download"},
}


def body(page, lang, paths):
    """The page's HTML in one language. paths are the site's addresses in that
    language (build_pages.PATHS[lang])."""
    return render(PAGES[page], SUMMARIES[page], lang, paths)


def render(sections, summary, lang, paths, updated=None, version=None, words=None,
           note=None):
    """A legal page from its sections and summary. The V1 site calls it with
    its own pages (tools/legal_v1_text.py), dates and link words."""
    i = 0 if lang == "fr" else 1
    ui = UI[lang]
    updated = (updated or UPDATED)[lang]
    version = version or VERSION
    names = dict(LINK_WORDS[lang], **((words or {}).get(lang, {})))
    words = {k: f'<a href="{paths[k]}">{w}</a>' for k, w in names.items() if k in paths}
    words["contact"] = CONTACT

    def fill(text):
        return text.format(**words)

    colon = " :" if lang == "fr" else ":"
    out = [f'<p class="updated">{ui["updated"]}{colon} {updated} · {ui["version"]} '
           f'{version}</p>']
    if note:
        out.append(f'<p class="legal-draft">{note[lang]}</p>')
    items = "\n".join(f"<li>{fill(pair[i])}</li>" for pair in summary)
    out.append(f'<aside class="legal-summary" aria-labelledby="summary-title">\n'
               f'<p class="legal-summary-title" id="summary-title">{ui["summary"]}</p>\n'
               f'<ul>\n{items}\n</ul>\n</aside>')
    toc = "\n".join(f'<li><a href="#{s["id"]}">{s["title"][i]}</a></li>'
                    for s in sections)
    out.append(f'<nav class="toc" aria-labelledby="toc-title">\n'
               f'<p class="toc-title" id="toc-title">{ui["toc"]}</p>\n<ol>\n{toc}\n</ol>\n</nav>')
    for s in sections:
        part = [f'<section id="{s["id"]}" tabindex="-1">', f'<h2>{s["title"][i]}</h2>']
        for kind, data in s["blocks"]:
            if kind == "p":
                part.append(f"<p>{fill(data[i])}</p>")
            elif kind == "h3":
                part.append(f"<h3>{data[i]}</h3>")
            elif kind in ("ul", "ol"):
                lis = "\n".join(f"<li>{fill(item[i])}</li>" for item in data)
                part.append(f"<{kind}>\n{lis}\n</{kind}>")
            elif kind == "table":
                head, rows = data
                th = "".join(f'<th scope="col">{h[i]}</th>' for h in head)
                trs = "\n".join("<tr>" + "".join(f"<td>{fill(c[i])}</td>" for c in row)
                                + "</tr>" for row in rows)
                part.append(f'<div class="table-wrap"><table>\n<thead><tr>{th}</tr></thead>\n'
                            f'<tbody>\n{trs}\n</tbody>\n</table></div>')
            elif kind == "tm":
                part.append(f'<p class="tm-notice">{TRADEMARK[lang]}</p>')
        part.append("</section>")
        out.append("\n".join(part))
    out.append(f'<p class="back-top"><a href="#main">{ui["top"]}</a></p>')
    return "\n\n".join(out) + "\n"
