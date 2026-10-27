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
Border tests check the drawing adapter and, when Kitty is available, 144 native
Tall layout cases across pane counts, viewport sizes, cell sizes, scales and
placement strategies. They reproduce the original stagger and check corrected
top/bottom alignment, right-column widths and fixed gaps without changing content.

Kitty's real configuration parser checks the main file, keybindings and all three
theme files using its embedded Python. It does not open a graphical window or
require a separate Python installation. `KITTY_BIN` can select an application
outside PATH. CI runs syntax, ShellCheck, installer tests and Kitty parsing on
Ubuntu and macOS; it must actually run after publication before CI success is
claimed.

Local checks use macOS and Zsh 5.9, with Kitty 0.49.2's parser and upstream shell
integration loaded from a temporary application copy. No packages, fonts or config
symlinks are installed into the user's active home by these checks.

The outline helper was also exercised in a disposable, running Kitty 0.49.2 on
macOS: 20 cases covering three/four panes, three window sizes, 16/18/22 pt fonts,
Stack-to-Tall switching and pane removal. Native border rectangle coordinates
confirmed aligned outer edges and equal gaps. Menlo was used because the requested
Nerd Font was unavailable locally. Screenshot access to Kitty was unavailable;
these were live geometry checks, not a visual inspection or a Kali VM test.

## Kali VM desktop checks still required

- Follow docs/kali-linux.md on the intended image and architecture.
- Run `bash scripts/check.sh --strict` with all intended tools installed.
- Check VM graphics, scrolling, resizing and font availability.
- Exercise directional focus, pane movement, resizing, focus toggle and tab selection.
- From one pane, press Ctrl-Shift-Enter twice: main pane left, two rows on the right.
- Re-run the installer to link aligned_borders.py and restart Kitty.
- Check full outlines at three and four panes, including after resizing and changing
  font size. Split panes should have 12 pt padding and 8 pt gaps, single panes 8 pt
  padding with no margin; top/bottom outline edges should align across columns.
- Add a pane while zoomed or focused on the main pane; it should return to Tall.
- Free Kitty's Ctrl-Alt arrows/numbers from Xfce grabs; verify desktop shortcuts separately.
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
