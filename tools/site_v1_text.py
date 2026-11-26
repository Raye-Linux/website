"""Every word of the V1 site, French and English side by side.

Each page is a list of blocks, and every text in a block is a pair
L(fr, en): the two languages cannot drift apart in structure, only in
wording. tools/site_v1.py turns the blocks into HTML.

Inside a text:
  {p:key}   the address of page `key` in the reader's language
  {m:key}   the value of MEASURES[key] in the reader's language
  <kbd>, <strong>, <a>, <em> are allowed; nothing else.

Every claim is something measured, said in the present tense. The
sentences are re-checked on the 1.0 image before the site goes online.

This file is long on purpose: it is the text of twelve pages in two
languages, nothing else. Splitting it would scatter one page's French
away from its English, which is the drift the pairing exists to stop."""


def L(fr, en):
    return {"fr": fr, "en": en}


# The version the site speaks for. The download page reads its own from
# tools/release.json; this one is for the text.
VERSION = "1.0"

# Every figure the site prints. `version` is the Raye version measured;
# at launch test_site_v1.py refuses anything that was not measured on 1.0.
# `machine` is a key of MACHINES. Source: the measures of each machine.
MEASURES = {
    "ram": {
        "name": L("Mémoire au repos", "Memory at idle"),
        "value": L("850 Mo", "850 MB"),
        "version": "1.0 Beta 2", "date": "2026-11-19", "machine": "vm130",
        "how": L("3 min après l'ouverture de la session, moyenne de 3 relevés",
                 "3 min after signing in, mean of 3 readings"),
    },
    "black": {
        "name": L("Écran noir au démarrage", "Black screen at startup"),
        "value": L("2,75 à 3 s", "2.75 to 3 s"),
        "version": "0.3", "date": "2026-11-11", "machine": "vm130",
        "how": L("entre le micrologiciel et l'image de Raye, une capture toutes les 250 ms ; "
                 "18,3 s en 0.2",
                 "between the firmware and the Raye picture, one capture every 250 ms; "
                 "18.3 s in 0.2"),
    },
    "install": {
        "name": L("Durée de l'installation", "Install time"),
        "value": L("5 min 50 s", "5 min 50 s"),
        "version": "0.3", "date": "2026-11-11", "machine": "vm130",
        "how": L("du clic sur Installer à « Redémarrage », disque de 64 Go chiffré",
                 "from the click on Install to “Restart”, 64 GB disk, encrypted"),
    },
    "restart": {
        "name": L("Redémarrage pour une mise à jour", "Restart for an update"),
        "value": L("24 s", "24 s"),
        "version": "0.3", "date": "2026-11-11", "machine": "vm130",
        "how": L("de l'image de démarrage à l'écran de connexion, pour le thème du bureau",
                 "from the startup picture to the sign-in screen, for the desktop theme"),
    },
    "fetch": {
        "name": L("Recherche des mises à jour", "Checking for updates"),
        "value": L("22 s", "22 s"),
        "version": "0.3", "date": "2026-11-11", "machine": "vm130",
        "how": L("recherche et téléchargement de 42 mises à jour, 60 Mo en tout",
                 "checking for and downloading 42 updates, 60 MB in all"),
    },
}

MACHINES = {
    "vm130": L("sur la machine de test (machine virtuelle, 8 cœurs, 16 Go, sans carte graphique)",
               "on the test machine (virtual machine, 8 cores, 16 GB, no graphics card)"),
    "latitude": L("sur un Dell Latitude 5420 (16 Go)", "on a Dell Latitude 5420 (16 GB)"),
}

# The free disk space the installer demands (installer welcomeq.conf,
# requiredStorage). test_site_v1.py reads that file and compares.
FREE_GB = 25

# The pages, in the order of the footer. Each has its address in both
# languages and the short name used in links.
PAGES = {
    "home": {"path": L("/", "/en/"), "name": L("Accueil", "Home")},
    "desktop": {"path": L("/bureau/", "/en/desktop/"), "name": L("Le bureau", "The desktop")},
    "windows": {"path": L("/programmes-windows/", "/en/windows-programs/"),
                "name": L("Programmes Windows", "Windows programs")},
    "updates": {"path": L("/mises-a-jour/", "/en/updates/"), "name": L("Mises à jour", "Updates")},
    "security": {"path": L("/securite/", "/en/security/"),
                 "name": L("Sécurité et vie privée", "Security and privacy")},
    "hardware": {"path": L("/materiel/", "/en/hardware/"), "name": L("Matériel", "Hardware")},
    "install": {"path": L("/installer/", "/en/install/"), "name": L("Installer", "Install")},
    "questions": {"path": L("/questions/", "/en/questions/"), "name": L("Questions", "Questions")},
    "releases": {"path": L("/versions/", "/en/releases/"), "name": L("Versions", "Releases")},
    "about": {"path": L("/a-propos/", "/en/about/"), "name": L("À propos", "About")},
    "privacy": {"path": L("/confidentialite/", "/en/privacy/"),
                "name": L("Confidentialité", "Privacy")},
    "download": {"path": L("/telecharger/", "/en/download/"), "name": L("Télécharger", "Download")},
    "games": {"path": L("/jeux/", "/en/games/"), "name": L("Jeux", "Games")},
    "desktops": {"path": L("/deux-bureaux/", "/en/two-desktops/"),
                 "name": L("Deux bureaux", "Two desktops")},
    "oldpcs": {"path": L("/vieux-pc/", "/en/old-pcs/"), "name": L("Vieux PC", "Older PCs")},
    "v1": {"path": L("/nouveautes/", "/en/whats-new/"), "name": L("Dans la V1", "What's in V1")},
    "soon": {"path": L("/ensuite/", "/en/whats-next/"), "name": L("Ensuite", "What's next")},
    "insider": {"path": L("/insider/", "/en/insider/"), "name": L("Raye Insider", "Raye Insider")},
}

# the pages about people, the legal pages and the shared ones (roadmap,
# source) live in site_v1_join_text.py; they join this list here
from site_v1_join_text import PAGES as _MORE  # noqa: E402

PAGES.update(_MORE)

NAV = ["desktop", "windows", "games", "install", "questions", "community"]
FOOTER = [
    (L("Découvrir", "Look around"), ["desktop", "desktops", "windows", "games", "updates",
                                      "security"]),
    (L("Avant d'installer", "Before you install"), ["hardware", "oldpcs", "install",
                                                    "download"]),
    (L("Le projet", "The project"), ["v1", "soon", "roadmap", "releases", "questions", "about",
                                      "source"]),
    (L("Communauté", "Community"), ["community", "insider", "join", "rules"]),
    (L("Légal", "Legal"), ["privacy", "terms", "cookies", "betaterms", "notice", "licenses"]),
]

UI = {
    "fr": {
        "skip": "Aller au contenu",
        "brand_label": "Raye Linux, accueil",
        "switch": "English", "switch_lang": "en", "switch_label": "Read this page in English",
        "nav_label": "Pages",
        "download": "Télécharger",
        "download_held": "Téléchargement à la sortie",
        "next": "La suite",
        "limits": "Ce qui manque encore",
        "shot_todo": "Capture à prendre",
        "shot_note": "Emplacement réservé : la capture sera prise sur la version {v}.",
        "mail": "bonjour@rayelinux.com",
        "rights": "© 2026 Raye Linux",
        "measured": "Mesuré le {date}, version {version}, {machine}.",
        "col_measure": "Mesure", "col_value": "Valeur", "col_where": "Machine et date",
        "planned": "prévu",
        "to_come": "à venir",
    },
    "en": {
        "skip": "Skip to content",
        "brand_label": "Raye Linux, home",
        "switch": "Français", "switch_lang": "fr", "switch_label": "Lire cette page en français",
        "nav_label": "Pages",
        "download": "Download",
        "download_held": "Download at release",
        "next": "Next",
        "limits": "What is still missing",
        "shot_todo": "Screenshot to take",
        "shot_note": "Placeholder: this screenshot will be taken on version {v}.",
        "mail": "bonjour@rayelinux.com",
        "rights": "© 2026 Raye Linux",
        "measured": "Measured on {date}, version {version}, {machine}.",
        "col_measure": "Measure", "col_value": "Value", "col_where": "Machine and date",
        "planned": "planned",
        "to_come": "to come",
    },
}

# The screenshots the pages show. Each id becomes
# assets/shots/<id>-<lang>-1600.webp (+ -800.webp, -1600.jpg) once taken on
# the 1.0 image in the test VM; until then the page shows a labelled placeholder.
# The text is the alt text of the picture, and on a placeholder it says
# what the screenshot has to show.
SHOTS = {
    "desktop": L("Le bureau de Raye : le menu Démarrer ouvert sur les applications épinglées, "
                 "au-dessus de la barre des tâches centrée.",
                 "The Raye desktop: the Start menu open on the pinned apps, above the centered "
                 "taskbar."),
    "explorer": L("L'Explorateur de fichiers sur la page Accueil, avec deux onglets ouverts dans "
                  "la barre de titre.",
                  "File Explorer on its Home page, with two tabs open in the title bar."),
    "update-live": L("Raye Update dans les Paramètres : des mises à jour déjà installées et une "
                     "seule marquée « Redémarrage requis ».",
                     "Raye Update in Settings: updates already installed and a single one marked "
                     "“Restart required”."),
    "start-all": L("Le menu Démarrer sur Toutes les applications, rangées en catégories.",
                   "The Start menu on All apps, sorted into categories."),
    "win-x": L("Le menu des liens rapides ouvert par Win+X, au-dessus du bouton Démarrer.",
               "The quick links menu opened by Win+X, above the Start button."),
    "snap": L("Une fenêtre glissée vers le haut de l'écran : la barre des dispositions et la zone "
              "où elle va se placer.",
              "A window dragged to the top of the screen: the layout bar and the area where it "
              "will land."),
    "quick": L("Les paramètres rapides ouverts depuis la barre : le réseau et le son, avec la "
               "tuile Ethernet du réseau filaire.",
               "Quick settings opened from the taskbar: network and sound, with the Ethernet "
               "tile of the wired network."),
    "thispc": L("Ce PC dans l'Explorateur, et la fenêtre Propriétés du lecteur Raye avec l'espace "
                "utilisé et libre.",
                "This PC in File Explorer, and the Properties window of the Raye drive with the "
                "used and free space."),
    "taskmgr": L("Le Gestionnaire des tâches sur la page Processus, ouvert avec Ctrl+Maj+Échap.",
                 "Task Manager on the Processes page, opened with Ctrl+Shift+Esc."),
    "settings": L("La fenêtre Paramètres sur la page Système, avec la liste des catégories à "
                  "gauche.",
                  "The Settings window on the System page, with the list of categories on the "
                  "left."),
    "control": L("Le Panneau de configuration ouvert par Win+R puis control, en vue par "
                 "catégories.",
                 "Control Panel opened with Win+R then control, in the category view."),
    "regedit": L("L'Éditeur du Registre de Raye sur une clé, avec l'invite de mot de passe "
                 "par-dessus avant une écriture système.",
                 "The Raye Registry Editor on a key, with the password prompt on top before a "
                 "system write."),
    "calendar": L("L'horloge de la barre ouverte sur le mois, et un rappel du Calendrier affiché "
                  "en notification.",
                  "The taskbar clock opened on the month, and a Calendar reminder shown as a "
                  "notification."),
    "store": L("Le Raye Store pendant l'installation d'une appli, avec la progression et le "
               "bouton Annuler.",
               "The Raye Store while an app installs, with the progress and the Cancel "
               "button."),
    "lock": L("L'écran de verrouillage de Raye, avec l'heure, la date et le champ du mot de "
              "passe.",
              "The Raye lock screen, with the time, the date and the password field."),
    "exe-setup": L("L'installateur d'un programme Windows ouvert d'un double-clic sur son "
                   "fichier .exe, en cours d'installation.",
                   "The installer of a Windows program opened by double-clicking its .exe file, "
                   "halfway through."),
    "exe-start": L("Le même programme Windows dans le menu Démarrer après son installation, puis "
                   "ouvert sur le bureau.",
                   "The same Windows program in the Start menu after it installed, then open on "
                   "the desktop."),
    "exe-native": L("Raye qui propose la version pour Raye d'un programme au double-clic sur son "
                    "installateur Windows.",
                    "Raye offering the Raye version of a program when its Windows installer is "
                    "double-clicked."),
    "update-boot": L("L'écran du redémarrage : l'œil de Raye, l'anneau et « Installation des "
                     "mises à jour » avec le pourcentage.",
                     "The restart screen: the Raye eye, the ring and “Installing updates” with "
                     "the percentage."),
    "restore": L("Points de restauration avec la paire « Avant les mises à jour » et « Après les "
                 "mises à jour ».",
                 "Restore points with the “Before updates” and “After updates” pair."),
    "uac": L("L'invite de mot de passe : l'écran assombri, « Éditeur vérifié : Raye Linux », "
             "Oui et Non.",
             "The password prompt: the dimmed screen, “Verified publisher: Raye Linux”, Yes and "
             "No."),
    "recovery-key": L("La fenêtre de la clé de récupération à la première connexion, la clé "
                      "elle-même floutée.",
                      "The recovery key window at the first sign-in, the key itself "
                      "blurred."),
    "setup-disk": L("La page Disque de l'installateur, sur « Installer à côté de Windows », avec la "
                    "réglette qui partage le disque.",
                    "The installer's Disk page on “Install alongside Windows”, with the slider "
                    "that splits the disk."),
    "setup-encrypt": L("La page Disque de l'installateur, case « Chiffrer le système Raye » cochée, "
                       "avec les deux champs du mot de passe du disque.",
                       "The installer's Disk page, “Encrypt the Raye system” ticked, with the two "
                       "disk password fields."),
    "setup-summary": L("Le résumé « Prêt pour l'installation » de l'installateur, avec le bandeau rouge qui "
                       "dit ce qui sera effacé.",
                       "The installer's “Ready to install” summary, with the red banner that "
                       "says what will be erased."),
    "boot-menu": L("Le menu de démarrage avec deux choix, Raye Linux et Windows, et le compte à "
                   "rebours.",
                   "The startup menu with two choices, Raye Linux and Windows, and the "
                   "countdown."),
}


def limits(*items):
    return ("limits", list(items))


def P(fr, en):
    return ("p", L(fr, en))


def H(key, fr, en):
    return ("h2", key, L(fr, en))


# ---------------------------------------------------------------- home

HOME = {
    "title": L("Raye Linux · Le bureau de Windows 11, gratuit, sur un autre système",
               "Raye Linux · The Windows 11 desktop, free, on another system"),
    "description": L("Raye Linux est un système gratuit pour PC qui reprend la disposition de "
                     "Windows 11. Chaque chiffre de ce site porte sa machine et sa date.",
                     "Raye Linux is a free system for PCs that keeps the Windows 11 layout. Every "
                     "figure on this site comes with its machine and its date."),
    "h1": L("Le bureau de Windows 11, sur un système qui n'en est pas un.",
            "The Windows 11 desktop, on a system that isn't Windows."),
    "lede": L("Raye Linux est gratuit et s'installe sur un PC ordinaire. Démarrer est au milieu de "
              "la barre, <kbd>Win</kbd>+<kbd>E</kbd> ouvre l'Explorateur, "
              "<kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>Échap</kbd> le Gestionnaire des tâches. "
              "Dessous, ce n'est pas Windows, et ce site dit ce que ça change.",
              "Raye Linux is free and installs on an ordinary PC. Start sits in the middle of the "
              "taskbar, <kbd>Win</kbd>+<kbd>E</kbd> opens File Explorer, "
              "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Esc</kbd> opens Task Manager. Underneath, it "
              "isn't Windows, and this site tells you what that changes."),
    "meta": L("Version {v}, en français et en anglais.",
              "Version {v}, in English and French."),
    "more": L("Ce qui change en venant de Windows", "What changes coming from Windows"),
    "hero_shot": "desktop",
    "blocks": [
        H("changes", "Ce qui ne change pas, ce qui change",
          "What stays the same, what changes"),
        ("pair",
         L("Vous retrouvez", "You'll find"),
         [L("La barre des tâches centrée, avec Démarrer, vos applis épinglées et l'horloge sur "
            "chaque écran.",
            "The centered taskbar, with Start, your pinned apps and the clock on every screen."),
          L("<kbd>Win</kbd>+<kbd>X</kbd>, <kbd>Win</kbd>+<kbd>R</kbd> et "
            "<kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>Échap</kbd>, qui ouvrent les mêmes fenêtres que "
            "sous Windows.",
            "<kbd>Win</kbd>+<kbd>X</kbd>, <kbd>Win</kbd>+<kbd>R</kbd> and "
            "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Esc</kbd>, which open the same windows as on "
            "Windows."),
          L("L'Explorateur avec ses onglets, Ce PC et les Propriétés d'un lecteur.",
            "File Explorer with its tabs, This PC and a drive's Properties."),
          L("Un Panneau de configuration et un Éditeur du Registre, ceux de Raye.",
            "A Control Panel and a Registry Editor, Raye's own."),
          L("Un fichier .exe qui se lance d'un double-clic.",
            "An .exe file that starts with a double-click.")],
         L("Ce qui est différent", "What is different"),
         [L("Il n'y a pas de lecteur « C: ». Le disque s'appelle Raye ; s'il y a une partition "
            "Windows, elle s'appelle Windows.",
            "There is no “C:” drive. The disk is called Raye; a Windows partition, if there is "
            "one, is called Windows."),
          L("Les mises à jour qui n'ont pas besoin d'un redémarrage s'installent pendant que vous "
            "travaillez. Les autres attendent que vous choisissiez « Mettre à jour et "
            "redémarrer ».",
            "Updates that don't need a restart install while you work. The others wait until "
            "you choose “Update and restart”."),
          L("Les applis viennent du Raye Store plutôt que d'un .exe trouvé sur le web, même si "
            "le .exe reste possible.",
            "Apps come from the Raye Store rather than an .exe found on the web, though the .exe "
            "still works."),
          L("Certains programmes Windows ne marchent pas, et les jeux protégés par un "
            "anti-triche du noyau de Windows ne marchent pas du tout.",
            "Some Windows programs don't run, and games protected by a Windows kernel "
            "anti-cheat don't run at all."),
          L("Quand un programme existe aussi pour Raye, comme Discord ou Steam, Raye vous "
            "propose cette version-là plutôt que celle de Windows.",
            "When a program also exists for Raye, such as Discord or Steam, Raye offers you "
            "that version rather than the Windows one.")]),
        ("shot", "explorer"),
        H("numbers", "Trois mesures, et leurs limites", "Three measurements, and their limits"),
        P("Je ne publie que ce que j'ai mesuré, avec la machine et la date. Pour l'instant, ces "
          "chiffres viennent d'une machine virtuelle sans carte graphique, plus lente qu'un vrai "
          "PC : sur un vrai PC, ils seront différents, et ils seront ici.",
          "I only publish what I measured, with the machine and the date. For now these figures "
          "come from a virtual machine without a graphics card, slower than a real PC: on a "
          "real PC they will be different, and they will be here."),
        ("measures", ["ram", "install", "black"]),
        P("Le détail, et ce que je n'ai pas encore pu mesurer, est sur la page "
          "<a href=\"{p:hardware}\">Matériel</a>.",
          "The details, and what I could not measure yet, are on the "
          "<a href=\"{p:hardware}\">Hardware</a> page."),
        H("start", "Par où commencer", "Where to start"),
        ("path", [
            ("desktop", L("Ce qui vous attend à l'écran : Démarrer, la barre, l'Explorateur, et "
                          "chaque appli de Raye.",
                          "What you'll see on screen: Start, the taskbar, File Explorer, and "
                          "each Raye app.")),
            ("windows", L("Est-ce que mes programmes Windows vont marcher ? Ce que je sais, et ce "
                          "que je ne sais pas encore.",
                          "Will my Windows programs run? What I know, and what I don't know "
                          "yet.")),
            ("games", L("Steam, la couche Windows des jeux, et les anti-triche : ce qui marche, "
                        "ce qui ne marche pas.",
                        "Steam, the Windows layer for games, and anti-cheat: what runs, what "
                        "doesn't.")),
            ("hardware", L("Ce qu'il faut comme PC, et sur quoi Raye a été essayé.",
                           "What kind of PC you need, and what Raye was tried on.")),
            ("install", L("La clé USB, l'installateur étape par étape, et Windows à côté.",
                          "The USB stick, the installer step by step, and Windows alongside.")),
            ("v1", L("Ce que contient la version {v}, et ce qui est encore en cours.",
                     "What version {v} contains, and what is still in progress.")),
        ]),
        ("note",
         L("Pourquoi je fais Raye", "Why I make Raye"),
         [L("Je fais Raye pour qu'on puisse changer de système sans réapprendre son ordinateur. "
            "La barre des tâches, Démarrer et les Paramètres doivent être là où la main va déjà. "
            "Quand ce n'est pas le cas, dites-le-moi.",
            "I make Raye so that changing systems doesn't mean learning your computer all over "
            "again. The taskbar, Start and Settings should be where your hand already goes. When "
            "they aren't, tell me."),
           L("La première image de travail date du 30 octobre 2026. Entre elle et cette version, "
             "il y a eu un Gestionnaire des tâches, un Explorateur refait, des mises à jour qui "
             "s'installent sans redémarrage, et beaucoup de choses essayées puis jetées. Tout est "
             "sur la page <a href=\"{p:releases}\">Versions</a>.",
             "The first working image dates from October 30, 2026. Between it and this version "
             "came a Task Manager, a rebuilt File Explorer, updates that install without a "
             "restart, and a lot of things tried and thrown away. It's all on the "
             "<a href=\"{p:releases}\">Releases</a> page."),
           L("Si quelque chose ne marche pas chez vous, écrivez-moi. C'est comme ça que je décide "
             "quoi régler en premier.",
             "If something doesn't work for you, write to me. That's how I decide what to fix "
             "first.")]),
    ],
}

# ---------------------------------------------------------------- pages

DESKTOP = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Le bureau et les applis de Raye", "The Raye desktop and apps"),
    "description": L("La barre des tâches, Démarrer, les raccourcis, l'Explorateur et les autres "
                     "applis de Raye : ce qu'elles font, et ce qui leur manque.",
                     "The taskbar, Start, the shortcuts, File Explorer and the other Raye apps: "
                     "what they do, and what they still lack."),
    "lede": L("J'ai essayé chaque chose décrite ici dans une session de Raye, pas seulement lu le "
              "code. Quand je connais un défaut, ou que je n'ai pas fini d'essayer, c'est écrit "
              "juste en dessous.",
              "I tried everything described here in a Raye session, not just read the code. When "
              "I know of a flaw, or haven't finished trying something, it's written right below "
              "it."),
    "next": "windows",
    "blocks": [
        H("taskbar", "La barre des tâches et Démarrer", "The taskbar and Start"),
        P("La barre est centrée : Démarrer, la recherche, vos applis épinglées, puis l'horloge à "
          "droite. Avec deux écrans, chacun a sa barre et son horloge ; les icônes de "
          "notification restent sur l'écran principal, comme sous Windows 11. Une fenêtre "
          "réduite garde son bouton.",
          "The taskbar is centered: Start, search, your pinned apps, then the clock on the right. "
          "With two screens each one gets its own taskbar and clock; the notification icons stay "
          "on the main screen, as in Windows 11. A minimized window keeps its button."),
        P("Démarrer montre vos applis épinglées, puis « Toutes les applications » en catégories, "
          "en grille ou en liste. Les applis portent les noms de Windows : Calculatrice, Paint, "
          "Photos, Lecteur multimédia, Gestionnaire des tâches.",
          "Start shows your pinned apps, then “All apps” as categories, a grid or a list. The "
          "apps carry their Windows names: Calculator, Paint, Photos, Media Player, Task "
          "Manager."),
        ("shot", "start-all"),
        limits(L("Le champ de recherche et la section Recommandé ne sont pas encore ceux de "
                 "Windows 11.",
                 "The search field and the Recommended section are not yet the Windows 11 "
                 "ones."),
               L("Démarrer et certains menus s'ouvrent avec un temps de retard, et leurs "
                 "animations ne sont pas encore celles de Windows 11.",
                 "Start and some menus open with a lag, and their animations are not yet the "
                 "Windows 11 ones.")),
        H("keys", "Les raccourcis", "The shortcuts"),
        P("Ceux-ci ont été essayés un par un. Le menu de <kbd>Win</kbd>+<kbd>X</kbd> s'ouvre "
          "aussi d'un clic droit sur Démarrer, sur l'écran où est la souris.",
          "These were tried one by one. The <kbd>Win</kbd>+<kbd>X</kbd> menu also opens with a "
          "right-click on Start, on the screen where the mouse is."),
        ("keys", [
            (L("<kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>Échap</kbd>",
               "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Esc</kbd>"),
             L("Gestionnaire des tâches", "Task Manager")),
            (L("<kbd>Win</kbd>+<kbd>E</kbd>", "<kbd>Win</kbd>+<kbd>E</kbd>"),
             L("Explorateur de fichiers", "File Explorer")),
            (L("<kbd>Win</kbd>+<kbd>R</kbd>", "<kbd>Win</kbd>+<kbd>R</kbd>"),
             L("Exécuter : <code>control</code>, <code>regedit</code>, et <code>notepad</code>, "
               "qui ouvre l'éditeur de texte",
               "Run: <code>control</code>, <code>regedit</code>, and <code>notepad</code>, which "
               "opens the text editor")),
            (L("<kbd>Win</kbd>+<kbd>X</kbd>", "<kbd>Win</kbd>+<kbd>X</kbd>"),
             L("Liens rapides : applications installées, gestion des disques, terminal, "
               "arrêter…",
               "Quick links: installed apps, disk management, terminal, shut down…")),
        ]),
        ("shot", "win-x"),
        H("windows", "Ranger les fenêtres", "Arranging windows"),
        P("Glissez une fenêtre vers le haut de l'écran : la barre des dispositions apparaît, et "
          "une zone pâle montre où la fenêtre va se poser. Lâchez, elle s'y place. Sur un écran "
          "de 1920×1080, il y a six dispositions. Sur le bureau, <kbd>Ctrl</kbd> et la molette "
          "changent la taille des icônes.",
          "Drag a window to the top of the screen: the layout bar shows up, and a pale area "
          "shows where the window will land. Let go and it snaps there. A 1920×1080 screen gets "
          "six layouts. On the desktop, <kbd>Ctrl</kbd> and the mouse wheel change the icon "
          "size."),
        ("shot", "snap"),
        H("quick", "Les paramètres rapides", "Quick settings"),
        P("Un clic à droite de la barre ouvre le réseau, le son et, sur un portable, la "
          "luminosité. Un clic au milieu d'une tuile l'allume ou l'éteint ; sa flèche ouvre une "
          "petite page dans le volet ; un clic droit mène aux Paramètres. Avec un câble branché, "
          "la tuile s'appelle Ethernet.",
          "A click on the right of the taskbar opens network, sound and, on a laptop, "
          "brightness. A click in the middle of a tile turns it on or off; its arrow opens a "
          "small page in the panel; a right-click leads to Settings. With a cable plugged in, "
          "the tile is called Ethernet."),
        ("shot", "quick"),
        H("explorer", "L'Explorateur de fichiers", "File Explorer"),
        P("Les dossiers s'ouvrent en onglets, dans la barre de titre, et la barre d'adresse sert "
          "aussi à chercher. Les Propriétés d'un lecteur donnent l'espace utilisé et libre à "
          "l'octet près, avec un bouton Nettoyer pour faire de la place.",
          "Folders open in tabs, in the title bar, and the address bar also searches. A drive's "
          "Properties give the used and free space to the byte, with a Clean up button to make "
          "room."),
        P("Il n'y a pas de lettres de lecteur. Dans Ce PC, le disque du système s'appelle Raye, "
          "et une partition Windows s'appelle Windows. C'est un choix : une lettre ne dit rien "
          "de ce qu'il y a dessus.",
          "There are no drive letters. In This PC the system disk is called Raye, and a Windows "
          "partition is called Windows. It's a choice: a letter says nothing about what's on "
          "the drive."),
        ("shot", "thispc"),
        H("taskmgr", "Le Gestionnaire des tâches", "Task Manager"),
        P("<kbd>Ctrl</kbd>+<kbd>Maj</kbd>+<kbd>Échap</kbd> l'ouvre sur Processus. Il a aussi "
          "Performances, Applications de démarrage, Utilisateurs, Détails et Services, avec les "
          "services qui tournent sur votre PC.",
          "<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Esc</kbd> opens it on Processes. It also has "
          "Performance, Startup apps, Users, Details and Services, with the services running on "
          "your PC."),
        ("shot", "taskmgr"),
        limits(L("Le premier lancement prend plusieurs secondes.",
                 "The first start takes several seconds."),
               L("Je n'ai vu les pages autres que Processus que sur un écran virtuel, pas encore "
                 "dans une session ouverte.",
                 "I have only seen the pages other than Processes on a virtual screen, not yet "
                 "in a signed-in session."),
               L("« Exécuter en tant qu'administrateur » ne lance pas un programme qui a une "
                 "fenêtre, et ne dit rien.",
                 "“Run as administrator” doesn't start a program that has a window, and says "
                 "nothing."),
               L("Quatre messages de confirmation restent en anglais dans une session en "
                 "français.",
                 "Four confirmation messages stay in English in a French session."),
               L("La page Utilisateurs n'a pas de bouton « Se déconnecter ».",
                 "The Users page has no “Sign out” button."),
               L("Démarrer ou arrêter un service depuis la page Services n'a pas encore été "
                 "essayé jusqu'au bout.",
                 "Starting or stopping a service from the Services page has not been tried all "
                 "the way yet.")),
        H("settings", "Les Paramètres", "Settings"),
        P("Une seule fenêtre, la liste des catégories à gauche. On y choisit l'écran principal, "
          "les mises à jour, les pilotes. Quand une page de Windows n'a pas d'équivalent dans "
          "Raye, elle le dit et renvoie au manuel plutôt que de rester vide.",
          "One window, the list of categories on the left. That's where you pick the main "
          "screen, updates, drivers. When a Windows page has no counterpart in Raye, it says so "
          "and points to the handbook instead of staying empty."),
        ("shot", "settings"),
        limits(L("Dans Applications installées, le menu « … » s'affiche transparent.",
                 "In Installed apps, the “…” menu shows up see-through."),
               L("Plusieurs pages ne sont pas finies.",
                 "Several pages are not finished.")),
        H("control", "Le Panneau de configuration et l'Éditeur du Registre",
          "Control Panel and the Registry Editor"),
        P("<kbd>Win</kbd>+<kbd>R</kbd>, <code>control</code> : le Panneau de configuration, par "
          "catégories. « Changer l'arrière-plan » ouvre la bonne page des Paramètres.",
          "<kbd>Win</kbd>+<kbd>R</kbd>, <code>control</code>: Control Panel, by category. "
          "“Change the background” opens the right page of Settings."),
        ("shot", "control"),
        P("<kbd>Win</kbd>+<kbd>R</kbd>, <code>regedit</code> : l'Éditeur du Registre de Raye. "
          "Raye n'a pas de registre ; l'éditeur montre ses vrais fichiers de réglages sous la "
          "forme d'un arbre, HKEY_CURRENT_USER pour les vôtres, HKEY_LOCAL_MACHINE pour ceux du "
          "système. Écrire dans le système demande votre mot de passe, une copie est faite "
          "avant chaque écriture, et Édition, Annuler remet le fichier exactement comme il "
          "était.",
          "<kbd>Win</kbd>+<kbd>R</kbd>, <code>regedit</code>: the Raye Registry Editor. Raye "
          "has no registry; the editor shows its real settings files as a tree, "
          "HKEY_CURRENT_USER for yours, HKEY_LOCAL_MACHINE for the system's. Writing to the "
          "system asks for your password, a copy is made before every write, and Edit, Undo "
          "puts the file back exactly as it was."),
        ("shot", "regedit"),
        limits(L("<kbd>Ctrl</kbd>+<kbd>Z</kbd> au clavier ne fait rien encore : passez par le "
                 "menu Édition.",
                 "<kbd>Ctrl</kbd>+<kbd>Z</kbd> does nothing yet: use the Edit menu."),
               L("Une fois votre mot de passe tapé, l'éditeur peut écrire dans le système "
                 "pendant cinq minutes sans le redemander.",
                 "Once you've typed your password, the editor can write to the system for five "
                 "minutes without asking again."),
               L("Un fichier de réglages d'une appli de Raye modifié ici n'est plus remplacé par "
                 "les mises à jour suivantes de cette appli.",
                 "A settings file of a Raye app changed here is no longer replaced by that app's "
                 "later updates.")),
        H("calendar", "Le Calendrier", "Calendar"),
        P("Créez un événement, fermez la fenêtre : entre deux rappels, aucun programme du "
          "Calendrier ne tourne. Le rappel arrive quand même à l'heure, avec « Plus tard » et "
          "« Ignorer ». L'horloge de la barre montre les événements du jour. Tout tient dans un "
          "seul fichier .ics sur votre PC, qu'on peut importer et exporter.",
          "Create an event, close the window: between two reminders, no Calendar program is "
          "running. The reminder still arrives on time, with “Later” and “Dismiss”. The taskbar "
          "clock shows the day's events. Everything lives in one .ics file on your PC, which "
          "you can import and export."),
        ("shot", "calendar"),
        limits(L("On ne peut pas encore glisser un événement, modifier une seule occurrence "
                 "d'une série, ni afficher les numéros de semaine.",
                 "You can't drag an event yet, change a single occurrence of a series, or show "
                 "week numbers."),
               L("En anglais, les dates sont encore dans l'ordre français, et les heures des "
                 "rappels sur 24 heures.",
                 "In English, dates are still in the French order, and reminder times on a "
                 "24-hour clock.")),
        H("store", "Le Raye Store", "The Raye Store"),
        P("Les applis de Flathub et celles de Raye, au même endroit. Pendant une installation, "
          "vous voyez la progression et pouvez annuler ; ensuite, Ouvrir et Désinstaller. Une "
          "appli proposée par deux sources n'apparaît qu'une fois.",
          "Apps from Flathub and Raye's own, in one place. While an app installs you see the "
          "progress and can cancel; afterwards, Open and Uninstall. An app offered by two "
          "sources shows up once."),
        ("shot", "store"),
        H("lock", "Le verrouillage et la connexion", "Lock and sign-in"),
        P("Le champ du mot de passe s'affiche sur l'écran où est la souris. Arrêter et "
          "Redémarrer marchent depuis l'écran de connexion.",
          "The password field shows on the screen where the mouse is. Shut down and Restart "
          "work from the sign-in screen."),
        ("shot", "lock"),
        limits(L("L'image de compte n'est pas la même à la connexion et au verrouillage.",
                 "The account picture is not the same at sign-in and on the lock screen.")),
        H("unfinished", "Ce qui n'a pas encore la forme de Raye",
          "What doesn't have Raye's shape yet"),
        P("Le terminal, l'outil de capture d'écran et quelques boîtes de dialogue ont les "
          "couleurs de Raye, mais pas encore sa forme. Il n'y a pas d'appli Bloc-notes : "
          "<code>notepad</code> ouvre l'éditeur de texte.",
          "The terminal, the screenshot tool and a few dialogs wear Raye's colors, but not its "
          "shape yet. There is no Notepad app: <code>notepad</code> opens the text editor."),
    ],
}

WINDOWS = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Vos programmes Windows", "Your Windows programs"),
    "description": L("Ce qui se passe quand on ouvre un .exe sur Raye Linux, ce qui manque encore, "
                     "et les jeux qui ne marcheront pas.",
                     "What happens when you open an .exe on Raye Linux, what is still missing, "
                     "and the games that won't run."),
    "lede": L("Un double-clic sur un fichier .exe lance son installateur, sans rien à préparer "
              "avant. Ce qui se passe ensuite dépend du programme, et je n'ai pas encore de liste "
              "de programmes essayés à publier : elle sera sur cette page.",
              "Double-clicking an .exe file starts its installer, with nothing to set up first. "
              "What happens next depends on the program, and I don't have a list of programs "
              "tried to publish yet: it will be on this page."),
    "next": "hardware",
    "blocks": [
        H("double-click", "Un double-clic", "A double-click"),
        P("Double-cliquez sur un fichier .exe ou .msi : il s'ouvre. Il n'y a rien à installer "
          "avant, et pas de question. L'installateur du programme fait son travail et ajoute "
          "son entrée au menu Démarrer, d'où le programme se lance ensuite comme une appli de "
          "Raye.",
          "Double-click an .exe or .msi file: it opens. There is nothing to install first, and "
          "no question. The program's installer does its job and adds an entry to the Start "
          "menu, and the program then starts from there like a Raye app."),
        ("shot", "exe-setup"),
        P("Chaque programme a son propre espace, si bien qu'un programme qui se comporte mal ne "
          "casse pas les autres. Cet espace se prépare en arrière-plan environ deux minutes "
          "après votre première connexion, puis de nouveau après certaines mises à jour : "
          "26 secondes de travail, et jusqu'à 3 Go de mémoire pendant ce temps, mesurés sur la "
          "machine de test.",
          "Every program gets its own space, so one that misbehaves doesn't break the others. "
          "That space is prepared in the background about two minutes after your first "
          "sign-in, and again after some updates: 26 seconds of work, using up to 3 GB of "
          "memory meanwhile, measured on the test machine."),
        ("shot", "exe-start"),
        H("native", "Quand il existe une version pour Raye", "When there is a Raye version"),
        P("Certains programmes existent aussi pour Raye, comme Discord ou Steam. Si vous "
          "double-cliquez sur leur installateur Windows, Raye vous propose plutôt cette "
          "version-là, faite pour Raye, qui n'a pas besoin de la couche Windows.",
          "Some programs also exist for Raye, such as Discord or Steam. If you double-click "
          "their Windows installer, Raye offers you that version instead, made for Raye, which "
          "doesn't need the Windows layer."),
        ("shot", "exe-native"),
        H("missing", "Ce qui manque, et pourquoi certains programmes ne démarrent pas",
          "What's missing, and why some programs don't start"),
        P("Voici ce que la couche Windows de Raye apporte d'elle-même, et ce qui lui manque "
          "encore. C'est ce qui manque, le plus souvent, qui explique qu'un programme ne démarre "
          "pas.",
          "Here is what Raye's Windows layer brings by itself, and what it still lacks. What's "
          "missing is, most of the time, why a program doesn't start."),
        ("list", [
            L("<strong>Direct3D vers Vulkan est inclus</strong> (DXVK et VKD3D-Proton) : les "
              "jeux et programmes en Direct3D 8 à 12 l'utilisent sans réglage.",
              "<strong>Direct3D to Vulkan is included</strong> (DXVK and VKD3D-Proton): games "
              "and programs that use Direct3D 8 to 12 get it with no setting."),
            L("<strong>Les polices de Windows</strong> (Arial, Times New Roman, Calibri, Cambria, "
              "Tahoma…) sont remplacées par des polices de la même taille, donc les fenêtres "
              "gardent leur disposition. Les polices d’origine de Windows ne sont pas incluses : "
              "un texte peut avoir l'air un peu différent.",
              "<strong>The Windows fonts</strong> (Arial, Times New Roman, Calibri, Cambria, "
              "Tahoma…) are replaced by fonts of the same size, so windows keep their layout. "
              "The original Windows fonts are not included: some text can look a little different."),
            L("<strong>Ce qui manque encore</strong> : le .NET Framework d’origine de Windows "
              "(Raye en fournit une version libre, qui suffit à la plupart des programmes) et le "
              "moteur web WebView2 d'Edge. Les programmes qui exigent l'un ou l'autre ne "
              "démarrent pas encore.",
              "<strong>What's still missing</strong>: the original .NET Framework of Windows (Raye ships "
              "a free version that most programs are happy with) and Edge's WebView2 web engine. "
              "Programs that require either one don't start yet."),
        ]),
        limits(L("Le premier programme ouvert après l'installation prend du temps.",
                 "The first program you open after installing takes a while."),
               L("Certains installateurs montrent une fenêtre grise à l'ancienne.",
                 "Some installers show an old-style gray window.")),
        H("games", "Les jeux", "Games"),
        P("Les jeux protégés par un anti-triche qui s'installe dans le noyau de Windows, comme "
          "Valorant ou Fortnite, ne marchent pas. Ce n'est pas un réglage qui manque : il faut "
          "que leur éditeur autorise Linux, et ce n'est pas le cas aujourd'hui. Roblox ne "
          "démarre pas non plus : son anti-triche refuse la couche Windows.",
          "Games protected by an anti-cheat that installs itself in the Windows kernel, such as "
          "Valorant or Fortnite, don't run. It isn't a missing setting: their publisher has to "
          "allow Linux, and today they don't. Roblox doesn't start either: its anti-cheat "
          "refuses the Windows layer."),
        P("Je n'ai lancé aucun autre jeu sur un PC qui a une vraie carte graphique, donc je ne "
          "publie rien sur eux. Steam s'installe depuis le Raye Store, en version pour Raye.",
          "I haven't started any other game on a PC with a real graphics card, so I don't "
          "publish anything about them. Steam installs from the Raye Store, as a Raye "
          "version."),
        H("report", "Si un programme ne marche pas", "If a program doesn't work"),
        P("Écrivez-moi son nom et sa version, ce que vous avez fait et ce qui s'est passé, à "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>. La liste des "
          "programmes qu'on me signale, c'est ce qui décide de l'ordre dans lequel je règle les "
          "choses.",
          "Send me its name and version, what you did and what happened, at "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>. The list of "
          "programs people report is what sets the order I fix things in."),
    ],
}

UPDATES = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Les mises à jour", "Updates"),
    "description": L("Comment Raye Linux se met à jour : ce qui s'installe pendant que vous "
                     "travaillez, ce qui attend le redémarrage, et les points de restauration.",
                     "How Raye Linux updates: what installs while you work, what waits for the "
                     "restart, and the restore points."),
    "lede": L("Le 11 novembre 2026, trois mises à jour sont arrivées sur la machine de test. Le "
              "Store et le Calendrier se sont installés pendant que la session était ouverte ; "
              "le thème du bureau a attendu le redémarrage.",
              "On November 11, 2026, three updates came in on the test machine. The Store and "
              "Calendar installed while the session was open; the desktop theme waited for the "
              "restart."),
    "next": "security",
    "blocks": [
        H("live", "Ce qui s'installe tout de suite, ce qui attend",
          "What installs right away, what waits"),
        P("Attend le redémarrage ce que le système garde chargé tant qu'il tourne : le noyau, "
          "les pilotes, les micrologiciels, les pièces centrales du système et le bureau "
          "lui-même. Une mise à jour de ce genre porte l'étiquette « Redémarrage requis ». Le "
          "reste s'installe dès qu'il est téléchargé, sans que vous ayez rien à faire.",
          "What waits for the restart is what the system keeps loaded while it runs: the "
          "kernel, drivers, firmware, the core pieces of the system and the desktop itself. An "
          "update of that kind carries the label “Restart required”. The rest installs as soon "
          "as it's downloaded, with nothing for you to do."),
        P("Les correctifs de sécurité font exception : ils s'installent tout de suite, même pour "
          "ces pièces-là.",
          "Security fixes are the exception: they install right away, even for those "
          "pieces."),
        ("shot", "update-live"),
        H("restart", "Le redémarrage", "The restart"),
        P("Ce qui attend s'installe quand vous choisissez « Mettre à jour et redémarrer », dans "
          "Démarrer, dans la notification ou dans les Paramètres. Un redémarrage ordinaire "
          "n'installe rien, et Raye ne redémarre pas de lui-même, sauf si vous lui avez demandé de le faire en dehors de vos heures d'activité. Pendant l'installation, "
          "l'image de Raye montre un anneau et « Installation des mises à jour » avec le "
          "pourcentage. Pour le thème du bureau, il s'est écoulé {m:restart} entre l'image de "
          "démarrage et l'écran de connexion sur la machine de test.",
          "What waits installs when you choose “Update and restart”, in Start, in the "
          "notification or in Settings. An ordinary restart installs nothing, and Raye doesn't "
          "restart on its own unless you asked it to outside your active hours. While it installs, the Raye picture shows a ring and "
          "“Installing updates” with the percentage. For the desktop theme, {m:restart} passed "
          "between the startup picture and the sign-in screen on the test machine."),
        ("shot", "update-boot"),
        limits(L("Quand une deuxième mise à jour du même paquet attend, la notification "
                 "« Redémarrage requis » ne revient pas.",
                 "When a second update of the same package is waiting, the “Restart required” "
                 "notification doesn't come back."),
               L("L'écran de verrouillage et <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Suppr</kbd> ne "
                 "proposent pas encore « Mettre à jour et redémarrer ».",
                 "The lock screen and <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Del</kbd> don't offer "
                 "“Update and restart” yet.")),
        H("when", "Quand Raye télécharge, et quand il attend",
          "When Raye downloads, and when it waits"),
        P("Les mises à jour se téléchargent en arrière-plan et attendent quand votre portable "
          "est sur batterie sous 40 %, sur une connexion limitée ou en train de jouer. Vous "
          "pouvez tout mettre en pause d'une à cinq semaines, sauf la sécurité. Chercher et "
          "télécharger 42 mises à jour, 60 Mo en tout, a pris {m:fetch} sur la machine de "
          "test.",
          "Updates download in the background and wait while your laptop is on battery below "
          "40%, on a metered connection or playing a game. You can pause everything for one to "
          "five weeks, except security. Checking for and downloading 42 updates, 60 MB in all, "
          "took {m:fetch} on the test machine."),
        limits(L("Sous 40 % de batterie, « Installer maintenant » ne fait rien, et n'affiche "
                 "rien.",
                 "Below 40% battery, “Install now” does nothing, and shows nothing.")),
        H("restore", "Les points de restauration", "Restore points"),
        P("Avant et après chaque installation de mises à jour, Raye prend un point de "
          "restauration du système, et les plus anciens partent seuls. Vous pouvez aussi en "
          "créer un dans Paramètres, Récupération.",
          "Before and after every update, Raye takes a restore point of the system, and the "
          "oldest go by themselves. You can also make one in Settings, Recovery."),
        ("shot", "restore"),
        limits(L("Revenir au point « Avant les mises à jour » réinstalle ces mêmes mises à jour "
                 "au démarrage suivant : ne comptez pas encore dessus pour annuler une mise à "
                 "jour.",
                 "Going back to the “Before updates” point reinstalls the same updates at the "
                 "next start: don't count on it yet to undo an update."),
               L("Un point créé à la main peut être effacé, sans avertissement, par ceux des "
                 "mises à jour suivantes.",
                 "A point made by hand can be deleted, with no warning, by those of the "
                 "following updates."),
               L("Un point de restauration garde le système, pas vos fichiers personnels. "
                 "Sauvegardez-les à part.",
                 "A restore point keeps the system, not your personal files. Back them up "
                 "separately."),
               L("On ne peut pas encore démarrer sur un état précédent depuis le menu de "
                 "démarrage.",
                 "You can't yet start from an earlier state through the startup menu.")),
        H("source", "D'où viennent les mises à jour", "Where updates come from"),
        P("Les paquets de Raye viennent de <code>dl.rayelinux.com</code> et de "
          "<code>raye-linux.github.io/packages</code>, deux copies identiques fichier par "
          "fichier, signées par la clé dont l'empreinte est "
          "<code>EA73 69D4 C3A3 10B2 DF3D FC16 D3AA 2E62 5DDE 161E</code>. Firefox vient de "
          "Mozilla, et le reste du système des serveurs du système de base ; si le principal ne "
          "répond plus, Raye passe tout seul à deux autres.",
          "Raye's packages come from <code>dl.rayelinux.com</code> and "
          "<code>raye-linux.github.io/packages</code>, two copies identical file by file, signed "
          "by the key whose fingerprint is "
          "<code>EA73 69D4 C3A3 10B2 DF3D FC16 D3AA 2E62 5DDE 161E</code>. Firefox comes from "
          "Mozilla, and the rest of the system from the base system's servers; if the main one "
          "stops answering, Raye moves to two others by itself."),
        limits(L("Sans connexion, Raye Update dit qu'il n'a pas pu vérifier : il n'a pas joint "
                 "les serveurs, rien n'est cassé.",
                 "Without a connection, Raye Update says it could not check: it didn't reach "
                 "the servers, nothing is broken.")),
    ],
}

SECURITY = {
    "eyebrow": L("Découvrir", "Look around"),
    "h1": L("Sécurité et vie privée", "Security and privacy"),
    "description": L("Secure Boot, le disque chiffré ouvert par la puce TPM, la clé de "
                     "récupération, l'invite de mot de passe, et ce que Raye Linux envoie sur "
                     "Internet.",
                     "Secure Boot, the encrypted disk opened by the TPM chip, the recovery key, "
                     "the password prompt, and what Raye Linux sends over the Internet."),
    "lede": L("Sur un PC qui a une puce TPM, vous ne tapez qu'un mot de passe au démarrage, celui "
              "de votre compte, et pourtant le disque est chiffré. Voici ce que ça protège, et ce "
              "que ça ne protège pas.",
              "On a PC with a TPM chip, you type only one password at startup, your account's, "
              "and yet the disk is encrypted. Here is what that protects, and what it "
              "doesn't."),
    "next": "hardware",
    "blocks": [
        H("secureboot", "Secure Boot", "Secure Boot"),
        P("Raye démarre avec Secure Boot activé et les clés que la plupart des PC ont d'usine : "
          "sur la machine de test, je n'ai rien eu à changer dans le micrologiciel. Certains PC, "
          "souvent vendus comme « Secured-core », n'acceptent d'office que Windows ; il faut "
          "alors autoriser, dans les réglages du micrologiciel, les clés dites « tierces » "
          "(third-party). Si votre PC refuse quand même de démarrer Raye, écrivez-moi son "
          "modèle.",
          "Raye starts with Secure Boot turned on and the keys most PCs ship with: on the test "
          "machine, I didn't have to change anything in the firmware. Some PCs, often sold as "
          "“Secured-core”, only accept Windows out of the box; you then have to allow the "
          "so-called “third-party” keys in the firmware settings. If your PC still refuses to "
          "start Raye, send me its model."),
        H("encryption", "Le disque chiffré", "The encrypted disk"),
        P("Si vous cochez « Chiffrer le système Raye » sur la page Disque de l'installateur, vous "
          "choisissez un mot de passe du disque, et tout le système est chiffré. Retiré du PC et "
          "branché ailleurs, le disque ne se lit pas sans ce mot de passe ou la clé de "
          "récupération.",
          "If you tick “Encrypt the Raye system” on the installer's Disk page, you pick a disk "
          "password, and the whole system is encrypted. Taken out of the PC and plugged in "
          "elsewhere, the disk can't be read without that password or the recovery key."),
        ("shot", "setup-encrypt"),
        P("Sur un PC qui a une puce TPM, c'est elle qui ouvre le disque au démarrage. Sur ce "
          "PC-là, c'est donc le mot de passe de votre compte qui protège vos fichiers, comme "
          "avec BitLocker. La puce ne surveille que les réglages de Secure Boot : s'ils "
          "changent, ou si le disque est mis dans un autre PC, Raye redemande le mot de passe "
          "du disque. D'autres changements dans le démarrage ne le redemandent pas. Sans puce "
          "TPM, le mot de passe du disque est demandé à chaque démarrage.",
          "On a PC with a TPM chip, the chip opens the disk at startup. On that PC, your "
          "account password is therefore what protects your files, as with BitLocker. The chip "
          "only watches the Secure Boot settings: if they change, or the disk is put in another "
          "PC, Raye asks for the disk password again. Other changes in the startup don't ask "
          "for it. Without a TPM chip, the disk password is asked at every startup."),
        P("Je l'ai essayé une fois sur la machine de test : une mise à jour du micrologiciel qui "
          "révoque d'anciennes clés de démarrage, et le disque s'est ouvert seul après. Si une "
          "mise à jour de ce genre s'installe avec d'autres au redémarrage, la clé de "
          "récupération peut vous être demandée une fois.",
          "I tried it once on the test machine: a firmware update that revokes old startup "
          "keys, and the disk opened by itself afterwards. If an update of that kind installs "
          "along with others at a restart, you may be asked for the recovery key once."),
        H("recovery", "La clé de récupération", "The recovery key"),
        P("À la première connexion, une fenêtre montre une clé de récupération : huit groupes de "
          "six chiffres. Elle ouvre le disque si vous oubliez son mot de passe. Copiez-la, "
          "notez-la sur papier ou dans un gestionnaire de mots de passe, gardez-la ailleurs que "
          "sur l'ordinateur, puis confirmez avec « J'ai enregistré ma clé ».",
          "At your first sign-in, a window shows a recovery key: eight groups of six digits. It "
          "opens the disk if you forget its password. Copy it, write it down on paper or in a "
          "password manager, keep it somewhere other than the computer, then confirm with “I "
          "saved my key”."),
        ("shot", "recovery-key"),
        H("prompt", "Le mot de passe avant qu'une appli change le système",
          "The password before an app changes the system"),
        P("Quand une appli veut modifier le système, l'écran s'assombrit et Raye demande votre "
          "mot de passe, avec le nom de l'éditeur, comme sous Windows 11. L'invite n'expire "
          "pas : sur un compte standard, vous avez le temps d'aller demander le mot de passe à "
          "l'administrateur du PC. Les mises à jour, elles, s'installent sans le demander.",
          "When an app wants to change the system, the screen dims and Raye asks for your "
          "password, with the publisher's name, as in Windows 11. The prompt doesn't time out: "
          "on a standard account, you have time to go and ask the PC's administrator for the "
          "password. Updates, on the other hand, install without asking for it."),
        ("shot", "uac"),
        limits(L("L'invite nomme parfois le programme technique plutôt que l'appli qui le "
                 "demande.",
                 "The prompt sometimes names the technical program rather than the app asking."),
               L("On ne peut pas encore chiffrer ou déchiffrer le disque une fois Raye installé : "
                 "c'est un choix à faire à l'installation.",
                 "You can't encrypt or decrypt the disk once Raye is installed yet: it's a "
                 "choice made when installing.")),
        H("crash", "Si le PC plante", "If the PC crashes"),
        P("Le noyau Raye, qu'on active dans Paramètres, Pilotes, montre un écran violet avec "
          "l'œil de Raye si le système plante, puis redémarre seul après 30 secondes. Le noyau "
          "d'origine reste installé et reste celui par défaut.",
          "The Raye kernel, which you turn on in Settings, Drivers, shows a violet screen with "
          "the Raye eye if the system crashes, then restarts by itself after 30 seconds. The "
          "original kernel stays installed and stays the default."),
        P("Avec Secure Boot, sa clé s'inscrit au redémarrage qui suit, en trois gestes : un "
          "écran bleu apparaît, appuyez sur une touche dans les 10 secondes, choisissez "
          "« Enroll MOK », puis tapez le code à six chiffres que les Paramètres vous ont "
          "montré. Si les 10 secondes passent, Raye démarre sur le noyau d'origine.",
          "With Secure Boot, its key is enrolled at the next restart, in three steps: a blue "
          "screen shows up, press a key within 10 seconds, choose “Enroll MOK”, then type the "
          "six-digit code Settings showed you. If the 10 seconds go by, Raye starts on the "
          "original kernel."),
        H("network", "Ce que Raye envoie sur Internet", "What Raye sends over the Internet"),
        P("Raye Update interroge les deux copies des paquets de Raye, les serveurs du système de "
          "base, ceux de Mozilla pour Firefox, et le service des micrologiciels pour les mises "
          "à jour du BIOS et des appareils. Le Store interroge Flathub. Le système vérifie "
          "aussi qu'Internet répond, pour repérer un réseau d'hôtel qui demande de se "
          "connecter, et règle son heure sur un serveur de temps. Firefox ouvre rayelinux.com "
          "à son démarrage, sans publicité et sans bandeau « géré par votre organisation ».",
          "Raye Update asks the two copies of Raye's packages, the base system's servers, "
          "Mozilla's for Firefox, and the firmware service for BIOS and device updates. The "
          "Store asks Flathub. The system also checks that the Internet answers, to spot a "
          "hotel network that wants you to sign in, and sets its clock from a time server. "
          "Firefox opens rayelinux.com when it starts, with no ads and no “managed by your "
          "organization” banner."),
        P("Deux choses ne partent que si vous les avez acceptées : votre position, quand une "
          "appli la demande et que vous dites oui, et des statistiques d'usage anonymes, une "
          "case décochée au départ sur la page Confidentialité de l'installateur.",
          "Two things only go out if you agreed to them: your location, when an app asks for it "
          "and you say yes, and anonymous usage statistics, a box left unticked on the "
          "installer's Privacy page."),
        P("Cette liste vient de ce que je sais du code. Je n'ai pas encore observé une "
          "installation neuve pendant une heure pour la vérifier adresse par adresse ; quand ce "
          "sera fait, le relevé sera sur cette page.",
          "This list comes from what I know of the code. I haven't yet watched a fresh install "
          "for an hour to check it address by address; once that's done, the record will be on "
          "this page."),
        P("Ce site ne pose aucun témoin et ne charge rien d'un autre site ; sa "
          "<a href=\"{p:privacy}\">politique de confidentialité</a> dit ce qu'il garde.",
          "This website sets no cookies and loads nothing from another site; its "
          "<a href=\"{p:privacy}\">privacy policy</a> says what it keeps."),
    ],
}

HARDWARE = {
    "eyebrow": L("Avant d'installer", "Before you install"),
    "h1": L("Le matériel, et ce que j'ai mesuré", "Hardware, and what I measured"),
    "description": L("La configuration minimale de Raye Linux, les mesures avec leur machine et "
                     "leur date, et les PC sur lesquels il a été essayé.",
                     "Raye Linux's minimum requirements, the measurements with their machine and "
                     "date, and the PCs it was tried on."),
    "lede": L("Raye a été essayé sur une machine virtuelle et sur un seul portable. C'est peu, et "
              "je préfère le dire avant le premier chiffre.",
              "Raye has been tried on one virtual machine and a single laptop. That's not much, "
              "and I'd rather say so before the first figure."),
    "next": "install",
    "blocks": [
        H("needs", "Ce qu'il faut", "What you need"),
        ("list", [
            L("Un processeur Intel ou AMD 64 bits, et un PC qui démarre en mode UEFI (la plupart "
              "des PC depuis 2012). Le mode BIOS d'autrefois est en cours d'essai pour la V1 : "
              "voir <a href=\"{p:oldpcs}\">Vieux PC</a>.",
              "A 64-bit Intel or AMD processor, and a PC that starts in UEFI mode (most PCs since "
              "2012). The old BIOS mode is being tried for V1: see "
              "<a href=\"{p:oldpcs}\">Older PCs</a>."),
            L("8 Go de mémoire conseillés. L'installateur accepte moins, mais je n'ai pas essayé "
              "Raye sur un PC de 4 Go.",
              "8 GB of memory recommended. The installer accepts less, but I haven't tried Raye "
              "on a 4 GB PC."),
            L("{free} Go d'espace disque libre : c'est ce que l'installateur exige lui-même.",
              "{free} GB of free disk space: that's what the installer itself demands."),
            L("Une clé USB de 8 Go ou plus pour l'installation.",
              "A USB stick of 8 GB or more to install."),
            L("Secure Boot et une puce TPM sont pris en charge, sans être obligatoires.",
              "Secure Boot and a TPM chip are supported, not required."),
        ]),
        H("measures", "Les mesures", "The measurements"),
        ("measures", ["ram", "black", "install", "restart", "fetch"]),
        P("Lisez chaque chiffre à côté de la machine d'où il vient. La machine de test n'a pas "
          "de carte graphique : tout le bureau y est dessiné par le processeur, ce qui gonfle "
          "sa mémoire. Environ 120 Mo des {m:ram} sont une réserve du noyau qui grandit avec la "
          "mémoire de la machine. Le chiffre est pris trois minutes après l'ouverture de la "
          "session, avec <code>free -m</code>.",
          "Read each figure next to the machine it came from. The test machine has no graphics "
          "card: the whole desktop is drawn by the processor there, which swells its memory. "
          "About 120 MB of the {m:ram} are a kernel reserve that grows with the machine's "
          "memory. The figure is taken three minutes after signing in, with "
          "<code>free -m</code>."),
        P("Le micrologiciel de la machine de test lit le disque à environ 7 Mo/s : ses temps de "
          "démarrage servent à comparer deux versions, pas à vous promettre une vitesse. Et "
          "après l'image de Raye, un second écran noir, de 3 à 5 s, reste avant l'écran de "
          "connexion à chaque démarrage.",
          "The test machine's firmware reads the disk at about 7 MB/s: its startup times are "
          "for comparing two versions, not for promising you a speed. And after the Raye "
          "picture, a second black screen of 3 to 5 s remains before the sign-in screen at "
          "every startup."),
        P("Mon but était 1 Go de mémoire au repos : la machine de test est passée dessous. Les Go et Mo de ce site "
          "se comptent comme Windows les compte, par 1 024.",
          "My goal was 1 GB of memory at idle: the test machine is now under it. The GB and MB on this site are "
          "counted the way Windows counts them, by 1,024."),
        H("machines", "Les machines essayées", "The machines tried"),
        P("<strong>La machine de test</strong> : une machine virtuelle à 8 cœurs et 16 Go de "
          "mémoire, sans carte graphique, avec deux écrans virtuels (1280×800 et 1920×1080), "
          "Secure Boot activé et une puce TPM 2.0. C'est sur elle que j'installe une version de "
          "zéro et que je la mets à jour depuis la précédente, avant de la publier. Je ne l'ai "
          "pas toujours fait : les deux séries de correctifs de la 0.2 Bêta 2 n'ont eu que "
          "l'essai de mise à jour.",
          "<strong>The test machine</strong>: a virtual machine with 8 cores and 16 GB of "
          "memory, no graphics card, two virtual screens (1280×800 and 1920×1080), Secure Boot "
          "on and a TPM 2.0 chip. That's where I install a version from scratch and update it "
          "from the previous one, before it goes out. I haven't always done it: the two rounds "
          "of fixes of 0.2 Beta 2 only got the update test."),
        P("<strong>Un Dell Latitude 5420</strong>, 16 Go, avec son écran de 1366×768 et un "
          "écran externe de 1920×1080 en HDMI, Wi-Fi et Ethernet Intel. Raye y tourne depuis le "
          "1er novembre 2026 et y reçoit ses mises à jour.",
          "<strong>A Dell Latitude 5420</strong>, 16 GB, with its 1366×768 screen and an "
          "external 1920×1080 screen over HDMI, Intel Wi-Fi and Ethernet. Raye has run on it "
          "since November 1, 2026, and gets its updates there."),
        limits(L("Sur le Latitude, la mise en veille échoue parfois, et le Wi-Fi comme "
                 "l'Ethernet mettent du temps à revenir après la veille.",
                 "On the Latitude, sleep sometimes fails, and Wi-Fi and Ethernet are slow to "
                 "come back after sleep."),
               L("La mise à jour de son BIOS par Raye Update a échoué une fois, faute d'une "
                 "pièce ajoutée depuis ; je ne l'ai pas encore vue réussir.",
                 "Updating its BIOS through Raye Update failed once, for want of a piece added "
                 "since; I haven't seen it succeed yet.")),
        H("untried", "Ce que je n'ai pas essayé", "What I haven't tried"),
        P("Aucun PC de bureau, aucune carte graphique AMD ou NVIDIA, aucun portable d'une autre "
          "marque, aucun PC de 4 Go. Je n'ai pas mesuré Raye contre Windows sur le même PC, ni "
          "le démarrage sur un vrai disque NVMe, ni l'autonomie sur batterie, ni un jeu. Si "
          "votre PC n'est pas dans cette page, ce qui est le cas de presque tous, dites-moi "
          "comment ça s'est passé : "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>.",
          "No desktop PC, no AMD or NVIDIA graphics card, no laptop of another brand, no 4 GB "
          "PC. I haven't measured Raye against Windows on the same PC, or startup on a real "
          "NVMe disk, or battery life, or a game. If your PC isn't on this page, which is true "
          "of almost all of them, tell me how it went: "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>."),
    ],
}

INSTALL = {
    "eyebrow": L("Avant d'installer", "Before you install"),
    "h1": L("Installer Raye, étape par étape", "Installing Raye, step by step"),
    "description": L("Préparer la clé USB, l'installateur étape par étape, garder Windows à côté, "
                     "et ce que l'installateur ne fait pas.",
                     "Making the USB stick, the installer step by step, keeping Windows "
                     "alongside, and what the installer doesn't do."),
    "lede": L("L'installateur pose ses questions en six étapes, que sa barre du haut affiche, et "
              "l'installation elle-même a pris {m:install} sur la machine de test. Avant de "
              "commencer, sauvegardez vos fichiers. Je le dirais pour n'importe quel système ; je "
              "le dis deux fois pour un système aussi jeune.",
              "The installer asks its questions in six steps, shown in its top bar, and the "
              "install itself took {m:install} on the test machine. Before you start, back up "
              "your files. I'd say it for any system; I say it twice for one this young."),
    "next": "download",
    "blocks": [
        H("before", "Avant de commencer", "Before you start"),
        P("Vérifiez que votre PC a ce qu'il faut (page <a href=\"{p:hardware}\">Matériel</a>). "
          "Une connexion Internet pendant l'installation est utile, pas obligatoire. Si vous "
          "gardez Windows, éteignez-le vraiment : désactivez le démarrage rapide et la "
          "veille prolongée. L'installateur vous prévient si Windows n'a pas été complètement "
          "arrêté.",
          "Check that your PC has what it takes (the <a href=\"{p:hardware}\">Hardware</a> "
          "page). An Internet connection while installing helps, it isn't required. If you're "
          "keeping Windows, shut it down properly: turn off fast startup and hibernation. The "
          "installer warns you if Windows wasn't fully shut down."),
        P("Si Windows est chiffré, par BitLocker ou par le « Chiffrement de l'appareil » que "
          "beaucoup de PC vendus avec Windows 11 ont d'office, Raye ne peut pas réduire sa "
          "partition. Désactivez ce chiffrement dans Windows et attendez la fin du "
          "déchiffrement, en gardant votre clé de récupération BitLocker. L'installateur dit "
          "encore de « suspendre la protection » : ça ne suffit pas, la partition reste "
          "chiffrée.",
          "If Windows is encrypted, by BitLocker or by the “Device encryption” many PCs sold "
          "with Windows 11 have turned on, Raye can't shrink its partition. Turn that encryption "
          "off in Windows and wait for the decryption to finish, keeping your BitLocker "
          "recovery key. The installer still says to “suspend protection”: that isn't enough, "
          "the partition stays encrypted."),
        H("usb", "La clé USB", "The USB stick"),
        ("steps", [
            (L("Téléchargez l'image", "Download the image"),
             L("Une fois l'image publiée, la page Télécharger donne le fichier, sa somme de "
               "contrôle et la façon de la vérifier.",
               "Once the image is out, the Download page gives the file, its checksum and how to "
               "check it.")),
            (L("Écrivez-la sur la clé", "Write it to the stick"),
             L("Avec Rufus, choisissez le <strong>mode image DD</strong> quand il le demande : le "
               "mode ISO donne une clé qui ne démarre pas. balenaEtcher marche aussi. Tout ce que "
               "la clé contient sera effacé.",
               "With Rufus, choose <strong>DD image mode</strong> when it asks: ISO mode gives a "
               "stick that doesn't start. balenaEtcher works too. Everything on the stick will "
               "be erased.")),
            (L("Démarrez sur la clé", "Start from the stick"),
             L("À l'allumage, souvent avec F12, F11, F8 ou Échap. Le menu de la clé, en anglais "
               "seulement, démarre par défaut sur « Try Raye Linux without installing » : une "
               "session d'essai qui ne touche pas au disque. L'icône « Install Raye Linux » est "
               "sur le bureau et en tête de Démarrer, et ouvre l'installateur en plein écran. "
               "Sur la ligne d'en dessous du menu, « Install Raye Linux » l'ouvre directement ; "
               "« Safe graphics » aide quand l'écran reste noir.",
               "At power on, often with F12, F11, F8 or Esc. The stick's menu, in English only, "
               "starts by default on “Try Raye Linux without installing”: a trial session that "
               "doesn't touch the disk. The “Install Raye Linux” icon is on the desktop and at "
               "the top of Start, and opens the installer full screen. On the line below in the "
               "menu, “Install Raye Linux” opens it directly; “Safe graphics” helps when the "
               "screen stays black.")),
        ]),
        ("shot", "try-raye"),
        H("pages", "L'installateur, étape par étape", "The installer, step by step"),
        ("steps", [
            (L("Région", "Region"),
             L("Français ou anglais, le fuseau horaire, puis la disposition du clavier.",
               "English or French, the time zone, then the keyboard layout.")),
            (L("Réseau", "Network"),
             L("La page suit votre connexion en direct : un câble branché apparaît tout de "
               "suite.",
               "The page follows your connection live: a plugged-in cable shows up right "
               "away.")),
            (L("Disque", "Disk"),
             L("Quatre choix : effacer le disque, installer à côté de Windows en réduisant sa "
               "partition, utiliser l'espace libre, ou remplacer une partition. La case "
               "« Chiffrer le système Raye » est sur la même page : cochée, elle vous fait "
               "choisir un mot de passe du disque. Avec une puce TPM, vous n'aurez pas à le "
               "taper au démarrage.",
               "Four choices: erase the disk, install alongside Windows by shrinking its "
               "partition, use the free space, or replace a partition. The “Encrypt the Raye "
               "system” box is on the same page: ticked, it has you pick a disk password. With "
               "a TPM chip, you won't have to type it at startup.")),
            (L("Compte", "Account"),
             L("Le nom du PC, puis votre nom et votre mot de passe. La page du compte Raye se "
               "passe avec « Utiliser plutôt un compte local ».",
               "The PC's name, then your name and your password. The Raye account page can be "
               "skipped with “Use a local account instead”.")),
            (L("Confidentialité", "Privacy"),
             L("La position et les statistiques d'usage, que vous pourrez changer plus tard "
               "dans les Paramètres.",
               "Location and usage statistics, which you can change later in Settings.")),
            (L("Installation", "Install"),
             L("« Prêt pour l'installation » dit tout ce qui va se passer, avec un bandeau rouge si "
               "quelque chose va être effacé.",
               "“Ready to install” says everything that will happen, with a red banner if "
               "anything is going to be erased.")),
        ]),
        ("shot", "setup-disk"),
        P("Juste avant d'écrire, l'installateur relit le disque. Si quoi que ce soit a changé "
          "depuis votre choix, il s'arrête au lieu de continuer.",
          "Right before writing, the installer reads the disk again. If anything changed since "
          "you chose, it stops instead of carrying on."),
        ("shot", "setup-summary"),
        H("alongside", "Garder Windows à côté", "Keeping Windows alongside"),
        P("« Installer à côté de Windows » réduit la partition Windows pour faire de la place, "
          "et les deux systèmes partagent la partition de démarrage. Au démarrage, un menu "
          "propose Raye Linux et Windows pendant 10 secondes. Depuis Raye, « Redémarrer sous "
          "Windows », dans Démarrer, redémarre directement dans Windows, une fois.",
          "“Install alongside Windows” shrinks the Windows partition to make room, and both "
          "systems share the startup partition. At startup, a menu offers Raye Linux and Windows "
          "for 10 seconds. From Raye, “Restart to Windows” in Start restarts straight into "
          "Windows, once."),
        ("shot", "boot-menu"),
        limits(L("Je l'ai prouvé sur une partition Windows de test, dans la machine de test : "
                 "50 Go réduits à 23 Go, et chaque fichier de Windows identique avant et après. "
                 "Pas encore sur un vrai Windows réduit puis redémarré. Sauvegardez avant.",
                 "I proved it on a test Windows partition, in the test machine: 50 GB shrunk to "
                 "23 GB, and every Windows file identical before and after. Not yet on a real "
                 "Windows shrunk and then restarted. Back up first."),
               L("Le menu de démarrage affiche encore « Raye Linux GNU/Linux » au lieu de « Raye "
                 "Linux ».",
                 "The startup menu still shows “Raye Linux GNU/Linux” instead of “Raye "
                 "Linux”."),
               L("Sur un PC en mode BIOS d'autrefois, j'ai vu la clé démarrer jusqu'à "
                 "l'installateur, pas l'installation complète : voir la page "
                 "<a href=\"{p:oldpcs}\">Vieux PC</a>.",
                 "On a PC in the old BIOS mode, I saw the stick start up to the installer, not a "
                 "full install: see the <a href=\"{p:oldpcs}\">Older PCs</a> page.")),
        H("not", "Ce que l'installateur ne fait pas", "What the installer doesn't do"),
        ("list", [
            L("Pas de partitionnement à la main.", "No manual partitioning."),
            L("Seule une partition Windows (NTFS) non chiffrée peut être réduite.",
              "Only an unencrypted Windows (NTFS) partition can be shrunk."),
            L("Un disque qui porte déjà un autre Linux n'a que le choix « Effacer » : pas de "
              "troisième système.",
              "A disk that already holds another Linux only gets “Erase”: no third system."),
            L("Pas de PC 32 bits.", "No 32-bit PC."),
        ]),
        H("key", "La clé de Raye et l'écran bleu", "Raye's key and the blue screen"),
        P("Le noyau de Raye est signé avec une clé de Raye. Pour que Secure Boot l'accepte, "
          "il faut inscrire cette clé une seule fois, et c'est le micrologiciel de votre PC qui "
          "le demande, sur un écran bleu au redémarrage, pas Raye. Avant de redémarrer, Raye vous "
          "montre un code à six chiffres à retenir.",
          "Raye's kernel is signed with a Raye key. For Secure Boot to accept it, that key has "
          "to be enrolled once, and it's your PC's firmware that asks, on a blue screen at "
          "restart, not Raye. Before restarting, Raye shows you a six-digit code to remember."),
        ("steps", [
            (L("Appuyez sur une touche", "Press a key"),
             L("Vous avez environ 10 secondes à l'écran bleu pour appuyer sur une touche.",
               "You have about 10 seconds at the blue screen to press a key.")),
            (L("Choisissez Enroll MOK", "Choose Enroll MOK"),
             L("Puis Continue, puis Yes.",
               "Then Continue, then Yes.")),
            (L("Tapez le code", "Type the code"),
             L("Le code à six chiffres que Raye vous a montré, puis Reboot.",
               "The six-digit code Raye showed you, then Reboot.")),
        ]),
        ("shot", "enroll-key"),
        P("Si vous manquez l'écran bleu, rien de grave : le PC démarre comme avant, avec le noyau "
          "du système de base, et Raye vous le redemandera. Sans Secure Boot, il n'y a pas "
          "d'écran bleu.",
          "If you miss the blue screen, no harm done: the PC starts as before, with the base "
          "system's kernel, and Raye will ask again. Without Secure Boot, there is no blue "
          "screen."),
        limits(L("Je l'ai vu marcher dans la machine de test, avec Secure Boot et une puce TPM "
                 "virtuelle : écran bleu manqué, puis écran bleu réussi, puis démarrage sur le "
                 "noyau de Raye. Pas encore sur un vrai PC.",
                 "I saw it work in the test machine, with Secure Boot and a virtual TPM chip: "
                 "blue screen missed, then blue screen done, then start on Raye's kernel. Not "
                 "yet on a real PC."),
               L("La clé USB d'essai garde le noyau signé d'origine : on n'inscrit rien pour "
                 "essayer Raye.",
                 "The trial USB stick keeps the original signed kernel: nothing is enrolled just "
                 "to try Raye.")),
        H("after", "Après", "Afterwards"),
        P("Au premier démarrage, si vous avez chiffré le disque, la puce TPM l'ouvre (sans puce, "
          "Raye demande le mot de passe du disque), puis vous tapez le mot de passe de votre "
          "compte. La clé de récupération s'affiche à la première connexion (voir "
          "<a href=\"{p:security}\">Sécurité</a>). Deux minutes plus tard, Raye prépare "
          "l'espace des programmes Windows en arrière-plan.",
          "At first startup, if you encrypted the disk, the TPM chip opens it (without a chip, "
          "Raye asks for the disk password), then you type your account password. The recovery "
          "key shows at your first sign-in (see <a href=\"{p:security}\">Security</a>). Two "
          "minutes later, Raye prepares the space for Windows programs in the background."),
        limits(L("Sans chiffrement, le menu de démarrage reste affiché 5 secondes à chaque "
                 "démarrage.",
                 "Without encryption, the startup menu stays on screen for 5 seconds at every "
                 "startup.")),
        H("back", "Revenir à Windows", "Going back to Windows"),
        P("Si vous avez gardé Windows à côté, il reste là : choisissez-le dans le menu de "
          "démarrage, ou « Redémarrer sous Windows » dans Démarrer. Retirer Raye du disque pour "
          "rendre toute la place à Windows n'a pas encore d'outil, et je n'ai pas encore essayé "
          "de marche à suivre : je ne vous en donne donc pas une.",
          "If you kept Windows alongside, it's still there: pick it in the startup menu, or "
          "“Restart to Windows” in Start. Removing Raye from the disk to give all the room back "
          "to Windows has no tool yet, and I haven't tried a way to do it: so I'm not giving "
          "you one."),
    ],
}

QUESTIONS = {
    "eyebrow": L("Le projet", "The project"),
    "h1": L("Questions", "Questions"),
    "description": L("Les questions qu'on pose en venant de Windows, avec des réponses franches.",
                     "The questions people ask coming from Windows, with straight answers."),
    "lede": L("Celles que je me poserais en venant de Windows.",
              "The ones I'd ask coming from Windows."),
    "next": "releases",
    "blocks": [
        ("qa", [
            (L("C'est gratuit ?", "Is it free?"),
             L("Oui. Raye ne coûte rien à télécharger ni à utiliser, et il n'y a pas de "
               "publicité dedans.",
               "Yes. Raye costs nothing to download or use, and there are no ads in it.")),
            (L("Est-ce que c'est Windows ?", "Is it Windows?"),
             L("Non. Raye reprend la disposition de Windows 11 pour que vos réflexes marchent, "
               "mais c'est un autre système. Les programmes Windows passent par une couche de "
               "compatibilité, avec les limites décrites sur la page "
               "<a href=\"{p:windows}\">Programmes Windows</a>.",
               "No. Raye keeps the Windows 11 layout so your habits work, but it's a different "
               "system. Windows programs go through a compatibility layer, with the limits "
               "described on the <a href=\"{p:windows}\">Windows programs</a> page.")),
            (L("Sur quoi c'est basé ?", "What is it built on?"),
             L("Raye Linux est basé sur Ubuntu 26.04 LTS, qui fournit des années de correctifs "
               "de sécurité pour le système de base et des pilotes pour la plupart des PC. Le "
               "bureau, les applis, l'installateur et les mises à jour par-dessus sont ceux de "
               "Raye, et c'est Raye qui les tient à jour. Raye n'est ni affilié à Canonical ni "
               "approuvé par elle.",
               "Raye Linux is based on Ubuntu 26.04 LTS, which provides years of security fixes "
               "for the base system and drivers for most PCs. The desktop, the apps, the "
               "installer and the updates on top are Raye's, and Raye keeps them up to date. "
               "Raye is not affiliated with Canonical or endorsed by it.")),
            (L("Je peux l'essayer sans l'installer ?", "Can I try it without installing?"),
             L("Oui, et c'est ce que fait la clé USB d'office : elle démarre sur « Try Raye "
               "Linux without installing ». Raye tourne depuis la clé et ne touche ni au disque "
               "ni à la mémoire d'échange de votre PC. L'icône Installer est sur le bureau quand "
               "vous voulez passer à l'installation.",
               "Yes, and that's what the USB stick does by default: it starts on “Try Raye Linux "
               "without installing”. Raye runs from the stick and touches neither your PC's disk "
               "nor its swap. The Install icon is on the desktop when you want to go on to the "
               "install.")),
            (L("Mes programmes vont-ils marcher ?", "Will my programs work?"),
             L("Un .exe se lance d'un double-clic. Au premier lancement, Raye lui donne seul ce "
               "qu'il demande souvent (.NET 6 à 9, Visual Basic 6, MFC, OpenAL, PhysX). Le Store "
               "a des programmes Windows installés et essayés un par un, et dit lesquels ne "
               "marchent qu'en partie, comme FL Studio et Affinity. Discord, Steam, VLC, GIMP ou "
               "LibreOffice existent en version pour Raye, dans le Store.",
               "An .exe starts with a double-click. On its first start, Raye gives it what "
               "programs often ask for (.NET 6 to 9, Visual Basic 6, MFC, OpenAL, PhysX) by "
               "itself. The Store has Windows programs installed and tried one by one, and says "
               "which ones only partly work, such as FL Studio and Affinity. Discord, Steam, VLC, "
               "GIMP or LibreOffice exist as Raye versions, in the Store.")),
            (L("Et mes jeux ?", "What about my games?"),
             L("Steam et Heroic sont dans le Store, et le mode jeu s'active tout seul pendant "
               "une partie. Roblox passe par Sober. Les jeux qui ont un anti-triche dans le "
               "noyau de Windows, comme Valorant, ne marchent pas. Easy Anti-Cheat v2 attend "
               "que la clé de Raye soit acceptée par Epic : tout est sur la page "
               "<a href=\"{p:games}\">Jeux</a>.",
               "Steam and Heroic are in the Store, and Game Mode turns on by itself while you "
               "play. Roblox runs through Sober. Games with an anti-cheat in the Windows kernel, "
               "such as Valorant, don't work. Easy Anti-Cheat v2 waits for Raye's key to be "
               "accepted by Epic: it's all on the <a href=\"{p:games}\">Games</a> page.")),
            (L("Qu'est-ce que c'est, cet écran bleu au redémarrage ?",
               "What is that blue screen at restart?"),
             L("Si Secure Boot est actif et que vous passez au noyau de Raye, le micrologiciel "
               "de votre PC demande une fois d'inscrire la clé de Raye. Raye vous montre "
               "avant un code à six chiffres : appuyez sur une touche dans les 10 secondes, "
               "choisissez Enroll MOK, Continue, Yes, tapez le code, puis Reboot. Si vous "
               "manquez l'écran, rien de grave. Voir la page "
               "<a href=\"{p:install}\">Installer</a>.",
               "If Secure Boot is on and you move to Raye's kernel, your PC's firmware asks once "
               "to enroll Raye's key. Raye shows you a six-digit code beforehand: press a key "
               "within 10 seconds, choose Enroll MOK, Continue, Yes, type the code, then Reboot. "
               "If you miss the screen, no harm done. See the <a href=\"{p:install}\">Install</a> "
               "page.")),
            (L("Y a-t-il un autre bureau que celui qui ressemble à Windows ?",
               "Is there another desktop besides the one that looks like Windows?"),
             L("Oui : Hyprland, où les fenêtres se rangent côte à côte et où l'on fait presque "
               "tout au clavier. Les deux sont dans la même installation. Voir "
               "<a href=\"{p:desktops}\">Deux bureaux</a>.",
               "Yes: Hyprland, where windows line up side by side and you do almost everything "
               "with the keyboard. Both are in the same install. See "
               "<a href=\"{p:desktops}\">Two desktops</a>.")),
            (L("Puis-je garder Windows ?", "Can I keep Windows?"),
             L("Oui, Raye peut s'installer à côté. Si Windows est chiffré par BitLocker, il faut "
               "d'abord désactiver ce chiffrement dans Windows. Lisez la mise en garde de la page "
               "<a href=\"{p:install}\">Installer</a>, et sauvegardez vos fichiers.",
               "Yes, Raye can go alongside it. If Windows is encrypted by BitLocker, you first "
               "have to turn that encryption off in Windows. Read the warning on the "
               "<a href=\"{p:install}\">Install</a> page, and back up your files.")),
            (L("Et mes fichiers Windows ?", "What about my Windows files?"),
             L("Si Windows est à côté, sa partition apparaît dans Ce PC sous le nom Windows, et "
               "après la première connexion, Raye propose Paramètres > Comptes > Fichiers de "
               "Windows pour copier vos dossiers, le fond d'écran et les favoris. Si Raye "
               "remplace Windows, « Remplacer Windows et garder mes fichiers » garde vos dossiers, "
               "le fond d'écran, les réseaux Wi-Fi et le profil du navigateur.",
               "If Windows is alongside, its partition shows in This PC under the name Windows, "
               "and after the first sign-in Raye offers Settings > Accounts > Files from Windows "
               "to copy your folders, wallpaper and favorites. If Raye replaces Windows, “Replace "
               "Windows and keep my files” keeps your folders, wallpaper, Wi-Fi networks and "
               "browser profile.")),
            (L("Je peux avoir le look de Windows 10 ?", "Can I have the Windows 10 look?"),
             L("Oui : Paramètres > Personnalisation > Style du bureau > Style Windows 10. La "
               "barre des tâches passe à gauche avec une zone de recherche, les coins deviennent "
               "carrés et Démarrer a une liste d'applis avec des tuiles.",
               "Yes: Settings > Personalization > Desktop style > Windows 10 style. The taskbar "
               "moves to the left with a search box, corners become square and Start gets an "
               "app list with tiles.")),
            (L("Combien de mémoire Raye utilise-t-il ?", "How much memory does Raye use?"),
             L("{m:ram} une fois la session ouverte, mesurés sur la machine de test, qui n'a pas "
               "de carte graphique. Sur un vrai PC, ce sera un autre chiffre, et il sera sur la "
               "page <a href=\"{p:hardware}\">Matériel</a>. 8 Go sont conseillés.",
               "{m:ram} once you've signed in, measured on the test machine, which has no "
               "graphics card. On a real PC the figure will differ, and it will be on the "
               "<a href=\"{p:hardware}\">Hardware</a> page. 8 GB is recommended.")),
            (L("Et sur un vieux PC ?", "What about an older PC?"),
             L("Raye démarre en UEFI, et la clé démarre aussi dans l'ancien mode BIOS : je l'ai "
               "vu dans une machine virtuelle de 2 Go. Si le processeur est ancien, "
               "l'installateur le dit dès sa première page, sans bloquer : certaines applis et "
               "certains jeux en demandent un plus récent. Aucun vrai vieux PC n'a encore été "
               "essayé : tout est sur la page <a href=\"{p:oldpcs}\">Vieux PC</a>.",
               "Raye starts in UEFI, and the stick also starts in the older BIOS mode: I saw it "
               "in a 2 GB virtual machine. If the processor is old, the installer says so on its "
               "first page, without stopping: some apps and games need a newer one. No real old "
               "PC has been tried yet: it's all on the <a href=\"{p:oldpcs}\">Older PCs</a> "
               "page.")),
            (L("Mon portable ne sort pas de la veille.", "My laptop doesn't wake from sleep."),
             L("Raye le voit : la première fois, il prévient, la deuxième fois de suite, il "
               "désactive la veille, et fermer le capot verrouille le PC et éteint l'écran. "
               "Paramètres > Système > Alimentation et batterie la réactive.",
               "Raye notices: the first time it warns you, the second time in a row it turns "
               "sleep off, and closing the lid locks the PC and turns the screen off. Settings > "
               "System > Power & battery turns it back on.")),
            (L("Pourquoi n'y a-t-il pas de lecteur C: ?", "Why is there no C: drive?"),
             L("Parce qu'une lettre ne dit rien de ce qu'il y a sur un disque. Le disque du "
               "système s'appelle Raye, une partition Windows s'appelle Windows.",
               "Because a letter says nothing about what's on a disk. The system disk is called "
               "Raye, a Windows partition is called Windows.")),
            (L("Une mise à jour va-t-elle redémarrer mon PC pendant que je travaille ?",
               "Will an update restart my PC while I work?"),
             L("Non. Celles qui n'ont pas besoin d'un redémarrage s'installent pendant que vous "
               "travaillez ; les autres attendent que vous choisissiez « Mettre à jour et "
               "redémarrer ». Voir <a href=\"{p:updates}\">Mises à jour</a>.",
               "No. The ones that don't need a restart install while you work; the others wait "
               "until you choose “Update and restart”. See "
               "<a href=\"{p:updates}\">Updates</a>.")),
            (L("Qu'est-ce que Raye ne fait pas ?", "What doesn't Raye do?"),
             L("Pas de dictée vocale, pas d'éclairage RVB, pas de diffusion sans fil vers un "
               "écran, pas d'Assistance rapide, pas de sous-titres en direct, pas de "
               "localisation de l'appareil, pas de comptes familiaux ni de sauvegarde vers le "
               "nuage de Windows. Le manuel dit, pour chacun, ce qu'on peut faire à la place.",
               "No voice typing, no RGB lighting, no wireless casting to a screen, no Quick "
               "Assist, no live captions, no find-my-device, no family accounts or backup to the "
               "Windows cloud. The handbook says, for each, what you can do instead.")),
            (L("Raye envoie-t-il des données sur moi ?", "Does Raye send data about me?"),
             L("Non : aucun rapport d'utilisation ni de plantage, et pas de publicité. Comme "
               "tout téléchargement, les serveurs de mises à jour voient l'adresse IP de votre "
               "PC et ce qui est téléchargé (Raye Update, le Store, Firefox). Le détail, avec les "
               "durées, est sur la page <a href=\"{p:privacy}\">Confidentialité</a>, et celle "
               "des <a href=\"{p:cookies}\">témoins</a> dit ce que le site garde dans votre "
               "navigateur.",
               "No: no usage reports and no crash reports, and no ads. Like any download, the "
               "update servers see your PC's IP address and what is downloaded (Raye Update, the "
               "Store, Firefox). The detail, with the durations, is on the "
               "<a href=\"{p:privacy}\">Privacy</a> page, and the "
               "<a href=\"{p:cookies}\">cookies</a> page says what the site keeps in your "
               "browser.")),
            (L("Faut-il un compte Raye ?", "Do I need a Raye account?"),
             L("Non, et les comptes ne sont pas encore ouverts. Raye marche pareil sans. Plus "
               "tard, un compte servira à garder une liste de réglages, votre photo et votre "
               "bibliothèque d'applications d'un PC à l'autre ; jamais vos mots de passe ni vos "
               "fichiers.",
               "No, and accounts are not open yet. Raye works the same without one. Later, an "
               "account will keep a list of settings, your picture and your app library from one "
               "PC to another; never your passwords or your files.")),
            (L("Qui fait Raye ?", "Who makes Raye?"),
             L("Moi, techoraye, au Québec. Il y a plus de détails sur la page "
               "<a href=\"{p:about}\">À propos</a>.",
               "Me, techoraye, in Quebec. There's more on the <a href=\"{p:about}\">About</a> "
               "page.")),
            (L("Comment signaler un problème ?", "How do I report a problem?"),
             L("Sur le serveur Discord, dans #bugs, ou à "
               "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a> : "
               "quel PC vous avez, ce que vous avez fait, ce que vous attendiez et ce qui s'est "
               "passé. Une photo de l'écran aide beaucoup.",
               "On the Discord server, in #bugs, or at "
               "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>: "
               "which PC you have, what you did, what you expected and what happened. A photo of "
               "the screen helps a lot.")),
        ]),
    ],
}

RELEASES = {
    "eyebrow": L("Le projet", "The project"),
    "h1": L("Les versions, de la 0.1 à la {v}", "The releases, from 0.1 to {v}"),
    "description": L("L'histoire de Raye Linux version par version, avec les dates.",
                     "The history of Raye Linux release by release, with the dates."),
    "lede": L("Avant la {v}, Raye n'a tourné que sur mes machines de test : aucune image n'a été "
              "publiée, et les bêtas leur sont arrivées par Raye Update, comme les mises à jour "
              "arriveront chez vous. Voici ce que chacune a apporté.",
              "Before {v}, Raye only ran on my test machines: no image was published, and the "
              "betas reached them through Raye Update, the way updates will reach you. Here is "
              "what each one brought."),
    "next": "about",
    "blocks": [
        ("timeline", [
            ("", L("{v}", "{v}"),
             L("Les applis Horloge et Carte graphique, des avis dans le Raye Store, le mode Essayer "
               "Raye sans l'installer, une installation qui garde vos fichiers, et Raye Update plus "
               "fiable.",
               "The Clock and Graphics Card apps, reviews in the Raye Store, Try Raye without "
               "installing, a Setup that keeps your files, and a more reliable Raye Update.")),
            ("2026-11-14", L("0.5 Bêta", "0.5 Beta"),
             L("La première image que tout le monde peut télécharger. Les archives dans l'Explorateur, le chiffrement du disque depuis les Paramètres, "
               "un Panneau de configuration rempli, et des correctifs : le clignotement de la "
               "page Performances, un menu transparent dans les Paramètres, l'écran de mise à "
               "jour décentré sur deux écrans, le Wi-Fi affiché sur un PC qui n'en a pas.",
               "The first image anyone can download. Archives in File Explorer, disk encryption from Settings, a filled Control "
               "Panel, and fixes: the flicker of the Performance page, a see-through menu in "
               "Settings, the update screen off-center on two screens, Wi-Fi shown on a PC "
               "that has none.")),
            ("2026-11-11", L("0.3 Bêta", "0.3 Beta"),
             L("Le Gestionnaire des tâches, un Explorateur refait avec ses onglets et Ce PC, le "
               "Calendrier, le Panneau de configuration et l'Éditeur du Registre. Les mises à "
               "jour qui s'installent sans redémarrage. Des couleurs plus calmes, six fonds "
               "d'écran, de nouveaux pointeurs. Sur la machine de test, le premier écran noir du "
               "démarrage passe de 18,3 s à 3 s ; un second, de 3 à 5 s avant l'écran de "
               "connexion, reste.",
               "Task Manager, a rebuilt File Explorer with its tabs and This PC, Calendar, "
               "Control Panel and the Registry Editor. Updates that install without a restart. "
               "Calmer colors, six wallpapers, new pointers. On the test machine, the first "
               "black screen at startup goes from 18.3 s to 3 s; a second one, 3 to 5 s before "
               "the sign-in screen, remains.")),
            ("2026-11-09", L("0.2 Bêta 2", "0.2 Beta 2"),
             L("Deux séries de correctifs dans la nuit du 8 au 9 novembre, à moins de cinq heures "
               "d'écart. La seconde ajoute la pièce qui manquait pour mettre à jour le BIOS d'un "
               "PC Dell, cache une estimation de batterie quand elle dépasse 24 heures et "
               "redresse l'icône de Raye Update.",
               "Two rounds of fixes on the night of November 8 to 9, less than five hours apart. "
               "The second adds the piece that was missing to update the BIOS of a Dell PC, "
               "hides a battery estimate when it goes past 24 hours and straightens the Raye "
               "Update icon.")),
            ("2026-11-08", L("0.2 Bêta", "0.2 Beta"),
             L("Les premiers paquets publiés. L'installateur a sa propre page Disque, qui relit "
               "le disque avant d'écrire. Une session en français a enfin ses dossiers en "
               "français. Une fenêtre réduite garde son bouton dans la barre.",
               "The first packages published. The installer got its own Disk page, which reads "
               "the disk again before writing. A French session finally gets French folder "
               "names. A minimized window keeps its taskbar button.")),
            ("2026-10-31", L("Le site", "The website"),
             L("rayelinux.com ouvre, avec une page « bientôt » et une liste d'inscription.",
               "rayelinux.com opens, with a “coming soon” page and a signup list.")),
            ("2026-10-30", L("0.1", "0.1"),
             L("La première image de travail, jamais publiée : de quoi installer, démarrer et "
               "commencer à mesurer.",
               "The first working image, never published: enough to install, start and begin "
               "measuring.")),
        ]),
    ],
}

ABOUT = {
    "eyebrow": L("Le projet", "The project"),
    "h1": L("Qui fait Raye, et comment", "Who makes Raye, and how"),
    "description": L("Qui fait Raye Linux, pourquoi, comment il est construit et vérifié, ses "
                     "licences et le code source.",
                     "Who makes Raye Linux, why, how it's built and checked, its licenses and "
                     "the source code."),
    "lede": L("Raye est fait par une seule personne, moi, au Québec. La première image de travail "
              "date du 30 octobre 2026.",
              "Raye is made by one person, me, in Quebec. The first working image dates from "
              "October 30, 2026."),
    "next": "home",
    "blocks": [
        H("why", "Pourquoi", "Why"),
        P("Je fais Raye pour quelqu'un qui connaît Windows 11 et qui veut changer de système "
          "sans réapprendre où sont les choses : la barre des tâches, Démarrer, les raccourcis, "
          "les Paramètres. Raye reprend cette disposition. Quand il s'en écarte, comme pour les "
          "lettres de lecteur, la page qui en parle dit pourquoi.",
          "I make Raye for someone who knows Windows 11 and wants to change systems without "
          "learning again where things are: the taskbar, Start, the shortcuts, Settings. Raye "
          "keeps that layout. When it departs from it, as with drive letters, the page about it "
          "says why."),
        H("how", "Comment c'est fait", "How it's made"),
        P("Raye Linux est basé sur Ubuntu 26.04 LTS. Par-dessus, une quinzaine de dépôts de code "
          "sont ceux de Raye : le bureau et son thème, l'installateur, les Paramètres, le "
          "Store, Raye Update, l'Explorateur, le Gestionnaire des tâches et les autres applis, "
          "le noyau optionnel, le manuel et ce site.",
          "Raye Linux is based on Ubuntu 26.04 LTS. On top of it, about fifteen code "
          "repositories are Raye's own: the desktop and its theme, the installer, Settings, the "
          "Store, Raye Update, File Explorer, Task Manager and the other apps, the optional "
          "kernel, the handbook and this website."),
        P("Avant de publier une version, je l'installe de zéro sur la machine de test et je la "
          "mets à jour depuis la précédente ; depuis la 0.3, des captures d'écran sont prises "
          "toutes les 250 ms pendant le démarrage. Les paquets sont signés, et publiés sur deux "
          "copies vérifiées identiques fichier par fichier.",
          "Before publishing a version, I install it from scratch on the test machine and "
          "update it from the previous one; since 0.3, screenshots are taken every 250 ms during "
          "startup. The packages are signed, and published on two copies checked to be "
          "identical file by file."),
        H("licence", "Licences et code source", "Licenses and source code"),
        P("Raye est fait surtout de logiciels libres ; certains micrologiciels de matériel, dont "
          "des cartes Wi-Fi ou graphiques ont besoin, ne le sont pas. Ce que j'écris pour Raye "
          "est sous licence GPL, version 3 ou ultérieure ; les pièces reprises d'ailleurs "
          "gardent leur licence (GPL, LGPL, MIT, BSD), et le manuel est sous CC BY-SA 4.0. Vous "
          "pouvez l'utiliser, le copier et le modifier selon ces licences.",
          "Raye is mostly made of free software; some hardware firmware, which Wi-Fi or "
          "graphics cards need, is not. What I write for Raye is under the GPL, version 3 or "
          "later; pieces taken from elsewhere keep their license (GPL, LGPL, MIT, BSD), and the "
          "handbook is under CC BY-SA 4.0. You may use, copy and change it under those "
          "licenses."),
        P("Pour le code source d'un paquet de Raye, écrivez à "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a> en nommant le "
          "paquet et sa version : je vous l'envoie.",
          "For the source code of a Raye package, write to "
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a> naming the package "
          "and its version: I'll send it to you."),
        H("marks", "Les marques", "Trademarks"),
        P("Raye Linux n'est ni affilié à Canonical Ltd. ni approuvé par elle. Windows est une "
          "marque de Microsoft Corporation, avec qui Raye n'a aucun lien.",
          "Raye Linux is not affiliated with Canonical Ltd. or endorsed by it. Windows is a "
          "trademark of Microsoft Corporation; Raye has no tie to that company."),
        H("contact", "Me joindre", "Getting in touch"),
        P("<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>, pour un problème, "
          "un programme qui ne marche pas, ou une question. Je lis tout.",
          "<a href=\"mailto:bonjour@rayelinux.com\">bonjour@rayelinux.com</a>, for a problem, a "
          "program that doesn't run, or a question. I read everything."),
    ],
}

# The site privacy page and the page not found carry their own description:
# the coming-soon one invites a signup the V1 site does not have.
PRIVACY_DESCRIPTION = L(
    "Ce que rayelinux.com garde quand vous vous inscrivez à sa liste, combien de temps, et "
    "comment tout faire effacer.",
    "What rayelinux.com keeps when you sign up to its list, for how long, and how to have it "
    "all deleted.")

NOT_FOUND = {
    "title": "Page introuvable · Page not found",
    "description": "Cette adresse n'existe pas sur rayelinux.com. "
                   "This address does not exist on rayelinux.com.",
    "h1": L("Page introuvable", "Page not found"),
    "text": L("Cette adresse n'existe pas sur le site. Ces pages-là existent :",
              "This address does not exist on the site. These pages do:"),
}

CONTENT = {
    "desktop": DESKTOP, "windows": WINDOWS, "updates": UPDATES, "security": SECURITY,
    "hardware": HARDWARE, "install": INSTALL, "questions": QUESTIONS,
    "releases": RELEASES, "about": ABOUT,
}

# the pages added for the launch (what is in V1, what comes next, games, the two
# desktops, older PCs) live in site_v1_more_text.py
from site_v1_more_text import CONTENT as _NEW  # noqa: E402

CONTENT.update(_NEW)
