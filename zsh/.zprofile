# Login environment. Homebrew is optional on both macOS and Linux.
for _zsh_brew in "${commands[brew]:-}" /opt/homebrew/bin/brew \
  /usr/local/bin/brew /home/linuxbrew/.linuxbrew/bin/brew "$HOME/.linuxbrew/bin/brew"; do
  if [[ -x $_zsh_brew ]]; then
    eval "$("$_zsh_brew" shellenv)"
    break
  fi
done
unset _zsh_brew

typeset -U path
[[ -d $HOME/.local/bin ]] && path=("$HOME/.local/bin" $path)
if [[ -d '/Applications/Sublime Text.app/Contents/SharedSupport/bin' ]]; then
  path=('/Applications/Sublime Text.app/Contents/SharedSupport/bin' $path)
fi
