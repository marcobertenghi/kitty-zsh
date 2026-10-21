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

`bat` and `fd` are the commands to type on both platforms. If only Debian's
`batcat` / `fdfind` executables are installed, Zsh supplies fallback aliases; native
`bat` / `fd` executables take precedence. These aliases apply to interactive Zsh;
scripts should detect the installed executable, as the fzf/man integration does.

fd/fdfind is used for fzf file and directory searches when available. With no fd,
ripgrep supplies the file list; fzf retains its default directory search. With
neither, fzf uses its own defaults. Optional-tool shortcuts appear only when those
tools are installed. There are no aliases replacing rg, grep or find.

```sh
rg 'pattern' .             # Search file contents; honours ignore files
rg --files                # List searchable files
fd config                 # Find matching filenames
bat README.md             # Highlighted file viewer, also on Debian/Kali
```

## Kitty controls

| Shortcut | Behaviour |
| --- | --- |
| Ctrl-Shift-Enter | New pane in the current directory |
| Ctrl-Alt-Enter | Side-by-side split (returns to splits layout first) |
| Ctrl-Alt-Shift-Enter | Top/bottom split (returns to splits layout first) |
| Ctrl-Alt-Arrow | Focus the pane in that direction |
| Ctrl-Alt-Shift-Arrow | Move the pane in that direction (layout dependent) |
| Ctrl-Shift-1 through 9 | Jump directly to a pane (Kitty defaults) |
| Ctrl-Shift-F7 | Visually select a pane (Kitty default) |
| Ctrl-Shift-Z | Focus current pane / restore previous layout |
| Ctrl-Shift-R | Interactive pane resizing (Kitty default; follow onscreen keys) |
| Ctrl-Alt-R | Reset pane sizes |
| Ctrl-Shift-T | New tab in the current directory |
| Ctrl-Alt-1 through 9 | Jump directly to a numbered tab |
| Ctrl-Shift-Right / Left | Next / previous tab (Kitty defaults) |
| Ctrl-Shift-W | Close current pane (Kitty default) |
| Ctrl-Shift-] / Ctrl-Shift-[ | Next / previous pane |
| Ctrl-Shift-L | Cycle splits, stack, tall and grid layouts |
| Ctrl-Shift-F5 | Reload Kitty config |
| Ctrl-Shift-F6 | Show Kitty's current configuration/debug information |
| Ctrl-Shift-H | Browse scrollback in a pager (Kitty default) |

Start with Ctrl-Alt-Enter, then Ctrl-Alt-Shift-Enter for a three-pane workspace.
Use Ctrl-Alt-Arrows to move between panes, and Ctrl-Shift-Z to give the active
pane the whole tab temporarily. Stack shows one pane at a time; tall arranges a
main pane beside a column; grid tiles panes automatically. Ctrl-Shift-Enter adds
a pane using the current layout. Explicit split shortcuts switch to splits first
because `vsplit` / `hsplit` placement only applies in that layout.

On macOS, Alt means Option. Desktop or VM shortcuts may intercept key combinations;
remap them in the private include if needed.

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
font_size 16
background_opacity 1.0
```

Colour preferences come from the automatic theme files and may override colour
settings in kitty.conf or the private include. All three files use Moon, keeping
it selected in dark, light and no-preference modes. To opt into appearance switching,
choose separate light/dark/no-preference themes with `kitten themes`. The files are
symlinked to this checkout; saving a theme can therefore change tracked files.

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

Kitty defaults to a 14 pt JetBrainsMono Nerd Font, 95% background opacity, 8 pt
padding, visible pane outlines and rounded powerline tabs with numbers. Set
`font_size 16` in the private include if you prefer larger text, or
`background_opacity 1.0` for maximum contrast. These are built-in Kitty features
and add no packages, background services or shell startup work.

The OS titlebar and outer window decorations are hidden with
`hide_window_decorations yes`, the Kitty equivalent of Ghostty's hidden titlebar
and disabled window decorations. `window_padding_width 8` sets both horizontal
and vertical padding to 8 pt. Internal pane outlines and the tab bar stay visible
for navigation. Restart Kitty after changing decorations; reloading alone is not
reliable for this setting. The exact appearance depends on the OS/window manager.
To restore the normal frame, set `hide_window_decorations no` in
`kitty.local.conf` and restart. See
[Kitty's decoration settings](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.hide_window_decorations).

Kitty uses Rosé Pine Moon in every desktop appearance mode. The Starship bar has
matching Moon backgrounds; the success/error and SSH/root indicators use ANSI
colours from the active theme. In the bundled Kitty themes ANSI green is Pine and
red is Love.

The cursor and its short native trail use Moon Gold (`#f6c177`) in every
appearance mode. A dark cursor text colour keeps block-cursor text readable.
The trail uses a 3 ms trigger delay, 100–250 ms decay and a two-cell movement
threshold to avoid animating each small typing movement. Cursor trails require
Kitty 0.37+ and use its built-in renderer, with no plugins or custom shaders.
Set `cursor_trail 0` in `kitty.local.conf` to disable the animation, or increase
`cursor_trail_decay` for a longer trail. Reload with Ctrl-Shift-F5.
See [Kitty's cursor settings](https://sw.kovidgoyal.net/kitty/conf/#cursor-trail).

For large repositories, use `starship timings` to check Git-status rendering before
disabling features. Startup, prompt rendering and terminal rendering are distinct
measurements. VM graphics results should be checked in the actual guest.
