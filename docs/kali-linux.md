# Install on Kali Linux

The intended setup is Kali in a VM or on a desktop, with Kitty installed from
Kali's own repositories. No Ubuntu PPA, AppImage or source build is needed when
that package is available. [Kali's Kitty package history](https://pkg.kali.org/pkg/kitty/news/).

Run commands from your normal user account. The package helper uses sudo for apt;
the config installer should be run without sudo.

## 1. Get the project

Copy the folder to a permanent location, or clone your published repository:

```sh
cd ~/Projects/kitty-zsh
```

The installed files will link to this checkout. Moving or deleting it breaks those
links. No GitHub URL is hardcoded because publication is a separate step.

## 2. Install Kitty and the shell tools

```sh
bash scripts/install-deps-kali.sh --dry-run
bash scripts/install-deps-kali.sh
```

The dry run inspects current apt candidates without updating or installing.
The real run refreshes package metadata and installs available dependencies; apt
asks for confirmation. Missing packages are reported explicitly. It adds no
repositories and runs no downloaded shell scripts.

Equivalent package set, when all packages have candidates on your image:

```sh
sudo apt update
sudo apt install kitty zsh git curl ca-certificates tar xz-utils fontconfig \
  less man-db bsdextrautils ncurses-bin fd-find ripgrep fzf bat eza zoxide \
  zsh-autosuggestions zsh-syntax-highlighting
```

Starship is checked separately and installed through apt if available. Package
availability can vary by Kali snapshot, architecture and work-managed repositories.
`col` is provided by `bsdextrautils`. Both Debian-style names `fdfind` and `batcat`
are detected automatically. [fd packaging](https://github.com/sharkdp/fd#installation),
[bat packaging](https://github.com/sharkdp/bat#installation).

Check key tools after installation:

```sh
kitty --version
fzf --version
rg --version
command -v fd || command -v fdfind
command -v bat || command -v batcat
```

### Starship if apt has no candidate

Download and inspect the [official Starship installer](https://starship.rs/guide/),
then install into your own account:

```sh
mkdir -p "$HOME/.local/bin"
tool_tmp=$(mktemp -d)
curl --fail --location https://starship.rs/install.sh -o "$tool_tmp/starship-install.sh"
less "$tool_tmp/starship-install.sh"
# Press q, then:
sh "$tool_tmp/starship-install.sh" --bin-dir "$HOME/.local/bin"
rm -rf -- "$tool_tmp"
export PATH="$HOME/.local/bin:$PATH"
starship --version
```

This project already initializes Starship; do not append a second init line.
If your work environment restricts external downloads, use its approved package
or retain the built-in Zsh prompt until Starship is available.

For other missing optional packages, consult the relevant
[upstream installation documentation](upstreams.md). No Rust, Node, Go or PHP
toolchain is needed to run this setup.

## 3. Install the font

```sh
bash scripts/install-font.sh
fc-match 'JetBrainsMono Nerd Font'
```

The helper downloads the roughly 7 MB JetBrainsMono archive from upstream
[Nerd Fonts v3.5.1](https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.5.1), verifies
its pinned SHA-256, and installs only the selected font family under your user
font directory. It refreshes fontconfig and does not execute remote shell code.
A desktop font manager is an alternative.

## 4. Install the configuration

```sh
bash install.sh --dry-run
bash install.sh
bash scripts/check.sh --strict
kitty
```

Keep the backup path printed by the installer. It respects `ZDOTDIR`,
`XDG_CONFIG_HOME`, `XDG_STATE_HOME` and `KITTY_CONFIG_DIRECTORY`. Existing
`STARSHIP_CONFIG` overrides are respected; clear one if you want the installed
Starship file to be selected instead.

Kitty explicitly launches `zsh -l`, so no `chsh` step is required. The Zsh files
also work in other terminals; Kitty integration is activated only when its
installed shell-integration resources are available.

## 5. Try the features

| Shortcut / command | Purpose |
| --- | --- |
| Ctrl-Shift-Enter | New pane in the current directory |
| Ctrl-Alt-Enter | Vertical split |
| Ctrl-Alt-Shift-Enter | Horizontal split |
| Ctrl-Shift-T | New tab in the current directory |
| Ctrl-Shift-] / Ctrl-Shift-[ | Next / previous pane (Kitty defaults) |
| Ctrl-Shift-L | Cycle split, stack and tall layouts |
| Ctrl-R | Fuzzy history search |
| Ctrl-T | Select files; bat preview where available |
| Alt-C | Select a directory |
| `rg 'pattern' .` | Search file contents, respecting ignore files |
| `fd name` or `fdfind name` | Find matching filenames |
| `ll`, `lt` | Detailed listing and shallow tree |
| `z name`, `zi` | zoxide navigation |
| `reload` | Fresh Zsh session with Kitty integration |

Use [private overrides](usage.md#private-overrides) for shortcuts intercepted by
the VM host or desktop. Do not repeatedly source `.zshrc`; use `reload`.

## VM and appearance notes

Kitty uses GPU rendering. VM graphics support and guest tools affect the experience;
verify scrolling and resizing in your actual VM. Start with the hypervisor's
supported graphics configuration and current guest tools. Avoid forcing latency
or rendering settings without measurements.

The dark theme is Rose Pine and light mode is Dawn. Automatic mode changes require
Kitty 0.38+ and a desktop that reports its appearance preference. With no preference
or older Kitty, the configured fallback is dark. The bundled theme files need no
network download at startup.

For an opaque window, put `background_opacity 1.0` in your private
`kitty.local.conf`. Use `kitty +list-fonts` and `fc-match` to diagnose missing icons.

## SSH

Inside Kitty, `kitty +kitten ssh user@host` enables Kitty's remote integration and
terminfo handling. It is opt-in; the project does not replace the ordinary ssh
command or connect to hosts. [Kitty SSH documentation](https://sw.kovidgoyal.net/kitty/kittens/ssh/).
Do not globally override TERM in `.zshrc`.

If you only need a terminal into the VM, you can also run Kitty on the host and
SSH into Kali. Install the shell tools/configs on Kali; the font is rendered on
the host in that arrangement.

## Updates and rollback

Use apt to update native packages. Once the project has a remote, `git pull` updates
linked configs; open a new tab and reload Kitty config with Ctrl-Shift-F5.
Re-run `install.sh` if an update adds more installed files.

To undo the config installation:

```sh
bash scripts/restore.sh /absolute/path/to/the/printed-backup-directory
```

Restore preserves history/private overrides and does not uninstall applications.
See [validation notes](validation.md) for what was checked locally and what still
needs an actual Kali VM session.
