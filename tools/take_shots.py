#!/usr/bin/env python3
"""Take every screenshot of the V1 site (the SHOTS of site_v1_text.py), in
English and in French, in the test VM 130, from a CLEAN install of the final
ISO, and write them where the site builder reads them (shots/).

    tools/take_shots.py --list                    what will be taken, by stage
    tools/take_shots.py --stage desktop --version 1.0 [--lang en] [--only snap,quick]
    tools/take_shots.py --dry-run ...             print the steps, touch nothing

Run it AFTER the final ISO is installed in VM 130 (not before: the pictures
carry the version) and while you hold the lock:

    flock /root/raye-final/v1/vm130.lock tools/take_shots.py --stage desktop --version 1.0

The stages follow what the VM shows, because the live stick, the installer and
the installed system are three different screens:

  live     the USB menu and the trial session (boot the ISO as the CD)
  setup    the installer pages (boot the ISO, start Install, stop before writing)
  desktop  the installed system, signed in as the example user

Rules the script enforces:
  * the example user is neutral (name "Sam Rivers", account "sam"); it REFUSES
    to shoot when the signed-in user's name looks like a test account;
  * the installed system must say it is the version given by --version, with
    no "development" or "beta" build text, or nothing is written;
  * the language is set for the whole session (plasma-localerc + a new
    sign-in), never by pressing keys in a menu;
  * a picture is only written when it is not blank (it has to show something).

How it drives the VM: /var/tmp/raye/pvectl.py for the screen (screendump,
keys) and the guest agent (`qm guest exec` on the Proxmox host) for commands:
programs are started in the example user's own graphical session. Where no
key reaches a screen safely (a drag, an install in progress, a real restart)
the recipe asks the person to set it up and waits for Enter. The script prints
each file it writes, so a wrong window is seen at once; --only redoes one.

Try the recipes on any other install (a test account, a release candidate)
with --trial DIR: the user and version checks are skipped, the pictures go to
DIR and shots/ and its manifest are never touched."""

import argparse
import datetime
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

SHOTS_DIR = os.path.join(REPO, "shots")
PVECTL = os.environ.get("RAYE_PVECTL", "/var/tmp/raye/pvectl.py")
USER, FULL_NAME = "sam", "Sam Rivers"
LANGS = ("en", "fr")
WIDTHS = ((1600, "webp"), (800, "webp"), (1600, "jpg"))
TESTISH = re.compile(r"test|raye|admin|root|demo|vm", re.I)
# what a build that is not the final release says about itself
PRERELEASE = re.compile(r"development|dev build|\bbeta\b|\brc ?\d|release candidate|sundog|brocken",
                        re.I)

# --- the recipes ------------------------------------------------------------
# a step is (verb, arg...):
#   key COMBO      pvectl key           type TEXT    pvectl type
#   wait SECONDS   sleep                shot         take the picture
#   run CMD        start CMD in the example user's graphical session
#                  (systemd-run --user, so it has the screen and the session bus)
#   root CMD       a command run as root in the VM (unlock, clean up)
#   ask TEXT       the person sets the screen up by hand, then presses Enter:
#                  for what no key can reach safely (a drag, a running install,
#                  a password prompt over a write, a real restart)
# Keys are the Windows ones Raye keeps. Program names and Settings page ids are
# the real ones (raye-settings --page <id of settings/data/layout.json>,
# raye-store --open <app>, dolphin raye:thispc).
DESKTOP = {
    "desktop": [("key", "super"), ("wait", 2), ("shot",), ("key", "esc")],
    "start-all": [("key", "super"), ("wait", 2),
                  ("ask", "click All in the Start menu"), ("shot",), ("key", "esc")],
    "win-x": [("key", "super-x"), ("wait", 1), ("shot",), ("key", "esc")],
    "explorer": [("key", "super-e"), ("wait", 3), ("key", "ctrl-t"), ("wait", 1), ("shot",),
                 ("key", "alt-f4")],
    "snap": [("key", "super-e"), ("wait", 3),
             ("ask", "drag the File Explorer window to the top of the screen and keep the "
                     "mouse button down on a layout (the picture is taken when you press Enter "
                     "in this terminal)"),
             ("shot",), ("key", "alt-f4")],
    "quick": [("key", "super-a"), ("wait", 2), ("shot",), ("key", "esc")],
    "thispc": [("run", "dolphin --new-window raye:thispc"), ("wait", 3),
               ("ask", "right-click the Raye drive, then Properties"), ("shot",),
               ("key", "alt-f4"), ("key", "alt-f4")],
    "taskmgr": [("key", "ctrl-shift-esc"), ("wait", 3), ("shot",), ("key", "alt-f4")],
    "settings": [("run", "raye-settings --page system"), ("wait", 4), ("shot",), ("key", "alt-f4")],
    "control": [("key", "super-r"), ("wait", 1), ("type", "control\n"), ("wait", 3), ("shot",),
                ("key", "alt-f4")],
    "regedit": [("key", "super-r"), ("wait", 1), ("type", "regedit\n"), ("wait", 3),
                ("ask", "open a key and change a value under HKEY_LOCAL_MACHINE so the password "
                        "prompt shows on top"),
                ("shot",), ("key", "esc"), ("key", "alt-f4")],
    "calendar": [("ask", "add a Calendar reminder due in one minute and wait for it"),
                 ("key", "super-n"), ("wait", 2), ("shot",), ("key", "esc")],
    "store": [("run", "raye-store"), ("wait", 5),
              ("ask", "start installing a small app and stay on its page while it installs"),
              ("shot",), ("key", "alt-f4")],
    "lock": [("key", "super-l"), ("wait", 4), ("shot",), ("root", "loginctl unlock-sessions"),
             ("wait", 2)],
    "uac": [("key", "super-r"), ("wait", 1), ("type", "pkexec true\n"), ("wait", 3), ("shot",),
            ("key", "esc")],
    "update-live": [("run", "raye-settings --page update/raye-update"), ("wait", 4),
                    ("ask", "the page has to show the installed updates and one that says "
                            "Restart required (install one first if needed)"),
                    ("shot",), ("key", "alt-f4")],
    "restore": [("run", "raye-settings --page system/recovery"), ("wait", 4),
                ("ask", "the list has to show a Before updates / After updates pair"),
                ("shot",), ("key", "alt-f4")],
    "desktop-choice": [("run", "raye-settings --page personalization/desktop"), ("wait", 4),
                       ("shot",), ("key", "alt-f4")],
    "steam-store": [("run", "raye-store --open steam"), ("wait", 6), ("shot",), ("key", "alt-f4")],
    "exe-setup": [("ask", "double-click the installer .exe of a small free Windows program "
                          "(in Downloads) and go halfway through it"),
                  ("shot",)],
    "exe-start": [("ask", "finish that install, open the program from the Start menu"),
                  ("shot",), ("key", "alt-f4")],
    "exe-native": [("ask", "double-click a Windows installer Raye has its own version of "
                           "(for example the VLC .exe)"),
                   ("shot",), ("key", "esc")],
    "update-boot": [("ask", "install an update that needs a restart and restart: the picture is "
                            "taken on the Installing updates screen"),
                    ("shot",)],
    # the last one: it leaves the default desktop
    "hypr-session": [("ask", "Settings > Desktop environment > Hyprland, sign in again, then "
                             "open two windows side by side"),
                     ("shot",),
                     ("ask", "switch back to Raye's desktop the same way")],
}
LIVE = {
    "try-raye": [("wait", 5), ("shot",)],
    "enroll-key": [("wait", 3), ("shot",)],
    "boot-menu": [("wait", 3), ("shot",)],
}
SETUP = {
    "setup-disk": [("wait", 2), ("shot",)],
    "setup-encrypt": [("wait", 2), ("shot",)],
    "setup-summary": [("wait", 2), ("shot",)],
    # the first sign-in after an encrypted install
    "recovery-key": [("wait", 2), ("shot",)],
}
STAGES = {"desktop": DESKTOP, "live": LIVE, "setup": SETUP}
VERBS = ("key", "type", "wait", "run", "root", "ask", "shot")
# Whole stages the person brings on screen first (the script waits for Enter):
# the installer and the blue key screen erase a disk or need a real boot.
MANUAL = {"live", "setup"}


def shot_ids():
    import site_v1_text as V
    import site_v1_more_text  # noqa: F401  (adds its shots to V.SHOTS)
    return list(V.SHOTS)


def must_show(sid, lang):
    """What the site says the picture shows (SHOTS of site_v1_text.py)."""
    import site_v1_text as V
    import site_v1_more_text  # noqa: F401
    text = V.SHOTS[sid]
    return text.get(lang, text.get("en")) if isinstance(text, dict) else text


def plan(stages=None, only=None):
    """[(stage, shot id)] in the order they are taken."""
    out = []
    for stage in (stages or STAGES):
        for sid in STAGES[stage]:
            if not only or sid in only:
                out.append((stage, sid))
    return out


# --- pictures ---------------------------------------------------------------

def is_blank(img):
    """True when the picture shows (almost) one colour: a black screen."""
    small = img.convert("L").resize((32, 20))
    lo, hi = small.getextrema()
    return hi - lo < 12


def write_pictures(png, sid, lang, out_dir=None):
    """The three files the site wants, from one screendump."""
    from PIL import Image
    out_dir = out_dir or SHOTS_DIR
    img = Image.open(png).convert("RGB")
    if is_blank(img):
        raise RuntimeError(f"{sid}-{lang}: the screen is blank, not written")
    for width, ext in WIDTHS:
        h = round(img.height * width / img.width)
        pic = img.resize((width, h), Image.LANCZOS) if img.width != width else img
        path = os.path.join(out_dir, f"{sid}-{lang}-{width}.{ext}")
        if ext == "webp":
            pic.save(path, "WEBP", quality=82, method=6)
        else:
            pic.save(path, "JPEG", quality=86, optimize=True)
    return [os.path.join(out_dir, f"{sid}-{lang}-{w}.{e}") for w, e in WIDTHS]


def write_manifest(entries, version, out_dir=None, today=None):
    out_dir = out_dir or SHOTS_DIR
    path = os.path.join(out_dir, "manifest.json")
    data = {}
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    day = (today or datetime.date.today()).isoformat()
    for key in entries:
        data[key] = {"version": version, "date": day}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


# --- the VM -----------------------------------------------------------------

class VM:
    """VM 130: the screen through pvectl (QMP on the host), commands through the
    guest agent (`qm guest exec` on the host). No SSH into the VM: a clean
    install has no key of ours, and that is how it should stay."""
    VMID = 130

    def __init__(self, dry=False, host=None):
        self.dry = dry
        self.host = host or os.environ.get("RAYE_PVE_HOST", "pve")

    def pvectl(self, *args):
        cmd = [sys.executable, PVECTL, *args]
        if self.dry:
            print("   $", " ".join(cmd))
            return ""
        return subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=120).stdout

    def guest_argv(self, argv, timeout=60):
        """The host command that runs argv as root in the VM."""
        return ["ssh", "-o", "BatchMode=yes", self.host,
                shlex.join(["qm", "guest", "exec", str(self.VMID), "--timeout", str(timeout),
                            "--", *argv])]

    def root(self, argv, timeout=60):
        """Run argv as root in the VM, give back what it printed."""
        if self.dry:
            print("   [vm as root]", shlex.join(argv))
            return ""
        r = subprocess.run(self.guest_argv(argv, timeout), capture_output=True, text=True,
                           timeout=timeout + 30)
        if r.returncode != 0:
            raise RuntimeError(f"guest exec failed: {r.stderr.strip()}")
        out = json.loads(r.stdout)
        if out.get("exitcode", 0) != 0:
            raise RuntimeError(f"{shlex.join(argv)} exited {out.get('exitcode')}: "
                               f"{out.get('err-data', '').strip()}")
        return out.get("out-data", "")

    def guest(self, command):
        """A shell command run as the example user (no screen)."""
        return self.root(["runuser", "-u", USER, "--", "sh", "-c", command])

    def launch_argv(self, command):
        """A program started in the example user's graphical session: the user's
        systemd manager has the screen and the session bus, an SSH shell has not."""
        return ["systemd-run", "--user", "--machine", f"{USER}@", "--collect", "--quiet",
                "--", "sh", "-c", command]

    def launch(self, command):
        return self.root(self.launch_argv(command))

    def check_clean(self, version):
        """Refuse a VM that is not the clean final install."""
        if self.dry:
            return
        name = self.guest(f"getent passwd {USER} | cut -d: -f5 | cut -d, -f1").strip()
        if name != FULL_NAME or TESTISH.search(name.replace(FULL_NAME, "")):
            sys.exit(f"the example user must be '{FULL_NAME}' ({USER}); the VM says '{name}'. "
                     "Install the final ISO with that name.")
        text = self.guest("grep -h -i -E '^(PRETTY_NAME|VERSION)=' /etc/os-release "
                          "/etc/raye-release 2>/dev/null")
        if PRERELEASE.search(text) or not re.search(rf"(?<![\d.]){re.escape(version)}(?![\d.~])", text):
            sys.exit(f"the VM does not say it is Raye {version} (final): {text.strip()!r}")

    def signed_in(self):
        """True when the example user has a graphical session (seat0) open."""
        out = self.root(["loginctl", "list-sessions", "--no-legend"])
        return any(USER in line.split() and "seat0" in line.split() for line in out.splitlines())

    def set_language(self, lang):
        """The language of the whole session: Plasma's locale file, then a new
        sign-in. The install has to sign the example user in automatically."""
        loc = "fr_CA.UTF-8" if lang == "fr" else "en_US.UTF-8"
        self.guest(f"mkdir -p ~/.config && printf '[Formats]\\nLANG={loc}\\n\\n"
                   f"[Translations]\\nLANGUAGE={lang}\\n' > ~/.config/plasma-localerc")
        self.root(["loginctl", "terminate-user", USER])
        if self.dry:
            return
        for _ in range(30):
            time.sleep(5)
            if self.signed_in():
                time.sleep(15)          # let the desktop finish drawing
                return
        sys.exit(f"{USER} was not signed in again within 150 s: turn on automatic sign-in "
                 "for that account (Settings > Accounts) and start again")

    def run(self, step):
        verb, args = step[0], step[1:]
        if verb == "wait":
            time.sleep(0 if self.dry else args[0])
        elif verb == "key":
            self.pvectl("key", args[0])
        elif verb == "type":
            self.pvectl("type", args[0])
        elif verb == "run":
            self.launch(args[0])
        elif verb == "root":
            self.root(["sh", "-c", args[0]])
        elif verb == "ask":
            print(f"   >> {args[0]}. Press Enter when the screen is ready.")
            if not self.dry:
                input()
        else:
            raise ValueError(f"unknown step {verb}")

    def screendump(self, dest):
        if self.dry:
            print(f"   [screendump] -> {dest}")
            return False
        self.pvectl("shot", dest)
        return True


def take(vm, stage, sid, lang, out_dir=None):
    """Play one recipe; give back "<id>-<lang>" when a picture was written."""
    print(f"== {stage}/{sid} ({lang})")
    print(f"   it has to show: {must_show(sid, lang)}")
    if stage in MANUAL:
        print(f"   bring the VM to that screen, in {'French' if lang == 'fr' else 'English'}. "
              "Press Enter when it is on screen.")
        if not vm.dry:
            input()
    taken = None
    for step in STAGES[stage][sid]:
        if step[0] == "shot":
            with tempfile.TemporaryDirectory(prefix="raye-shot-") as tmp:
                png = os.path.join(tmp, "s.png")
                if vm.screendump(png):
                    files = write_pictures(png, sid, lang, out_dir)
                    print("   written", ", ".join(os.path.basename(f) for f in files))
                    taken = f"{sid}-{lang}"
        else:
            vm.run(step)          # the steps after the picture close the window
    return taken


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--stage", choices=sorted(STAGES), action="append")
    ap.add_argument("--lang", choices=LANGS, action="append")
    ap.add_argument("--only")
    ap.add_argument("--version", default="1.0")
    ap.add_argument("--trial", metavar="DIR",
                    help="any install: pictures go to DIR, shots/ and the manifest stay as they are")
    args = ap.parse_args(argv)
    only = set(args.only.split(",")) if args.only else None

    missing = set(shot_ids()) - {s for st in STAGES.values() for s in st}
    if missing:
        sys.exit("SHOTS without a recipe: " + ", ".join(sorted(missing)))
    todo = plan(args.stage, only)
    if args.list:
        for stage, sid in todo:
            print(f"{stage:8} {sid}")
        return 0
    vm = VM(dry=args.dry_run)
    out_dir = None
    if args.trial:
        out_dir = os.path.abspath(args.trial)
        if os.path.realpath(out_dir) == os.path.realpath(SHOTS_DIR):
            sys.exit("--trial writes beside the site, never into shots/")
        os.makedirs(out_dir, exist_ok=True)
    else:
        vm.check_clean(args.version)
    done = []
    for lang in args.lang or LANGS:
        if any(st == "desktop" for st, _ in todo):
            vm.set_language(lang)
        for stage, sid in todo:
            key = take(vm, stage, sid, lang, out_dir)
            if key:
                done.append(key)
    if done and not args.dry_run and not args.trial:
        write_manifest(done, args.version)
        print("manifest.json updated:", len(done), "entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
