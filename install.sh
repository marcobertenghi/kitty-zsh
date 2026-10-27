#!/usr/bin/env bash
# Link shared shell configs and Kitty settings, preserving replaced files.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
dry_run=0
case ${1:-} in
  --dry-run) dry_run=1 ;;
  --help|-h)
    printf 'Usage: %s [--dry-run]\nInstall user configs with backups. Run without sudo.\n' "$0"
    exit 0 ;;
  '') ;;
  *) printf 'Unknown option: %s\n' "$1" >&2; exit 2 ;;
esac
[[ $# -le 1 ]] || { printf 'Too many arguments.\n' >&2; exit 2; }
[[ -z ${SUDO_USER:-} ]] || { printf 'Run install.sh without sudo to target your own account.\n' >&2; exit 1; }
config_home=${XDG_CONFIG_HOME:-$HOME/.config}
state_home=${XDG_STATE_HOME:-$HOME/.local/state}
zdotdir=${ZDOTDIR:-$HOME}
case $(uname -s) in
  Darwin|Linux) ;;
  *) printf 'Supported platforms: macOS and Linux.\n' >&2; exit 1 ;;
esac
kitty_dir=${KITTY_CONFIG_DIRECTORY:-$config_home/kitty}
keys=(zshrc zprofile starship kitty kitty-dark kitty-light kitty-default kitty-borders)
sources=("$repo/zsh/.zshrc" "$repo/zsh/.zprofile" "$repo/starship/starship.toml"
  "$repo/kitty/kitty.conf" "$repo/kitty/dark-theme.auto.conf"
  "$repo/kitty/light-theme.auto.conf" "$repo/kitty/no-preference-theme.auto.conf"
  "$repo/kitty/aligned_borders.py")
targets=("$zdotdir/.zshrc" "$zdotdir/.zprofile" "$config_home/starship.toml"
  "$kitty_dir/kitty.conf" "$kitty_dir/dark-theme.auto.conf"
  "$kitty_dir/light-theme.auto.conf" "$kitty_dir/no-preference-theme.auto.conf"
  "$kitty_dir/aligned_borders.py")
changes=()
for value in "$repo" "$HOME" "$config_home" "$state_home" "$zdotdir" "$kitty_dir"; do
  [[ $value == /* && $value != *$'\n'* && $value != *$'\t'* ]] || {
    printf 'Paths must be absolute and contain no tabs or newlines: %s\n' "$value" >&2; exit 1;
  }
done
for i in "${!sources[@]}"; do
  [[ -f ${sources[$i]} && -r ${sources[$i]} ]] || { printf 'Missing source: %s\n' "${sources[$i]}" >&2; exit 1; }
  if [[ -d ${targets[$i]} && ! -L ${targets[$i]} ]]; then
    printf 'Expected a config file, found a directory: %s\n' "${targets[$i]}" >&2; exit 1
  fi
  if [[ -L ${targets[$i]} && $(readlink "${targets[$i]}") == "${sources[$i]}" ]]; then
    printf 'Already linked: %s\n' "${targets[$i]}"
  else
    changes+=("$i")
    printf 'Link: %s -> %s\n' "${targets[$i]}" "${sources[$i]}"
  fi
done
if [[ ${#changes[@]} -eq 0 ]]; then
  printf 'Everything is already installed.\n'; exit 0
fi
if [[ $dry_run -eq 1 ]]; then
  printf 'Dry run: no files or directories changed.\n'; exit 0
fi
umask 077
mkdir -p "$state_home/kitty-zsh/backups"
backup=$(mktemp -d "$state_home/kitty-zsh/backups/$(date -u +%Y%m%dT%H%M%SZ).XXXXXX")
saved=(); linked=()
for i in "${!keys[@]}"; do saved[i]=0; linked[i]=0; done
rollback() {
  trap - ERR INT TERM
  set +e
  for ((j=${#keys[@]}-1; j>=0; j--)); do
    if [[ ${linked[$j]} == 1 && -L ${targets[$j]} && $(readlink "${targets[$j]}") == "${sources[$j]}" ]]; then
      rm -- "${targets[$j]}"
    fi
    if [[ ${saved[$j]} == 1 && ! -e ${targets[$j]} && ! -L ${targets[$j]} ]]; then
      mv -- "$backup/${keys[$j]}" "${targets[$j]}"
    fi
  done
  printf 'rolled-back\n' > "$backup/status"
  printf 'Installation failed; rollback attempted. Backup directory: %s\n' "$backup" >&2
}
trap 'rollback; exit 1' ERR INT TERM
: > "$backup/manifest.tsv"
for i in "${changes[@]}"; do
  mkdir -p "$(dirname -- "${targets[$i]}")"
  if [[ -e ${targets[$i]} || -L ${targets[$i]} ]]; then
    mv -- "${targets[$i]}" "$backup/${keys[$i]}"
    saved[i]=1
  fi
  ln -s -- "${sources[$i]}" "${targets[$i]}"
  linked[i]=1
  printf '%s\t%s\t%s\t%s\n' "${keys[$i]}" "${targets[$i]}" "${sources[$i]}" "${saved[$i]}" >> "$backup/manifest.tsv"
done
printf 'active\n' > "$backup/status"
trap - ERR INT TERM
printf '\nInstalled. Backups: %s\n' "$backup"
printf 'Restore with: bash %q %q\n' "$repo/scripts/restore.sh" "$backup"
printf 'Keep this repository in place; the installed files are symlinks.\n'
printf 'Restart Kitty to load the configuration and border watcher.\n'
