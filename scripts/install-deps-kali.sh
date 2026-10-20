#!/usr/bin/env bash
# Install from configured apt repositories only; do not add external repositories.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
case ${1:-} in
  --dry-run) dry_run=1 ;;
  --help|-h) printf 'Usage: %s [--dry-run]\nInstall available Kali/Debian apt dependencies.\n' "$0"; exit 0 ;;
  '') dry_run=0 ;;
  *) printf 'Unknown argument: %s\n' "$1" >&2; exit 2 ;;
esac
[[ $# -le 1 ]] || exit 2
if ! command -v apt-get >/dev/null || ! command -v apt-cache >/dev/null; then
  printf 'This helper requires apt (Kali/Debian).\n' >&2; exit 1
fi
run_apt() {
  if [[ $EUID -eq 0 ]]; then apt-get "$@"; else sudo apt-get "$@"; fi
}
if [[ $dry_run -eq 0 ]]; then run_apt update; fi
available=(); missing=()
while IFS= read -r package || [[ -n $package ]]; do
  [[ -n $package && $package != \#* ]] || continue
  candidate=$(LC_ALL=C apt-cache policy "$package" 2>/dev/null | awk '/Candidate:/ && !seen++ { print $2 }')
  if [[ -n $candidate && $candidate != '(none)' ]]; then
    available+=("$package")
  else
    missing+=("$package")
  fi
done < "$repo/dependencies/kali-apt.txt"
# Starship packaging varies by Kali snapshot and CPU architecture.
package=starship
candidate=$(LC_ALL=C apt-cache policy "$package" 2>/dev/null | awk '/Candidate:/ && !seen++ { print $2 }')
if [[ -n $candidate && $candidate != '(none)' ]]; then available+=("$package"); else missing+=("$package"); fi
if [[ ${#available[@]} -gt 0 ]]; then
  printf 'Apt packages: %s\n' "${available[*]}"
  if [[ $dry_run -eq 0 ]]; then run_apt install "${available[@]}"; fi
fi
if [[ ${#missing[@]} -gt 0 ]]; then
  printf '\nNo apt candidate: %s\n' "${missing[*]}"
  printf 'See docs/kali-linux.md for upstream/alternative installation steps.\n'
fi
[[ $dry_run -eq 0 ]] || printf 'Dry run: no apt update or installation performed.\n'
