# Install on macOS

With [Homebrew](https://brew.sh/) installed, run from this checkout:

```sh
brew bundle --file=dependencies/Brewfile
bash install.sh --dry-run
bash install.sh
bash scripts/check.sh --strict
```

The Brewfile includes Kitty, JetBrainsMono Nerd Font, Starship, fd, ripgrep, fzf,
bat, eza, zoxide and both Zsh plugins. There is no need to run the font helper if
the font cask is installed.

Launch Kitty from Applications. Its config lives in `~/.config/kitty` by default,
just as on Linux, and launches `zsh -l` without changing your account's default
shell. Both Intel and Apple Silicon Homebrew locations are supported.

The CLI may be available through PATH or at
`/Applications/kitty.app/Contents/MacOS/kitty`; the check scripts detect both.
For a nonstandard installation, set `KITTY_BIN` to the executable when running
checks. This affects validation only, not shell startup.

Cross-platform Ctrl shortcuts are documented in [usage](usage.md); Kitty's normal
macOS shortcuts remain available too. On macOS, Alt means Option, and the OS/VM
may intercept some combinations. Private override files let you remap them.

Ctrl-Shift-F5 reloads Kitty configuration. Open a new tab or run `reload` to load
Zsh changes. The shell's manual Kitty integration survives `exec zsh`.

When switching from another terminal project, common Zsh/Starship destinations
are replaced with backups, while the other terminal's own config is preserved.
Rollback uses the exact command printed by `install.sh`.
