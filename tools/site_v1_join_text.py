"""The words of the V1 pages about people: "Join the team" (one overview
and one page per role), the Community page and the community rules.
French and English side by side, as in site_v1_text.py, which merges the
PAGES below into its own.

The role keys ("beta", "public-beta", ...) are the ones the backend
accepts (backend/raye_site/applications.py, DISCORD_ROLES); a test checks
that both lists agree. Nothing here promises what is not built: the beta
update channels are planned, the account sign-in is not open, and every
application is read by a person of the Raye Team."""


def L(fr, en):
    return {"fr": fr, "en": en}


# page key -> addresses and short names. Keys stay [a-z]+ for {p:key}.
PAGES = {
    "join": {"path": L("/rejoindre/", "/en/join/"),
             "name": L("Rejoindre l'équipe", "Join the team")},
    "jbeta": {"path": L("/rejoindre/beta-privee/", "/en/join/beta/"),
              "name": L("Testeur de la bêta privée", "Beta tester")},
    "jpublic": {"path": L("/rejoindre/beta-publique/", "/en/join/public-beta/"),
                "name": L("Testeur de la bêta publique", "Public beta tester")},
    "jdev": {"path": L("/rejoindre/beta-dev/", "/en/join/beta-dev/"),
             "name": L("Testeur Dev", "Beta tester Dev")},
    "jmod": {"path": L("/rejoindre/moderation/", "/en/join/moderator/"),
             "name": L("Modérateur Discord", "Discord moderator")},
    "jtranslate": {"path": L("/rejoindre/traduction/", "/en/join/translator/"),
                   "name": L("Traducteur", "Translator")},
    "jcode": {"path": L("/rejoindre/developpement/", "/en/join/developer/"),
              "name": L("Développeur", "Developer")},
    "jother": {"path": L("/rejoindre/design-et-autres/", "/en/join/design-and-more/"),
               "name": L("Design et autres", "Design and more")},
    "community": {"path": L("/communaute/", "/en/community/"),
                  "name": L("Communauté", "Community")},
    "rules": {"path": L("/regles/", "/en/rules/"),
              "name": L("Règles de la communauté", "Community rules")},
    "betaterms": {"path": L("/conditions-beta/", "/en/beta-terms/"),
                  "name": L("Conditions du programme bêta", "Beta program terms")},
    "cookies": {"path": L("/temoins/", "/en/cookies/"),
                "name": L("Témoins (cookies)", "Cookies")},
    "terms": {"path": L("/conditions/", "/en/terms/"),
              "name": L("Conditions d'utilisation", "Terms of use")},
    "notice": {"path": L("/mentions-legales/", "/en/legal/"),
               "name": L("Mentions légales", "Legal notice")},
    "licenses": {"path": L("/licences/", "/en/licenses/"),
                 "name": L("Licences", "Licenses")},
    "roadmap": {"path": L("/feuille-de-route/", "/en/roadmap/"),
                "name": L("Feuille de route", "Roadmap")},
    "source": {"path": L("/code-source/", "/en/source/"),
               "name": L("Code source", "Source code")},
}

# ------------------------------------------------------------- join: overview

JOIN = {
    "eyebrow": L("Rejoindre l'équipe", "Join the team"),
    "h1": L("Aidez à faire Raye.", "Help make Raye."),
    "lede": L("Raye est fait par une seule personne, avec l'aide de sa communauté. Si vous "
              "voulez tester, traduire, modérer, coder ou dessiner, choisissez un rôle, lisez ce "
              "qu'il demande, puis envoyez une courte candidature.",
              "Raye is made by one person, with help from its community. If you want to test, "
              "translate, moderate, write code or draw, pick a role, read what it asks for, "
              "then send a short application."),
    "description": L("Les rôles ouverts dans l'équipe de Raye Linux : tests, modération, "
                     "traduction, code et design. Chaque candidature est lue par la Raye Team.",
                     "The open roles on the Raye Linux team: testing, moderation, translation, "
                     "code and design. Every application is read by the Raye Team."),
    "roles_title": L("Les rôles", "The roles"),
    "how_title": L("Comment ça se passe", "How it works"),
    "how": [
        (L("Vous envoyez le formulaire", "You send the form"),
         L("Deux minutes : votre nom Discord, une adresse pour vous répondre, et quelques "
           "phrases sur ce que vous voulez faire.",
           "Two minutes: your Discord name, an address to answer you, and a few sentences on "
           "what you want to do.")),
        (L("La Raye Team la lit", "The Raye Team reads it"),
         L("Une personne de l'équipe lit chaque candidature. Rien n'est accepté automatiquement. "
           "Nous essayons de répondre en moins de deux semaines.",
           "A person on the team reads every application. Nothing is accepted automatically. "
           "We try to answer within two weeks.")),
        (L("Vous recevez votre rôle", "You get your role"),
         L("Si c'est oui, vous recevez le rôle sur notre serveur Discord, avec son salon privé. "
           "Pour les rôles de test, l'accès au canal de mises à jour correspondant suivra quand "
           "ces canaux ouvriront.",
           "If it's a yes, you get the role on our Discord server, with its private channel. "
           "For the testing roles, access to the matching update channel will follow when "
           "those channels open.")),
        (L("Vous partez quand vous voulez", "You leave whenever you like"),
         L("Dites-le sur Discord ou par courriel : le rôle est retiré et votre candidature est "
           "effacée.",
           "Say so on Discord or by email: the role is removed and your application is "
           "deleted.")),
    ],
    "why_title": L("Ce que vous y gagnez", "What's in it for you"),
    "why": [
        L("Vous voyez les nouveautés avant tout le monde, et votre avis change ce qui sort.",
          "You see what's new before everyone else, and your opinion changes what ships."),
        L("Vous parlez directement avec la Raye Team, dans un salon privé.",
          "You talk with the Raye Team directly, in a private channel."),
        L("Rien à payer, aucun contrat : c'est du bénévolat, à votre rythme.",
          "Nothing to pay, no contract: it's volunteering, at your own pace."),
    ],
    "open": L("Lire et postuler", "Read and apply"),
}

# ------------------------------------------------------------- join: roles

# role (backend key) -> its page. "at" is the "at a glance" list,
# "means" what the role is, "expect" what we ask, "need" what to have.
ROLES = {
    "beta": {
        "page": "jbeta",
        "summary": L("Installer les bêtas privées avant leur sortie et dire ce qui casse.",
                     "Install the private betas before they ship and say what breaks."),
        "lede": L("Les testeurs de la bêta privée reçoivent les versions de Raye avant tout le "
                  "monde, sur un vrai PC, et nous disent ce qui ne va pas avant que ça arrive "
                  "chez les autres.",
                  "Private beta testers get Raye versions before anyone else, on a real PC, and "
                  "tell us what's wrong before it reaches everyone."),
        "at": [(L("Temps", "Time"), L("quelques heures par bêta", "a few hours per beta")),
               (L("Discord", "Discord"), L("rôle Beta Tester, salon #beta-testers",
                                           "Beta Tester role, #beta-testers channel")),
               (L("Canal de mises à jour", "Update channel"),
                L("bêta", "beta"))],
        "means": [
            L("Vous installez chaque bêta privée sur un PC que vous utilisez vraiment, ou à "
              "côté de votre système actuel.",
              "You install each private beta on a PC you really use, or next to your current "
              "system."),
            L("Vous suivez une courte liste de choses à essayer, puis vous utilisez Raye comme "
              "d'habitude.",
              "You go through a short list of things to try, then use Raye as you normally "
              "would."),
            L("Vous signalez chaque problème dans #beta-testers, avec ce que vous avez fait et "
              "ce qui s'est passé.",
              "You report each problem in #beta-testers, with what you did and what "
              "happened."),
        ],
        "expect": [
            L("Un PC où une mise à jour ratée ne vous empêche pas de travailler, ou une copie de "
              "vos fichiers.",
              "A PC where a failed update won't stop your work, or a copy of your files."),
            L("Des rapports précis plutôt que nombreux : une capture et les étapes valent mieux "
              "qu'un « ça marche pas ».",
              "Clear reports rather than many: a screenshot and the steps are worth more than "
              "“it doesn't work”."),
            L("Garder pour vous ce qui n'est pas encore sorti, tant que l'équipe le demande "
              "pour une bêta donnée.",
              "Keeping unreleased things to yourself whenever the team asks for a given "
              "beta."),
        ],
    },
    "public-beta": {
        "page": "jpublic",
        "summary": L("Passer à la bêta publique et en parler dans un salon dédié.",
                     "Switch to the public beta and talk about it in its own channel."),
        "lede": L("La bêta publique est la version presque finie, ouverte à qui veut. Le rôle "
                  "vous donne le salon où ses testeurs se parlent et où l'équipe répond.",
                  "The public beta is the nearly finished version, open to anyone who wants it. "
                  "The role gives you the channel where its testers talk and the team "
                  "answers."),
        "at": [(L("Temps", "Time"), L("à votre rythme", "at your own pace")),
               (L("Discord", "Discord"), L("rôle Public Beta Tester, salon #public-beta",
                                           "Public Beta Tester role, #public-beta channel")),
               (L("Canal de mises à jour", "Update channel"),
                L("bêta publique", "public beta"))],
        "means": [
            L("Vous utilisez la bêta publique au quotidien et vous dites ce qui vous gêne.",
              "You use the public beta every day and say what gets in your way."),
            L("Vous aidez les autres testeurs quand vous connaissez la réponse.",
              "You help other testers when you know the answer."),
        ],
        "expect": [
            L("Aucune connaissance technique : savoir décrire ce que vous voyez suffit.",
              "No technical knowledge: being able to describe what you see is enough."),
            L("Suivre les règles de la communauté, comme partout sur le serveur.",
              "Following the community rules, as everywhere on the server."),
        ],
    },
    "beta-dev": {
        "page": "jdev",
        "summary": L("Les versions de développement, qui peuvent casser, pour les gens à l'aise.",
                     "The development builds, which can break, for people who are at ease."),
        "lede": L("Le canal Dev reçoit ce qui vient d'être fait, parfois le jour même. Il casse "
                  "plus souvent que les autres. Il sert aux gens qui savent lire un journal et "
                  "revenir en arrière seuls.",
                  "The Dev channel gets what was just made, sometimes the same day. It breaks "
                  "more often than the others. It's for people who can read a log and roll "
                  "back on their own."),
        "at": [(L("Temps", "Time"), L("régulier, idéalement chaque semaine",
                                      "regular, ideally every week")),
               (L("Discord", "Discord"), L("rôle Beta Tester Dev, salon #beta-dev",
                                           "Beta Tester Dev role, #beta-dev channel")),
               (L("Canal de mises à jour", "Update channel"), L("dev", "dev"))],
        "means": [
            L("Vous installez les versions de développement dès qu'elles sortent.",
              "You install development builds as soon as they come out."),
            L("Quand quelque chose casse, vous trouvez le message d'erreur et le joignez à "
              "votre rapport.",
              "When something breaks, you find the error message and attach it to your "
              "report."),
            L("Vous essayez les correctifs qu'on vous propose et vous dites s'ils marchent.",
              "You try the fixes we send you and say whether they work."),
        ],
        "expect": [
            L("Être à l'aise avec un terminal et avec les points de restauration de Raye.",
              "Being at ease with a terminal and with Raye's restore points."),
            L("Un PC de test, ou une machine virtuelle, jamais votre seul PC de travail.",
              "A test PC, or a virtual machine, never your only work PC."),
            L("Garder pour vous ce qui n'est pas encore sorti quand l'équipe le demande.",
              "Keeping unreleased things to yourself when the team asks."),
        ],
    },
    "moderator": {
        "page": "jmod",
        "summary": L("Garder le serveur Discord de Raye Linux accueillant et utile, avec calme.",
                     "Keep the Raye Linux Discord server welcoming and useful, calmly."),
        "lede": L("Les modérateurs gardent le serveur accueillant : ils répondent, orientent, et "
                  "retirent ce qui enfreint les règles, avec calme.",
                  "Moderators keep the server welcoming: they answer, point people to the right "
                  "place, and remove what breaks the rules, calmly."),
        "at": [(L("Temps", "Time"), L("quelques passages par semaine", "a few visits a week")),
               (L("Discord", "Discord"), L("rôle Moderator, salons de l'équipe",
                                           "Moderator role, team channels")),
               (L("Langues", "Languages"), L("anglais ou français, idéalement les deux",
                                             "English or French, ideally both"))],
        "means": [
            L("Vous accueillez les nouveaux et vous les orientez vers le bon salon.",
              "You welcome newcomers and point them to the right channel."),
            L("Vous appliquez les règles : un rappel d'abord, une mise en sourdine ensuite, "
              "l'exclusion en dernier.",
              "You apply the rules: a reminder first, a timeout next, removal last."),
            L("Vous signalez à l'équipe ce qui dépasse la modération : une faille, une menace, "
              "un problème juridique.",
              "You tell the team about what goes beyond moderation: a security hole, a threat, "
              "a legal problem."),
        ],
        "expect": [
            L("Connaître les règles de la communauté et les appliquer à tous de la même façon.",
              "Knowing the community rules and applying them to everyone the same way."),
            L("Activer la validation en deux étapes sur votre compte Discord.",
              "Turning on two-step sign-in on your Discord account."),
            L("Ne jamais partager ce que vous voyez des membres dans les outils de modération.",
              "Never sharing what you see about members in the moderation tools."),
        ],
    },
    "translator": {
        "page": "jtranslate",
        "summary": L("Mettre Raye et ce site dans une nouvelle langue, ou relire le français.",
                     "Put Raye and this site in a new language, or proofread the French."),
        "lede": L("Raye parle anglais et français. Les traducteurs l'ouvrent à d'autres langues "
                  "et relisent les textes existants pour qu'ils sonnent juste.",
                  "Raye speaks English and French. Translators open it to other languages and "
                  "proofread the existing texts so they sound right."),
        "at": [(L("Temps", "Time"), L("à votre rythme, par lots de textes",
                                      "at your own pace, in batches of texts")),
               (L("Discord", "Discord"), L("rôle Translator", "Translator role")),
               (L("Langues", "Languages"), L("dites lesquelles dans le formulaire",
                                             "say which in the form"))],
        "means": [
            L("Vous traduisez les textes des applications de Raye et de ce site, à partir de "
              "l'anglais.",
              "You translate the texts of Raye's apps and of this site, from English."),
            L("Vous gardez les mots que Raye utilise partout de la même façon (Démarrer, "
              "Paramètres, Explorateur de fichiers).",
              "You keep the words Raye uses the same everywhere (Start, Settings, File "
              "Explorer)."),
            L("Vous relisez la traduction dans Raye lui-même, pour les textes trop longs ou "
              "coupés.",
              "You check the translation in Raye itself, for texts that are too long or cut "
              "off."),
        ],
        "expect": [
            L("Écrire la langue cible comme votre langue de tous les jours.",
              "Writing the target language like your everyday language."),
            L("Bien lire l'anglais.", "Reading English well."),
            L("Des phrases simples, sans jargon : Raye est fait pour des gens qui ne sont pas "
              "techniciens.",
              "Simple sentences, no jargon: Raye is made for people who are not "
              "technicians."),
        ],
    },
    "developer": {
        "page": "jcode",
        "summary": L("Corriger des bogues et écrire du code dans les dépôts publics.",
                     "Fix bugs and write code in the public repositories."),
        "lede": L("Tout le code de Raye est public. Les développeurs commencent par un petit "
                  "bogue, puis prennent ce qui leur plaît.",
                  "All of Raye's code is public. Developers start with a small bug, then take "
                  "on what they like."),
        "at": [(L("Temps", "Time"), L("à votre rythme", "at your own pace")),
               (L("Discord", "Discord"), L("rôle Raye Developer, salon de développement",
                                           "Raye Developer role, development channel")),
               (L("Code", "Code"), L("C++ et QML, Python, Rust, shell",
                                     "C++ and QML, Python, Rust, shell"))],
        "means": [
            L("Vous choisissez un bogue dans le forum #bugs ou sur la feuille de route.",
              "You pick a bug from the #bugs forum or from the roadmap."),
            L("Vous proposez votre changement dans un des dépôts publics ; il est relu avant "
              "d'entrer.",
              "You propose your change in one of the public repositories; it is reviewed "
              "before it goes in."),
            L("Chaque changement vient avec ses tests, comme le reste du code.",
              "Each change comes with its tests, like the rest of the code."),
        ],
        "expect": [
            L("Savoir lire le code qui existe avant d'en écrire.",
              "Being able to read the code that exists before writing more."),
            L("Accepter que votre code soit publié sous la licence du dépôt, le plus souvent la "
              "GPL.",
              "Agreeing that your code is published under the repository's license, most "
              "often the GPL."),
        ],
    },
    "other": {
        "page": "jother",
        "summary": L("Icônes, fonds d'écran, sons, guides, vidéos : ce que vous savez faire.",
                     "Icons, wallpapers, sounds, guides, videos: whatever you're good at."),
        "lede": L("Raye a besoin de plus que du code : des images, des sons, des guides et des "
                  "vidéos. Dites-nous ce que vous savez faire.",
                  "Raye needs more than code: pictures, sounds, guides and videos. Tell us what "
                  "you're good at."),
        "at": [(L("Temps", "Time"), L("par projet", "per project")),
               (L("Discord", "Discord"), L("rôle Contributor", "Contributor role")),
               (L("Licence", "License"), L("libre, choisie ensemble", "free, chosen together"))],
        "means": [
            L("Vous proposez une idée ou vous prenez une demande de l'équipe.",
              "You suggest an idea or take on a request from the team."),
            L("Vous montrez des essais tôt, dans le salon de l'équipe, pour en parler.",
              "You show early drafts in the team channel, to talk about them."),
        ],
        "expect": [
            L("Un travail qui est le vôtre, sans élément copié d'ailleurs.",
              "Work that is your own, with nothing copied from elsewhere."),
            L("Le publier sous une licence libre, pour qu'il puisse faire partie de Raye.",
              "Publishing it under a free license, so it can be part of Raye."),
            L("Suivre le style de Raye : sobre, lisible, pas d'effets pour rien.",
              "Following Raye's style: plain, readable, no effects for their own sake."),
        ],
    },
}

ROLE_UI = {
    "at": L("En bref", "At a glance"),
    "means": L("Ce que fait ce rôle", "What the role is"),
    "expect": L("Ce que nous demandons", "What we ask"),
    "apply": L("Postuler", "Apply"),
    "all_roles": L("Tous les rôles", "All roles"),
    "approval": L("Chaque candidature est lue par la Raye Team. Rien n'est accepté "
                  "automatiquement.",
                  "Every application is read by the Raye Team. Nothing is accepted "
                  "automatically."),
}

# ------------------------------------------------------------- the form

FORM = {
    "title": L("Votre candidature", "Your application"),
    "intro": L("Les champs marqués d'un astérisque sont obligatoires. Comptez deux minutes.",
               "Fields with an asterisk are required. It takes two minutes."),
    "email": L("Adresse courriel", "Email address"),
    "email_hint": L("Pour vous répondre. Elle n'est jamais publiée, ni envoyée sur Discord.",
                    "To answer you. It is never published, nor sent to Discord."),
    "accounts": L("Les comptes Raye ne sont pas encore ouverts. Quand ils le seront, vous "
                  "pourrez postuler avec votre compte au lieu d'une adresse.",
                  "Raye accounts are not open yet. Once they are, you'll be able to apply "
                  "with your account instead of an address."),
    "discord": L("Nom d'utilisateur Discord", "Discord username"),
    "discord_hint": L("Le rôle est donné à ce compte. Vous le trouvez dans Discord, sur votre "
                      "profil, sous votre nom.",
                      "The role is given to this account. You'll find it in Discord, on your "
                      "profile, under your name."),
    "languages": L("Langues", "Languages"),
    "languages_hint": L("Celles que vous parlez ou écrivez bien, par exemple : français, "
                        "anglais.",
                        "The ones you speak or write well, for example: French, English."),
    "languages_tr": L("Langues dans lesquelles vous pouvez traduire",
                      "Languages you can translate into"),
    "skills": L("Ce que vous savez faire", "What you're good at"),
    "skills_hint": L("En quelques mots : votre matériel, vos outils, ce que vous avez déjà fait.",
                     "In a few words: your hardware, your tools, what you've done before."),
    "why": L("Pourquoi voulez-vous aider ?", "Why do you want to help?"),
    "why_hint": L("Entre 30 et 1 500 caractères.", "Between 30 and 1,500 characters."),
    "consent": L("J'accepte que la Raye Team garde cette candidature pour l'étudier, comme le "
                 "dit la {privacy}.",
                 "I agree that the Raye Team keeps this application to review it, as the "
                 "{privacy} says."),
    "privacy_link": L("politique de confidentialité", "privacy policy"),
    "required": L("(obligatoire)", "(required)"),
    "hp": L("Ne remplissez pas ce champ", "Leave this field empty"),
    "send": L("Envoyer ma candidature", "Send my application"),
    "sending": L("Envoi…", "Sending…"),
    "done": L("Candidature envoyée", "Application sent"),
    "failed": L("L'envoi n'a pas abouti. Vérifiez votre connexion et réessayez, ou écrivez à "
                "bonjour@rayelinux.com.",
                "Sending failed. Check your connection and try again, or write to "
                "bonjour@rayelinux.com."),
    "reference": L("Référence", "Reference"),
}

# ------------------------------------------------------------- community

COMMUNITY = {
    "eyebrow": L("Communauté", "Community"),
    "h1": L("Les gens de Raye.", "The people of Raye."),
    "lede": L("La communauté se retrouve sur Discord, en anglais et en français. C'est là "
              "qu'on pose ses questions, qu'on signale un bogue et qu'on propose ce qui viendra "
              "ensuite.",
              "The community meets on Discord, in English and French. That's where you ask "
              "questions, report a bug and suggest what comes next."),
    "description": L("Le serveur Discord de Raye Linux : aide en anglais et en français, bogues, "
                     "idées et nouvelles. Le nombre de membres en direct, et comment y entrer.",
                     "The Raye Linux Discord server: help in English and French, bugs, ideas "
                     "and news. How many people are there right now, and how to join."),
    "live_label": L("Sur le serveur Discord", "On the Discord server"),
    "live_wait": L("Le nombre de membres s'affiche ici quand la page a pu le lire.",
                   "The number of members shows here once the page could read it."),
    "members": L("membres", "members"),
    "online": L("en ligne maintenant", "online now"),
    "join": L("Rejoindre le serveur Discord", "Join the Discord server"),
    "privacy": L("Cette page ne charge rien depuis Discord. Notre serveur lui demande les deux "
                 "nombres toutes les dix minutes ; votre navigateur ne contacte Discord que si "
                 "vous cliquez sur le bouton.",
                 "This page loads nothing from Discord. Our server asks it for the two numbers "
                 "every ten minutes; your browser only contacts Discord if you click the "
                 "button."),
    "there_title": L("Ce que vous y trouvez", "What you'll find there"),
    "there": [
        (L("Aide", "Help"),
         L("Une question sur Raye, l'installation ou un programme : posez-la, en anglais ou en "
           "français.",
           "A question about Raye, installing it or a program: ask it, in English or "
           "French.")),
        (L("Bogues", "Bugs"),
         L("Un forum où chaque bogue a son fil, avec ce qui a été essayé et sa correction.",
           "A forum where each bug has its own thread, with what was tried and its fix.")),
        (L("Idées et feuille de route", "Ideas and roadmap"),
         L("Vos idées, et la liste de ce qui s'en vient, la même que sur ce site.",
           "Your ideas, and the list of what's coming, the same as on this site.")),
        (L("Notes de version", "Release notes"),
         L("Ce qui change à chaque mise à jour, dès sa sortie.",
           "What changes with each update, as soon as it ships.")),
        (L("Jeux et programmes Windows", "Games and Windows programs"),
         L("Ce qui fonctionne, ce qui ne fonctionne pas, et comment.",
           "What runs, what doesn't, and how.")),
    ],
    "help_title": L("Aller plus loin", "Going further"),
    "help": L("Le serveur a ses {rules}. Et si vous voulez donner un coup de main pour tester, "
              "traduire ou modérer, voyez {join}.",
              "The server has its {rules}. And if you'd like to help test, translate or "
              "moderate, see {join}."),
    "rules_word": L("règles", "rules"),
    "join_word": L("les rôles ouverts", "the open roles"),
}

# ------------------------------------------------------------- rules

RULES = {
    "eyebrow": L("Communauté", "Community"),
    "h1": L("Règles de la communauté", "Community rules"),
    "lede": L("Les mêmes règles que sur notre serveur Discord. Elles valent aussi pour ce que "
              "vous envoyez par ce site : rapports de bogue et candidatures.",
              "The same rules as on our Discord server. They also apply to what you send "
              "through this site: bug reports and applications."),
    "description": L("Les règles du serveur Discord de Raye Linux et de ce que vous envoyez par "
                     "le site, et ce que font les modérateurs.",
                     "The rules of the Raye Linux Discord server and of what you send through "
                     "the site, and what moderators do."),
    "rules": [
        (L("Soyez bienveillants.", "Be kind."),
         L("Respectez tout le monde, quel que soit son niveau. Pas d'insultes, de harcèlement, "
           "de haine ni de discrimination.",
           "Respect everyone, whatever their level. No insults, harassment, hate or "
           "discrimination.")),
        (L("Utilisez le bon salon.", "Use the right channel."),
         L("Les questions vont dans le salon d'aide, les bogues dans le forum des bogues, les "
           "idées dans le salon des idées.",
           "Questions go in the help channel, bugs in the bugs forum, ideas in the ideas "
           "channel.")),
        (L("Pas de spam ni d'autopromotion.", "No spam or self-promotion."),
         L("Pas de publicité, pas de liens d'invitation, pas de mentions en masse.",
           "No ads, no invite links, no mass mentions.")),
        (L("Pas de piratage, de cracks ni de triche.", "No piracy, cracks or cheats."),
         L("Nous n'aidons personne à contourner une licence ou un anti-triche.",
           "We don't help anyone get around a license or an anti-cheat.")),
        (L("Restez convenables.", "Keep it safe for work."),
         L("Aucun contenu pour adultes, violent ou choquant.",
           "No adult, violent or shocking content.")),
        (L("Protégez votre vie privée.", "Protect your privacy."),
         L("Ne publiez jamais un mot de passe, une clé de récupération ou des données "
           "personnelles, même dans une capture d'écran.",
           "Never post a password, a recovery key or personal details, not even in a "
           "screenshot.")),
        (L("Anglais ou français.", "English or French."),
         L("Discutez en anglais ou en français. Dans les forums, les deux langues sont "
           "bienvenues.",
           "Chat in English or French. In the forums, either language is fine.")),
        (L("Respectez les règles de Discord.", "Follow Discord's rules."),
         L("Ses conditions d'utilisation et ses règles de la communauté, publiées sur "
           "discord.com, s'appliquent aussi.",
           "Its Terms of Service and Community Guidelines, published on discord.com, apply "
           "too.")),
    ],
    "mod_title": L("Ce que font les modérateurs", "What moderators do"),
    "mod": [
        L("Ils peuvent retirer tout ce qui enfreint ces règles.",
          "They can remove anything that breaks these rules."),
        L("En général : un rappel d'abord, une mise en sourdine ensuite, l'exclusion en "
          "dernier. Une faute grave peut mener tout de suite à l'exclusion.",
          "Usually: a reminder first, a timeout next, removal last. A serious breach can lead "
          "straight to removal."),
        L("Si quelque chose vous dérange, mentionnez un modérateur ou ouvrez un ticket sur le "
          "serveur.",
          "If something bothers you, mention a moderator or open a ticket on the server."),
    ],
    "appeal_title": L("Contester une décision", "Appealing a decision"),
    "appeal": L("Écrivez à <a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a> "
                "en disant ce qui s'est passé. Une autre personne de l'équipe que celle qui a "
                "décidé relit la décision quand c'est possible.",
                "Write to <a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a> "
                "and say what happened. Someone on the team other than the person who decided "
                "reviews the decision whenever possible."),
}


# The V1 site names no upstream project, even where the roadmap list (shared
# with the Discord and the live site) does: these lines are worded again on
# the V1 roadmap page only. A line here that no longer appears stops the build.
ROADMAP_V1_WORDS = {
    "en": [],
    "fr": [],
}
