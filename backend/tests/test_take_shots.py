"""tools/take_shots.py: every screenshot the site shows has a recipe, nothing is
written from a blank screen or a test account, and the pictures and manifest
are what the site builder reads."""

import datetime
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "tools"))
sys.path.insert(0, TOOLS)
sys.dont_write_bytecode = True
import take_shots as T  # noqa: E402

from PIL import Image, ImageDraw  # noqa: E402


def sample(path, blank=False):
    img = Image.new("RGB", (1280, 800), (10, 10, 20))
    if not blank:
        ImageDraw.Draw(img).rectangle((100, 100, 900, 600), fill=(120, 80, 220))
    img.save(path)


class ShotsTests(unittest.TestCase):
    def test_every_shot_of_the_site_has_exactly_one_recipe(self):
        ids = T.shot_ids()
        recipes = [s for st in T.STAGES.values() for s in st]
        self.assertEqual(sorted(ids), sorted(recipes))
        self.assertEqual(len(recipes), len(set(recipes)))

    def test_each_recipe_takes_a_picture_and_uses_known_steps(self):
        for stage, recipes in T.STAGES.items():
            for sid, steps in recipes.items():
                with self.subTest(shot=sid):
                    self.assertIn(("shot",), steps)
                    for st in steps:
                        self.assertIn(st[0], T.VERBS)

    def test_pictures_are_the_three_files_the_builder_wants(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = os.path.join(tmp, "a.png")
            sample(png)
            files = T.write_pictures(png, "snap", "en", tmp)
            self.assertEqual([os.path.basename(f) for f in files],
                             ["snap-en-1600.webp", "snap-en-800.webp", "snap-en-1600.jpg"])
            for f in files:
                self.assertTrue(os.path.getsize(f) > 500)
            self.assertEqual(Image.open(files[1]).size[0], 800)

    def test_a_blank_screen_is_never_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            png = os.path.join(tmp, "b.png")
            sample(png, blank=True)
            with self.assertRaises(RuntimeError):
                T.write_pictures(png, "snap", "en", tmp)
            self.assertEqual(os.listdir(tmp), ["b.png"])

    def test_the_manifest_names_the_version_and_keeps_other_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "manifest.json"), "w") as f:
                json.dump({"old-fr": {"version": "1.0", "date": "x"}}, f)
            T.write_manifest(["snap-en"], "1.0", tmp, today=datetime.date(2026, 12, 1))
            data = json.load(open(os.path.join(tmp, "manifest.json")))
            self.assertEqual(data["snap-en"], {"version": "1.0", "date": "2026-12-01"})
            self.assertIn("old-fr", data)

    def test_the_example_user_is_neutral_and_never_a_test_account(self):
        self.assertEqual(T.FULL_NAME, "Sam Rivers")
        self.assertNotRegex(T.FULL_NAME + T.USER, T.TESTISH)
        self.assertNotIn("Test Raye", json.dumps(T.STAGES))

    def test_the_script_refuses_a_vm_that_is_not_the_clean_final_install(self):
        class Fake(T.VM):
            def __init__(self, answers):
                super().__init__()
                self.answers = list(answers)

            def guest(self, command):
                return self.answers.pop(0)

        Fake(["Sam Rivers", 'PRETTY_NAME="Raye Linux 1.0"\n']).check_clean("1.0")
        for answers in (["Test Raye", 'PRETTY_NAME="Raye Linux 1.0"'],
                        ["Sam Rivers", 'PRETTY_NAME="Raye Linux 1.0 Beta Sundog"'],
                        ["Sam Rivers", 'PRETTY_NAME="Raye Linux 1.0 (development build)"'],
                        ["Sam Rivers", 'PRETTY_NAME="Raye Linux 0.5"']):
            with self.subTest(answers=answers):
                with self.assertRaises(SystemExit):
                    Fake(answers).check_clean("1.0")

    def test_dry_run_touches_nothing(self):
        before = sorted(os.listdir(T.SHOTS_DIR))
        r = subprocess.run([sys.executable, os.path.join(TOOLS, "take_shots.py"), "--dry-run",
                            "--stage", "desktop", "--lang", "fr", "--only", "snap"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(sorted(os.listdir(T.SHOTS_DIR)), before)


class DriverTests(unittest.TestCase):
    def test_programs_start_in_the_users_graphical_session(self):
        # an SSH shell has no screen and no session bus: a window started from
        # it never shows, so programs go through the user's systemd manager
        argv = T.VM().launch_argv("raye-settings --page system")
        self.assertEqual(argv[:4], ["systemd-run", "--user", "--machine", "sam@"])
        self.assertEqual(argv[-1], "raye-settings --page system")
        vm = T.VM()
        seen = []
        vm.root = lambda a, timeout=60: seen.append(a) or ""
        vm.run(("run", "dolphin --new-window raye:thispc"))
        self.assertEqual(seen[0][:2], ["systemd-run", "--user"])

    def test_commands_go_through_the_guest_agent_not_ssh_into_the_vm(self):
        argv = T.VM(host="pve").guest_argv(["loginctl", "unlock-sessions"])
        self.assertEqual(argv[:3], ["ssh", "-o", "BatchMode=yes"])
        self.assertIn("qm guest exec 130", argv[-1])
        self.assertTrue(argv[-1].endswith("-- loginctl unlock-sessions"))

    def test_a_failing_guest_command_stops_the_script(self):
        vm = T.VM()

        class R:
            returncode, stderr = 0, ""
            stdout = json.dumps({"exitcode": 1, "err-data": "no such page"})
        orig = T.subprocess.run
        T.subprocess.run = lambda *a, **k: R()
        try:
            with self.assertRaises(RuntimeError):
                vm.root(["false"])
        finally:
            T.subprocess.run = orig

    def test_a_release_candidate_or_a_beta_name_is_not_the_final_release(self):
        class Fake(T.VM):
            def __init__(self, answers):
                super().__init__()
                self.answers = list(answers)

            def guest(self, command):
                return self.answers.pop(0)

        for pretty in ('PRETTY_NAME="Raye Linux 1.0 RC 1"', 'VERSION="1.0~rc1"',
                       'PRETTY_NAME="Raye Linux 1.0 Sundog"',
                       'PRETTY_NAME="Raye Linux 1.0 Release Candidate"',
                       'PRETTY_NAME="Raye Linux 1.0.1"'):
            with self.subTest(pretty=pretty):
                with self.assertRaises(SystemExit):
                    Fake(["Sam Rivers", pretty]).check_clean("1.0")

    def test_no_recipe_clicks_at_guessed_places(self):
        # the old recipes clicked at a guessed share of the screen; a wrong
        # guess opens the wrong thing and the picture still gets written
        for recipes in T.STAGES.values():
            for sid, steps in recipes.items():
                self.assertNotIn("click", [s[0] for s in steps], sid)

    def test_every_picture_says_what_it_has_to_show(self):
        for lang in T.LANGS:
            for sid in T.shot_ids():
                self.assertTrue(T.must_show(sid, lang).strip(), sid)


class TrialTests(unittest.TestCase):
    def run_trial(self, out):
        class Fake(T.VM):
            def __init__(self, dry=False, host=None, user=T.USER):
                super().__init__(dry, host, user)

            def check_clean(self, version):
                raise AssertionError("a trial checks no user and no version")

            def set_language(self, lang):
                pass

            def run(self, step):
                pass

            def screendump(self, dest):
                sample(dest)
                return True
        orig = T.VM
        T.VM = Fake
        try:
            return T.main(["--trial", out, "--stage", "desktop", "--lang", "en",
                           "--only", "quick,win-x"])
        finally:
            T.VM = orig

    def test_a_trial_writes_beside_the_site_and_never_the_manifest(self):
        before = {n: os.path.getmtime(os.path.join(T.SHOTS_DIR, n)) for n in os.listdir(T.SHOTS_DIR)}
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self.run_trial(tmp), 0)
            self.assertEqual(sorted(os.listdir(tmp)),
                             sorted(f"{s}-en-{w}" for s in ("quick", "win-x")
                                    for w in ("1600.webp", "800.webp", "1600.jpg")))
        after = {n: os.path.getmtime(os.path.join(T.SHOTS_DIR, n)) for n in os.listdir(T.SHOTS_DIR)}
        self.assertEqual(before, after)

    def test_a_trial_on_another_account_drives_that_account(self):
        # the release candidate in the VM has its own account; a trial there
        # must start programs and set the language for it, not for "sam"
        vm = T.VM(dry=True, user="testr")
        self.assertEqual(vm.launch_argv("true")[:4], ["systemd-run", "--user", "--machine", "testr@"])
        seen = []
        vm.root = lambda a, timeout=60: seen.append(a) or ""
        vm.set_language("fr")
        self.assertIn(["loginctl", "terminate-user", "testr"], seen)
        self.assertEqual(seen[0][:3], ["runuser", "-u", "testr"])
        self.assertEqual(T.VM().user, "sam")

    def test_another_account_only_for_a_trial(self):
        # the pictures of the site come from the neutral example user only
        with self.assertRaises(SystemExit) as cm:
            T.main(["--user", "testr", "--dry-run", "--stage", "desktop", "--only", "quick"])
        self.assertIn("--trial", str(cm.exception.code))

    def test_a_trial_into_shots_is_refused(self):
        with self.assertRaises(SystemExit):
            self.run_trial(T.SHOTS_DIR)


if __name__ == "__main__":
    unittest.main()
