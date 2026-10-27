"""Integration checks for real installers, using disposable homes and tool fixtures."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")
KITTY = os.environ.get("KITTY_BIN") or shutil.which("kitty")
if not KITTY and Path("/Applications/kitty.app/Contents/MacOS/kitty").is_file():
    KITTY = "/Applications/kitty.app/Contents/MacOS/kitty"


def system_tools_only(bindir):
    """Keep fixture PATH independent of optional tools installed on CI runners."""
    for name in ["mkdir", "mv", "rm", "cat", "id", "uname", "chmod", "ls", "head", "sed", "awk", "grep", "sort", "date", "wc", "cut"]:
        path = bindir / name
        original = shutil.which(name)
        if original and not path.exists():
            path.symlink_to(original)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kitty-zsh-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home with spaces"
        self.home.mkdir()
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.env = {k: v for k, v in os.environ.items() if k not in {
            "ZDOTDIR", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "SUDO_USER", "KITTY_CONFIG_DIRECTORY"
        }}
        self.env.update(HOME=str(self.home), PATH=f"{self.bin}:{os.environ['PATH']}")
        self.tool("uname", 'printf "Linux\\n"')

    def tool(self, name, body):
        dest = self.bin / name
        dest.write_text("#!/bin/sh\n" + body + "\n")
        dest.chmod(0o755)

    def run_script(self, script="install.sh", *args, success=True):
        proc = subprocess.run([BASH, str(REPO / script), *map(str, args)],
                              env=self.env, cwd=self.root, capture_output=True,
                              text=True, timeout=15)
        if success:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        return proc

    def backups(self):
        base = Path(self.env.get("XDG_STATE_HOME", self.home / ".local/state"))
        return sorted((base / "kitty-zsh/backups").glob("*"))

    def test_dry_run_has_no_side_effects(self):
        self.run_script("install.sh", "--dry-run")
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_links_and_repeated_install_is_idempotent(self):
        self.run_script()
        expected = {
            self.home / ".zshrc": REPO / "zsh/.zshrc",
            self.home / ".zprofile": REPO / "zsh/.zprofile",
            self.home / ".config/starship.toml": REPO / "starship/starship.toml",
            self.home / ".config/kitty/kitty.conf": REPO / "kitty/kitty.conf",
            self.home / ".config/kitty/aligned_borders.py": REPO / "kitty/aligned_borders.py",
        }
        for dest, source in expected.items():
            self.assertTrue(dest.is_symlink())
            self.assertEqual(dest.resolve(), source)
        for name in ["dark-theme.auto.conf", "light-theme.auto.conf", "no-preference-theme.auto.conf"]:
            self.assertEqual((self.home / ".config/kitty" / name).resolve(), REPO / "kitty" / name)
        self.run_script()
        self.assertEqual(len(self.backups()), 1)

    def test_originals_overrides_and_history_survive_restore(self):
        original = self.home / ".zshrc"
        original.write_text("# original rc\n")
        previous = self.home / "previous-profile"
        previous.write_text("# previous profile\n")
        (self.home / ".zprofile").symlink_to(previous)
        override = self.home / ".zshrc.local"
        history = self.home / ".zsh_history"
        override.write_text("# private\n")
        history.write_text("private history\n")
        self.run_script()
        backup = self.backups()[0]
        self.assertEqual((backup / "zshrc").read_text(), "# original rc\n")
        self.run_script("scripts/restore.sh", backup)
        self.assertEqual(original.read_text(), "# original rc\n")
        self.assertTrue((self.home / ".zprofile").is_symlink())
        self.assertEqual((self.home / ".zprofile").resolve(), previous.resolve())
        self.assertFalse((self.home / ".config/starship.toml").exists())
        self.assertFalse((self.home / ".config/kitty/aligned_borders.py").exists())
        self.assertEqual(override.read_text(), "# private\n")
        self.assertEqual(history.read_text(), "private history\n")
        self.run_script("scripts/restore.sh", backup)

    def test_broken_symlink_is_preserved(self):
        dest = self.home / ".zshrc"
        dest.symlink_to(self.home / "missing-original")
        self.run_script()
        self.run_script("scripts/restore.sh", self.backups()[0])
        self.assertTrue(dest.is_symlink())
        self.assertEqual(os.readlink(dest), str(self.home / "missing-original"))

    def test_restore_refuses_changed_file_before_restoring_anything(self):
        self.run_script()
        dest = self.home / ".config/starship.toml"
        dest.unlink()
        dest.write_text("# new local config\n")
        self.run_script("scripts/restore.sh", self.backups()[0], success=False)
        self.assertEqual(dest.read_text(), "# new local config\n")
        self.assertTrue((self.home / ".zshrc").is_symlink())

    def test_existing_directory_is_rejected_before_any_changes(self):
        (self.home / ".zprofile").mkdir()
        self.run_script(success=False)
        self.assertFalse((self.home / ".zshrc").exists())
        self.assertEqual(self.backups(), [])

    def test_custom_xdg_zdotdir_and_existing_kitty_settings(self):
        config = self.root / "xdg config"
        zdot = self.root / "zsh dotfiles"
        state = self.root / "xdg state"
        kitty = config / "kitty/kitty.conf"
        kitty.parent.mkdir(parents=True)
        kitty.write_text("# old terminal\n")
        private = config / "kitty/kitty.local.conf"
        private.write_text("font_size 14\n")
        light = config / "kitty/light-theme.auto.conf"
        light.write_text("background #ffffff\n")
        self.env.update(XDG_CONFIG_HOME=str(config), XDG_STATE_HOME=str(state), ZDOTDIR=str(zdot))
        self.run_script()
        self.assertTrue((zdot / ".zshrc").is_symlink())
        self.assertTrue((config / "starship.toml").is_symlink())
        self.assertTrue(kitty.is_symlink())
        self.run_script("scripts/restore.sh", self.backups()[0])
        self.assertEqual(kitty.read_text(), "# old terminal\n")
        self.assertEqual(light.read_text(), "background #ffffff\n")
        self.assertEqual(private.read_text(), "font_size 14\n")

    def test_macos_uses_the_same_kitty_directory(self):
        self.tool("uname", 'printf "Darwin\\n"')
        self.run_script()
        path = self.home / ".config/kitty/kitty.conf"
        self.assertTrue(path.is_symlink())
        self.assertFalse((self.home / "Library/Application Support").exists())

    def test_custom_kitty_config_directory(self):
        custom = self.root / "custom kitty"
        self.env["KITTY_CONFIG_DIRECTORY"] = str(custom)
        self.run_script()
        self.assertTrue((custom / "kitty.conf").is_symlink())
        self.assertFalse((self.home / ".config/kitty").exists())

    def test_late_theme_failure_rolls_back_all_earlier_links(self):
        original = self.home / ".zshrc"
        original.write_text("# original\n")
        real_ln = shutil.which("ln")
        self.tool("ln", f'case "$*" in *light-theme.auto.conf*) exit 1 ;; esac\nexec "{real_ln}" "$@"')
        self.run_script(success=False)
        self.assertEqual(original.read_text(), "# original\n")
        self.assertFalse((self.home / ".config/kitty/kitty.conf").exists())
        self.assertFalse((self.home / ".config/kitty/dark-theme.auto.conf").exists())

    def test_failed_link_rolls_back_prior_changes(self):
        original = self.home / ".zshrc"
        original.write_text("# keep me\n")
        real_ln = shutil.which("ln")
        self.tool("ln", f'case "$*" in *.zprofile*) exit 1 ;; esac\nexec "{real_ln}" "$@"')
        self.run_script(success=False)
        self.assertEqual(original.read_text(), "# keep me\n")
        self.assertFalse(original.is_symlink())
        self.assertFalse((self.home / ".zprofile").exists())
        self.assertEqual((self.backups()[0] / "status").read_text(), "rolled-back\n")

    def test_relative_xdg_path_is_rejected(self):
        self.env["XDG_CONFIG_HOME"] = "relative/path"
        self.run_script(success=False)
        self.assertEqual(list(self.home.iterdir()), [])

    @unittest.skipUnless(KITTY, "Kitty is needed for parser checks")
    def test_real_kitty_parser_loads_private_include_through_symlinks(self):
        self.run_script()
        config = self.home / ".config/kitty"
        (config / "kitty.local.conf").write_text("font_size 13.5\nbackground_opacity 1.0\n")
        self.env.update(KITTY_BIN=KITTY, TEST_KITTY_CONFIG=str(config / "kitty.conf"))
        self.run_script("scripts/validate-kitty.sh", config)
        proc = subprocess.run([KITTY, "+runpy", '''
import os
from kitty.config import load_config
opts = load_config(os.environ["TEST_KITTY_CONFIG"])
assert opts.font_size == 13.5 and opts.background_opacity == 1.0
'''], env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    @unittest.skipUnless(KITTY, "Kitty is needed for parser checks")
    def test_real_kitty_parser_rejects_invalid_private_setting(self):
        self.run_script()
        config = self.home / ".config/kitty"
        (config / "kitty.local.conf").write_text("font_size definitely-invalid\n")
        self.env["KITTY_BIN"] = KITTY
        self.run_script("scripts/validate-kitty.sh", config, success=False)

    def test_apt_dry_run_never_invokes_apt_or_sudo(self):
        self.tool("apt-get", "exit 90")
        self.tool("sudo", "exit 91")
        self.tool("apt-cache", '''case "$2" in
starship) printf '  Candidate: (none)\\n' ;;
*) printf '  Candidate: 1.0\\n' ;;
esac''')
        proc = self.run_script("scripts/install-deps-kali.sh", "--dry-run")
        self.assertIn("No apt candidate: starship", proc.stdout)
        packages = proc.stdout.split("Apt packages: ")[1].splitlines()[0].split()
        for package in ["kitty", "ripgrep", "fd-find", "fzf"]:
            self.assertIn(package, packages)
        self.assertIn("Dry run", proc.stdout)

    def test_font_checksum_failure_does_not_install_files(self):
        self.tool("curl", '''while [ "$#" -gt 0 ]; do
  if [ "$1" = --output ]; then printf 'invalid archive' > "$2"; exit 0; fi
  shift
done
exit 1''')
        self.run_script("scripts/install-font.sh", success=False)
        self.assertFalse((self.home / ".local/share/fonts").exists())

    @unittest.skipUnless(shutil.which("zsh"), "Zsh is needed for the startup check")
    def test_zsh_starship_xdg_path_and_explicit_override(self):
        bindir = self.home / ".local/bin"
        bindir.mkdir(parents=True)
        starship = bindir / "starship"
        starship.write_text("#!/bin/sh\nprintf '%s\\n' 'typeset -g TEST_STARSHIP_CONFIG=\"$STARSHIP_CONFIG\"'\n")
        starship.chmod(0o755)
        source = (REPO / "zsh/.zshrc").read_text()
        # Keep the host's optional packages out of this startup fixture.
        for prefix in ["/opt/homebrew", "/usr/local", "/usr/share"]:
            source = source.replace(prefix, str(self.root / "packages" / prefix.lstrip("/")))
        config = self.root / "fixture.zshrc"
        config.write_text(source)
        system_tools_only(self.bin)
        env = {k: v for k, v in self.env.items() if not k.startswith(("HOMEBREW_", "KITTY_", "STARSHIP_"))}
        env.update(PATH=str(self.bin), TERM="xterm-256color",
                   XDG_CONFIG_HOME=str(self.root / "xdg config"), TEST_ZSHRC=str(config))
        for override in [None, str(self.root / "custom prompt.toml")]:
            if override:
                env["STARSHIP_CONFIG"] = override
            env["EXPECTED_STARSHIP_CONFIG"] = override or str(self.root / "xdg config/starship.toml")
            proc = subprocess.run([shutil.which("zsh"), "-f", "-ic", '''
              source "$TEST_ZSHRC"
              unset HISTFILE
              [[ $STARSHIP_CONFIG == "$EXPECTED_STARSHIP_CONFIG" &&
                 $TEST_STARSHIP_CONFIG == "$EXPECTED_STARSHIP_CONFIG" ]]
            '''], env=env, capture_output=True, text=True, timeout=15)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(proc.stderr, "")


@unittest.skipUnless(shutil.which("zsh"), "Zsh is needed for startup checks")
class StartupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kitty-zsh-startup-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "home with spaces"
        self.bin = self.home / ".local/bin"
        self.bin.mkdir(parents=True)
        system_tools_only(self.bin)
        source = (REPO / "zsh/.zshrc").read_text()
        for prefix in ["/opt/homebrew", "/usr/local", "/usr/share"]:
            source = source.replace(prefix, str(self.root / "packages" / prefix.lstrip("/")))
        config = self.root / "fixture.zshrc"
        config.write_text(source)
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(
            ("HOMEBREW_", "KITTY_", "STARSHIP_", "FZF_", "XDG_"))
            and k not in {"ZDOTDIR", "MANPAGER", "MANROFFOPT"}}
        self.env.update(HOME=str(self.home), PATH=str(self.bin), TERM="xterm-256color",
                        XDG_CACHE_HOME=str(self.root / "cache"), TEST_ZSHRC=str(config))

    def tool(self, name, body="exit 0"):
        path = self.bin / name
        path.write_text("#!/bin/sh\n" + body + "\n")
        path.chmod(0o755)

    def fzf(self):
        self.tool("fzf", "printf '%s\\n' 'typeset -g TEST_FZF_INIT=loaded'")

    def run_zsh(self, checks):
        proc = subprocess.run([shutil.which("zsh"), "-f", "-ic",
                               'source "$TEST_ZSHRC"; unset HISTFILE; ' + checks],
                              env=self.env, capture_output=True, text=True, timeout=15)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertEqual(proc.stderr, "")

    def test_minimal_install_has_working_defaults(self):
        self.run_zsh('''
          (( ! $+commands[fd] && ! $+commands[rg] && ! $+commands[fzf] )) || exit 11
          [[ ! -v aliases[ls] && $aliases[ll] == 'ls -lah' ]] || exit 12
          [[ $options[sharehistory] == on && $options[incappendhistory] == off ]] || exit 13
          [[ $PROMPT == *'%# '* && -z ${MANPAGER-} ]]
        ''')

    def test_fd_takes_precedence_over_ripgrep(self):
        self.fzf()
        self.tool("fd", "printf 'fd-result\\n'")
        self.tool("rg", "printf 'rg-result\\n'")
        self.run_zsh('''
          [[ $TEST_FZF_INIT == loaded ]] || exit 21
          [[ $(eval "$FZF_DEFAULT_COMMAND") == fd-result ]] || exit 22
          [[ $(eval "$FZF_ALT_C_COMMAND") == fd-result ]]
        ''')

    def test_ripgrep_fallback_without_fd(self):
        self.fzf()
        self.tool("rg", "printf 'rg-result\\n'")
        self.run_zsh('''
          [[ $(eval "$FZF_CTRL_T_COMMAND") == rg-result ]] || exit 31
          (( ! ${+FZF_ALT_C_COMMAND} ))
        ''')

    def test_debian_executable_names(self):
        self.fzf()
        self.tool("fdfind", "printf 'fdfind-result\\n'")
        self.tool("batcat", "printf '%s\\n' \"$@\"")
        self.run_zsh('''
          [[ $(eval "$FZF_CTRL_T_COMMAND") == fdfind-result ]] || exit 41
          [[ $FZF_CTRL_T_OPTS == *batcat* ]] || exit 42
          [[ $(eval 'bat --plain "file with spaces"') == $'--plain\\nfile with spaces' ]] || exit 43
          [[ $(eval 'fd config') == fdfind-result ]]
        ''')

    def test_native_bat_and_fd_take_precedence_over_debian_names(self):
        self.fzf()
        self.tool("bat", "printf 'native-bat\\n'")
        self.tool("batcat", "exit 91")
        self.tool("fd", "printf 'native-fd\\n'")
        self.tool("fdfind", "exit 92")
        self.run_zsh('''
          [[ ! -v aliases[bat] && ! -v aliases[fd] ]] || exit 51
          [[ $(eval 'bat') == native-bat && $(eval 'fd') == native-fd ]] || exit 52
          [[ $(eval "$FZF_CTRL_T_COMMAND") == native-fd ]] || exit 53
          [[ $FZF_CTRL_T_OPTS == *"'bat "* ]]
        ''')


if __name__ == "__main__":
    unittest.main()
