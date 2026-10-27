"""Border alignment checks, including Kitty's real Tall layout when available."""
from collections import namedtuple
from pathlib import Path
import importlib.util
import os
import shutil
import subprocess
import unittest

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('aligned_borders', REPO / 'kitty/aligned_borders.py')
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)
Edges = namedtuple('Edges', 'left top right bottom')


class Group:
    def __init__(self, index=1, padding=12, border=1, margin=4):
        self.id = self.active_window_id = index
        self.padding, self.border, self.margin = padding, border, margin
        self.geometry = None

    def effective_padding(self, edge):
        return self.padding

    def effective_border(self):
        return self.border

    def decoration(self, edge, border_mult=1, **kwargs):
        return self.padding + self.border * border_mult + self.margin

    def set_geometry(self, geometry):
        self.geometry = geometry


class Windows:
    def __init__(self, count, scale):
        self.groups = [Group(i + 1, 12 * scale, scale, 4 * scale) for i in range(count)]
        self.num_groups = count

    def iter_all_layoutable_groups(self):
        return iter(self.groups)


def verify_native_geometry():
    from kitty import borders
    from kitty.config import load_config
    from kitty.fast_data_types import Region, set_options
    from kitty.layout.base import lgd, set_layout_options
    from kitty.layout.tall import Tall

    opts = load_config(str(REPO / 'kitty/kitty.conf'))
    set_options(opts)
    set_layout_options(opts)
    assert not opts.draw_minimal_borders
    assert all(x == 4 for x in opts.window_margin_width)
    HELPER._install()

    def bounds(rects):
        return (min(r.left for r in rects), min(r.top for r in rects),
                max(r.right for r in rects), max(r.bottom for r in rects))

    checked = staggered = 0
    for count in (2, 3, 4):
        for width, height in ((1280, 720), (1441, 901), (1920, 1080), (1919, 1079)):
            for cw, ch in ((11, 23), (15, 30), (21, 43)):
                for scale in (1, 2):
                    for alignment in (-1, 0):
                        lgd.central = Region((0, 0, width - 1, height - 1, width, height))
                        lgd.cell_width, lgd.cell_height = cw, ch
                        lgd.alignment_x = lgd.alignment_y = alignment
                        windows = Windows(count, scale)
                        Tall(0, 0, 'bias=60;full_size=1').do_layout(windows)
                        outlined, plain = [], []
                        for group in windows.groups:
                            geometry = group.geometry
                            rects = []
                            borders.add_borders(rects, borders.BorderColor.active, group)
                            outlined.append(bounds(rects))
                            rects = []
                            borders.add_borders.__wrapped__(rects, borders.BorderColor.active, group)
                            plain.append(bounds(rects))
                            assert group.geometry is geometry  # Drawing never resizes terminal contents.
                        main, upper, lower = outlined[0], outlined[1], outlined[-1]
                        assert main[1] == upper[1] == 4 * scale, outlined
                        assert main[3] == lower[3] == height - 4 * scale, outlined
                        assert upper[0] - main[2] == 8 * scale, outlined
                        assert all(r[0] == upper[0] and r[2] == width - 4 * scale for r in outlined[1:]), outlined
                        for previous, following in zip(outlined[1:], outlined[2:]):
                            assert following[1] - previous[3] == 8 * scale, outlined
                        staggered += plain[0][1] != plain[1][1] or plain[0][3] != plain[-1][3]
                        checked += 1
    assert staggered > 0, 'The checks must reproduce the original misalignment'
    print(f'OK      {checked} native Tall outline cases; reproduced {staggered} staggered originals')


class AlignedBorderTests(unittest.TestCase):
    def test_remainders_extend_outline_but_preserve_intentional_margin(self):
        group = Group()
        geometry = namedtuple('Geometry', 'spaces')(Edges(17, 20, 24, 31))
        group.geometry = geometry
        view = HELPER._AlignedGroup(group)
        self.assertEqual([view.effective_padding(e) for e in Edges._fields], [12, 15, 19, 26])
        self.assertEqual(group.padding, 12)
        self.assertIs(view.geometry, geometry)

    def test_constrained_geometry_does_not_shrink_padding(self):
        group = Group()
        group.geometry = namedtuple('Geometry', 'spaces')(Edges(0, 0, 0, 0))
        self.assertEqual(HELPER._AlignedGroup(group).effective_padding('left'), 12)

    def test_installation_is_idempotent_and_disable_switch_keeps_native_group(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        fake = SimpleNamespace(add_borders=lambda rects, color, group: rects.append(group))
        options = SimpleNamespace(env={})
        with patch.dict('sys.modules', {
            'kitty': SimpleNamespace(borders=fake),
            'kitty.fast_data_types': SimpleNamespace(get_options=lambda: options),
        }):
            self.assertTrue(HELPER._install())
            self.assertFalse(HELPER._install())
            group = Group()
            group.geometry = SimpleNamespace(spaces=Edges(17, 17, 17, 17))
            rects = []
            fake.add_borders(rects, 1, group)
            self.assertIsInstance(rects[-1], HELPER._AlignedGroup)
            options.env['KITTY_ZSH_ALIGNED_BORDERS'] = '0'
            fake.add_borders(rects, 1, group)
            self.assertIs(rects[-1], group)

    def test_legacy_drawing_keeps_background_padding_unchanged(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        calls = []
        fake = SimpleNamespace(draw_edges=lambda *args, **kwargs: calls.append(args[3]))
        with patch.dict('sys.modules', {
            'kitty': SimpleNamespace(borders=fake),
            'kitty.fast_data_types': SimpleNamespace(get_options=lambda: SimpleNamespace(env={})),
        }):
            self.assertTrue(HELPER._install())
            group = Group()
            group.geometry = SimpleNamespace(spaces=Edges(17, 17, 17, 17))
            fake.draw_edges(1, 1, [], group, borders=False)
            self.assertIs(calls[-1], group)
            fake.draw_edges(1, 1, [], group, borders=True)
            self.assertIsInstance(calls[-1], HELPER._AlignedGroup)

    @unittest.skipUnless(os.environ.get('KITTY_BIN') or shutil.which('kitty'), 'Kitty not available')
    def test_native_tall_outlines_across_sizes_scales_and_cell_metrics(self):
        kitty = os.environ.get('KITTY_BIN') or shutil.which('kitty')
        script = f'import runpy; ns = runpy.run_path({str(Path(__file__).resolve())!r}); ns["verify_native_geometry"]()'
        result = subprocess.run([kitty, '+runpy', script], text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
