"""Include cell-grid remainders inside full pane outlines.

Loaded by Kitty's watcher API, using its embedded Python. Only the border drawing
view changes: terminal geometry, padding settings and layouts remain untouched.
Kitty's drawing functions are internal APIs; keep compatibility checks here and
fall back to native outlines if the required geometry is unavailable.
"""
from functools import wraps


class _AlignedGroup:
    def __init__(self, group):
        self.group = group

    def __getattr__(self, name):
        return getattr(self.group, name)

    def effective_padding(self, edge):
        # spaces includes margin + border + padding + cell-grid remainder.
        # decoration excludes the remainder, so leave intentional margins alone.
        extra = max(0, getattr(self.group.geometry.spaces, edge) - self.group.decoration(edge))
        return self.group.effective_padding(edge) + extra


def _drawing_group(group):
    from kitty.fast_data_types import get_options
    if get_options().env.get('KITTY_ZSH_ALIGNED_BORDERS') == '0':
        return group
    geometry = group.geometry
    if geometry is None or not hasattr(geometry, 'spaces') or not callable(getattr(group, 'decoration', None)):
        return group
    return _AlignedGroup(group)


def _install():
    from kitty import borders
    original = getattr(borders, 'add_borders', None)
    if callable(original):
        if getattr(original, '_kitty_zsh_aligned', False):
            return False

        @wraps(original)
        def aligned(rects, color, group, *args, **kwargs):
            return original(rects, color, _drawing_group(group), *args, **kwargs)

        aligned._kitty_zsh_aligned = True
        borders.add_borders = aligned
    else:
        # Kitty 0.37 used draw_edges for both padding and full borders.
        original = getattr(borders, 'draw_edges', None)
        if not callable(original) or getattr(original, '_kitty_zsh_aligned', False):
            return False

        @wraps(original)
        def aligned(os_id, tab_id, colors, group, borders=False):
            view = _drawing_group(group) if borders else group
            return original(os_id, tab_id, colors, view, borders=borders)

        aligned._kitty_zsh_aligned = True
        borders.draw_edges = aligned
    return True


def on_resize(boss, window, data):
    # Resize also fires on initial creation. Install once per Kitty process;
    # future draws calculate the remainder afresh, without relayout loops/timers.
    if _install():
        tab = window.tabref()
        if tab is not None:
            tab.relayout_borders()
