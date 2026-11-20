"""The legal pages of the V1 site: the privacy policy and the terms of use
of the live site with what the V1 adds (applications to join the team, the
live Community page, the beta program), and a new page, the beta program
terms. Written like tools/legal_text.py, whose helpers it uses, French and
English side by side.

These texts are a DRAFT, marked as such on every page: version 3.0 (live)
applies until the V1 site goes online. A lawyer should read them before."""

from legal_text import (H, L, P, PRIVACY, PRIVACY_SUMMARY, S, T, TERMS, TERMS_SUMMARY)

UPDATED = {"fr": "20 novembre 2026", "en": "November 20, 2026"}
VERSION = "4.0"
DRAFT = {
    "fr": "Version préparée pour la V1 du site. Elle s'appliquera à sa mise en ligne ; "
          "d'ici là, la version 3.0 publiée sur rayelinux.com reste celle qui vaut.",
    "en": "Version prepared for the V1 site. It will apply when that site goes online; until "
          "then, version 3.0 published on rayelinux.com is the one in force.",
}

# how a V1 page names the new pages inside a sentence ({betaterms}, ...)
WORDS = {
    "fr": {"betaterms": "conditions du programme bêta", "rules": "règles de la communauté",
           "join": "Rejoindre l'équipe", "community": "Communauté"},
    "en": {"betaterms": "beta program terms", "rules": "community rules",
           "join": "Join the team", "community": "Community"},
}

TITLES = {
    "betaterms": {"fr": "Conditions du programme bêta", "en": "Beta program terms"},
}


def _with_rows(section, *rows):
    """A copy of a section whose first table has more rows."""
    blocks, done = [], False
    for kind, data in section["blocks"]:
        if kind == "table" and not done:
            head, old = data
            data, done = (head, tuple(old) + rows), True
        blocks.append((kind, data))
    return dict(section, blocks=tuple(blocks))


def _insert(sections, after, *new):
    out = []
    for s in sections:
        out.append(s)
        if s["id"] == after:
            out.extend(new)
    assert len(out) == len(sections) + len(new), "section %s not found" % after
    return out


# ------------------------------------------------------------- privacy

APPLICATIONS = S(
    "applications", "Les candidatures pour rejoindre l'équipe",
    "Applications to join the team",
    P("Les pages « Rejoindre l'équipe » ont un formulaire. Quand vous l'envoyez, je garde, sur "
      "mon serveur au Québec :",
      "The \"Join the team\" pages have a form. When you send it, I keep, on my server in "
      "Québec:"),
    L(("le rôle demandé et la langue de la page ;", "the role asked for and the page language;"),
      ("votre <strong>adresse courriel</strong>, pour vous répondre (ou, quand les comptes Raye "
       "ouvriront, l'identifiant de votre compte à la place) ;",
       "your <strong>email address</strong>, to answer you (or, once Raye accounts open, your "
       "account id instead);"),
      ("votre <strong>nom d'utilisateur Discord</strong>, pour vous donner le rôle ;",
       "your <strong>Discord username</strong>, to give you the role;"),
      ("ce que vous écrivez : langues, ce que vous savez faire, pourquoi vous voulez aider ;",
       "what you write: languages, what you're good at, why you want to help;"),
      ("la version du texte d'accord que vous avez coché, et les dates : envoi, décision, "
       "rôle donné ;",
       "the version of the consent text you ticked, and the dates: sent, decided, role "
       "given;"),
      ("la décision et qui, dans l'équipe, l'a prise.",
       "the decision and who on the team made it.")),
    P("Je ne garde <strong>pas</strong> votre adresse IP : elle sert seulement, en mémoire et "
      "pendant une heure, à limiter le nombre de candidatures par visiteur.",
      "I do <strong>not</strong> keep your IP address: it is only used, in memory and for one "
      "hour, to limit the number of applications per visitor."),
    H("Qui la lit", "Who reads it"),
    P("Un message part dans un salon Discord privé de la Raye Team, pour qu'elle sache qu'une "
      "candidature attend. Il contient le rôle, votre nom Discord, vos langues, ce que vous "
      "savez faire et votre texte. Il ne contient <strong>pas</strong> votre adresse courriel, "
      "qui reste sur mon serveur. Discord est aux États-Unis : voyez la section sur les "
      "transferts plus bas. Seules les personnes de l'équipe qui étudient les candidatures y "
      "ont accès, et elles s'engagent à ne rien en faire d'autre.",
      "A message goes to a private Discord channel of the Raye Team, so it knows an "
      "application is waiting. It holds the role, your Discord name, your languages, what "
      "you're good at and your text. It does <strong>not</strong> hold your email address, "
      "which stays on my server. Discord is in the United States: see the section on "
      "transfers below. Only the people on the team who review applications can see it, and "
      "they commit to doing nothing else with it."),
    H("Combien de temps", "How long"),
    T([("Situation", "Situation"), ("Durée", "How long")],
      [("En attente de réponse", "Waiting for an answer"),
       ("180 jours au plus, puis effacée", "180 days at most, then deleted")],
      [("Refusée ou retirée", "Declined or withdrawn"),
       ("effacée 30 jours après la décision", "deleted 30 days after the decision")],
      [("Acceptée", "Accepted"),
       ("tant que vous avez le rôle ; effacée sous 30 jours quand vous le quittez",
        "as long as you hold the role; deleted within 30 days when you leave it")],
      [("Message du salon privé", "Private channel message"),
       ("supprimé en même temps que la candidature", "deleted with the application")]),
    H("Vos choix", "Your choices"),
    P("Envoyer une candidature est un choix : rien n'en dépend sur le site ni dans Raye. Vous "
      "pouvez retirer votre accord à tout moment en écrivant à {contact} ; votre candidature "
      "est alors effacée et, si vous aviez reçu un rôle, il est retiré. Vous pouvez aussi en "
      "demander une copie ou la faire corriger, comme le dit la section sur vos droits.",
      "Sending an application is a choice: nothing on the site or in Raye depends on it. You "
      "can withdraw your consent at any time by writing to {contact}; your application is "
      "then deleted and, if you had been given a role, it is removed. You can also ask for a "
      "copy or have it corrected, as the section on your rights says."),
)

COMMUNITY_PAGE = S(
    "community-page", "La page Communauté", "The Community page",
    P("La page Communauté affiche le nombre de membres du serveur Discord et combien sont en "
      "ligne. C'est mon serveur qui demande ces deux nombres à Discord, toutes les dix minutes, "
      "par l'adresse publique d'invitation ; votre navigateur ne contacte pas Discord. Rien sur "
      "vous n'est envoyé ni gardé pour cela. Si vous cliquez sur « Rejoindre le serveur "
      "Discord », vous allez sur Discord, et ses propres règles s'appliquent.",
      "The Community page shows how many members the Discord server has and how many are "
      "online. My server asks Discord for these two numbers, every ten minutes, through the "
      "public invite address; your browser does not contact Discord. Nothing about you is "
      "sent or kept for it. If you click \"Join the Discord server\", you go to Discord, and "
      "its own rules apply."),
)

BETA_CHANNELS = S(
    "beta-channels", "Le programme bêta et les canaux de mises à jour",
    "The beta program and update channels",
    P("Le programme bêta passe par les candidatures décrites plus haut. Aujourd'hui, être "
      "accepté donne un rôle et un salon sur Discord. Raye Update aura plus tard des canaux "
      "(stable, bêta publique, bêta, dev) ; l'accès aux canaux non publics sera réservé aux "
      "personnes acceptées. Ce mécanisme n'est <strong>pas encore construit</strong> : avant "
      "qu'il ouvre, cette section dira exactement ce que Raye Update envoie pour prouver "
      "l'accès, et rien ne sera envoyé avant.",
      "The beta program goes through the applications described above. Today, being accepted "
      "gives a role and a channel on Discord. Raye Update will later have channels (stable, "
      "public beta, beta, dev); access to the non-public ones will be kept for accepted "
      "people. That mechanism is <strong>not built yet</strong>: before it opens, this "
      "section will say exactly what Raye Update sends to prove access, and nothing will be "
      "sent before then."),
    P("Quel que soit le canal, les vérifications de mises à jour restent celles de la section "
      "« Ce que Raye Linux contacte depuis votre PC » : un téléchargement, sans rapport "
      "d'utilisation.",
      "Whatever the channel, update checks stay the ones of the section \"What Raye Linux "
      "contacts from your PC\": a download, with no usage report."),
)


def _privacy():
    out = []
    for s in PRIVACY:
        if s["id"] == "overview":
            s = _with_rows(
                s,
                [("Candidature pour rejoindre l'équipe (rôle, courriel, nom Discord, texte, "
                  "dates, décision)",
                  "Application to join the team (role, email, Discord name, text, dates, "
                  "decision)"),
                 ("mon serveur, au Québec ; sans le courriel : salon Discord privé",
                  "my server, in Québec; without the email: private Discord channel"),
                 ("en attente : 180 jours ; refusée : 30 jours ; acceptée : tant que vous avez "
                  "le rôle",
                  "waiting: 180 days; declined: 30 days; accepted: while you hold the role")],
                [("Nombres de la page Communauté", "Community page numbers"),
                 ("mémoire de mon serveur", "my server's memory"),
                 ("10 minutes ; rien sur vous", "10 minutes; nothing about you")])
        elif s["id"] == "bases":
            s = _with_rows(
                s,
                [("Candidatures", "Applications"),
                 ("étudier votre candidature, vous donner le rôle",
                  "review your application, give you the role"),
                 ("consentement exprès", "express consent")],
                [("Décision gardée pendant le rôle", "Decision kept while you hold the role"),
                 ("savoir qui a quel accès", "know who has which access"),
                 ("intérêt légitime", "legitimate interest")])
        out.append(s)
    return _insert(out, "discord", APPLICATIONS, COMMUNITY_PAGE, BETA_CHANNELS)


PRIVACY_V1 = _privacy()
PRIVACY_V1_SUMMARY = PRIVACY_SUMMARY[:4] + [
    ("Une candidature pour rejoindre l'équipe garde votre courriel, votre nom Discord et votre "
     "texte, le temps de l'étudier ; votre courriel n'est jamais envoyé sur Discord.",
     "An application to join the team keeps your email, your Discord name and your text, while "
     "it is reviewed; your email is never sent to Discord."),
] + PRIVACY_SUMMARY[4:]

# ------------------------------------------------------------- terms

TEAM = S(
    "team", "Rejoindre l'équipe", "Joining the team",
    P("Les rôles de l'équipe (tests, modération, traduction, code, design) sont du bénévolat. "
      "Ils ne créent aucun emploi, aucun contrat de travail ni aucune rémunération.",
      "Team roles (testing, moderation, translation, code, design) are volunteer work. They "
      "create no employment, no work contract and no pay."),
    L(("Chaque candidature est lue par la Raye Team, qui décide seule de l'accepter ou non, "
       "sans avoir à se justifier.",
       "Each application is read by the Raye Team, which alone decides whether to accept it, "
       "without having to give a reason."),
      ("Un rôle peut être retiré si les {rules} ne sont pas suivies, ou après une longue "
       "absence ; nous vous prévenons d'abord quand c'est possible.",
       "A role can be removed if the {rules} are not followed, or after a long absence; we tell "
       "you first whenever we can."),
      ("Ce que vous créez pour Raye (code, traduction, image, son) est publié sous la licence "
       "libre du dépôt où il entre ; vous en restez l'auteur.",
       "What you create for Raye (code, translation, picture, sound) is published under the "
       "free license of the repository it goes into; you remain its author."),
      ("Les tests suivent en plus les {betaterms}.",
       "Testing also follows the {betaterms}.")),
)


def _terms():
    return _insert(list(TERMS), "community", TEAM)


TERMS_V1 = _terms()
TERMS_V1_SUMMARY = TERMS_SUMMARY + [
    ("Les rôles de l'équipe sont bénévoles et accordés par la Raye Team seule.",
     "Team roles are volunteer work and granted by the Raye Team only."),
]

# ------------------------------------------------------------- beta terms

BETA_TERMS = [
    S("program", "Le programme", "The program",
      P("Le programme bêta permet d'essayer Raye avant ses versions finales. Il a trois "
        "niveaux : la bêta publique, ouverte à qui la demande ; la bêta privée, et la bêta "
        "Dev, réservées aux personnes que la Raye Team accepte après une candidature sur "
        "{join}.",
        "The beta program lets you try Raye before its final versions. It has three levels: "
        "the public beta, open to whoever asks; the private beta, and the Dev beta, kept for "
        "people the Raye Team accepts after an application on {join}."),
      P("Aujourd'hui, être accepté donne un rôle et un salon sur notre serveur Discord. Les "
        "canaux de mises à jour correspondants dans Raye Update sont prévus et ne sont pas "
        "encore ouverts.",
        "Today, being accepted gives a role and a channel on our Discord server. The matching "
        "update channels in Raye Update are planned and not open yet.")),
    S("software", "Un logiciel en essai", "Software under test",
      P("Une bêta n'est pas finie. Elle peut planter, mal se comporter avec votre matériel, "
        "ou demander de réinstaller Raye. La bêta Dev casse plus souvent que les autres.",
        "A beta is not finished. It can crash, misbehave with your hardware, or need Raye to "
        "be reinstalled. The Dev beta breaks more often than the others."),
      L(("Gardez une copie de vos fichiers importants ailleurs que sur le PC de test.",
         "Keep a copy of your important files somewhere other than the test PC."),
        ("N'installez pas une bêta privée ou Dev sur le seul PC dont vous avez besoin pour "
         "travailler.",
         "Don't install a private or Dev beta on the only PC you need for work."),
        ("Les points de restauration de Raye aident, mais ne remplacent pas une copie.",
         "Raye's restore points help, but don't replace a copy."))),
    S("warranty", "Aucune garantie", "No warranty",
      P("Les bêtas sont fournies telles quelles, sans garantie qu'elles fonctionnent ou "
        "conviennent à un usage précis, dans la mesure où la loi le permet. Les sections "
        "« Garanties » et « Responsabilité » des {terms} s'appliquent. Rien ici ne retire les "
        "droits que la loi vous donne comme consommateur.",
        "Betas are provided as they are, with no warranty that they work or suit a given use, "
        "as far as the law allows. The \"Warranties\" and \"Liability\" sections of the "
        "{terms} apply. Nothing here removes the rights the law gives you as a consumer.")),
    S("feedback", "Vos rapports et vos idées", "Your reports and ideas",
      P("Les rapports, captures et idées que vous partagez servent à corriger et améliorer "
        "Raye. Vous nous permettez de les utiliser librement, sans paiement. Vous restez "
        "l'auteur de ce que vous écrivez. Ne mettez dans un rapport ni mot de passe, ni clé de "
        "récupération, ni renseignement sur une autre personne.",
        "The reports, screenshots and ideas you share are used to fix and improve Raye. You "
        "let us use them freely, without payment. You remain the author of what you write. "
        "Don't put a password, a recovery key or information about another person in a "
        "report.")),
    S("confidentiality", "Ce qui n'est pas encore sorti", "What hasn't shipped yet",
      P("Rien dans le programme n'est secret par défaut, et il n'y a aucun accord de "
        "confidentialité à signer. Quand l'équipe demande de garder une version ou une "
        "fonction pour vous jusqu'à sa sortie, elle le dit clairement dans le salon concerné, "
        "et nous comptons sur vous pour le respecter. Ne pas le faire peut mener au retrait du "
        "rôle.",
        "Nothing in the program is secret by default, and there is no confidentiality "
        "agreement to sign. When the team asks you to keep a version or a feature to yourself "
        "until it ships, it says so clearly in the channel concerned, and we count on you to "
        "respect it. Not doing so can lead to the role being removed.")),
    S("leaving", "Partir, ou perdre l'accès", "Leaving, or losing access",
      L(("Vous pouvez quitter le programme à tout moment : dites-le sur Discord ou à "
         "{contact}.",
         "You can leave the program at any time: say so on Discord or at {contact}."),
        ("L'équipe peut retirer l'accès si les {rules} ou ces conditions ne sont pas "
         "suivies, ou après une longue absence.",
         "The team can remove access if the {rules} or these terms are not followed, or after "
         "a long absence."),
        ("Le programme peut changer ou s'arrêter ; les changements importants sont annoncés "
         "sur Discord.",
         "The program can change or stop; important changes are announced on Discord."))),
    S("privacy", "Vos renseignements", "Your information",
      P("Ce que la candidature garde, combien de temps et comment le faire effacer est dans la "
        "{privacy}, section « Les candidatures pour rejoindre l'équipe ».",
        "What the application keeps, for how long and how to have it deleted is in the "
        "{privacy}, section \"Applications to join the team\".")),
    S("contact", "Contact", "Contact",
      P("Une question sur ces conditions : {contact}.",
        "A question about these terms: {contact}.")),
]

BETA_TERMS_SUMMARY = [
    ("Trois niveaux : bêta publique pour qui la demande ; bêta privée et Dev après acceptation "
     "par la Raye Team.",
     "Three levels: public beta for whoever asks; private and Dev beta after the Raye Team "
     "accepts you."),
    ("Une bêta peut casser : gardez une copie de vos fichiers, pas de bêta Dev sur votre seul "
     "PC de travail.",
     "A beta can break: keep a copy of your files, no Dev beta on your only work PC."),
    ("Aucune garantie, dans la mesure où la loi le permet ; vos droits de consommateur "
     "restent.",
     "No warranty, as far as the law allows; your consumer rights stay."),
    ("Aucun accord de confidentialité ; si l'équipe demande de garder quelque chose pour vous, "
     "elle le dit.",
     "No confidentiality agreement; if the team asks you to keep something to yourself, it "
     "says so."),
    ("Vous partez quand vous voulez.", "You leave whenever you like."),
]

PAGES = {
    "privacy": (PRIVACY_V1, PRIVACY_V1_SUMMARY),
    "terms": (TERMS_V1, TERMS_V1_SUMMARY),
    "betaterms": (BETA_TERMS, BETA_TERMS_SUMMARY),
}
