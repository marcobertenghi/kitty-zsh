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

With eza installed, `ls`, `ll`, `la` and `lt` emit clickable filename links when
their output goes to a terminal. Kitty renders these OSC 8 hyperlinks; the listing
tool creates them. Use **Ctrl-Shift-left-click** to open a linked file or directory
with the configured URL handler (normally the desktop's associated application).
A plain left-click also opens links when no selection is active. Opening a linked
directory does not run `cd` in your current shell. Right-click still copies selected
text, and Ctrl-Shift-V pastes it.

The small eza wrapper adds `--hyperlink` only when stdout is a terminal, supporting
older eza releases as well. Piped/redirected listings stay free of hyperlink escape
sequences. Without eza, the existing system-ls fallback remains available. No new
package is required beyond the existing eza dependency. See
[eza's hyperlink option](https://eza.rocks/) and
[Kitty hyperlink support](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.allow_hyperlinks).

Local checks with eza 0.23.5 verified terminal hyperlinks, filenames with spaces,
and plain piped output. That version leaves `#` unescaped in filename URLs, which
can be interpreted as a URL fragment; open such files by their normal path if a
click fails. Actual desktop opening still depends on your Kali file associations.

## Kitty controls

| Shortcut | Behaviour |
| --- | --- |
| Right-click with text selected | Copy selected text to the system clipboard |
| Ctrl-Shift-C | Copy selected text (Kitty default) |
| Ctrl-Shift-V | Paste from the system clipboard (Kitty default) |
| Ctrl-Shift-left-click a link | Open a linked filename or URL (Kitty default) |
| Ctrl-Shift-Enter | Add a pane in Tall, in the current directory |
| Ctrl-Alt-Enter | Side-by-side split (returns to splits layout first) |
| Ctrl-Alt-Shift-Enter | Top/bottom split (returns to splits layout first) |
| Ctrl-Alt-Arrow | Focus the pane in that direction |
| Ctrl-Alt-Shift-Arrow | Rearrange the active pane toward its neighbour |
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
| Ctrl-Shift-L | Cycle tall, splits, stack and grid layouts |
| Ctrl-Shift-F5 | Reload Kitty config |
| Ctrl-Shift-F6 | Show Kitty's current configuration/debug information |
| Ctrl-Shift-H | Browse scrollback in a pager (Kitty default) |

The default is **Tall**, with one full-height main pane occupying about 60% of
the width and the remaining panes stacked in the right-hand 40%. Starting with
one terminal, press **Ctrl-Shift-Enter twice** to get three panes:

```text
                 60%                  40%
┌────────────────────────────┬───────────────────┐
│                            │         B         │
│             A              ├───────────────────┤
│                            │         C         │
└────────────────────────────┴───────────────────┘
```

The first press adds B beside A; the second adds C below B. It takes two new-pane
actions to go from one pane to three. The shortcut returns to Tall and appends new
panes at the end, so it also works after zooming a pane or focusing A. A fourth
pane would add another row on the right; there is no hard three-pane limit.

**Focus** and **rearrangement** are different actions:

- **Ctrl-Alt-Arrow** moves the input focus toward a neighbouring pane. For example,
  Left from B or C focuses A; Up/Down switches between the two right-hand panes.
  Right from A selects a right-hand neighbour using Kitty's focus history. Nothing
  is physically moved or restarted.
- **Ctrl-Alt-Shift-Arrow** moves the active terminal into a neighbouring position.
  In Tall this swaps pane positions: Left from B exchanges it with A, promoting B
  to the large main slot. Its shell and running command stay attached to it.
- **Ctrl-Shift-1/2/3** selects a numbered pane directly. Numbers refer to pane
  order, which can change when you rearrange panes.
- **Ctrl-Shift-Z** shows the active pane alone (Stack); press again to restore
  the previous layout. The other panes continue running.

Tabs contain these panes. **Ctrl-Alt-1 through 9** selects a tab, while
**Ctrl-Shift-Left/Right** selects the previous/next tab. Neither changes the Linux
desktop workspace.

For manual placement, Ctrl-Alt-Enter creates a side-by-side split and
Ctrl-Alt-Shift-Enter creates a top/bottom split of the focused pane. Both switch to
Splits first. Grid arranges panes automatically. See
[Kitty's Tall and Splits layouts](https://sw.kovidgoyal.net/kitty/layouts/).

Kali Xfce binds some of the same Ctrl-Alt shortcuts globally, including arrows and
tab-number combinations. Keep the Kitty bindings and remap the desktop actions
using [the Xfce instructions](kali-desktop.md#kitty-panes-and-xfce-workspaces).
The desktop otherwise intercepts these keys before Kitty receives them. On macOS,
Alt means Option; a VM host can also intercept shortcuts.

Native tabs/splits require no tmux dependency. Defaults not listed here remain
unchanged. See [Kitty's overview](https://sw.kovidgoyal.net/kitty/overview/).

### Startup window size

Each new Kitty OS window starts at **3262×1635 pixels**, 85% of the intended
3838×1923 Kali desktop's width and height. `remember_window_size no` and
`remember_window_position no` stop Kitty from restoring its previous geometry.
Initial placement remains with Xfce, which already centers new terminals in this
setup. Open a new OS window or restart Kitty to check the startup size; existing
windows are not resized by a config reload.

Kitty's native startup dimensions accept pixels or character cells, not screen
percentages. These values are fixed; for a different desktop resolution, override
`initial_window_width` and `initial_window_height` in `kitty.local.conf`.
See [Kitty's startup size settings](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.initial_window_width).

There is no added centering shortcut, kitten or window-control dependency.
Repositioning an already moved window is a separate window-manager action. Xfce's
standard shortcut list has no dedicated center-window action; a small optional
function can be considered later if wanted.

### Function keys and Penelope

Unmodified F1-F12 are available to terminal applications. Penelope's default
PTY detach key is F12, encoded as `ESC [ 24 ~`; under `cat -v` this appears as
`^[[24~`. A function key is an escape sequence, so seeing it printed by `cat -v`
is expected. Seeing a fragment typed at a shell prompt does not identify the key.

The reported `^[[57436u` identifies **Previous Track**, not F12, even with Kitty's
legacy keyboard mode active. This points to keyboard Fn mode or host/VM translation.
The shared config translates that specific incoming event with
`map media_track_previous send_key f12`. It sends a real F12 through Kitty's
application-aware encoder rather than forcing escape bytes for every program.
Consequently, Previous Track received by Kitty now acts as F12 too. Set
`map media_track_previous no_op` in the private include to restore native media-key
handling. This workaround does not repair the keyboard's entire function row.

For the whole row, compare F12 with Fn/Globe+F12. If only the latter produces
`^[[24~`, enable standard function keys in the host keyboard settings or use the
keyboard's Fn-lock setting. The exact control depends on the keyboard and VM;
do not assume Fn-Esc is supported. If a key never reaches Kitty, inspect the host,
VM and Xfce shortcuts. To identify the incoming events, run `kitten show-key -m kitty`
(older installations: `kitty +kitten show_key`), press the affected keys, then exit
the diagnostic. Do not guess mappings for the rest of the row from F12 alone.

After updating the checkout, reload Kitty with Ctrl-Shift-F5 and run `cat -v`.
Press the reported F12 key, then Enter: expect `^[[24~`; Ctrl-C exits. Test Penelope's
detach key in an authorized local lab session as well. The project does not change
Penelope's configuration. See [Kitty's key definitions](https://sw.kovidgoyal.net/kitty/keyboard-protocol/#functional-key-definitions),
[send_key](https://sw.kovidgoyal.net/kitty/actions/#action-send_key), and
[Penelope's defaults](https://github.com/brightio/penelope/blob/main/penelope.py).

Select text with the left mouse button, then right-click to copy it. Paste with
Ctrl-Shift-V in Kitty, Ctrl-V in ordinary Linux GUI apps, or Cmd-V on macOS.
This uses the system clipboard, so the copied text remains available after you
clear the highlight. Shift-left-click still extends a selection. Mouse-aware
terminal programs retain their right-click handling; use Ctrl-Shift-C to copy a
Kitty selection there. See [Kitty's copy/paste actions](https://sw.kovidgoyal.net/kitty/actions/#copy-paste).

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
font_size 18
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

Kitty defaults to an 18 pt JetBrainsMono Nerd Font, 95% background opacity, 12 pt
padding in split panes (8 pt in a single pane), aligned full pane outlines and
rounded powerline tabs with numbers. Override
`font_size` in the private include to adjust text size, or set
`background_opacity 1.0` for maximum contrast. These settings and the small border
watcher add no packages, background services or shell startup work.

The OS titlebar and outer window decorations are hidden with
`hide_window_decorations yes`, the Kitty equivalent of Ghostty's hidden titlebar
and disabled window decorations. `window_padding_width 12` sets both horizontal
and vertical padding in split panes; `single_window_padding_width 8` keeps the
single-pane inset compact. Internal pane outlines and the tab bar stay visible
for navigation. Restart Kitty after changing decorations; reloading alone is not
reliable for this setting. The exact appearance depends on the OS/window manager.
To restore the normal frame, set `hide_window_decorations no` in
`kitty.local.conf` and restart. See
[Kitty's decoration settings](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.hide_window_decorations).

`draw_minimal_borders no` keeps a complete outline around each pane.
`window_margin_width 4` contributes 4 pt from each neighbor, making an 8 pt gap
between outlines; `single_window_margin_width 0` avoids extra space in a single pane.
Kitty rounds terminal contents to whole character cells. Its native full outlines
exclude leftover space, which can stagger the edges of a full-height pane and a
stack of shorter panes. `aligned_borders.py` includes that leftover space inside
each outline, leaving the configured gap outside. It changes the border drawing
view, without resizing terminal contents or changing the 60/40 Tall workflow.
`placement_strategy top-left` keeps the content starts aligned too.

The helper uses Kitty's [watcher mechanism](https://sw.kovidgoyal.net/kitty/launch/#watching-launched-windows)
and embedded Python, with no separate Python installation or background process.
It adapts Kitty's internal border drawing functions, which are not a stable public
API; an incompatible geometry API falls back to native outlines. To disable the
correction, set `env KITTY_ZSH_ALIGNED_BORDERS=0` in `kitty.local.conf` and restart.
For shared separators instead, also set `window_margin_width 0` and
`draw_minimal_borders yes`. See [Kitty's spacing settings](https://sw.kovidgoyal.net/kitty/conf/#opt-kitty.window_margin_width).

After updating an existing checkout, run `bash install.sh` once to link the new
watcher file, then restart Kitty. Existing links are preserved. Later spacing
changes can be reloaded with Ctrl-Shift-F5.

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
