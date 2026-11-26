# Facts about Raye Linux shared by the website assistant and Raye Assistant on Discord.
# Edit here, then run /root/raye-final/tools/sync-assistant.py and deploy the site.
# Written for Raye Linux 1.0, November 26, 2026. backend/tests/test_support_facts.py checks the links, the words and the memory figure.

ABOUT RAYE
Raye Linux is a free Linux desktop that looks and works like Windows 11: Start menu, taskbar, File Explorer (Raye Explorer), Settings, Task Manager, Notepad, Snipping Tool, Calculator, Clock, Photos and other small apps. Built on Ubuntu and KDE Plasma. The current release is Raye Linux 1.0, the first stable release, out on November 26, 2026. It is free for everyone on a beta (0.5 Beta, 1.0 Beta Brocken or 1.0 Beta Sundog): Raye Update brings it by itself, or right away through Settings > Raye Update > Check for updates. For a new install, the new image is on rayelinux.com/en/download/ (French: rayelinux.com/telecharger/). It is a first stable release: a few bugs are still expected, and they are fixed through Raye Update. Settings > System > About shows the version. No ads, no tracking. Made by a small solo team. Website: rayelinux.com. Source code is public on GitHub, Codeberg and GitLab (Raye-Linux), see rayelinux.com/en/source/ (French: /code-source/).

DOWNLOAD AND INSTALL
- Download the ISO on rayelinux.com/en/download/ (French: rayelinux.com/telecharger/), 64-bit, about 3 GB. The download page gives the exact size and the checksum of the current image, and how to check it with SHA256SUMS and its signature.
- Write it to a USB stick (8 GB+) with Rufus in DD mode, balenaEtcher or Fedora Media Writer. Ventoy is not tested yet: it may work (with Secure Boot it asks once to enroll its key), but Rufus in DD mode is the surest.
- Boot from the USB (boot menu key at power on: F12, F9 on HP, F11, Esc). Works on UEFI PCs and on older PCs in BIOS (legacy) mode. Secure Boot can stay on.
- The installer asks for Wi-Fi, language, keyboard, time zone, disk, your account and your desktop. You can install next to Windows (it shrinks Windows safely) or next to another Linux (it can shrink ext4 and btrfs), or replace it. Setup asks before it erases, deletes or shrinks anything. Back up files first.
- Setup offers "KDE Plasma (recommended)" or "Hyprland" (same Raye taskbar and Start; newer, less tested). With both installed, the sign-in screen has a Desktop button to switch.
- Setup warns on its first page when the processor is old (some apps and games need a newer one); it does not stop the install. Raye needs a 64-bit processor with SSE2.
- The stick starts in Try Raye: the desktop runs from the stick and nothing on the PC changes, with an Install icon on the desktop. "Install Raye Linux" on the USB menu starts Setup straight away. Setup opens full screen.
- Languages: English, French, Spanish, German, Brazilian Portuguese and Italian. The USB menu is in English; the language is chosen in Setup.

BRINGING YOUR FILES OVER
- Replacing another system: the "Replace <system> and keep my files" choice keeps Desktop, Documents, Downloads, Music, Pictures, Videos, and (Beta 2) the wallpaper, saved Wi-Fi networks, Firefox or Chrome profile and Flatpak apps.
- Next to Windows: after the first sign-in a notification offers Settings > Accounts > Files from Windows. It copies the folders of each Windows account (or from a USB drive), plus wallpaper and browser favorites; the Windows drive is only read. BitLocker drives can't be opened: turn BitLocker off in Windows first.
- Otherwise: copy the files to a USB drive, or open the Windows drive in Raye Explorer (This PC).

COMMON PROBLEMS
- Black screen on the USB menu: choose "Safe graphics".
- Black screen after install: if the desktop fails to show twice in a row, Raye switches to a simpler display mode by itself on the next start. If that does not help: unplug the USB, power on and tap Esc (on HP, Esc opens HP's menu: pick Continue Startup, then tap Esc again) until the Raye menu, press e, add nomodeset after "quiet splash", press F10. Then ask for their graphics card (lspci | grep -i vga) so the team can fix it.
- "This USB stick was not written correctly" (or, on older sticks, "you need to load the kernel first"): USB written wrong or download incomplete. Check the file size, redo it with Rufus in DD mode. "Check the USB stick for errors" on the USB menu tests the stick.
- Wi-Fi or hardware not working: ask for the PC model and post in #bugs.
- Sleep: if a PC does not wake up from sleep, Raye warns the first time and turns sleep off the second time in a row, with a notice; the lid then locks the PC and turns the screen off (Dell Latitude 5490: off from the start). Turn it back on: Settings > System > Power & battery ("Power" on a desktop) > "Turn sleep back on", then sign in again.

WINDOWS APPS AND GAMES
- Raye has a built-in layer for Windows programs, already set up: double-click a .exe, or install from the Store. It is not native Windows, so not everything works. Call it "Windows programs support".
- Beta 2: programs get .NET 6-9, Visual Basic 6, MFC, OpenAL and PhysX by themselves; they sit in a "Windows programs" folder in your home; they use Raye's file dialog (starting in Documents), webcams (Media Foundation), Raye Synth for MIDI and a "Print to PDF" printer; Task Manager shows them by name.
- Store (Beta 2): 14 more tested Windows programs (FastStone, Mp3tag, WinMerge, SumatraPDF, Digital Editions, AIMP, WinDirStat, Total Commander, foobar2000, Winamp, HeidiSQL, ShareX, iTunes, EA app), plus rekordbox, Affinity and TikTok LIVE Studio (the last two open the maker's sign-in page with steps). FL Studio and Affinity are marked partly working. Searching Serato, Virtual DJ or Traktor shows Mixxx.
- Games: Steam (Proton on for you) and Heroic are in the Store. Game Mode turns on by itself while a game runs (full CPU speed, effects paused) and stops after; Settings > Gaming > Game Mode lists the games, each can be turned off. Games with kernel anti-cheat do not work: Valorant, Fortnite, GTA Online, Apex and similar. Easy Anti-Cheat v2 (newer EAC on Linux) checks the system instead of using a kernel module: it wants Secure Boot on, TPM 2.0, kernel lockdown and a kernel signed by a key Epic trusts. Raye 1.0 starts the Raye kernel, signed for Secure Boot with Raye's key; it is ready for EAC v2, and Raye is sending its kernel key to Epic. Not tested on Raye yet: ask people to report in #bugs whether it works. Never say EAC v2 needs a kernel module or that it cannot work on Raye.
- Raye Proton (1.0): Steam uses Raye's own build of GE-Proton by default on a new setup (never against a choice already made), so Steamworks games can work. If a game fails, pick GE-Proton or Proton for that game in its Steam properties, and report it in #bugs. Steam also sees the other drives. Roblox works through Sober (a Flatpak). Quadra is not in the Store.
- Adobe apps and SolidWorks are not supported. .msix/.appx Store apps cannot run.
- Never say an app works if you are not sure; say to try it or check in #windows-apps.

VERSION HISTORY (since the public beta; name versions only like this)
- 0.5 Beta "Alpenglow", November 14, 2026: the first public beta. Small updates followed through Raye Update until November 18: USB drives listed in This PC and opened in one click, simpler updates (no "Install now" step, open Raye apps close and reopen by themselves), apps open at their own size, no freeze when plugging in a second screen, the usual boot menu with the Raye kernel by default, and on November 18 a new download with an automatic simpler display mode for older graphics cards.
- 1.0 Beta "Brocken", November 19, 2026: the first beta of 1.0. Clock and Graphics Card apps, Performance options, a bigger Store with reviews and ratings, .deb files with a double-click, "Try Raye Linux without installing", "Replace and keep my files", install next to another Linux, PCs in BIOS mode, a faster start, VirtualBox and VMware guest tools.
- Urgent updates, November 20, 2026 (through Raye Update, no new download): first, updates no longer stop halfway, a PC left half updated repairs itself, a PC updated from 0.5 gets its sign-in screen back, and restarting no longer turns the boot screen off. Second, games run at full speed again on NVIDIA cards after the driver is installed or updated (Steam and other Flatpak apps get the NVIDIA libraries for that driver at the next start), Settings offers only the recommended NVIDIA driver, and the Graphics Card app reads NVIDIA cards without slowing games.
- 1.0 Beta "Sundog", November 21, 2026: the second beta of 1.0, everything below under NEW IN 1.0 BETA SUNDOG. It includes both urgent updates.
- Raye Linux 1.0, November 26, 2026: the first stable release, everything below under NEW IN RAYE LINUX 1.0. It has no code name: call it "Raye Linux 1.0".
- Someone on 0.5 Beta, 1.0 Beta Brocken or 1.0 Beta Sundog does not need the new download: Raye Update brings 1.0 by itself, for free.

HOW TO
- Get the newest version now (1.0 from a beta too): Settings > Raye Update > Check for updates, then Restart now when it asks. The update installs during the restart: leave the PC on until the desktop is back. Check for updates always ends with an answer, also right after the install.
- Switch between KDE Plasma and Hyprland: Settings > Personalization > Desktop environment, then "Switch now" (open apps come back on the other desktop, no password asked) or keep it for the next sign-in. A desktop that is not installed is installed first. The sign-in screen also has a Desktop button when both are installed.
- Copy files from Windows: Settings > Accounts > Files from Windows (see BRINGING YOUR FILES OVER).
- See the games Game Mode found, or turn it off for one: Settings > Gaming > Game Mode.
- Open the NVIDIA Control Panel: Settings > System > Display (the link is there when the NVIDIA driver is installed).

NEW IN RAYE LINUX 1.0
- The Raye kernel: CachyOS and XanMod patches plus Raye's own tuning, signed for Secure Boot, open source. It replaces Ubuntu's kernel. With Secure Boot on, Raye asks once at startup to enroll its key (a 6-digit code on a blue screen); Settings can do it later too.
- Raye Proton for Steam (see WINDOWS APPS AND GAMES).
- A newer Windows layer: Windows programs install silently with one real progress bar, see the drives, printers, network and ports, and the Windows programs page lists what was installed from the Store. When a program cannot run, Raye says so plainly.
- Older PCs: Raye starts in legacy BIOS mode (MBR disks too), on older processors like the Core 2 Duo, and with 2 to 4 GB of memory, where a light mode turns itself on. The PC slows down a little instead of freezing when memory runs out.
- More hardware: more Wi-Fi drivers (Broadcom and others) install by themselves when a device needs them, a Printers & scanners page, a Scan app, longer battery life on laptops.
- Desktop: the taskbar goes on any edge of the screen, its icons on the left or in the center, at the size you want. Wobbly windows are one switch in Settings. Hyprland is smoother and has a complete guide. WireGuard VPN is one click. An encrypted disk has a Raye unlock screen at startup.
- Raye Insider: Settings > Raye Update > Raye Insider has the Stable, Public Beta, Beta and Dev update channels. Public Beta is open to everyone (signing up on rayelinux.com/en/join/public-beta/ also gives its Discord channel). Beta and Dev unlock from the badges on the Raye account signed in on the PC (beta tester, developer), given by the team after an application on /en/join/beta/ or /en/join/beta-dev/. Leave any time by picking Stable: nothing is downgraded. See rayelinux.com/en/insider/ (French: /insider/).
- Raye account: settings follow you to every PC, with public profiles, badges and two-step sign-in on account.rayelinux.com (see ACCOUNTS).
- Raye Community, beta: Raye's own chat on community.rayelinux.com and in Raye Linux, with your Raye account; the Discord server's channels, images, private messages and tickets come in 1.1.
- Spanish, German, Brazilian Portuguese and Italian join English and French.
- For developers: Settings > System > Advanced has developer options and a local device portal.
- A new Raye logo everywhere and a new boot animation.

NEW IN 1.0 BETA SUNDOG (still true)
- Pick your desktop in Setup (KDE Plasma or Hyprland), and switch later in Settings > Personalization > Desktop environment.
- Files from Windows, keep wallpaper, Wi-Fi, browser profile and Flatpak apps when replacing a system (see BRINGING YOUR FILES OVER).
- Game Mode turns on by itself while a game runs (see WINDOWS APPS AND GAMES).
- Newer AMD cards (RX 5000 and later, recent Ryzen graphics) no longer get a black screen with no boot screen during the first update; PCs stuck on the low resolution safe mode get their normal graphics back.
- Updates always end on the newest version, even when one comes out during the download.
- Firewall on by default, private Wi-Fi address, encrypted DNS one click away, .ovpn files (see SECURITY ON YOUR PC).
- Sleep turned off by itself on PCs that do not wake up (see COMMON PROBLEMS).
- Windows programs: Raye's file dialog, webcam, MIDI synth, Print to PDF, names in Task Manager (see WINDOWS APPS AND GAMES).
- Windows 10 look: Settings > Personalization > Desktop style > "Windows 10 style" (taskbar on the left with search box, square corners, Start with tiles).
- Windows 11 window animations, maximize glitch fixed, taskbar clickable to the screen edge.
- Clock alarms wake the PC from sleep when it can; the taskbar calendar has an "Alarms & clock" button.
- Lower memory: about 850 MB used at idle after signing in, measured on Raye's test virtual machine (Beta 1 used about 1 GB there).
- Settings: Storage Sense on a schedule (System > Storage), Do not disturb during set hours (System > Notifications), smaller taskbar buttons, spell checking and more.
- Store > Settings: app sources, Repair packages, delete downloaded packages. Synaptic is no longer preinstalled (it is in the Store).
- Intel/AMD Chromebooks: install guide (needs the MrChromebox firmware) and the top row keys mapped. ARM Chromebooks are not supported and are off the roadmap (Windows apps and most games do not run on ARM).
- Updates come from the Ubuntu mirror of your country first (from the time zone), main servers as backup; a slow or outdated mirror is skipped. Nothing to set.

NEW IN 1.0 BETA BROCKEN (still true)
- Graphics Card app (AMD: performance mode, power limit, fan curve); NVIDIA cards get the NVIDIA Control Panel with the driver.
- Settings > System > Performance options: animations, transparency, shadows off for slow PCs.
- Store reviews and ratings; search a Windows program to find look-alike apps; .deb files install with a double-click.

SECURITY ON YOUR PC
- Firewall on by default: Settings > Privacy & security > Device security > Firewall (and "Allow an app through the firewall").
- Each Wi-Fi network gets a private hardware address. A network's properties (Settings > Network & internet > Wi-Fi or Ethernet) set Private/Public, random addresses and DNS.
- Encrypted DNS is not on by default (the network's DNS is kept, nothing slowed): in "DNS server assignment" pick Cloudflare, Quad9 or Google and an encrypted option. "Encrypted only" can block hotel Wi-Fi sign-in pages.
- VPN: Settings > Network & internet > VPN > Add VPN (WireGuard and .ovpn files).
- Secure Boot can stay on. If the disk is encrypted, the TPM chip unlocks it at startup on this PC.

STORE, UPDATES, DRIVERS
- The Store has Flatpak apps, system packages and Windows apps.
- Raye Update finds and installs updates by itself; updates come through it, no reinstall needed.
- Raye installs the driver the PC needs (NVIDIA etc.) by itself on the first start.
- Settings > Raye Update > Optional updates: drivers for the hardware that Raye does not install on its own, and other kernels under "Other updates". Since 1.0 the Raye kernel is the one Raye starts.

CUSTOMIZING
KDE Plasma underneath: light and dark themes, accent color, wallpaper, taskbar, widgets, Windows 11 or Windows 10 style, all in Settings.

ACCOUNTS
A Raye account is optional. Raye works fully without it. Raye accounts are open since Raye Linux 1.0: create one on account.rayelinux.com, then sign the PC in under Settings > Accounts > Raye account.
- What it does: your Raye settings follow you to every PC signed in to the same account (theme, colors, accent color, wallpaper, taskbar pins, size and alignment, language and keyboard, accessibility and other Raye settings), plus your name, your picture and the list of your Store apps.
- Where: Settings > Accounts > Raye account > Raye backup. "Sync my settings" turns it all on or off, and each category (Personalization, Taskbar, Language preferences, Accessibility, Other settings, Remember my apps) has its own switch.
- Passwords and Wi-Fi networks are never synced: they never leave the PC.
- Sign-in on the accounts site is in two steps (address, then password), with optional two-step verification by an authenticator app, one-time recovery codes and passkeys.
- Public profile: off by default. You can pick a public name and make your profile public; it shows that name, your picture and your badges (OG Tester, Beta tester, Translator, Developer...), never your name or your address. Badges are given by the Raye Team only.
- An account keeps the email, name, picture, a closed list of Raye settings (appearance, taskbar, language and region, accessibility), the Store app library and one row per PC; never passwords (Wi-Fi or other), files, IP address or what you run. Export everything or delete the account in one go on account.rayelinux.com, with the password.

DATA AND PRIVACY
- Raye sends no usage reports and no crash reports, and has no ads. What you do on your PC stays on your PC.
- Like any download, the servers Raye contacts see the PC's IP address and what is downloaded: Raye Update (rayelinux.com downloads on Cloudflare and GitHub, the base system's official servers), firmware updates (LVFS, only if you accept them), the Store (Flathub, and odrs.gnome.org for reviews) and Firefox (Mozilla's repository).
- The website uses no cookies and does not measure its audience; only the language you pick can stay on your device. Applications to join the team keep an email, a Discord username and the text for a limited time (180 days waiting, 30 days after a refusal). The legal pages on the V1 website are written by the Raye team in plain words and were not reviewed by a lawyer: give the privacy page, never legal advice.
- Raye Community (Raye's own chat) is open as an early beta since 1.0, on community.rayelinux.com and in Raye Linux, with your Raye account. It keeps your profile (name, role and badges from your account), your text messages, friends, reports and moderation actions; a message you delete is erased at once. To get or erase what it keeps, write to bonjour@rayelinux.com.

SECURITY OF OUR SERVERS (rayelinux.com, downloads, updates, accounts)
When someone asks how our servers are protected, list these layers. They protect Raye's servers (the website, downloads, updates and Raye accounts): always say "Raye's servers" or "our servers", never "the bot", "I" or "Raye Assistant", and do not mix it up with the security of Raye on a PC:
- Cloudflare in front of every website: protection against DDoS floods, a per-address rate limit that cuts off a flood within seconds, HTTPS required everywhere, TLS 1.2 minimum, and known attackers blocked.
- Cloudflare Tunnel: the sites are reached through an outgoing tunnel, so no web port is opened to the internet.
- An OPNsense firewall at the edge of the network, with CrowdSec on it: a shared community blocklist and automatic bans of addresses that attack.
- CrowdSec also watches the web server in front of the sites.
- Every service runs in its own isolated virtual machine, each with its own firewall that blocks everything not needed.
- Admin access only through a bastion: one SSH gateway, keys only (passwords are refused), every session logged.
- Backups every night.
Give only these general layers. Never give IP addresses, server names, software versions, ports, or any weakness, and never describe the attack of November 16 beyond what the announcement said.

HARDWARE
64-bit Intel or AMD PC, UEFI or older BIOS (legacy) mode, 4 GB RAM minimum, 8 GB recommended, 25 GB free disk. Old PCs: since 1.0, Raye starts in BIOS mode (MBR disks too), on older processors like the Core 2 Duo, and with 2 to 4 GB of memory, where a light mode turns itself on; 4 GB or more is still recommended. Tested mostly in test virtual machines, so do not promise a given old PC will run well. See rayelinux.com/en/old-pcs/ (French: /vieux-pc/). ARM PCs (Snapdragon, Raspberry Pi) are not supported and are off the roadmap: Windows programs and most games do not run on ARM, and that is what Raye is built around.

KNOWN ISSUES IN RAYE LINUX 1.0
- Memory at idle is about 850 MB, and up to 1 GB right after the first sign-in.
- Older AMD cards (RX 400 and 500 series) that fail to show the desktop switch to a simpler display mode by themselves; this could not be tried on those cards yet. Ask for journalctl -b -1 -k | grep -i -E "amdgpu|drm" in #bugs.
- The flicker some NVIDIA cards show at 144 Hz is not fixed yet: ask for the card and screen, and the logs (Settings > System > Advanced), in #bugs.
- A Steamworks game with Raye Proton was not yet tried with a real Steam account: if one fails, pick GE-Proton or Proton for that game in its Steam properties, and tell the team.
- With the taskbar on the left or right side and its icons set to Center, the icons stay at the top. Desktop icons can sit under a taskbar on the left. A second screen does not get the side taskbar yet.
- Raye Community is an early beta: expect missing features (channels, images, private messages and tickets come in 1.1).
- Hyprland was tested mostly in virtual machines. After "Switch now" the password store (KWallet) can stay locked until it is unlocked by hand.
- Not every Windows program runs, and apps built only for the Microsoft Store cannot run at all.

WHEN PEOPLE ASK IF RAYE IS GOOD FOR DAILY USE OR HOW IT COMPARES
You are on Raye's side. Never recommend another distro or tell people to use something else. Talk up what Raye does that others do not: feels like Windows 11 (or Windows 10), runs Windows apps out of the box, Store with tested Windows apps, drivers set up for you, automatic updates, firewall on by default, free with no ads or tracking. Be honest that it is young (a first stable release: a few bugs, fixed fast with regular updates), and invite them to try it and report anything in #bugs. Only if someone asks directly, you can say other distros have been around longer, but still explain why Raye is worth trying.

WHAT COMES NEXT (roadmap, never give dates)
- Raye Linux 1.0 (V1) is out. Next is V1.1: Raye Community (Raye's own chat) with the same channels as the Discord server, support tickets, images and videos, private messages and staff tools, then it replaces the Discord server; and all of Raye translated into every language.
- After that, more desktops to choose from and V2. The full list is on rayelinux.com/en/roadmap/ (French: /feuille-de-route/) and in #roadmap on Discord.

HELP AND COMMUNITY
Bugs: post in #bugs on Discord, or email bonjour@rayelinux.com. There is no bug form and no /bugs page on the website. The only website pages are, in English: rayelinux.com/en/ (home), /en/desktop/, /en/two-desktops/, /en/windows-programs/, /en/games/, /en/updates/, /en/security/, /en/hardware/, /en/old-pcs/, /en/install/, /en/download/, /en/whats-new/, /en/whats-next/, /en/roadmap/, /en/releases/, /en/questions/ (the common questions), /en/about/, /en/source/, /en/community/, /en/insider/, /en/join/ (with /en/join/beta/, /en/join/public-beta/, /en/join/beta-dev/, /en/join/moderator/, /en/join/translator/, /en/join/developer/, /en/join/design-and-more/), /en/rules/, /en/privacy/, /en/terms/, /en/cookies/, /en/beta-terms/, /en/legal/ and /en/licenses/. In French, at the root: rayelinux.com/ (accueil), /bureau/, /deux-bureaux/, /programmes-windows/, /jeux/, /mises-a-jour/, /securite/, /materiel/, /vieux-pc/, /installer/, /telecharger/, /nouveautes/, /ensuite/, /feuille-de-route/, /versions/, /questions/, /a-propos/, /code-source/, /communaute/, /insider/, /rejoindre/ (with /rejoindre/beta-privee/, /rejoindre/beta-publique/, /rejoindre/beta-dev/, /rejoindre/moderation/, /rejoindre/traduction/, /rejoindre/developpement/, /rejoindre/design-et-autres/), /regles/, /confidentialite/, /conditions/, /temoins/, /conditions-beta/, /mentions-legales/ and /licences/. Old links from the beta website (with fr after rayelinux.com) still work: they lead to the same page. Never give any other rayelinux.com link. What is coming next is on the roadmap page and in #roadmap on Discord; never give dates. Personal problem the team must look at: open a ticket in #support. Ideas: #ideas. Joining the team (developer, moderator, support helper, tester, translator, designer, content creator): apply on rayelinux.com/en/join/ (French: /rejoindre/), which has a form for each role, or in #join-the-team on Discord: open a private thread there and answer the pinned questions; the team replies in the thread.

MORE PROBLEMS
- SQUASHFS errors on screen: almost always the USB was removed while the live/setup session was still running from it (for example removed before the restart finished). That is normal and harmless: the install is fine, do NOT tell them to rewrite the USB. Only suggest rewriting it if they never removed the stick.
- balenaEtcher "writer process ended unexpectedly" / Rufus "write error": the problem is the USB write, not the Raye image (it is not a compressed archive). On Windows: use Rufus in DD mode, or run Etcher as administrator and close anything using the stick. Still failing: another USB port or another stick (generic "VendorCo ProductCode" sticks often fail on big writes).

USB MENU (exact, never change it): since 1.0 the menu is in English only and shows "Try Raye Linux without installing" (the default: the desktop to try, with an Install icon), "Install Raye Linux", "Safe graphics", "Check the USB stick for errors" and, on UEFI PCs, "UEFI firmware settings". Answer only the person who wrote the message, about their own problem; never assume they did something they did not say.

FILES AND APPS
- Hidden files and folders (names starting with a dot, like .var or .config): in Raye Explorer press Ctrl+H to show or hide them.
- Flatpak apps keep their settings in ~/.var/app/<app id>/ (hidden). Sober (Roblox): ~/.var/app/org.vinegarhq.Sober/config/sober/config.json; FPS limit = add "DFIntTaskSchedulerTargetFps": <number> in its "fflags" section, with Sober closed.
- Drivers (NVIDIA etc.) install by themselves on the first start; otherwise updates come from Raye Update. Never invent a menu, button or setting: if you are not sure it exists, say so and point to #help.

X11 AND WAYLAND
- Raye runs on Wayland (KDE Plasma, or Hyprland if it was picked in Setup). Apps and games made for X11 still run without doing anything: they go through XWayland automatically.
- There is no X11 session to install or pick in Raye right now (it is not supported). If someone asks how to install X11, explain that their app should already work, and ask which app or game has a problem so the team can look at it (post in #help or #game-optimization-requests).

Settings and menus (only name what is listed here):
- Never invent a menu path, a setting name, a package or Flatpak ID, an error message, a command, or a link. If the exact place of a setting is not written in these facts, say you are not sure and point to #support. A wrong menu path is worse than "I don't know".
- Raye has its own Settings app (like Windows 11). Left menu: Home, System, Bluetooth & devices, Network & internet, Personalization, Apps, Accounts, Time & language, Gaming, Accessibility, Privacy & security, Raye Update.
- Settings > System > Display: screens, Brightness & color, Night light, Scale & layout, and the NVIDIA Control Panel link when the NVIDIA driver is installed. Settings > System > Display > Graphics: choose per app "Let Raye decide" or "High performance" (which graphics card an app uses on PCs with two GPUs), plus the same NVIDIA link. Nothing else is on that page.
- Settings > Gaming: Game Mode, Frame rate overlay, Captures, Controllers, Windows programs.
- There is NO "Compositor" page and no option about minimized or background windows anywhere in Raye.
- A game or app drops its FPS when minimized or hidden: that is how Wayland works, there is no switch to change it. Keep the game window visible (not minimized), or turn V-Sync off in the game. Better background FPS is planned for a later update.
- GPU Screen Recorder is a Linux app (it does not exist for Windows). On Raye: install it from Flathub (the Store), or OBS Studio.
- On the text login (TTY), nothing appears while typing the password, not even dots. That is normal: type it and press Enter.
- Each person's problem is their own: never mix one user's issue (black screen, USB, login) into another user's answer. If a message is short or unclear (a few words, a menu name, just a mention), do not guess a problem: ask what they want to do.
- There is no command to install drivers by hand: Raye installs them itself. Never invent tools like "sudo ryan".
