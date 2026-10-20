#!/usr/bin/env bash
# Restore only links created by a successful install; refuse to overwrite edits.
set -euo pipefail
if [[ $# -ne 1 || ${1:-} == --help || ${1:-} == -h ]]; then
  printf 'Usage: %s BACKUP_DIRECTORY\n' "$0"
  [[ ${1:-} == --help || ${1:-} == -h ]] && exit 0
  exit 2
fi
backup=$1
[[ -f $backup/manifest.tsv && -f $backup/status ]] || { printf 'Not an installer backup: %s\n' "$backup" >&2; exit 1; }
status=$(cat "$backup/status")
[[ $status != restored ]] || { printf 'This backup has already been restored.\n'; exit 0; }
[[ $status == active ]] || { printf 'Backup is not active: %s\n' "$status" >&2; exit 1; }
keys=(); targets=(); originals=()
while IFS=$'\t' read -r key target source original extra; do
  case $key in zshrc|zprofile|starship|kitty|kitty-dark|kitty-light|kitty-default) ;; *) printf 'Invalid backup entry.\n' >&2; exit 1 ;; esac
  [[ $target == /* && $source == /* && -z $extra && ( $original == 0 || $original == 1 ) ]] || { printf 'Invalid manifest.\n' >&2; exit 1; }
  if [[ -e $target || -L $target ]]; then
    [[ -L $target && $(readlink "$target") == "$source" ]] || {
      printf 'Refusing to overwrite a changed file: %s\nMove it aside, then retry.\n' "$target" >&2; exit 1;
    }
  fi
  if [[ $original == 1 && ! -e $backup/$key && ! -L $backup/$key ]]; then
    printf 'Missing original: %s/%s\n' "$backup" "$key" >&2; exit 1
  fi
  keys+=("$key"); targets+=("$target"); originals+=("$original")
done < "$backup/manifest.tsv"
[[ ${#keys[@]} -gt 0 ]] || { printf 'Empty manifest.\n' >&2; exit 1; }
# Preflight every entry above before changing any destination.
for i in "${!keys[@]}"; do
  if [[ -L ${targets[$i]} ]]; then rm -- "${targets[$i]}"; fi
  if [[ ${originals[$i]} == 1 ]]; then
    mkdir -p "$(dirname -- "${targets[$i]}")"
    mv -- "$backup/${keys[$i]}" "${targets[$i]}"
  fi
  printf 'Restored: %s\n' "${targets[$i]}"
done
printf 'restored\n' > "$backup/status"
printf 'Open a new shell and reload Kitty configuration.\n'
