#!/usr/bin/env bash
# Download only the selected Nerd Font release to the user's font directory.
set -euo pipefail
case ${1:-} in
  --help|-h) printf 'Usage: %s\nInstalls JetBrainsMono Nerd Font v3.5.1 for this user.\n' "$0"; exit 0 ;;
  '') ;;
  *) printf 'Unexpected argument.\n' >&2; exit 2 ;;
esac
if ! command -v curl >/dev/null || ! command -v tar >/dev/null; then
  printf 'Install curl, tar and xz support first.\n' >&2; exit 1
fi
case $(uname -s) in
  Darwin) font_dir="$HOME/Library/Fonts/JetBrainsMonoNerdFont" ;;
  Linux) font_dir="${XDG_DATA_HOME:-$HOME/.local/share}/fonts/JetBrainsMonoNerdFont" ;;
  *) printf 'Supported platforms: macOS and Linux.\n' >&2; exit 1 ;;
esac
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
curl --fail --location --proto '=https' --tlsv1.2 \
  https://github.com/ryanoasis/nerd-fonts/releases/download/v3.5.1/JetBrainsMono.tar.xz \
  --output "$tmp/JetBrainsMono.tar.xz"
# Digest published with the pinned upstream v3.5.1 release asset.
checksum=04d5e8f903693f9dd13e16f867e994834e681eb3c72c0d337a770dcda09010cf
if command -v sha256sum >/dev/null; then
  printf '%s  %s\n' "$checksum" "$tmp/JetBrainsMono.tar.xz" | sha256sum -c -
elif command -v shasum >/dev/null; then
  printf '%s  %s\n' "$checksum" "$tmp/JetBrainsMono.tar.xz" | shasum -a 256 -c -
else
  printf 'Install sha256sum or shasum to verify the font archive.\n' >&2; exit 1
fi
tar -xJf "$tmp/JetBrainsMono.tar.xz" -C "$tmp"
mkdir -p "$font_dir"
found=0
for font in "$tmp"/JetBrainsMonoNerdFont-*.ttf; do
  [[ -f $font ]] || continue
  install -m 644 "$font" "$font_dir/${font##*/}"
  found=1
done
[[ $found -eq 1 ]] || { printf 'No matching font files in archive.\n' >&2; exit 1; }
if command -v fc-cache >/dev/null; then fc-cache -f "$font_dir"; fi
printf 'Font installed in %s\nRestart Kitty to refresh its font list.\n' "$font_dir"
