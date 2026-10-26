# Rosé Pine Moon desktop for Kali Xfce

This is an optional, manual desktop setup for Kali's Xfce session. Run the commands
inside Kali, as your normal desktop user. The Kitty installer does not apply these
settings. The recommendations cover the desktop theme/wallpaper, one compact panel,
and an application launcher.

## Recommended combination

| Component | Selection |
| --- | --- |
| Applications and window frames | Rosé Pine Moon, from the GTK v2.2.0 release |
| Icons | Kali's existing Flat-Remix-Blue-Dark |
| Wallpaper | Block Wave Moon; Leafy Moon is the alternative |
| Panel | Existing Xfce panel, top, one row, 32 px, full width |
| Application buttons | Docklike Taskbar, with a gold active indicator |
| Launcher | Existing Xfce Application Finder on Super-Space |
| Interface font | Existing Sans font at 11 pt; adjust for display scaling |

These are design recommendations, not claims of measured performance. Theme files
and a static wallpaper do not add a background service. Docklike is a panel plugin;
Application Finder already belongs to Xfce.

## 1. Applications, frames and wallpaper

### Install the Moon theme

Source: [Rosé Pine GTK v2.2.0](https://github.com/rose-pine/gtk/releases/tag/v2.2.0).
The release archive contains `gtk3/rose-pine-moon-gtk/`, including `gtk-2.0`,
`gtk-3.0`, `gtk-3.20` and `xfwm4`. It therefore provides application styling and
Xfwm window decorations from the same download. No theme installer script is needed.

Download and install only the Moon variant:

```sh
mkdir -p "$HOME/Downloads/kali-moon" "$HOME/.themes"
curl -fL \
  https://github.com/rose-pine/gtk/releases/download/v2.2.0/gtk3.tar.gz \
  -o "$HOME/Downloads/kali-moon/gtk3-v2.2.0.tar.gz"
tar -xzf "$HOME/Downloads/kali-moon/gtk3-v2.2.0.tar.gz" \
  --exclude='*/._*' --strip-components=1 -C "$HOME/.themes" \
  gtk3/rose-pine-moon-gtk
```

The archive inspected on 22 October 2026 had SHA-256:
`3e790f6898b39f43b23fb4794217c5cc31b64060de951db6d37c4243452d0d93`.
You can inspect your download with
`sha256sum "$HOME/Downloads/kali-moon/gtk3-v2.2.0.tar.gz"`.

Record your current choices so they are easy to restore:

```sh
xfconf-query -c xsettings -p /Net/ThemeName
xfconf-query -c xsettings -p /Net/IconThemeName
xfconf-query -c xfwm4 -p /general/theme
```

Apply the theme to both Xfce settings channels:

```sh
xfconf-query -c xsettings -p /Net/ThemeName -s rose-pine-moon-gtk
xfconf-query -c xfwm4 -p /general/theme -s rose-pine-moon-gtk
```

Alternatively, open **Settings → Appearance → Style** and choose the Moon theme,
then do the same under **Settings → Window Manager → Style**. Depending on the
dialog, the display name may be `oomox-rose-pine-moon`, while the installed folder
and the command-line setting are `rose-pine-moon-gtk`.

Under **Appearance → Icons**, keep **Flat-Remix-Blue-Dark** initially. It preserves
Kali's existing icon selection without another icon download. Under **Fonts**, try
the existing Sans face at 11 pt. Keep JetBrainsMono Nerd Font for Kitty.

The archive also includes GTK2 styling. If older GTK2 apps report missing Murrine
or Clearlooks engines, install `gtk2-engines-murrine` and `gtk2-engines`; GTK3/Xfwm
styling does not require those engines. Applications with their own theme systems
may need separate settings, and this guide does not install global GTK4 CSS.

An optional alternative icon set is the
[official Moon icon archive](https://github.com/rose-pine/gtk/releases/download/v2.2.0/rose-pine-moon-icons.tar.gz)
(about 33 MB compressed). Its layout is `icons/rose-pine-moon-icons/`; extract
with one leading component removed into `~/.icons`. The directory name is
`rose-pine-moon-icons`, and its display name is `oomox-rose-pine-moon`. The default
recommendation above uses the icons already supplied by Kali.

### Wallpaper choices

Both choices come from the [Rosé Pine wallpaper collection](https://github.com/rose-pine/wallpapers).

| Wallpaper | Recommendation | Download |
| --- | --- | --- |
| Block Wave Moon | First choice: dark purple, restrained pixel pattern, scattered palette accents | [PNG](https://raw.githubusercontent.com/rose-pine/wallpapers/main/illustration/block-wave-moon.png) |
| Leafy Moon | Softer illustration: foliage at the edges and open space through the middle | [PNG](https://raw.githubusercontent.com/rose-pine/wallpapers/main/illustration/leafy-moon.png) |

Download either or both:

```sh
mkdir -p "$HOME/Pictures/Wallpapers/rose-pine"
curl -fL \
  https://raw.githubusercontent.com/rose-pine/wallpapers/main/illustration/block-wave-moon.png \
  -o "$HOME/Pictures/Wallpapers/rose-pine/block-wave-moon.png"
curl -fL \
  https://raw.githubusercontent.com/rose-pine/wallpapers/main/illustration/leafy-moon.png \
  -o "$HOME/Pictures/Wallpapers/rose-pine/leafy-moon.png"
```

Open **Settings → Desktop → Background**, select that folder, and choose
`block-wave-moon.png`. Use **Zoomed** to fill the display; use **Scaled** to keep
the entire image visible if your monitor's aspect ratio differs. Disable wallpaper
cycling for a consistent background. Under Desktop's **Icons** settings, hide
filesystem/removable-device icons if you want an uncluttered desktop.

## 2. One useful top panel

Install the additional panel plugin from Kali's repositories:

```sh
sudo apt update
sudo apt install xfce4-docklike-plugin
```

Before restructuring the panel, you can export the current layout with
[Xfce Panel Profiles](https://docs.xfce.org/apps/xfce4-panel-profiles/start) if it is
already installed. It is optional and does not need to stay running.

Right-click the existing panel and open **Panel → Panel Preferences**. Keep the
current VPN/network and tray items while arranging the panel.

| Setting | Recommended value |
| --- | --- |
| Mode / position | Horizontal, top edge |
| Row size / rows | 32 px / 1 row; increase to 36–40 px if needed for scaling |
| Length | Full width; 100% or the full monitor width, depending on Xfce version |
| Lock panel | Enabled after placing it |
| Automatically hide | Never, to keep connection state visible |
| Background | Solid colour `#2a273f` (Moon Surface) |
| Enter / leave opacity | 100% / 100%, keeping icons and text fully readable |

Suggested left-to-right order in **Items**:

```text
Menu | Workspaces | Docklike Taskbar | expanding separator | VPN/network | Tray | Clock
```

Add **Docklike Taskbar** first. Once it shows your running apps, remove the old
**Window Buttons** item to avoid duplicate taskbars. If you have a separate bottom
launcher panel, move its useful launchers to Docklike before removing that panel.

Launch Kitty, your browser, Burp, your notes app and Thunar, then right-click each
Docklike icon and pin it. The application must supply a desktop launcher to pin
reliably; package-installed applications normally do.

Use **Ctrl-right-click → Properties** on Docklike. Recommended settings:

- Icon size around 24 px in a 32 px panel.
- Window previews enabled.
- A simple line or dot active indicator.
- Custom active indicator colour `#f6c177` (Moon Gold), if offered by your version.
- Enable Super-number application switching if you want it; leave the standalone
  Super-key action off so it does not interfere with the application menu.
- If the middle-click behaviour is configurable, set it to do nothing: this avoids
  closing grouped windows during an engagement.

Docklike's optional Super-1, Super-2, etc. shortcuts select applications by their
position in the panel. They are distinct from Kitty's Ctrl-Alt-number tab shortcuts.
If a desktop shortcut already uses Super-number, resolve that conflict in Xfce's
keyboard settings first.

References: [Panel preferences](https://docs.xfce.org/xfce/xfce4-panel/preferences)
and [Docklike usage](https://docs.xfce.org/panel-plugins/xfce4-docklike-plugin/start).

## 6. A centred application launcher

Use Xfce's existing **Application Finder**. If it is missing, install
`xfce4-appfinder` from apt. Open it once from a terminal:

```sh
xfce4-appfinder
```

Open its **Preferences**, then set:

| Preference | Value |
| --- | --- |
| Always centre the window | Enabled |
| Hide category pane | Enabled |
| View items as icons | Disabled, for a compact list with application names |
| Item icon size | Normal, or around 24 px if a numeric choice is available |
| Sort recently used items first | Enabled |
| Keep running instance in the background | Disabled initially |

The launcher inherits the Moon GTK theme. Disabling the background instance reduces
idle memory use; you can enable it later if faster reopening matters more to you.

Open **Settings → Keyboard → Application Shortcuts → Add**:

```text
Command:  xfce4-appfinder
Shortcut: Super+Space
```

Super is normally the Windows-logo key. Use the command without `--collapsed` for
searching installed GUI applications. Type an application name, select a result,
and press Enter; Escape closes the launcher. If Super-Space is already assigned
to input-language switching, choose a different shortcut or reassign it deliberately.

Reference: [Application Finder preferences](https://docs.xfce.org/xfce/xfce4-appfinder/preferences).

## Kitty panes and Xfce workspaces

A Kitty **pane** is a terminal inside a tab. A **tab** contains panes. An Xfce
**workspace** is an entire desktop containing application windows. Kitty cannot
receive a shortcut that Xfce has already captured globally.

Kali's [shipped Xfce shortcuts](https://gitlab.com/kalilinux/packages/kali-themes/-/blob/kali/master/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml)
include Ctrl-Alt-Arrows for desktop workspace switching, Ctrl-Alt-Shift-Arrows for
moving whole application windows between workspaces, and Ctrl-Alt-1 through 9 for
selecting numbered workspaces. Those conflict with this project's Kitty controls.
Keep Kitty's controls and change the Xfce bindings.

Recommended pattern: **Ctrl-Alt** controls terminals; **Alt-Super** controls
desktop workspaces; adding **Shift** moves the terminal/window instead of focus.
Super is normally the Windows-logo key. This also leaves Super-number Docklike
shortcuts, Super-Space launching, and Kali's existing Ctrl-Super window shortcuts
available.

Inside your Kali Xfce session, open **Settings → Window Manager → Keyboard**.
Change the existing actions using these mappings (wording varies slightly by
Xfce version):

| Xfce action | Replace the old binding with |
| --- | --- |
| Left workspace | Alt-Super-Left |
| Right workspace | Alt-Super-Right |
| Upper workspace | Alt-Super-Up |
| Bottom/lower workspace | Alt-Super-Down |
| Move window to left workspace | Alt-Super-Shift-Left |
| Move window to right workspace | Alt-Super-Shift-Right |
| Move window to upper workspace | Alt-Super-Shift-Up |
| Move window to bottom/lower workspace | Alt-Super-Shift-Down |
| Workspace 1 through 9 | Alt-Super-1 through 9 |
| Move window to workspace 1 through 9 (optional) | Alt-Super-Shift-1 through 9 |

Double-click an action's current shortcut and press the new combination. Edit the
existing binding rather than merely adding another one: the old Ctrl-Alt binding
must be removed to free the key for Kitty. Change all of Workspace 1 through 9,
even if you currently use fewer desktops, since unused workspace shortcuts can
still grab keys. Reassign any additional custom global bindings using those same
Kitty combinations as well.

To inspect the bindings actually present in your session:

```sh
xfconf-query -c xfce4-keyboard-shortcuts -lv
```

`<Primary>` means Ctrl; `<Super>` is the Windows-logo key. Inspect the `/xfwm4/custom/`
entries for your active overrides; `/xfwm4/default/` entries are the supplied
defaults and may remain visible after a GUI change. Use the GUI's displayed active
shortcut and an actual keypress to confirm the result. If a proposed new binding
is already used by a custom action, reassign that action or choose a free variant.

After updating this project's configuration, reload Kitty with Ctrl-Shift-F5.
Open a fresh tab, or press Ctrl-Shift-Enter to switch the current tab to Tall and
add a pane. Starting with one pane, two presses produce a full-height main pane on
the left and two stacked panes on the right. Ctrl-Alt-Arrows should focus Kitty
panes; Alt-Super-Arrows should change the desktop workspace. Add Shift to move
the corresponding pane or application window.

The remapping is a one-time Xfce desktop setting. The terminal installer does not
change global shortcuts, and the Linux session cannot be configured from this
Mac checkout alone. For more detail, see
[Kitty controls](usage.md#kitty-controls) and
[Xfce keyboard settings](https://docs.xfce.org/xfce/xfwm4/keyboard_shortcuts).

## Check the result

Open Thunar and Application Finder, check that both use Moon, and verify that
window frames match. Check the panel at your actual VM/display scaling. Test
Docklike pinning/previews, your VPN indicator, and Super-Space. Reopen applications
that have kept their previous theme; logging out and in can refresh the entire
session.

To undo the theme, select your previous choices in Appearance and Window Manager,
or restore the theme names recorded above with `xfconf-query`. Panel Profiles can
restore an exported panel layout. All desktop changes in this guide are separate
from the terminal configuration installer.

The release archive layout and named wallpaper previews were inspected on
22 October 2026. The finished desktop has not been tested in the user's Kali VM.
