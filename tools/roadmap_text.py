"""Text of the roadmap page (tools/build_pages.py).

The list itself is tools/roadmap.json, the same file as #roadmap on the
Discord (copied here by roadmap/update.sh). FR holds the French of every
section title and item, keyed by the English without its emoji. An item
missing here stops the build: add its French, then rebuild."""

PAGE = {
    "en": {
        "title": "Roadmap",
        "nav": "Roadmap",
        "description": "What's coming to Raye Linux, in order: what's done, what's being "
                       "built and what's planned.",
        "lede": "What's next for Raye Linux. Ideas from the community come first: share "
                "yours in #ideas on <a href=\"{discord}\" rel=\"noopener\">our Discord</a>.",
        "same": "The #roadmap channel on the Discord has the same list.",
        "legend": "Legend",
        "count": "{done} of {total} done",
    },
    "fr": {
        "title": "Feuille de route",
        "nav": "Feuille de route",
        "description": "Ce qui s'en vient pour Raye Linux, dans l'ordre : ce qui est fait, "
                       "ce qui est en cours et ce qui est prévu.",
        "lede": "La suite pour Raye Linux. Les idées de la communauté passent en premier : "
                "proposez les vôtres dans #ideas sur <a href=\"{discord}\" "
                "rel=\"noopener\">notre Discord</a>.",
        "same": "Le salon #roadmap du Discord a la même liste.",
        "legend": "Légende",
        "count": "Fait : {done} sur {total}",
    },
}

STATES = {
    "en": {"done": "Done", "doing": "In progress", "planned": "Planned"},
    "fr": {"done": "Fait", "doing": "En cours", "planned": "Prévu"},
}

# Items the site words its own way: the site names no other system, even
# where the Discord does. English and French.
RENAMED = {
    "Arch edition, kept in sync with the Ubuntu edition":
        ("A second edition with rolling updates, kept in sync with the main one",
         "Une deuxième édition en mise à jour continue, synchronisée avec la principale"),
    "Android apps":
        ("Phone apps on your PC", "Les applis de téléphone sur votre PC"),
    "Faster Ubuntu updates everywhere: your country's server first, others as backup":
        ("Faster system updates everywhere: your country's server first, others as backup",
         "Des mises à jour du système plus rapides partout : le serveur de votre pays "
         "d'abord, les autres en secours"),
    "Raye kernel only (Ubuntu's kernel removed)":
        ("Raye kernel only (the stock kernel is removed)",
         "Seulement le noyau Raye (le noyau d'origine est retiré)"),
}

FR = {
    # section titles; \u00a0 keeps « » on the line of their words
    "Recently done": "Fait récemment",
    "V1 Beta 1 · out November 19": "V1 Bêta 1 · sortie le 19 novembre",
    "V1 Beta 2 (next big update)": "V1 Bêta 2 (la prochaine grosse mise à jour)",
    "V1 Beta 2 · out November 21": "V1 Bêta 2 · sortie le 21 novembre",
    "V1 final": "V1 finale",
    "V1 · end of November": "V1 · fin novembre",
    "Fix for the sign-in screen that shows only its background on some PCs (it still works when you type your password)": "Correctif pour l'écran de connexion qui n'affiche que son fond sur certains PC (il fonctionne quand même quand on tape son mot de passe)",
    "Community idea: DankMaterialShell (DMS) as a one-click setup for Hyprland, and for niri and MangoWC once Raye offers them": "Idée de la communauté : DankMaterialShell (DMS) comme configuration en un clic pour Hyprland, et pour niri et MangoWC quand Raye les proposera",
    "Community idea: Horizon (Minecraft Java rewritten in Rust, faster) in the Store, with Game Mode while you play": "Idée de la communauté : Horizon (Minecraft Java réécrit en Rust, plus rapide) dans le Store, avec le mode Jeu pendant la partie",
    "A Team page on the website: everyone accepted into the Raye team shows up on their own, grouped by role (team, developers, translators, contributors, testers), with their Discord name and picture, or their Raye account's picture": "Une page Équipe sur le site : chaque personne acceptée dans l'équipe Raye y apparaît d'elle-même, par rôle (équipe, développeurs, traducteurs, contributeurs, testeurs), avec son nom et sa photo Discord, ou la photo de son compte Raye",
    "Raye Team panel: new moderators and team members start on probation, then get full access and their own staff key by email (Raye account plus key to sign in); people already in the team are added and told by private message": "Panneau Raye Team : les nouveaux modérateurs et membres commencent en probation, puis reçoivent l'accès complet et leur propre clé staff par courriel (compte Raye plus clé pour se connecter) ; les membres déjà dans l'équipe sont ajoutés et prévenus par message privé",
    "Join the team: links to your past work in the form, a starting trust score that grows with your work, emails at each step; accepting someone gives their Discord role, then access step by step (a safe test mirror, GitHub, the server mirror), and new developers' changes go to the Dev channel for testers": "Rejoindre l'équipe : des liens vers vos travaux dans le formulaire, un score de confiance de départ qui monte avec votre travail, un courriel à chaque étape ; accepter quelqu'un donne son rôle Discord, puis ses accès petit à petit (un miroir de test sans danger, GitHub, le miroir du serveur), et les changements des nouveaux développeurs vont dans le canal Dev pour les testeurs",
    "Raye Community complete, built on Matrix: end-to-end encryption everywhere (your Raye account handles the keys), images and videos, private messages, the same channels as the Discord server and support tickets, a layout like Discord's with older messages as you scroll, who's online and a status (online, idle, do not disturb, invisible), your Raye profile picture, its own right-click menu, bots and commands with Raye Assistant answering, staff tools, then it replaces the Discord server": "Raye Community complet, basé sur Matrix : chiffrement de bout en bout partout (votre compte Raye gère les clés), images et vidéos, messages privés, les mêmes salons que le serveur Discord et des tickets d'aide, une disposition comme Discord avec les anciens messages en remontant, qui est en ligne et un statut (en ligne, inactif, ne pas déranger, invisible), la photo de profil de votre compte Raye, son propre menu du clic droit, des bots et des commandes avec Raye Assistant qui répond, des outils pour le staff, puis il remplace le serveur Discord",
    "Join the team: people already in the team (accepted on the website or on Discord) are added to the new system and told by private message": "Rejoindre l'équipe : les personnes déjà dans l'équipe (acceptées sur le site ou sur Discord) sont ajoutées au nouveau système et prévenues par message privé",
    "Join the team: changes from new developers, once built and tested, go to the Dev channel of Raye Insider so testers can try them": "Rejoindre l'équipe : les changements des nouveaux développeurs, une fois construits et testés, vont dans le canal Dev de Raye Insider pour que les testeurs les essaient",
    "Join the team: a starting trust score from what you write in the form, then it grows with your work": "Rejoindre l'équipe : un score de confiance de départ selon ce que vous écrivez dans le formulaire, qui monte ensuite avec votre travail",
    "Join the team: the form takes links to your past work (GitHub, projects, translations) to show what you've collaborated on": "Rejoindre l'équipe : le formulaire accepte des liens vers vos travaux (GitHub, projets, traductions) pour montrer ce à quoi vous avez collaboré",
    "Raye Team panel: new moderators and team members start on probation with a trust score, then get full access, their Discord role and their own staff key by email (sign in with your Raye account plus your key)": "Panneau Raye Team : les nouveaux modérateurs et membres de l'équipe commencent en probation avec un score de confiance, puis reçoivent l'accès complet, leur rôle Discord et leur propre clé staff par courriel (connexion avec votre compte Raye plus votre clé)",
    "Join the team: accepting someone gives their Discord role, then access step by step (a safe test mirror, GitHub, the server mirror) as their trust score grows, with an email at each step": "Rejoindre l'équipe : accepter quelqu'un lui donne son rôle Discord, puis ses accès petit à petit (un miroir de test sans danger, GitHub, le miroir du serveur) selon son score de confiance, avec un courriel à chaque étape",
    "Community idea: app icons closer to the Windows 11 look, drawn by Raye": "Idée de la communauté : des icônes d'applis plus proches du style de Windows 11, dessinées par Raye",
    "Community idea: a lock screen you can customize (picture, clock, what it shows)": "Idée de la communauté : un écran de verrouillage personnalisable (image, horloge, ce qu'il affiche)",
    "Community idea: more blur, like Windows' acrylic, on the taskbar, Start, menus and panels": "Idée de la communauté : plus de flou, comme l'acrylique de Windows, sur la barre des tâches, Démarrer, les menus et les panneaux",
    "Community idea: bigger icons in Start, with a size setting": "Idée de la communauté : de plus grandes icônes dans Démarrer, avec un réglage de taille",
    "Taskbars on several screens show the same apps in the same order": "Les barres des tâches de plusieurs écrans montrent les mêmes applis dans le même ordre",
    "Raye Community: who's online in the member list, and a status like Discord's: online, idle, do not disturb, invisible": "Raye Community : qui est en ligne dans la liste des membres, et un statut comme Discord : en ligne, inactif, ne pas déranger, invisible",
    "Raye Community built on Matrix: your Raye account handles the encryption keys and their backup, nothing to set up": "Raye Community basé sur Matrix : votre compte Raye s'occupe des clés de chiffrement et de leur sauvegarde, rien à configurer",
    "Raye Community: your Raye account's profile picture in the chat, with settings like Discord's (show it or not)": "Raye Community : la photo de profil de votre compte Raye dans le chat, avec des réglages comme Discord (l'afficher ou non)",
    "Raye Community: its own right-click menu (reply, react, edit, copy text or link, report) instead of the web browser's": "Raye Community : son propre menu du clic droit (répondre, réagir, modifier, copier le texte ou le lien, signaler) au lieu de celui du navigateur web",
    "Join the team: emails from the staff panel (application received, accepted or not, a reply written by staff for each application)": "Rejoindre l'équipe : des courriels depuis le panneau du staff (candidature reçue, acceptée ou non, une réponse écrite par le staff pour chaque candidature)",
    "Raye Community: end-to-end encryption everywhere, private messages and channels (only the people in the conversation can read it, not even Raye's server)": "Raye Community : chiffrement de bout en bout partout, messages privés et salons (seules les personnes de la conversation peuvent lire, pas même le serveur de Raye)",
    "V1.1 · early December": "V1.1 · début décembre",
    "V1.2 · December 11–12": "V1.2 · 11-12 décembre",
    "Later": "Plus tard",
    "V1.2 · December": "V1.2 · décembre",
    "Raye Community: bots and commands like RivenBot (welcome, roles, polls, levels) and Raye Assistant answering in the chat": "Raye Community : des bots et des commandes comme RivenBot (bienvenue, rôles, sondages, niveaux) et Raye Assistant qui répond dans le chat",
    "Fix for apps that crash on start (Qoder and other Electron apps)": "Correctif des applis qui plantent au démarrage (Qoder et autres applis Electron)",
    "Wi-Fi password box keeps the cursor while networks refresh": "La case du mot de passe Wi-Fi garde le curseur pendant le rafraîchissement des réseaux",
    "File Explorer opens right away, even when a network drive is out of reach": "L'Explorateur s'ouvre tout de suite, même si un disque réseau est injoignable",
    "Windows programs page lists the ones installed from the Store": "La page Programmes Windows liste aussi ceux installés depuis le Store",
    "Smoother Hyprland": "Hyprland sans saccades",
    "Unneeded services removed and global optimizations, for a lighter and more stable Raye": "Services inutiles retirés et optimisations globales, pour un Raye plus léger et plus stable",
    "WireGuard VPN in one click: import a file, turn it on from Quick Settings": "VPN WireGuard en un clic : importer un fichier, l'activer depuis les Paramètres rapides",
    "Info Center opens Raye's Task Manager and looks like Raye": "Le Centre d'informations ouvre le Gestionnaire des tâches de Raye et prend le style Raye",
    "Budgie desktop as another choice": "Le bureau Budgie comme autre choix",
    "V1 Beta 4": "V1 Bêta 4",
    "V1 Beta 3": "V1 Bêta 3",
    "Every language: all of Raye translated": "Toutes les langues : tout Raye traduit",
    "Raye Community: older messages load as you scroll up, and a layout like Discord's (channel categories, member list with roles, unread markers)": "Raye Community : les anciens messages se chargent en remontant, et une disposition comme Discord (catégories de salons, liste des membres avec leurs rôles, messages non lus)",
    "Welcome app after install: quick setup (drivers, updates, apps, Raye account, look) and where to get help": "Appli de bienvenue après l'installation : réglages rapides (pilotes, mises à jour, applis, compte Raye, apparence) et où trouver de l'aide",
    "Taskbar: a transparency slider and an apps-only taskbar": "Barre des tâches : un curseur de transparence et une barre avec seulement les applis",
    "Raye Community: the same channels as the Discord server, set up for you, and support tickets": "Raye Community : les mêmes salons que le serveur Discord, déjà en place, et des tickets d'aide",
    "Forgot your password? Reset it from the sign-in screen, with a recovery key made in Setup or with your Raye account": "Mot de passe oublié ? Réinitialisez-le depuis l'écran de connexion, avec une clé de récupération créée dans l'installation ou avec votre compte Raye",
    "Complete Windows bridge: Windows programs see your drives, printers, network and ports": "Pont Windows complet : les programmes Windows voient vos disques, imprimantes, réseau et ports",
    "Raye Proton built on GE-Proton, with per-game fixes from Raye Update": "Raye Proton construit sur GE-Proton, avec des correctifs par jeu livrés par Raye Update",
    "Raye in Spanish, German, Brazilian Portuguese and Italian": "Raye en espagnol, allemand, portugais du Brésil et italien",
    "Raye Community: Raye's own chat on the website and in Raye Linux, with your Raye account, friends, roles, moderation, images and videos, private messages and staff tools, then it replaces the Discord server":
        "Raye Community : le chat de Raye, sur le site et dans Raye Linux, avec votre compte Raye, les amis, les rôles, la modération, les images et vidéos, les messages privés et les outils du staff, puis il remplace le serveur Discord",
    "The V1 website, with fresh screenshots of the real system":
        "Le site de la V1, avec de nouvelles captures du vrai système",
    "Website refresh: a cleaner, more professional look and more pages":
        "Site refait : un style plus soigné et plus professionnel, et plus de pages",
    "New Raye logo everywhere: system, installer, website, Discord":
        "Nouveau logo de Raye partout : système, installateur, site, Discord",
    "New boot animation with the new logo": "Nouvelle animation de démarrage avec le nouveau logo",
    "V1 Beta 3 · next week": "V1 Bêta 3 · la semaine prochaine",
    "Steam sees your other drives": "Steam voit vos autres disques",
    "Same low RAM use at idle on every PC (about 850 MB), even with lots of RAM":
        "La même faible RAM au repos sur tous les PC (environ 850 Mo), même avec beaucoup de RAM",
    "V1 Beta 1 (Nov 19): faster boot, AMD and NVIDIA panels, Clock app, bigger Store, new installer, Try Raye":
        "V1 Bêta 1 (19 novembre) : démarrage plus rapide, panneaux AMD et NVIDIA, appli Horloge, Store plus grand, nouvel installateur, Essayer Raye",
    "V2": "V2",
    "V3": "V3",
    "V4": "V4",

    # recently done
    "New download (Nov 18) with all the latest fixes built in":
        "Nouveau téléchargement (18 novembre) avec tous les derniers correctifs inclus",
    "New download (Nov 21): 1.0 Beta Sundog, with all the latest fixes built in":
        "Nouveau téléchargement (21 novembre) : 1.0 Bêta Sundog, avec tous les derniers correctifs inclus",
    "Join the team: apply in #join-the-team":
        "Rejoindre l'équipe : postulez dans #join-the-team",
    "Automatic graphics fallback for older cards (more fixes for some AMD cards still coming)":
        "Affichage de secours automatique pour les cartes graphiques plus anciennes "
        "(d'autres correctifs arrivent pour certaines cartes AMD)",
    "Simpler updates: no extra \"Install now\" step, apps reopen by themselves":
        "Mises à jour plus simples : plus d'étape «\u00a0Install now\u00a0», les applis se rouvrent "
        "toutes seules",
    "USB drives in This PC, opened in one click":
        "Les clés USB dans Ce PC, ouvertes en un clic",
    "Apps open at their own size, minimize animation into the taskbar":
        "Les applis s'ouvrent à leur propre taille, et la réduction s'anime vers la barre "
        "des tâches",
    "No more freeze when plugging in a second screen":
        "Plus de gel quand on branche un deuxième écran",

    # V1 Beta 1
    "A much faster boot": "Un démarrage beaucoup plus rapide",
    "NVIDIA and AMD control panels (fans, power, profiles)":
        "Panneaux de contrôle NVIDIA et AMD (ventilateurs, alimentation, profils)",
    "Better File Explorer and smoother mouse scrolling everywhere":
        "Un meilleur Explorateur de fichiers et un défilement à la souris plus doux partout",
    "Many more settings like Windows 11, with a transparency switch":
        "Beaucoup plus de réglages comme dans Windows 11, avec un bouton pour la transparence",
    "New Clock app: alarms, timer, stopwatch, world clocks":
        "Nouvelle appli Horloge : alarmes, minuteur, chronomètre, horloges du monde",
    "Windows apps work out of the box, plus better support for Windows apps and games":
        "Les applis Windows marchent dès l'installation, et les applis et jeux Windows sont "
        "mieux pris en charge",
    "Bigger Store, with Steam and Heroic built in":
        "Un Store plus grand, avec Steam et Heroic inclus",
    "Pinned web apps keep their real icon":
        "Les applis web épinglées gardent leur vraie icône",
    "New installer: dual boot next to Windows or another Linux, resize partitions, "
    "better Wi-Fi page":
        "Nouvel installateur : double démarrage à côté de Windows ou d'un autre Linux, "
        "partitions redimensionnables, meilleure page Wi-Fi",
    "Cleaner, more reliable Raye Update": "Raye Update plus clair et plus fiable",
    "\"Try Raye\" mode: use Raye from the USB stick without installing":
        "Mode «\u00a0Essayer Raye\u00a0» : utilisez Raye depuis la clé USB, sans l'installer",
    "Store reviews and ratings": "Avis et notes dans le Store",
    "Switch to Raye from another system and keep your files":
        "Passez à Raye depuis un autre système en gardant vos fichiers",

    # V1 Beta 2
    "Windows-style window animations, maximize and snap":
        "Des animations de fenêtres comme dans Windows, pour l'agrandissement et l'ancrage aussi",
    "TikTok LIVE Studio and Affinity in the Store, FL Studio settings checked":
        "TikTok LIVE Studio et Affinity dans le Store, réglages de FL Studio vérifiés",
    "Game mode that turns on by itself while you play":
        "Un mode jeu qui s'active tout seul pendant que vous jouez",
    "Community Store requests: rekordbox and Mixxx":
        "Demandes de la communauté pour le Store : rekordbox et Mixxx",
    "14 more Windows apps in the Store, each one tested":
        "14 applis Windows de plus dans le Store, chacune essayée",
    "Windows bridge: copy your files, wallpaper and favorites from Windows":
        "Pont Windows : copiez vos fichiers, votre fond d'écran et vos favoris depuis Windows",
    "Clock: opens from the taskbar clock, and alarms wake the PC from sleep when it can":
        "Horloge : s'ouvre depuis l'horloge de la barre des tâches, et les alarmes sortent le PC de la veille quand il le permet",
    "Your files from Windows offered right after Setup":
        "Vos fichiers de Windows proposés juste après l'installation",
    "40+ popular Windows apps in the Store, each one tested, and \"Optimized for Raye\" badges":
        "Plus de 40 applis Windows populaires dans le Store, chacune essayée, avec le badge « Optimisé pour Raye »",
    "Complete Windows bridge: share drivers and settings with Windows":
        "Pont Windows complet : partager pilotes et réglages avec Windows",
    "Choose KDE or Hyprland during installation":
        "Choisir KDE ou Hyprland pendant l'installation",
    "Windows 10 look option": "Option pour l'apparence de Windows 10",
    "A real Windows 10 Start menu": "Un vrai menu Démarrer de Windows 10",
    "Windows-style window animations and snap previews":
        "Des animations de fenêtres comme dans Windows, et les aperçus d'ancrage",
    "FL Studio, TikTok LIVE Studio and Affinity, \"Optimized for Raye\" once tested":
        "FL Studio, TikTok LIVE Studio et Affinity, «\u00a0Optimisé pour Raye\u00a0» une fois testés",
    "Import your files from Windows": "Importer vos fichiers depuis Windows",
    "Install guide and keyboard support for Intel/AMD Chromebooks":
        "Guide d'installation et prise en charge du clavier pour les Chromebook Intel et AMD",
    "Fix for older AMD cards (RX 400/500) stuck on a black screen or low resolution":
        "Correctif pour les cartes AMD plus anciennes (RX 400/500) bloquées sur un écran noir "
        "ou en basse résolution",
    "Game performance: higher FPS and an advanced game mode":
        "Performances en jeu : plus d'images par seconde et un mode jeu avancé",
    "New Raye kernel: CachyOS and XanMod patches plus Raye's own tuning":
        "Nouveau noyau Raye : les correctifs de CachyOS et XanMod, plus les réglages de Raye",
    "Ready for Easy Anti-Cheat v2 (Fortnite): Raye's kernel key sent to Epic":
        "Prêt pour Easy Anti-Cheat v2 (Fortnite) : la clé du noyau Raye envoyée à Epic",
    "Lower RAM use at idle: 600–700 MB":
        "Moins de mémoire utilisée au repos : 600 à 700 Mo",
    "Ready-made virtual machine images": "Des images de machine virtuelle prêtes à l'emploi",
    "Community Store requests: Quadra, rekordbox and Mixxx":
        "Demandes de la communauté pour le Store : Quadra, rekordbox et Mixxx",
    "40+ popular Windows apps in the Store, each one tested":
        "Plus de 40 applis Windows populaires dans le Store, chacune testée",
    "Windows apps install silently with a real progress bar, start to finish":
        "Les applis Windows s'installent sans fenêtres à cliquer, avec une vraie barre de "
        "progression du début à la fin",
    "Complete Windows bridge: share drivers, files and settings with Windows":
        "Un vrai pont avec Windows : partagez pilotes, fichiers et réglages avec Windows",

    # V1 final
    "Final polish and fixes from both betas":
        "Dernières finitions et correctifs venus des deux bêtas",
    "New website, with fresh screenshots of the real system":
        "Nouveau site, avec de nouvelles captures du vrai système",
    "More languages": "Plus de langues",
    "Raye Assistant updated, on Discord and the website":
        "Assistant Raye mis à jour, sur Discord et sur le site",
    "Works on older PCs too (legacy BIOS, older processors like Core 2 Duo, 2–4 GB RAM)":
        "Marche aussi sur les PC plus anciens (BIOS ancien, processeurs plus vieux comme les Core 2 Duo, 2 à 4 Go de "
        "mémoire)",
    "Legal pages and FAQ": "Pages légales et foire aux questions",
    "New ISO for everyone": "Une nouvelle image ISO pour tout le monde",

    # V2
    "Raye account: your settings follow you to every PC":
        "Compte Raye : vos réglages vous suivent sur tous vos PC",
    "ARM PCs": "Les PC ARM",
    "Spanish, German, Portuguese and Italian": "Espagnol, allemand, portugais et italien",
    "Fingerprint readers": "Les lecteurs d'empreintes digitales",
    'More hardware works out of the box: Realtek and other Wi-Fi, webcam and sound drivers installed on their own when a device needs them':
        'Plus de matériel fonctionne tout de suite : les pilotes Wi-Fi, webcam et son de Realtek et d\'autres s\'installent tout seuls quand un appareil en a besoin',
    'More desktops to choose from: GNOME and niri, with a Windows look':
        'Plus de bureaux au choix : GNOME et niri, avec un look Windows',
    'Quick fixes (Nov 21): Steam and Heroic .deb install again, cleaner Game Mode list, Hyprland fixed (one taskbar on every screen, full screen, no wallet popup)':
        'Correctifs rapides (21 nov.) : les .deb de Steam et Heroic s\'installent de nouveau, liste du mode jeu épurée, Hyprland corrigé (une barre des tâches sur chaque écran, plein écran, plus de fenêtre du portefeuille)',
    'Printers & scanners page and a Scan app, plus longer laptop battery life':
        'Page Imprimantes et scanners et une appli de numérisation, plus d\'autonomie sur les portables',
    'Urgent fixes (Nov 20): full NVIDIA game speed, updates never stop halfway':
        'Correctifs urgents (20 nov.) : pleine vitesse en jeu sur NVIDIA, les mises à jour ne s\'arrêtent plus à moitié',
    'New install: start in Try Raye with an Install icon, full-screen Setup, English boot menu, Setup fixes':
        'Nouvelle installation : on démarre dans Essayer Raye avec une icône Installer, installateur en plein écran, menu de la clé en anglais, correctifs de l\'installateur',
    'Store apps you have move from Flatpak to APT once, nothing lost':
        'Vos applis du Store passent de Flatpak à APT une seule fois, sans rien perdre',
    'USB copies show the real speed, with close and minimize buttons':
        'Les copies vers une clé USB montrent la vraie vitesse, avec boutons fermer et réduire',
    'Customize Hyprland your way: your own settings file, simple instructions, never overwritten':
        'Personnaliser Hyprland à votre façon : votre propre fichier de réglages, des instructions simples, jamais écrasé',
    'Developer options and remote web page':
        'Options pour développeurs et page web à distance',
    'A real Raye screen to unlock an encrypted disk at startup':
        'Un vrai écran Raye pour déverrouiller un disque chiffré au démarrage',
    'Everything checked in French, screen by screen (installer included)':
        'Tout vérifié en français, écran par écran (installateur compris)',
    'Adobe apps: Photoshop first, then the others we can make work':
        "Applis Adobe : Photoshop d'abord, puis celles qu'on arrive à faire fonctionner",
    'Quadra in the Store (AppImage), with game mode on while Roblox runs':
        'Quadra dans le Store (AppImage), avec le mode jeu actif pendant Roblox',
    'No more freezes when RAM runs out: the PC slows down a little instead':
        'Plus de gel quand la mémoire manque : le PC ralentit un peu à la place',
    'Lower RAM use at idle: about 850 MB, down from 1 GB':
        'Moins de mémoire utilisée au repos : environ 850 Mo, contre 1 Go',
    'Switch between KDE and Hyprland from Settings in seconds, your apps reopen':
        'Passer de KDE à Hyprland depuis les Paramètres en quelques secondes, vos applis se rouvrent',
    'Updates always end on the newest version, even mid-download':
        'Les mises à jour finissent toujours sur la version la plus récente, même en plein téléchargement',
    'Store: APT apps first, Flatpak only when not on APT, plus AppImage':
        'Store : les applis APT d\'abord, Flatpak seulement si elles ne sont pas en APT, et AppImage',
    'Taskbar settings: left or center, icon size, taskbar height, auto-hide':
        'Réglages de la barre des tâches : à gauche ou au centre, taille des icônes, hauteur de la barre, masquage automatique',
    'Settings and every Raye app work well on Hyprland': 'Les Paramètres et toutes les applis Raye marchent bien sous Hyprland',
    'Complete Hyprland guide: change everything, Raye apps included, step by step': 'Guide complet de Hyprland : tout modifier, applis Raye comprises, étape par étape',
    'Install other Hyprland setups (dotfiles like Caelestia) in one step, and go back to Raye\'s anytime': 'Installer d’autres configurations Hyprland (dotfiles comme Caelestia) en une étape, et revenir à celle de Raye à tout moment',
    'KDE or Hyprland: choose at install, switch from Settings in seconds': 'KDE ou Hyprland : au choix à l’installation, bascule depuis les Paramètres en quelques secondes',
    'Windows 10 look, real Windows 10 Start menu, Windows-style animations and snap': 'Look Windows 10, vrai menu Démarrer de Windows 10, animations et dispositions à la Windows',
    'Bring your files, wallpaper, Wi-Fi and apps from Windows or your old system': 'Vos fichiers, fond d’écran, Wi-Fi et applis repris de Windows ou de votre ancien système',
    'Bigger Store: TikTok LIVE Studio, Affinity, rekordbox, Mixxx and 14 more tested apps': 'Store plus grand : TikTok LIVE Studio, Affinity, rekordbox, Mixxx et 14 autres applis testées',
    'Game mode on by itself, NVIDIA Control Panel, RAM at idle about 850 MB': 'Mode jeu automatique, Panneau de configuration NVIDIA, RAM au repos d’environ 850 Mo',
    'Many more settings, Clock that wakes the PC, real update percentage at startup': 'Beaucoup plus de réglages, Horloge qui réveille le PC, vrai pourcentage de mise à jour au démarrage',
    'Safe by default: firewall, private Wi-Fi address, automatic kernel security updates': 'Sûr par défaut : pare-feu, adresse Wi-Fi privée, mises à jour de sécurité du noyau automatiques',
    "Many fixes: snap, taskbar edge, sleep on PCs that can't, faster updates from your country's server": 'Beaucoup de correctifs : dispositions, bord de la barre des tâches, veille sur les PC incompatibles, mises à jour plus rapides depuis le serveur de votre pays',
    'Upgraded Windows layer: newest version, faster, more Windows apps tested and working': 'Couche Windows améliorée : dernière version, plus rapide, plus d’applis Windows testées et qui marchent',
    'Wobbly windows: a switch in Settings': 'Fenêtres gélatine : un interrupteur dans les Paramètres',
    'Taskbar on top or on the side of the screen': 'Barre des tâches en haut ou sur le côté de l’écran',
    'Join the team and a staff panel on the website':
        "Rejoindre l'équipe et un panneau du staff sur le site",
    'Public profiles and badges':
        'Profils publics et badges',
    'Raye Insider in Settings: Public Beta (sign up on the website), Beta and Dev update channels (application, access tied to your Raye account), leave anytime':
        'Raye Insider dans les Paramètres : canaux de mises à jour Bêta publique (inscription sur le site), Bêta et Dev (candidature, accès lié à votre compte Raye), quittez quand vous voulez',
    'Raye Assistant knows every version since 0.5':
        'Raye Assistant connaît chaque version depuis la 0.5',
    "Urgent fix (Nov 20): full game speed on NVIDIA again, one recommended driver, Graphics Card app fixed":
        "Correctif urgent (20 nov.) : pleine vitesse des jeux sur NVIDIA, un seul pilote recommandé, appli Carte graphique corrigée",
    "Urgent fix (Nov 20): updates no longer stop halfway, stuck PCs repair themselves, boot screen kept":
        "Correctif urgent (20 nov.) : les mises à jour ne s'arrêtent plus à moitié, les PC bloqués se réparent seuls, l'écran de démarrage reste",
    "Fix: the right NVIDIA driver installs automatically again (full FPS), and the NVIDIA app works":
        "Correctif : le bon pilote NVIDIA s'installe de nouveau tout seul (FPS au complet), et l'appli NVIDIA fonctionne",
    "Fix: an update can never stop halfway again (sign-in screen without mouse or keyboard)":
        "Correctif : une mise à jour ne peut plus s'arrêter à moitié (écran de connexion sans souris ni clavier)",
    "Raye Community beta: Raye's own chat, on the website and in Raye Linux, with your Raye account, roles, moderation and friends":
        "Raye Community en bêta : la discussion de Raye, sur le site et dans Raye Linux, avec ton compte Raye, des rôles, de la modération et des amis",
    "Raye Community complete: images and videos, private messages, staff tools, then it replaces the Discord server":
        "Raye Community complète : images et vidéos, messages privés, outils du staff, puis elle remplace le serveur Discord",
    "New account website and emails, with two-factor sign-in":
        "Nouveau site et nouveaux courriels du compte, avec la connexion en deux étapes",
    "Chromebooks with ARM chips": "Les Chromebook à puce ARM",
    "Raye Proton: pick Raye's Windows layer for Steam games":
        "Raye Proton : choisir la couche Windows de Raye pour les jeux Steam",

    # V3
    "Accounts: badges, community and admin panel":
        "Comptes : badges, communauté et panneau d'administration",
    "Local assistant, developer options and remote web page":
        "Assistant local, options pour les développeurs et page web à distance",
    "Every other language": "Toutes les autres langues",
    "Performance options in Settings, with a transparency switch":
        "Options de performances dans les Paramètres, avec un interrupteur de transparence",
    "Windows apps get their fonts, 32-bit games can use 4 GB, Store packages open":
        "Les applis Windows ont leurs polices, les jeux 32 bits peuvent utiliser 4 Go, les paquets du Store s'ouvrent",
    "AMD Graphics Card panel (fans, power, profiles) and the NVIDIA Control Panel":
        "Panneau Carte graphique AMD (ventilateurs, puissance, profils) et Panneau de configuration NVIDIA",
    "Fix for the flicker on NVIDIA cards at 144 Hz":
        "Correctif du scintillement des cartes NVIDIA à 144 Hz",
    "NVIDIA Control Panel opened from Settings":
        "Panneau de configuration NVIDIA ouvert depuis les Paramètres",
    "Clock: opens from the taskbar clock, and alarms wake the PC from sleep":
        "Horloge : s'ouvre depuis l'horloge de la barre des tâches, et les alarmes sortent le PC de la veille",
    "Many more settings like Windows 11":
        "Beaucoup plus de réglages comme dans Windows 11",
    "Windows layer fully hidden: Raye file dialogs, no technical names in Task Manager":
        "Couche Windows entièrement cachée : fenêtres de fichiers Raye, aucun nom technique dans le Gestionnaire des tâches",
    "Bring your wallpaper, Wi-Fi networks, apps and browser data from your old system":
        "Ramener ton fond d'écran, tes réseaux Wi-Fi, tes applis et les données de ton navigateur de ton ancien système",
    "Import your files from Windows right in Setup":
        "Importer tes fichiers de Windows directement pendant l'installation",
    "Check for very old processors before installing":
        "Vérification des très vieux processeurs avant l'installation",
    "Update screen at startup shows its real percentage":
        "L'écran de mise à jour au démarrage montre son vrai pourcentage",
    "Try Raye never touches the PC's own swap":
        "Le mode Essayer Raye ne touche jamais à l'espace d'échange du PC",
    "Store settings, and Synaptic removed":
        "Paramètres du Store, et Synaptic retiré",
    "Fix the maximize and snap glitch":
        "Correctif du bug d'agrandissement et d'ancrage des fenêtres",
    "Taskbar buttons clickable up to the screen edge":
        "Boutons de la barre des tâches cliquables jusqu'au bord de l'écran",
    "PCs whose sleep doesn't work get it turned off automatically, with a clear message "
    "(turn it back on in Settings)":
        "Sur les PC où la veille ne marche pas, elle est coupée automatiquement, avec un message "
        "clair (on peut la réactiver dans les Paramètres)",
    "Automatic kernel security updates":
        "Mises à jour de sécurité du noyau automatiques",
    "Fix the Merge folders window in File Explorer":
        "Correctif de la fenêtre « Fusionner les dossiers » de l'Explorateur",
    "The ISO works in virtual machines (VirtualBox, VMware, QEMU guest tools included)":
        "L'ISO fonctionne dans les machines virtuelles (outils invités VirtualBox, VMware et QEMU inclus)",
    "Safe by default: firewall on and a private Wi-Fi address, encrypted DNS one click away "
    "in Settings, nothing slowed down":
        "Sûr par défaut : pare-feu actif et adresse Wi-Fi privée, DNS chiffré à un clic dans "
        "les Paramètres, rien de ralenti",
    "Webcam, a built-in MIDI synth and Print to PDF for Windows programs":
        "Webcam, synthé MIDI intégré et Imprimer en PDF pour les programmes Windows",
}
