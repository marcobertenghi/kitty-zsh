# Validation

This package adapts the previously reviewed portable Zsh setup to Kitty and adds
ripgrep explicitly. Starship's config path is selected from XDG_CONFIG_HOME unless
a STARSHIP_CONFIG override is already set.

## Automated checks

```sh
bash -n install.sh
for script in scripts/*.sh; do bash -n "$script"; done
zsh -n zsh/.zshrc
zsh -n zsh/.zprofile
python3 -m unittest discover -s tests -v
bash scripts/validate-kitty.sh
# Optional developer static check:
shellcheck install.sh scripts/*.sh
```

Tests run in temporary homes with fixture tools. They cover backups and restore,
repeated install, dry-run, broken symlinks, custom XDG/ZDOTDIR/Kitty directories,
private-file preservation, partial-failure rollback, apt manifests and font checks.
Startup checks exercise optional dependencies and fzf fallbacks.

Kitty's real configuration parser checks the main file, keybindings and all three
theme files using its embedded Python. It does not open a graphical window or
require a separate Python installation. `KITTY_BIN` can select an application
outside PATH. CI runs syntax, ShellCheck, installer tests and Kitty parsing on
Ubuntu and macOS; it must actually run after publication before CI success is
claimed.

Local checks use macOS and Zsh 5.9, with Kitty 0.49.2's parser and upstream shell
integration loaded from a temporary application copy. No packages, fonts or config
symlinks are installed into the user's active home by these checks.

## Kali VM desktop checks still required

- Follow docs/kali-linux.md on the intended image and architecture.
- Run `bash scripts/check.sh --strict` with all intended tools installed.
- Check VM graphics, scrolling, resizing and font availability.
- Exercise directional focus, pane movement, resizing, focus toggle and tab selection.
- Check explicit splits after switching to grid/stack and same-directory launching.
- Verify Moon stays selected across desktop light/dark appearance changes.
- Try Ctrl-R/Ctrl-T/Alt-C, previews, history sharing and man paging.
- Check prompt markers and cursor behaviour after `reload` and nested Zsh.
- Check SSH/root indicators in deliberately opened sessions.

Local parser tests and Ubuntu CI do not establish actual Kali VM GUI performance.

## Timing

Measure shell startup separately from Kitty startup and prompt rendering:

```sh
time zsh -ic 'unset HISTFILE'
time zsh -lic 'unset HISTFILE'
starship timings
```

Use a warm completion cache for repeated startup measurements. No numeric Kitty or
Kali VM speed claim is made from the configuration-only tests.
