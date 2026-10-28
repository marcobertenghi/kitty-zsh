"""Check the observed media event and Penelope's F12 bytes with Kitty itself."""
import os
from pathlib import Path
import shutil
import subprocess
import unittest

REPO = Path(__file__).resolve().parents[1]
KITTY = os.environ.get('KITTY_BIN') or shutil.which('kitty')
if not KITTY and Path('/Applications/kitty.app/Contents/MacOS/kitty').is_file():
    KITTY = '/Applications/kitty.app/Contents/MacOS/kitty'


def verify_function_keys():
    from types import SimpleNamespace
    from kitty.config import load_config
    from kitty.fast_data_types import encode_key_for_tty, set_options
    from kitty.options.utils import parse_shortcut
    from kitty.window import Window

    bad = []
    opts = load_config(str(REPO / 'kitty/kitty.conf'), accumulate_bad_lines=bad)
    assert not bad, bad
    set_options(opts)
    keymap = opts.keyboard_modes[''].keymap
    incoming = parse_shortcut('media_track_previous')
    assert incoming.key == 57436
    assert encode_key_for_tty(key=incoming.key, action=1, key_encoding_flags=0,
                              cursor_key_mode=False) == '\x1b[57436u'
    definition = keymap[incoming][-1].definition.split()
    assert definition[0] == 'send_key'

    class Sink:
        encoded_key = Window.encoded_key

        def __init__(self, flags):
            self.data = bytearray()
            self.screen = SimpleNamespace(current_key_encoding_flags=lambda: flags,
                                          cursor_key_mode=False)

        def write_to_child(self, data):
            self.data.extend(data)

        def scroll_end(self):
            pass

    sink = Sink(0)
    assert Window.send_key(sink, *definition[1:]) is False
    assert sink.data == b'\x1b[24~', sink.data  # Penelope's default PTY detach sequence.
    # Enhanced applications still receive key-release reports when requested.
    enhanced = Sink(3)
    Window.send_key(enhanced, *definition[1:])
    assert b':3' in enhanced.data, enhanced.data
    assert enhanced.data != sink.data
    # The fallback must not intercept genuine unmodified function keys.
    assert all(parse_shortcut(f'f{i}') not in keymap for i in range(1, 13))
    print('OK      CSI 57436 u maps to F12/ESC[24~; negotiated reporting and F1-F12 passthrough preserved')


class FunctionKeyTests(unittest.TestCase):
    @unittest.skipUnless(KITTY, 'Kitty not available')
    def test_reported_media_event_becomes_penelope_f12(self):
        script = f'import runpy; ns=runpy.run_path({str(Path(__file__).resolve())!r}); ns["verify_function_keys"]()'
        proc = subprocess.run([KITTY, '+runpy', script], text=True, capture_output=True, timeout=30)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == '__main__':
    unittest.main()
