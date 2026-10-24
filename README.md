# Kitty + Zsh

A lightweight, feature-rich terminal setup for Kali Linux and macOS: Kitty splits
and tabs, Rosé Pine Moon colours, a useful Zsh prompt, and fast file/content search.
No plugin framework and no downloads during shell startup.

**[Install on Kali Linux](docs/kali-linux.md)** · [macOS](docs/macos.md) ·
[Shortcuts and customisation](docs/usage.md)

For matching Xfce styling, see the optional
[Kali desktop guide](docs/kali-desktop.md): Moon theme, wallpapers, panel and launcher.

## Quick start on Kali

From a permanent copy of this repository, as your normal user:

```sh
bash scripts/install-deps-kali.sh
bash scripts/install-font.sh
bash install.sh --dry-run
bash install.sh
bash scripts/check.sh --strict
kitty
```

The apt helper installs the available packages in `dependencies/kali-apt.txt` and
reports missing candidates. If Starship is unavailable through apt, follow its
[upstream installation steps in the Kali guide](docs/kali-linux.md#starship-if-apt-has-no-candidate).
The shell also works with optional tools absent. The config launches `zsh -l`;
you do not need to change your account's login shell.

## Included

- Portable Zsh history, completion, prefix search, directory stack and keybindings.
- Starship with Rose Pine styling, automatic OS icons, SSH hostname and root styling.
- Kitty splits, grid/tall layouts, directional pane navigation and a focus toggle.
- Numbered tabs, current-directory launching and shell integration after `reload`.
- fd, ripgrep (`rg`), fzf, bat, eza and zoxide integration (Debian names aliased).
- Autosuggestions and syntax highlighting, loaded without a plugin manager.
- Rosé Pine Moon in every desktop appearance mode, with a matching Starship palette.
- An 18 pt font, right-click copying, subtle transparency and rounded powerline tabs.
- Package manifests, font helper, config checks, backup/restore and CI tests.

Only the small MIT-licensed Rose Pine colour files are vendored, with their
[licence](kitty/ROSE-PINE-LICENSE). Applications, fonts and plugins are installed
through package managers or upstream releases, rather than bundled as binaries.

## Dependencies

| Tool | Purpose | Without it |
| --- | --- | --- |
| Zsh | Shell, history and native completion | Required for this shell config |
| Kitty | Terminal, tabs, splits and shell integration | Zsh works in other terminals |
| JetBrainsMono Nerd Font | Prompt icons | Install the font or use a plain prompt |
| Starship | Styled prompt | Built-in Zsh prompt |
| fd / fdfind | Fast file and directory search | rg for fzf files, otherwise fzf defaults |
| ripgrep / rg | Search file contents; fallback file finder | fd or fzf defaults still work |
| fzf | Ctrl-R, Ctrl-T, Alt-C fuzzy search | Native history/completion |
| bat / batcat + col + less | Highlighted previews and man pages | Plain previews / default man pager |
| eza | Enhanced listings and tree previews | System ls |
| zoxide | `z` / `zi` directory navigation | Normal cd |
| zsh-autosuggestions | Suggestions while typing | Normal editing |
| zsh-syntax-highlighting | Command syntax colouring | Normal editing |

Node, Go, Rust and PHP are not required. Starship shows them only in relevant
projects where those runtimes are already installed. An editor is your choice;
this project does not install one.

## Files and installer behaviour

| Source | Destination |
| --- | --- |
| `zsh/.zshrc`, `zsh/.zprofile` | `${ZDOTDIR:-$HOME}/` |
| `starship/starship.toml` | `${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml` |
| `kitty/kitty.conf` and three `*.auto.conf` files | `${KITTY_CONFIG_DIRECTORY:-${XDG_CONFIG_HOME:-$HOME/.config}/kitty}/` |

Kitty uses the same configuration layout on Linux and macOS. The installer links
individual files; other Kitty files, SSH settings, history and private overrides
are preserved. Existing destination files and symlinks are backed up before being
replaced. Repeated installation skips links that already point here.

**Keep the checkout in place**, because installed files are symlinks. The installer
has no downloads, package installation or login-shell changes. Use `--dry-run` to
preview changes without creating directories or files.

The shared `.zshrc`, `.zprofile` and Starship destinations are also used by other
terminal setups. Installing this project replaces those destinations with backups;
it does not remove another terminal's configuration or project directory.

## Restore

The installer prints the exact backup directory and restore command. Backups live
under `${XDG_STATE_HOME:-$HOME/.local/state}/kitty-zsh/backups/`.

```sh
bash scripts/restore.sh /absolute/path/to/the/printed-backup-directory
```

Restore reinstates original files/symlinks and removes only this installation's
links. It refuses to overwrite files you replaced after installation. Applications
and fonts are separate installations and are not removed by config restore.

## Checks

```sh
bash -n install.sh
for script in scripts/*.sh; do bash -n "$script"; done
zsh -n zsh/.zshrc
zsh -n zsh/.zprofile
python3 -m unittest discover -s tests -v
bash scripts/validate-kitty.sh
```

Kitty validates its config using its own embedded Python; this does not open a GUI
or require a separate Python install. Python 3 is needed only for development tests.
The shell needs Zsh, while installers use Bash 3.2+ and ordinary system tools.
CI checks Ubuntu and macOS; actual Kali VM graphics and interactive behaviour
still require [desktop validation](docs/validation.md).

## Licence

[MIT](LICENSE) for this project's files. The bundled Rose Pine files retain their
own MIT notice. Tools, plugins and fonts keep their upstream licences. See
[upstream projects](docs/upstreams.md).
