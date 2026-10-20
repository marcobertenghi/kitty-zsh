#!/usr/bin/env bash
# Parse using Kitty's embedded Python and its real config parser; no GUI required.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
[[ $# -le 1 ]] || { printf 'Usage: %s [KITTY_CONFIG_DIRECTORY]\n' "$0" >&2; exit 2; }
kitty=${KITTY_BIN:-$(command -v kitty || true)}
if [[ -z $kitty && -x /Applications/kitty.app/Contents/MacOS/kitty ]]; then kitty=/Applications/kitty.app/Contents/MacOS/kitty; fi
[[ -n $kitty ]] || { printf 'Install Kitty, or set KITTY_BIN to its executable.\n' >&2; exit 1; }
KITTY_ZSH_VALIDATE_DIR=${1:-$repo/kitty} "$kitty" +runpy '
import os, sys
from pathlib import Path
from kitty.config import load_config
root = Path(os.environ["KITTY_ZSH_VALIDATE_DIR"])
failed = False
for name in ("kitty.conf", "dark-theme.auto.conf", "light-theme.auto.conf", "no-preference-theme.auto.conf"):
    path = root / name
    if not path.is_file():
        print("Missing configuration: " + str(path), file=sys.stderr)
        failed = True
        continue
    bad = []
    load_config(str(path), accumulate_bad_lines=bad)
    for problem in bad:
        print(str(path) + ": " + str(problem), file=sys.stderr)
    failed = failed or bool(bad)
if failed:
    raise SystemExit(1)
print("OK      Kitty configuration and all three theme files")
'
