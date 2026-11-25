"""The V1 pages added for the launch: what is in V1, what comes next, games,
the two desktops and older PCs. Same block format as site_v1_text.py, which
imports this module at its end (so everything it needs is already defined).

What is said here comes from the V1 section of the roadmap
(/root/raye-final/roadmap/roadmap.json) and from the lots' reports; a thing
that was not seen working is said to be so in a "what is still missing" box."""

import site_v1_text as V
from site_v1_text import H, L, P, limits

# the screenshots these pages show (placeholders until taken on the 1.0 image)
V.SHOTS.update({
    "try-raye": L("La session d'essai de Raye, lancée depuis la clé USB : le bureau avec l'icône "
                  "Installer Raye Linux posée dessus.",
                  "Raye's trial session, started from the USB stick: the desktop with the Install "
                  "Raye Linux icon on it."),
    "enroll-key": L("L'écran bleu du démarrage où l'on inscrit la clé de Raye : la liste « Enroll "
                    "MOK » et le champ du code à six chiffres.",
                    "The blue startup screen where Raye's key is enrolled: the “Enroll MOK” list "
                    "and the six-digit code field."),
    "desktop-choice": L("Paramètres, page Environnement de bureau : les deux cartes, le bureau de "
                        "Raye et Hyprland, avec celle qui est utilisée.",
                        "Settings, Desktop environment page: the two cards, Raye's desktop and "
                        "Hyprland, with the one in use marked."),
    "hypr-session": L("La session Hyprland de Raye : des fenêtres rangées côte à côte, et la barre "
                      "de Raye en haut avec l'horloge.",
                      "Raye's Hyprland session: windows tiled side by side, and Raye's bar at the "
                      "top with the clock."),
    "steam-store": L("La page de Steam dans le Raye Store, avec la rangée du format du paquet "
                     "et le bouton Installer.",
                     "Steam's page in the Raye Store, with the package format row and the "
                     "Install button."),
})

# ---------------------------------------------------------------- what is in V1

WHATSNEW = {
    "eyebrow": L("Le projet", "The project"),
    "h1": L("Ce que contient la version {v}", "What version {v} contains"),
    "description": L("La liste de ce que la V1 de Raye Linux apporte : installation, jeux, "
                     "mémoire, Hyprland, applis, et ce qui reste en cours.",
                     "What V1 of Raye Linux brings: install, games, memory, Hyprland, apps, and "
                     "what is still in progress."),
    "lede": L("Cette page suit la feuille de route : chaque ligne vient de sa section V1, que je "
              "tiens à jour. Une ligne est écrite ici quand le changement est fait ; ce que je "
              "n'ai pas pu essayer sur un vrai PC est dit à part, en bas.",
              "This page follows the roadmap: every line comes from its V1 section, which I keep "
              "up to date. A line is written here when the change is made; what I couldn't try "
              "on a real PC is said apart, at the bottom."),
    "next": "soon",
    "blocks": [
        H("install", "Installer et démarrer", "Installing and starting"),
        ("list", [
            L("La clé USB démarre sur l'essai de Raye, avec une icône Installer sur le bureau. "
              "L'installateur s'ouvre en plein écran. Détails sur la page "
              "<a href=\"{p:install}\">Installer</a>.",
              "The USB stick starts on the Raye trial, with an Install icon on the desktop. The "
              "installer opens full screen. Details are on the <a href=\"{p:install}\">Install</a> "
              "page."),
            L("Le menu de démarrage est en anglais seulement, et plusieurs défauts de "
              "l'installateur sont corrigés : le bouton Accessibilité décalé, le champ du "
              "Wi-Fi, la fenêtre de copie qui restait sur « Finishing writing ».",
              "The startup menu is in English only, and several installer flaws are fixed: the "
              "misplaced Accessibility button, the Wi-Fi field, the copy window that stayed on "
              "“Finishing writing”."),
            L("Un noyau Raye, qui remplace celui du système de base : des correctifs de la "
              "communauté pour la réactivité, la mémoire et la veille, plus les réglages de "
              "Raye. Le passage de l'un à l'autre demande "
              "d'inscrire une clé une seule fois, sur un écran bleu au redémarrage (page "
              "<a href=\"{p:install}\">Installer</a>).",
              "A Raye kernel, which replaces the base system's: community patches for "
              "responsiveness, memory and sleep, plus Raye's own tuning. Switching from one to "
              "the other asks you to enroll a key once, "
              "on a blue screen at restart (<a href=\"{p:install}\">Install</a> page)."),
        ]),
        H("games", "Jeux et cartes graphiques", "Games and graphics cards"),
        ("list", [
            L("Steam voit vos autres disques : ce qui est monté sous <code>/media</code>, "
              "<code>/run/media</code> et <code>/mnt</code>. Prouvé dans la machine de test, "
              "pour Steam installé par le Store.",
              "Steam sees your other drives: whatever is mounted under <code>/media</code>, "
              "<code>/run/media</code> and <code>/mnt</code>. Proved in the test machine, for "
              "Steam installed from the Store."),
            L("Un correctif pour les anciennes cartes AMD (RX 400 et 500), qui restaient en basse "
              "résolution ou sur un écran noir, et un pour le clignotement noir des cartes NVIDIA "
              "sur un écran à 144 Hz.",
              "A fix for older AMD cards (RX 400 and 500), which stayed in low resolution or on a "
              "black screen, and one for the black flicker of NVIDIA cards on a 144 Hz screen."),
            L("Raye est prêt pour Easy Anti-Cheat v2 : la clé de son noyau a été demandée à Epic. "
              "Tout est sur la page <a href=\"{p:games}\">Jeux</a>.",
              "Raye is ready for Easy Anti-Cheat v2: its kernel's key was sent to Epic. It's all "
              "on the <a href=\"{p:games}\">Games</a> page."),
        ]),
        H("memory", "Mémoire et stabilité", "Memory and stability"),
        ("list", [
            L("La même mémoire au repos sur tous les PC, environ 850 Mo, même avec beaucoup de "
              "RAM. Avant, le noyau en réservait d'autant plus que la machine en avait.",
              "The same memory at idle on every PC, about 850 MB, even with a lot of RAM. "
              "Before, the kernel reserved more of it the more the machine had."),
            L("Plus de gel quand la mémoire manque : le PC ralentit un peu.",
              "No more freezes when memory runs out: the PC slows down a little instead."),
            L("Des services inutiles retirés et des réglages de fond, pour un Raye plus léger et "
              "plus stable.",
              "Unneeded services removed and background tuning, for a lighter and more stable "
              "Raye."),
            L("Les applis Electron qui plantaient au lancement (Qoder, entre autres) démarrent.",
              "The Electron apps that crashed on start (Qoder, among others) start."),
        ]),
        H("apps", "Fichiers, réseau et applis", "Files, network and apps"),
        ("list", [
            L("L'Explorateur s'ouvre tout de suite, même quand un disque réseau ne répond pas.",
              "File Explorer opens right away, even when a network drive doesn't answer."),
            L("La fenêtre de copie vers une clé USB montre la vraie vitesse, avec ses boutons "
              "Réduire et Fermer.",
              "The copy window to a USB stick shows the real speed, with its Minimize and Close "
              "buttons."),
            L("Le champ du mot de passe Wi-Fi des paramètres rapides garde le curseur pendant que "
              "la liste des réseaux se rafraîchit.",
              "The Wi-Fi password field in quick settings keeps the cursor while the list of "
              "networks refreshes."),
            L("Un VPN WireGuard en un clic : importez un fichier, allumez-le depuis les "
              "paramètres rapides.",
              "A WireGuard VPN in one click: import a file, turn it on from quick settings."),
            L("Le Centre d'information ouvre le Gestionnaire des tâches de Raye et en prend "
              "l'allure.",
              "Info Center opens Raye's Task Manager and takes its look."),
            L("La page Programmes Windows liste aussi ceux installés depuis le Store.",
              "The Windows programs page also lists the ones installed from the Store."),
            L("Le Store prend les paquets APT d'abord, Flatpak seulement quand il n'y a pas "
              "d'APT, et accepte les AppImage. Les applis que vous avez en Flatpak passent en "
              "APT une seule fois, sans rien perdre.",
              "The Store takes APT packages first, Flatpak only when there is no APT one, and "
              "accepts AppImage. The apps you have as Flatpak move to APT once, with nothing "
              "lost."),
        ]),
        H("look", "Le bureau et son allure", "The desktop and its look"),
        ("list", [
            L("Le nouveau logo de Raye, dans le système, l'installateur, le site et Discord, "
              "avec une nouvelle animation de démarrage.",
              "Raye's new logo, in the system, the installer, the website and Discord, with a new "
              "startup animation."),
            L("Paramètres de la barre des tâches : à gauche ou au centre, taille des icônes, "
              "hauteur, masquage automatique.",
              "Taskbar settings: left or center, icon size, height, auto-hide."),
            L("Des fenêtres qui ondulent quand on les déplace, avec un interrupteur dans les "
              "Paramètres.",
              "Windows that wobble when you move them, with a switch in Settings."),
        ]),
        H("hypr", "Hyprland", "Hyprland"),
        ("list", [
            L("Une session Hyprland plus souple, des Paramètres et des applis de Raye qui "
              "marchent dessus, et un guide complet. Tout est sur la page "
              "<a href=\"{p:desktops}\">Deux bureaux</a>.",
              "A smoother Hyprland session, Settings and Raye apps that work on it, and a "
              "complete guide. It's all on the <a href=\"{p:desktops}\">Two desktops</a> page."),
        ]),
        limits(L("Les correctifs pour les anciennes cartes AMD et pour les cartes NVIDIA n'ont "
                 "pas été essayés sur une vraie carte : la machine de test n'a pas de carte "
                 "graphique.",
                 "The fixes for older AMD cards and for NVIDIA cards were not tried on a real "
                 "card: the test machine has no graphics card."),
               L("Les PC anciens (démarrage en mode BIOS, processeurs comme le Core 2 Duo, 2 à "
                 "4 Go de mémoire) sont encore en cours d'essai. Voir la page "
                 "<a href=\"{p:oldpcs}\">Vieux PC</a>.",
                 "Older PCs (BIOS-mode start, processors such as the Core 2 Duo, 2 to 4 GB of "
                 "memory) are still being tried. See the <a href=\"{p:oldpcs}\">Older PCs</a> "
                 "page."),
               L("Le noyau de Raye n'a pas encore été essayé sur un vrai PC avec Secure Boot, ni "
                 "avec une vraie carte NVIDIA, et l'hibernation est bloquée quand Secure Boot "
                 "est actif.",
                 "Raye's kernel hasn't yet been tried on a real PC with Secure Boot, or with a "
                 "real NVIDIA card, and hibernation is blocked while Secure Boot is on."),
               L("Je repasse encore chaque écran en français, installateur compris.",
                 "I'm still going through every screen in French, installer included."),
               L("Le VPN WireGuard et les réglages de la barre ont été vus dans la machine de "
                 "test ; je n'ai pas encore vu l'ondulation des fenêtres, que le rendu de la "
                 "machine de test ne peut pas montrer.",
                 "The WireGuard VPN and the taskbar settings were seen in the test machine; I "
                 "haven't seen the wobbling windows yet, which the test machine's rendering "
                 "can't show.")),
    ],
}

# ---------------------------------------------------------------- what comes next

SOON = {
    "eyebrow": L("Le projet", "The project"),
    "h1": L("Ce qui vient après la V1", "What comes after V1"),
    "description": L("Les versions 1.1 et 1.2 de Raye Linux : ce qui est prévu, dans quel ordre, "
                     "et ce que je ne promets pas encore.",
                     "Versions 1.1 and 1.2 of Raye Linux: what is planned, in what order, and "
                     "what I'm not promising yet."),
    "lede": L("Une version tous les quinze jours environ. Les dates sont des cibles, pas des "
              "promesses : quand quelque chose prend plus de temps que prévu, ça passe à la "
              "version suivante. La liste complète et à jour est sur la page "
              "<a href=\"{p:roadmap}\">Feuille de route</a>.",
              "About one version every two weeks. The dates are targets, not promises: when "
              "something takes longer than planned, it moves to the next version. The full, "
              "up-to-date list is on the <a href=\"{p:roadmap}\">Roadmap</a> page."),
    "next": "roadmap",
    "blocks": [
        H("v11", "La 1.1, début décembre", "1.1, early December"),
        ("list", [
            L("L'installation d'un programme Windows se fait sans fenêtre, avec une vraie barre "
              "de progression du début à la fin.",
              "Installing a Windows program happens without a window, with a real progress bar "
              "from start to finish."),
            L("Raye Proton : choisir la couche Windows de Raye pour les jeux de Steam.",
              "Raye Proton: pick Raye's Windows layer for Steam games."),
            L("Le pont complet avec Windows : partager pilotes et réglages avec la partition "
              "Windows.",
              "The complete bridge with Windows: share drivers and settings with the Windows "
              "partition."),
            L("Plus de matériel qui marche d'emblée : Wi-Fi Realtek et autres, caméra et son, "
              "dont les pilotes s'installent seuls quand un appareil en a besoin.",
              "More hardware that works out of the box: Realtek and other Wi-Fi, webcam and "
              "sound, whose drivers install on their own when a device needs them."),
            L("Une page Imprimantes et scanners et une appli Scan, et une meilleure autonomie "
              "sur portable.",
              "A Printers & scanners page and a Scan app, and longer battery life on laptops."),
            L("Un vrai écran de Raye pour déverrouiller un disque chiffré au démarrage.",
              "A real Raye screen to unlock an encrypted disk at startup."),
            L("La barre des tâches en haut ou sur le côté de l'écran.",
              "The taskbar on top or on the side of the screen."),
            L("Quadra dans le Store, avec le mode jeu allumé pendant que Roblox tourne.",
              "Quadra in the Store, with game mode on while Roblox runs."),
            L("Le compte Raye, pour que vos réglages vous suivent d'un PC à l'autre, avec un "
              "nouveau site de compte, des courriels et une connexion en deux étapes.",
              "The Raye account, so your settings follow you from PC to PC, with a new account "
              "website, emails and two-step sign-in."),
            L("Une première version de Raye Community, le clavardage de Raye, sur le site et dans "
              "le système.",
              "A first version of Raye Community, Raye's own chat, on the website and in the "
              "system."),
            L("Les pages « Rejoindre l'équipe » avec un panneau pour l'équipe, les profils "
              "publics et les badges.",
              "The Join the team pages with a panel for the team, public profiles and badges."),
            L("Ce site avec de vraies captures du système, les pages légales et la FAQ revues.",
              "This site with real screenshots of the system, and the legal pages and FAQ "
              "reviewed."),
        ]),
        H("v12", "La 1.2, les 11 et 12 décembre", "1.2, December 11 and 12"),
        ("list", [
            L("Raye Community complète : images et vidéos, messages privés, outils pour "
              "l'équipe, puis elle remplace le serveur Discord.",
              "Raye Community complete: images and videos, private messages, tools for the team, "
              "then it replaces the Discord server."),
            L("Raye dans toutes les langues.",
              "Raye in every language."),
            L("Raye Insider, dans les Paramètres : la bêta publique (inscription sur le site) et "
              "les canaux Bêta et Dev, sur candidature, liés à votre compte Raye. Vous pouvez "
              "en sortir à tout moment.",
              "Raye Insider, in Settings: the public beta (sign up on the website) and the Beta "
              "and Dev channels, by application, tied to your Raye account. You can leave "
              "anytime."),
            L("Plus de 40 programmes Windows populaires dans le Store, essayés un par un, avec "
              "un badge « Optimisé pour Raye ».",
              "More than 40 popular Windows programs in the Store, each one tried, with an "
              "“Optimized for Raye” badge."),
            L("Des options pour développeurs et une page web distante.",
              "Developer options and a remote web page."),
            L("Les comptes : badges, communauté et panneau d'administration.",
              "Accounts: badges, community and an admin panel."),
            L("Une seconde édition de Raye, tenue au même niveau que celle-ci.",
              "A second edition of Raye, kept in step with this one."),
        ]),
        limits(L("Rien de cette page n'est fait : tout est prévu, certaines lignes sont "
                 "commencées. Je les retire ou je les déplace plutôt que de les laisser "
                 "traîner sans le dire.",
                 "None of this page is done: all of it is planned, some lines are started. I "
                 "remove or move them rather than leave them sitting without saying so.")),
    ],
}

# ---------------------------------------------------------------- games

GAMES = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Les jeux : Steam, Proton et les anti-triche",
            "Games: Steam, Proton and anti-cheat"),
    "description": L("Jouer sur Raye Linux : Steam, la couche Windows pour les jeux, Easy "
                     "Anti-Cheat v2 et les jeux qui ne marchent pas, dits franchement.",
                     "Playing on Raye Linux: Steam, the Windows layer for games, Easy Anti-Cheat "
                     "v2 and the games that don't run, said plainly."),
    "lede": L("Beaucoup de jeux Windows marchent sur Raye, certains non, et la raison est "
              "souvent un programme anti-triche. Cette page dit ce que je sais, et ce que je "
              "n'ai pas encore pu essayer : je n'ai mesuré aucun jeu sur un vrai PC.",
              "Many Windows games run on Raye, some don't, and the reason is often an "
              "anti-cheat program. This page says what I know, and what I haven't been able to "
              "try yet: I haven't measured a single game on a real PC."),
    "next": "install",
    "blocks": [
        H("steam", "Steam", "Steam"),
        P("Steam est dans le Raye Store. Raye l'installe comme un paquet de Raye (APT) plutôt "
          "qu'en Flatpak ; si vous l'aviez déjà en Flatpak, Raye le déplace une fois, avec vos "
          "jeux et vos réglages, et vous prévient à la connexion. Steam voit vos autres disques : "
          "ce qui est monté sous <code>/media</code>, <code>/run/media</code> et "
          "<code>/mnt</code> est proposé quand vous ajoutez un dossier de bibliothèque.",
          "Steam is in the Raye Store. Raye installs it as a Raye package (APT) rather than "
          "Flatpak; if you already had it as Flatpak, Raye moves it once, with your games and "
          "settings, and tells you at sign-in. Steam sees your other drives: whatever is "
          "mounted under <code>/media</code>, <code>/run/media</code> and <code>/mnt</code> is "
          "offered when you add a library folder."),
        ("shot", "steam-store"),
        P("Le mode jeu s'allume tout seul pendant une partie. Heroic, pour les boutiques "
          "d'autres éditeurs, est aussi dans le Store.",
          "Game Mode turns on by itself while you play. Heroic, for other publishers' stores, "
          "is also in the Store."),
        limits(L("Sur une carte NVIDIA, Steam qui s'ouvre puis n'affiche rien a été signalé. J'ai "
                 "corrigé ce que j'ai trouvé, sans pouvoir l'essayer sans carte NVIDIA : si ça "
                 "vous arrive, dites-le moi.",
                 "On an NVIDIA card, Steam that opens and then shows nothing was reported. I "
                 "fixed what I found, without being able to try it without an NVIDIA card: if "
                 "it happens to you, tell me.")),
        H("proton", "Proton, la couche Windows des jeux", "Proton, the Windows layer for games"),
        P("Steam lance les jeux Windows avec Proton, sa couche de compatibilité : c'est elle "
          "qui fait tourner la plupart d'entre eux. Raye prévoit sa propre couche, Raye Proton, "
          "que vous choisirez pour un jeu dans Steam. Elle est prévue pour la 1.1, pas pour la "
          "V1.",
          "Steam launches Windows games with Proton, its compatibility layer: that's what runs "
          "most of them. Raye is planning its own layer, Raye Proton, which you'll pick for a "
          "game in Steam. It's planned for 1.1, not for V1."),
        H("anticheat", "Les anti-triche", "Anti-cheat"),
        P("Un anti-triche est un programme qui surveille le jeu et, parfois, le système. Ce qu'il "
          "faut savoir sur Raye tient en trois lignes :",
          "An anti-cheat is a program that watches the game and, sometimes, the system. What "
          "you need to know about Raye fits in three lines:"),
        ("list", [
            L("<strong>Ceux qui vivent dans le noyau de Windows</strong>, comme Vanguard de "
              "Valorant : ils ne marchent pas sur Raye, et je ne vois pas comment cela "
              "changerait.",
              "<strong>The ones that live in the Windows kernel</strong>, such as Valorant's "
              "Vanguard: they don't run on Raye, and I don't see how that would change."),
            L("<strong>Easy Anti-Cheat v2</strong> : il existe pour Linux, mais il vérifie le "
              "noyau et l'état de Secure Boot, et son éditeur, Epic, tient une liste des clés "
              "qu'il accepte. Voir plus bas.",
              "<strong>Easy Anti-Cheat v2</strong>: it exists for Linux, but it checks the "
              "kernel and the state of Secure Boot, and its publisher, Epic, keeps a list of the "
              "keys it accepts. See below."),
            L("<strong>Tous les autres</strong> : cela dépend du jeu et de son studio. "
              "ProtonDB dit, jeu par jeu, ce que les joueurs ont constaté.",
              "<strong>All the others</strong>: it depends on the game and its studio. "
              "ProtonDB says, game by game, what players have found."),
        ]),
        H("eac", "Easy Anti-Cheat v2 et le noyau de Raye", "Easy Anti-Cheat v2 and Raye's kernel"),
        P("Le noyau de Raye est signé avec une clé de Raye, que vous inscrivez une fois dans "
          "votre PC. Avec Secure Boot actif, Raye met en route ce qu'Easy Anti-Cheat v2 "
          "contrôle : le verrouillage du noyau, <code>kexec</code> coupé et l'IOMMU sans "
          "passthrough. Je les ai vérifiés dans la machine de test, avec Secure Boot et une puce "
          "TPM virtuelle, pas encore sur un vrai portable.",
          "Raye's kernel is signed with a Raye key, which you enroll once in your PC. With "
          "Secure Boot on, Raye turns on what Easy Anti-Cheat v2 checks: kernel lockdown, "
          "<code>kexec</code> off and the IOMMU without passthrough. I checked those settings "
          "in the test machine, with Secure Boot and a virtual TPM chip, not yet on a real "
          "laptop."),
        P("Reste la liste d'Epic. J'ai demandé qu'on y ajoute les clés de Raye ; la réponse "
          "n'est pas arrivée. Tant qu'Epic ne les connaît pas, Easy Anti-Cheat v2 refuse le "
          "noyau de Raye. Le jour où elles y sont, ce sera écrit ici, pas avant.",
          "What's left is Epic's list. I asked for Raye's keys to be added; the answer hasn't "
          "come. As long as Epic doesn't know them, Easy Anti-Cheat v2 refuses Raye's kernel. "
          "The day they're on it, it will be written here, not before."),
        limits(L("Même avec la clé acceptée, un jeu n'est jouable que si son studio a activé "
                 "Easy Anti-Cheat pour Linux. Fortnite est le but que je me suis donné ; je ne "
                 "peux pas vous le promettre.",
                 "Even with the key accepted, a game is only playable if its studio turned on "
                 "Easy Anti-Cheat for Linux. Fortnite is the goal I set myself; I can't promise "
                 "it to you."),
               L("Les PC qui ont déjà inscrit l'ancienne clé de Raye doivent la retirer : "
                 "Easy Anti-Cheat veut que toutes les clés inscrites soient connues.",
                 "PCs that already enrolled Raye's old key have to remove it: Easy Anti-Cheat "
                 "wants every enrolled key to be known.")),
        H("graphics", "Les cartes graphiques", "Graphics cards"),
        P("Raye sait revenir à un affichage plus simple quand le bureau ne démarre pas deux fois "
          "de suite, et choisir « Safe graphics » sur la clé aide quand l'écran reste noir. Deux "
          "problèmes signalés par des joueurs sont corrigés dans la V1 : les anciennes cartes "
          "AMD (RX 400 et 500) qui restaient en basse résolution, et le clignotement noir de "
          "cartes NVIDIA sur un écran à 144 Hz. Je n'ai ni l'une ni l'autre de ces cartes : "
          "dites-moi si ça marche chez vous.",
          "Raye can fall back to a simpler display when the desktop doesn't start twice in a row, "
          "and picking “Safe graphics” on the stick helps when the screen stays black. Two "
          "problems reported by players are fixed in V1: older AMD cards (RX 400 and 500) that "
          "stayed in low resolution, and the black flicker of NVIDIA cards on a 144 Hz screen. I "
          "have neither of those cards: tell me if it works for you."),
        limits(L("Des images par seconde faibles dans Counter-Strike 2 ont été signalées sur une "
                 "GTX 1650 ; je ne l'ai pas mesuré.",
                 "Low frames per second in Counter-Strike 2 were reported on a GTX 1650; I "
                 "haven't measured it.")),
    ],
}

# ---------------------------------------------------------------- the two desktops

DESKTOPS = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Deux bureaux : celui de Raye et Hyprland",
            "Two desktops: Raye's and Hyprland"),
    "description": L("Raye Linux a deux bureaux : le sien, qui ressemble à Windows 11, et "
                     "Hyprland, où les fenêtres se rangent seules. Comment choisir, et le guide.",
                     "Raye Linux has two desktops: its own, which looks like Windows 11, and "
                     "Hyprland, where windows tile themselves. How to choose, and the guide."),
    "lede": L("Le bureau dont parle tout ce site est celui de Raye. Hyprland est un second "
              "bureau, pour ceux qui veulent des fenêtres rangées d'office et le clavier "
              "d'abord. Les deux sont dans la même installation, et vous passez de l'un à "
              "l'autre sans réinstaller.",
              "The desktop all of this site talks about is Raye's. Hyprland is a second "
              "desktop, for people who want windows tiled by default and the keyboard first. "
              "Both are in the same install, and you move from one to the other without "
              "reinstalling."),
    "next": "install",
    "blocks": [
        H("choose", "Choisir", "Choosing"),
        P("Le bureau de Raye reprend la disposition de Windows 11 : barre centrée, Démarrer, "
          "fenêtres qu'on glisse et qu'on accroche. C'est celui qu'on a après l'installation.",
          "Raye's desktop keeps the Windows 11 layout: centered taskbar, Start, windows you "
          "drag and snap. It's the one you get after installing."),
        P("Hyprland est un bureau où les fenêtres se rangent côte à côte sans qu'on les "
          "place, et où l'on fait presque tout au clavier. Il est pour qui le connaît déjà, ou "
          "veut l'apprendre. Raye lui met sa barre, son thème et ses applis, et l'installation "
          "propose Hyprland si vous le voulez.",
          "Hyprland is a desktop where windows line up side by side without you placing them, "
          "and where you do almost everything with the keyboard. It's for people who already "
          "know it, or want to learn it. Raye gives it its bar, its theme and its apps, and the "
          "installer offers Hyprland if you want it."),
        ("shot", "desktop-choice"),
        P("Le choix se fait dans Paramètres > Personnalisation > Environnement de bureau, ou "
          "sur l'écran de connexion, avec le bouton Bureau en bas à droite. Passer de l'un à "
          "l'autre rouvre l'Explorateur et les Paramètres sur le nouveau bureau.",
          "You choose in Settings > Personalization > Desktop environment, or on the sign-in "
          "screen, with the Desktop button at the bottom right. Switching reopens File Explorer "
          "and Settings on the new desktop."),
        ("shot", "hypr-session"),
        H("yours", "Le régler à votre façon", "Setting it up your way"),
        P("Raye garde sa configuration d'Hyprland pour elle et vous laisse un fichier à vous : "
          "<code>user.conf</code>. Raye ne l'écrase jamais, même à une mise à jour. Sur la page "
          "Environnement de bureau, « Ouvrir mes réglages Hyprland » l'ouvre dans l'éditeur, et "
          "<code>raye-hyprland-config</code> recharge, ouvre ou revient aux réglages de Raye "
          "depuis le terminal. Pour y revenir d'un coup, il suffit de retirer vos lignes.",
          "Raye keeps its Hyprland configuration for itself and leaves you a file of your own: "
          "<code>user.conf</code>. Raye never overwrites it, even on an update. On the Desktop "
          "environment page, “Open my Hyprland settings” opens it in the editor, and "
          "<code>raye-hyprland-config</code> reloads, opens or goes back to Raye's settings from "
          "the terminal. To go back in one go, just remove your lines."),
        H("guide", "Le guide", "The guide"),
        P("Le manuel de Raye a un chapitre sur Hyprland, « Hyprland sur Raye », ouvert par le "
          "bouton « Guide Hyprland » de la même page. Il dit où sont les fichiers, ce qu'on "
          "peut changer et comment : écarts, bordures, coins, flou, animations, raccourcis, "
          "règles de fenêtres, écrans et échelle, clavier, démarrage, fond d'écran, barre, "
          "verrouillage et veille. Chaque exemple est à copier, et tous passent la vérification "
          "de configuration d'Hyprland. Il dit aussi comment régler les applis de Raye "
          "(thème, icônes, curseur, polices) et que faire quand l'une s'affiche mal.",
          "Raye's handbook has a chapter on Hyprland, “Hyprland on Raye”, opened by the "
          "“Hyprland guide” button on that same page. It says where the files are, what you can "
          "change and how: gaps, borders, corners, blur, animations, shortcuts, window rules, "
          "screens and scale, keyboard, startup, wallpaper, bar, lock and sleep. Every example "
          "is ready to copy, and all of them pass Hyprland's configuration check. It also says "
          "how to set Raye's apps (theme, icons, cursor, fonts) and what to do when one "
          "displays badly."),
        H("others", "Les réglages des autres", "Other people's setups"),
        P("Beaucoup de gens publient leur configuration d'Hyprland. Raye peut en installer une "
          "d'une commande, <code>raye-hyprland-config dots install</code> suivie de l'adresse du "
          "dépôt. Avant de lancer quoi que ce soit, la commande sauvegarde vos réglages, vous "
          "montre le script et ce qu'il touche (<code>sudo</code>, installation de paquets, "
          "suppressions) et vous demande de taper <code>yes</code>. Sans réponse, rien n'est "
          "modifié. <code>dots restore</code> remet l'état d'avant, et le bureau de Raye "
          "revient tout seul à la connexion suivante si la configuration installée plante "
          "au démarrage.",
          "Many people publish their Hyprland setup. Raye can install one with a single "
          "command, <code>raye-hyprland-config dots install</code> followed by the repository "
          "address. Before running anything, the command saves your settings, shows you the "
          "script and what it touches (<code>sudo</code>, package installs, deletions) and "
          "asks you to type <code>yes</code>. With no answer, nothing is changed. "
          "<code>dots restore</code> puts the previous state back, and Raye's desktop comes "
          "back by itself at the next sign-in if the installed setup crashes at start."),
        limits(L("Beaucoup de ces configurations sont écrites pour d'autres systèmes : leur "
                 "script peut ne pas marcher sur Raye. Dans ce cas la sauvegarde vous protège, "
                 "mais l'installation n'aboutit pas. Je n'ai pas encore essayé un dépôt public "
                 "de bout en bout.",
                 "Many of these setups are written for other systems: their script may not run "
                 "on Raye. In that case the backup protects you, but the install doesn't go "
                 "through. I haven't yet tried a public repository from end to end."),
               L("Sous Hyprland, les Paramètres chargent leurs 90 pages sans erreur, mais je ne "
                 "les ai pas toutes regardées à l'écran. Éclairage nocturne et Multitâche sont "
                 "marqués « Disponible sous le bureau de Raye », car ils ne commandent que ce "
                 "bureau. La souris, l'écran de verrouillage et les effets de transparence se "
                 "règlent dans le fichier d'Hyprland plutôt que dans les Paramètres.",
                 "Under Hyprland, Settings loads its 90 pages without error, but I haven't "
                 "looked at all of them on screen. Night light and Multitasking say “Available "
                 "on Raye's desktop”, because they only control that desktop. The mouse, the "
                 "lock screen and the transparency effects are set in Hyprland's file rather "
                 "than in Settings.")),
    ],
}

# ---------------------------------------------------------------- older PCs

OLDPCS = {
    "eyebrow": L("Avant d'installer", "Before you install"),
    "h1": L("Un vieux PC : ce qui a été essayé et ce qui ne l'a pas été",
            "An older PC: what was tried and what wasn't"),
    "description": L("Raye Linux sur un PC ancien : démarrage en mode BIOS, vieux processeur, 2 à "
                     "4 Go de mémoire, carte graphique sans 3D. Ce qui est vu, et ce qui ne "
                     "l'est pas.",
                     "Raye Linux on an older PC: BIOS-mode start, old processor, 2 to 4 GB of "
                     "memory, graphics card without 3D. What was seen, and what wasn't."),
    "lede": L("Faire marcher Raye sur un PC d'avant 2012 est un but de la V1, pas un résultat. "
              "Voici ce que j'ai vu dans une machine virtuelle qui imite un vieux PC, et ce que "
              "je n'ai pas vu. Aucun vrai vieux PC n'a encore reçu Raye.",
              "Making Raye run on a PC from before 2012 is a goal of V1, not a result. Here is "
              "what I saw in a virtual machine that imitates an old PC, and what I didn't. No "
              "real old PC has received Raye yet."),
    "next": "hardware",
    "blocks": [
        H("seen", "Ce que j'ai vu", "What I saw"),
        ("list", [
            L("Dans une machine virtuelle en mode BIOS d'autrefois, avec 2 Go de mémoire, un "
              "processeur générique et une carte graphique simple, la clé démarre, et "
              "l'installateur s'ouvre en une vingtaine de secondes.",
              "In a virtual machine in the old BIOS mode, with 2 GB of memory, a generic "
              "processor and a plain graphics card, the stick starts, and the installer opens "
              "in about twenty seconds."),
            L("L'installateur dit alors, dès sa première page, que le processeur est ancien : "
              "certains programmes et certains jeux en demandent un plus récent. Il ne bloque "
              "pas l'installation.",
              "The installer then says, on its first page, that the processor is on the older "
              "side: some programs and some games need a newer one. It doesn't stop the "
              "install."),
        ]),
        H("tried", "Ce que j'essaie pour la V1", "What I'm trying for V1"),
        ("list", [
            L("Le démarrage en mode BIOS, jusqu'à l'installation complète.",
              "Starting in BIOS mode, all the way through a full install."),
            L("Les processeurs 64 bits anciens, comme le Core 2 Duo.",
              "Older 64-bit processors, such as the Core 2 Duo."),
            L("2 à 4 Go de mémoire.",
              "2 to 4 GB of memory."),
            L("Une carte graphique sans accélération 3D.",
              "A graphics card without 3D acceleration."),
        ]),
        limits(L("L'installation complète en mode BIOS n'a pas été refaite avec la version "
                 "actuelle : seul le démarrage jusqu'à l'installateur a été vu.",
                 "A full install in BIOS mode wasn't redone with the current version: only the "
                 "start up to the installer was seen."),
               L("Aucune mesure sur un vrai PC de 2 ou 4 Go. Avec moins de 4 Go, je ne sais pas "
                 "si le bureau reste agréable : 8 Go restent conseillés.",
                 "No measurement on a real 2 or 4 GB PC. With under 4 GB, I don't know whether "
                 "the desktop stays pleasant: 8 GB is still recommended."),
               L("Raye est 64 bits : un PC 32 bits, ou un processeur de 64 bits trop ancien pour "
                 "le système de base, ne peut pas le démarrer.",
                 "Raye is 64-bit: a 32-bit PC, or a 64-bit processor too old for the base "
                 "system, can't start it.")),
        H("yours", "Si vous essayez", "If you try it"),
        P("Si vous avez un PC ancien, essayez la session d'essai depuis la clé : elle ne touche "
          "pas au disque. Puis dites-moi, sur Discord ou à "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>, le modèle du PC, "
          "ce qui s'est passé, et le fichier <code>raye-gpu.txt</code> si l'écran est resté "
          "noir ou en basse résolution. C'est comme ça que cette page s'allongera.",
          "If you have an older PC, try the trial session from the stick: it doesn't touch the "
          "disk. Then tell me, on Discord or at "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>, the PC's model, "
          "what happened, and the <code>raye-gpu.txt</code> file if the screen stayed black or "
          "in low resolution. That's how this page will grow."),
    ],
}

CONTENT = {"v1": WHATSNEW, "soon": SOON, "games": GAMES, "desktops": DESKTOPS,
           "oldpcs": OLDPCS}
