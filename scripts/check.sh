#!/usr/bin/env bash
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
strict=0
case ${1:-} in --strict) strict=1 ;; --help|-h) printf 'Usage: %s [--strict]\n' "$0"; exit 0 ;; '') ;; *) exit 2 ;; esac
missing=0
for group in 'zsh' 'starship' 'zoxide' 'fzf' 'fd fdfind' 'rg' 'bat batcat' 'eza' 'col' 'less'; do
  found=''
  # Intentional splitting: each group lists alternative executable names.
  for executable in $group; do
    if command -v "$executable" >/dev/null; then found=$(command -v "$executable"); break; fi
  done
  if [[ -n $found ]]; then printf 'OK      %-12s %s\n' "$group" "$found"; else printf 'MISSING %s\n' "$group"; missing=1; fi
done
kitty=${KITTY_BIN:-$(command -v kitty || true)}
if [[ -z $kitty && -x /Applications/kitty.app/Contents/MacOS/kitty ]]; then kitty=/Applications/kitty.app/Contents/MacOS/kitty; fi
if [[ -n $kitty ]]; then
  KITTY_BIN="$kitty" bash "$repo/scripts/validate-kitty.sh"
else
  printf 'MISSING Kitty (not required to use this Zsh config)\n'; missing=1
fi
for plugin in zsh-autosuggestions zsh-syntax-highlighting; do
  found=''
  for base in "${HOMEBREW_PREFIX:-/opt/homebrew}/share" /opt/homebrew/share /usr/local/share /usr/share; do
    if [[ -r $base/$plugin/$plugin.zsh ]]; then found="$base/$plugin/$plugin.zsh"; break; fi
  done
  if [[ -n $found ]]; then printf 'OK      %s\n' "$plugin"; else printf 'MISSING %s\n' "$plugin"; missing=1; fi
done
if command -v zsh >/dev/null; then
  zsh -n "$repo/zsh/.zshrc"
  zsh -n "$repo/zsh/.zprofile"
  printf 'OK      Zsh syntax\n'
fi
if command -v fc-match >/dev/null; then
  family=$(fc-match -f '%{family}\n' 'JetBrainsMono Nerd Font')
  case $family in *'JetBrainsMono Nerd Font'*) printf 'OK      Nerd Font\n' ;; *) printf 'MISSING Nerd Font (fontconfig matched %s)\n' "$family"; missing=1 ;; esac
else
  printf 'INFO    Check the font manually with: kitty +list-fonts\n'
fi
printf 'Startup and interactive keybindings should also be checked in Kitty.\n'
if [[ $strict -eq 1 && $missing -ne 0 ]]; then exit 1; fi
