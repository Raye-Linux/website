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
        "lede": "What's coming to Raye Linux, in order. Ideas from the community come "
                "first: a lot of what's below started as a message in #ideas on our "
                "Discord.",
        "idea": "Share an idea on Discord",
        "same": "Same list as #roadmap on the Discord.",
        "legend": "Legend",
    },
    "fr": {
        "title": "Feuille de route",
        "nav": "Feuille de route",
        "description": "Ce qui s'en vient pour Raye Linux, dans l'ordre : ce qui est fait, "
                       "ce qui est en cours et ce qui est prévu.",
        "lede": "Ce qui s'en vient pour Raye Linux, dans l'ordre. Les idées de la "
                "communauté passent en premier : bien des choses plus bas ont commencé par "
                "un message dans #ideas, sur notre Discord.",
        "idea": "Proposer une idée sur Discord",
        "same": "La même liste que le salon #roadmap du Discord.",
        "legend": "Légende",
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
}

FR = {
    # section titles; \u00a0 keeps « » on the line of their words
    "Recently done": "Fait récemment",
    "V1 Beta 1 · out November 19": "V1 Bêta 1 · sortie le 19 novembre",
    "V1 Beta 2 (next big update)": "V1 Bêta 2 (la prochaine grosse mise à jour)",
    "V1 final": "V1 finale",
    "V2": "V2",
    "V3": "V3",

    # recently done
    "New download (Nov 18) with all the latest fixes built in":
        "Nouveau téléchargement (18 novembre) avec tous les derniers correctifs inclus",
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
    "New Raye kernel tuned for gaming and smoothness":
        "Nouveau noyau Raye, réglé pour les jeux et un bureau plus réactif",
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
    "New ISO for everyone": "Une nouvelle image ISO pour tout le monde",

    # V2
    "Raye account: your settings follow you to every PC":
        "Compte Raye : vos réglages vous suivent sur tous vos PC",
    "ARM PCs": "Les PC ARM",
    "Spanish, German, Portuguese and Italian": "Espagnol, allemand, portugais et italien",

    # V3
    "Local assistant and developer options":
        "Assistant local et options pour les développeurs",
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
    "Laptops wake from sleep reliably":
        "Les portables sortent de la veille sans problème",
    "Automatic kernel security updates":
        "Mises à jour de sécurité du noyau automatiques",
    "Fix the Merge folders window in File Explorer":
        "Correctif de la fenêtre « Fusionner les dossiers » de l'Explorateur",
    "The ISO works in virtual machines (VirtualBox, VMware, QEMU guest tools included)":
        "L'ISO fonctionne dans les machines virtuelles (outils invités VirtualBox, VMware et QEMU inclus)",
    "Locked-down by default: firewall on, encrypted DNS, private Wi-Fi address, without limiting anything":
        "Verrouillé par défaut : pare-feu actif, DNS chiffré, adresse Wi-Fi privée, sans rien limiter",
    "Webcam, a built-in MIDI synth and Print to PDF for Windows programs":
        "Webcam, synthé MIDI intégré et Imprimer en PDF pour les programmes Windows",
}
