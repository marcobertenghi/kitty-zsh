# Daily use and customisation

## Shell tools

| Shortcut / command | Behaviour |
| --- | --- |
| Ctrl-R | fzf history search |
| Ctrl-T | fzf file selection |
| Alt-C | fzf directory selection |
| Ctrl-/ inside fzf | Toggle preview |
| Up / Down after a prefix | Search matching history |
| Ctrl-Space or Right | Accept an autosuggestion |
| Ctrl-X Ctrl-E | Edit the command line using your configured editor |
| Ctrl-Left / Ctrl-Right | Move by word when passed through by the desktop |
| `z name`, `zi` | zoxide navigation / interactive selection |
| `ll`, `la`, `lt` | Detailed, hidden and shallow-tree listings |
| `dirs -v`, `cd -2` | Browse the directory stack |
| `reload` | Replace the shell with a fresh Zsh |

fd/fdfind is used for fzf file and directory searches when available. With no fd,
ripgrep supplies the file list; fzf retains its default directory search. With
neither, fzf uses its own defaults. Optional-tool shortcuts appear only when those
tools are installed. There are no aliases replacing rg, grep or find.

```sh
rg 'pattern' .             # Search file contents; honours ignore files
rg --files                # List searchable files
fd config                 # Find matching filenames
# Debian's executable may instead be named fdfind:
fdfind config
```

## Kitty controls

| Shortcut | Behaviour |
| --- | --- |
| Ctrl-Shift-Enter | New pane in the current directory |
| Ctrl-Alt-Enter | Vertical split |
| Ctrl-Alt-Shift-Enter | Horizontal split |
| Ctrl-Shift-T | New tab in the current directory |
| Ctrl-Shift-] / Ctrl-Shift-[ | Next / previous pane |
| Ctrl-Shift-L | Cycle splits, stack and tall layouts |
| Ctrl-Shift-F5 | Reload Kitty config |
| Ctrl-Shift-F6 | Show Kitty's current configuration/debug information |
| Ctrl-Shift-H | Browse scrollback in a pager (Kitty default) |

Native tabs/splits require no tmux dependency. Defaults not listed here remain
unchanged. See [Kitty's overview](https://sw.kovidgoyal.net/kitty/overview/).

## Private overrides

Create private copies only if they do not exist:

```sh
cp -n zsh/.zshrc.local.example "${ZDOTDIR:-$HOME}/.zshrc.local"
cp -n kitty/kitty.local.conf.example "${KITTY_CONFIG_DIRECTORY:-${XDG_CONFIG_HOME:-$HOME/.config}/kitty}/kitty.local.conf"
```

The installer neither creates nor overwrites these private files. Both are ignored
by Git. `.zshrc.local` loads after tool defaults, before Kitty integration and the
two optional plugins. Syntax highlighting is sourced last.

```zsh
# ~/.zshrc.local
export EDITOR=nvim
ZSH_AUTOSUGGEST_STRATEGY=(history)
ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=120
# To customise Kitty integration flags:
KITTY_ZSH_INTEGRATION='enabled no-sudo'
# Or: KITTY_ZSH_INTEGRATION=disabled
```

The editor must already be installed. Configure additional completion fpath entries
before compinit, for example in `.zprofile` for login shells or `.zshenv` for all
shells. Manual integration follows Kitty's documented approach: automatic injection
is disabled in kitty.conf, and Zsh loads Kitty's installed script. The script's
state guard prevents double initialization. Other shells can configure their own
integration separately.

```text
# ~/.config/kitty/kitty.local.conf
font_size 14
background_opacity 1.0
```

Colour preferences come from the automatic theme files and may override colour
settings in kitty.conf or the private include. Edit the theme files to change the
palette. No-preference defaults to dark; point that file at the Dawn palette if
your desktop reports no preference for its light appearance.

## History and caches

History is shared across tabs/splits. A leading space excludes a command from saved
Zsh history, not from other logs or process arguments. HISTFILE lives under
`${ZDOTDIR:-$HOME}`; it is not part of this repository.

Completion uses a version-specific dump and separate audit timestamp there. Cold
starts, a changed .zshrc and stamps older than a day trigger an audit; other starts
reuse the dump. Completion result caches use `${XDG_CACHE_HOME:-$HOME/.cache}/zsh`.

After adding or removing completion packages, refresh the stamp:

```zsh
rm -f -- "${ZDOTDIR:-$HOME}/.zcompdump-$ZSH_VERSION.checked"
reload
```

fzf uses installed integration scripts or its modern `--zsh` output without a
persistent generated cache. Missing plugins/tools do not prevent shell startup.

## Style and performance

Kitty selects Rose Pine / Dawn when the desktop reports dark / light preference
and supports automatic themes. The Starship bar has explicit Rose Pine backgrounds;
the success/error and SSH/root indicators use ANSI colours from the active theme.
In the bundled Kitty themes ANSI green is Pine and red is Love, with variant-specific
hex values.

For large repositories, use `starship timings` to check Git-status rendering before
disabling features. Startup, prompt rendering and terminal rendering are distinct
measurements. VM graphics results should be checked in the actual guest.
