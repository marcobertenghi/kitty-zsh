# Shared interactive setup for macOS and Linux; all enhancements are optional.
[[ -o interactive ]] || return 0

# PATH: keep inherited entries, prepend only directories that actually exist.
typeset -U path fpath
for _zsh_dir in /usr/local/sbin /usr/local/bin /opt/homebrew/sbin \
  /opt/homebrew/bin "$HOME/go/bin" "$HOME/.local/bin"; do
  [[ -d $_zsh_dir ]] && path=("$_zsh_dir" $path)
done
unset _zsh_dir

# History: SHARE_HISTORY already appends each command as it is entered.
HISTFILE=${ZDOTDIR:-$HOME}/.zsh_history
HISTSIZE=120000
SAVEHIST=100000
setopt EXTENDED_HISTORY HIST_EXPIRE_DUPS_FIRST HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE HIST_REDUCE_BLANKS HIST_VERIFY SHARE_HISTORY
unsetopt INC_APPEND_HISTORY INC_APPEND_HISTORY_TIME

# Navigation and editing.
setopt AUTO_CD AUTO_PUSHD PUSHD_IGNORE_DUPS PUSHD_SILENT
setopt INTERACTIVE_COMMENTS NO_BEEP EXTENDED_GLOB
WORDCHARS=${WORDCHARS//[\/\-.=]}

# Optional package completions; preserve the system's existing fpath.
_zsh_share_dirs=(
  "${HOMEBREW_PREFIX:-/opt/homebrew}/share"
  /opt/homebrew/share /usr/local/share /usr/share
)
for _zsh_dir in $_zsh_share_dirs; do
  for _zsh_completion_dir in "$_zsh_dir/zsh/site-functions" \
    "$_zsh_dir/zsh-completions" "$_zsh_dir/zsh-completions/site-functions"; do
    [[ -d $_zsh_completion_dir ]] && fpath+=("$_zsh_completion_dir")
  done
done
unset _zsh_dir _zsh_completion_dir

# Completion: full audit on first use, after editing this file, and daily.
# A separate stamp matters: compinit need not rewrite an unchanged dump.
_zsh_cache=${XDG_CACHE_HOME:-$HOME/.cache}/zsh
_zsh_dump=${ZDOTDIR:-$HOME}/.zcompdump-$ZSH_VERSION
_zsh_check=$_zsh_dump.checked
_zsh_rc=${(%):-%x}
[[ -d $_zsh_cache ]] || command mkdir -p -- "$_zsh_cache" 2>/dev/null

autoload -Uz compinit
if [[ ! -w ${_zsh_dump:h} ]]; then
  compinit -i -D
elif [[ ! -s $_zsh_dump || ! -f $_zsh_check || $_zsh_rc -nt $_zsh_check ||
        -n $_zsh_check(#qN.mh+24) ]]; then
  # -i excludes insecure completion directories rather than prompting at startup.
  if compinit -i -d "$_zsh_dump"; then
    : > "$_zsh_check"
  fi
else
  compinit -C -d "$_zsh_dump"
fi
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' list-colors "${(@s.:.)${LS_COLORS:-di=34:ln=36:ex=32}}"
zstyle ':completion:*' group-name ''
zstyle ':completion:*:descriptions' format '%F{yellow}%d%f'
if [[ -w $_zsh_cache ]]; then
  zstyle ':completion:*' use-cache on
  zstyle ':completion:*' cache-path "$_zsh_cache/zcompcache"
fi
unset _zsh_cache _zsh_dump _zsh_check _zsh_rc

# Keybindings: Emacs editing with prefix history search on the arrow keys.
bindkey -e
autoload -Uz up-line-or-beginning-search down-line-or-beginning-search
zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search
bindkey '^[[A' up-line-or-beginning-search
bindkey '^[[B' down-line-or-beginning-search
bindkey '^[OA' up-line-or-beginning-search
bindkey '^[OB' down-line-or-beginning-search
bindkey '^[[1;5C' forward-word
bindkey '^[[1;5D' backward-word
bindkey '^[[3~' delete-char
autoload -Uz edit-command-line
zle -N edit-command-line
bindkey '^X^E' edit-command-line

# Prompt: useful even on a minimal machine without Starship or Nerd Fonts.
if [[ $TERM == dumb ]]; then
  PROMPT='%n@%m %~ %# '
elif (( $+commands[starship] )); then
  # Starship does not consistently follow XDG_CONFIG_HOME across platforms.
  if [[ -z ${STARSHIP_CONFIG:-} ]]; then
    export STARSHIP_CONFIG=${XDG_CONFIG_HOME:-$HOME/.config}/starship.toml
  fi
  eval "$(starship init zsh)"
else
  PROMPT='%(!.%F{red}%n%f .)%F{cyan}%~%f %# '
  if [[ -n ${SSH_CONNECTION:-}${SSH_CLIENT:-}${SSH_TTY:-} ]]; then
    PROMPT='%(!.%F{red}.%F{yellow})%n@%m%f %F{cyan}%~%f %# '
  fi
fi
(( $+commands[zoxide] )) && eval "$(zoxide init zsh)"

# Debian-family packages may name these executables fdfind and batcat.
_zsh_fd=''
_zsh_bat=''
if (( $+commands[fd] )); then
  _zsh_fd=fd
elif (( $+commands[fdfind] )); then
  _zsh_fd=fdfind
  alias fd=fdfind
fi
if (( $+commands[bat] )); then
  _zsh_bat=bat
elif (( $+commands[batcat] )); then
  _zsh_bat=batcat
  alias bat=batcat
fi

# fzf: installed scripts update with the package, so no generated cache is needed.
if (( $+commands[fzf] )); then
  export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --bind ctrl-/:toggle-preview'
  if [[ -n $_zsh_fd ]]; then
    export FZF_DEFAULT_COMMAND="$_zsh_fd --type f --hidden --follow --exclude .git"
    export FZF_CTRL_T_COMMAND=$FZF_DEFAULT_COMMAND
    export FZF_ALT_C_COMMAND="$_zsh_fd --type d --hidden --follow --exclude .git"
  elif (( $+commands[rg] )); then
    export FZF_DEFAULT_COMMAND="rg --files --hidden --follow --glob '!.git'"
    export FZF_CTRL_T_COMMAND=$FZF_DEFAULT_COMMAND
  fi
  if [[ -n $_zsh_bat ]]; then
    export FZF_CTRL_T_OPTS="--preview '$_zsh_bat -n --paging=never --color=always --line-range :300 -- {}'"
  else
    export FZF_CTRL_T_OPTS="--preview 'head -n 300 -- {}'"
  fi
  if (( $+commands[eza] )); then
    export FZF_ALT_C_OPTS="--preview 'eza --tree --level=2 --git-ignore --color=always -- {}'"
  else
    export FZF_ALT_C_OPTS="--preview 'ls -Ap -- {}'"
  fi

  _zsh_fzf_loaded=0
  for _zsh_dir in "${commands[fzf]:A:h:h}/shell" \
    "${commands[fzf]:A:h:h}/share/fzf" \
    /usr/local/share/fzf /usr/share/fzf /usr/share/doc/fzf/examples; do
    if [[ -r $_zsh_dir/completion.zsh && -r $_zsh_dir/key-bindings.zsh ]]; then
      source "$_zsh_dir/completion.zsh"
      source "$_zsh_dir/key-bindings.zsh"
      _zsh_fzf_loaded=1
      break
    fi
  done
  # Some binary-only installs provide integration through --zsh (fzf 0.48+).
  if (( ! _zsh_fzf_loaded )); then
    if _zsh_fzf_init=$(fzf --zsh 2>/dev/null) && [[ -n $_zsh_fzf_init ]]; then
      eval "$_zsh_fzf_init"
    fi
  fi
  unset _zsh_dir _zsh_fzf_loaded _zsh_fzf_init
fi

# Aliases and man pages: retain working system defaults without extra packages.
if (( $+commands[eza] )); then
  # The bare flag also supports older eza versions. Only emit links to a terminal,
  # so pipelines and redirected listings stay plain text on those versions too.
  _kitty_zsh_eza() {
    if [[ -t 1 ]]; then
      command eza --hyperlink "$@"
    else
      command eza "$@"
    fi
  }
  # Retain eza's argument completion when its packaged completion is available.
  if (( ${+_comps[eza]} )); then
    compdef "${_comps[eza]}" _kitty_zsh_eza
  fi
  alias ls='_kitty_zsh_eza --group-directories-first'
  alias ll='_kitty_zsh_eza -lah --group-directories-first --git'
  alias la='_kitty_zsh_eza -a --group-directories-first'
  alias lt='_kitty_zsh_eza --tree --level=2 --git-ignore'
else
  alias ll='ls -lah'
  alias la='ls -A'
  (( $+commands[tree] )) && alias lt='tree -L 2'
fi
alias reload='exec zsh'
if [[ -n $_zsh_bat ]] && (( $+commands[col] )); then
  export MANPAGER="sh -c 'col -bx | $_zsh_bat --language=man --paging=always --plain'"
  export MANROFFOPT='-c'
fi
unset _zsh_fd _zsh_bat

# Personal or work-specific overrides go here; keep this file out of Git.
ZSH_AUTOSUGGEST_STRATEGY=(history completion)
ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=80
[[ -r ${ZDOTDIR:-$HOME}/.zshrc.local ]] && source "${ZDOTDIR:-$HOME}/.zshrc.local"

# Kitty's documented manual integration survives `exec zsh` and nested shells.
# kitty.conf disables automatic injection; the packaged script guards duplicates.
# Override KITTY_ZSH_INTEGRATION in .zshrc.local, or set it to disabled to opt out.
if [[ -n ${KITTY_INSTALLATION_DIR:-} &&
      -r $KITTY_INSTALLATION_DIR/shell-integration/zsh/kitty-integration &&
      ${KITTY_ZSH_INTEGRATION:-enabled} != disabled ]] && (( ! $+_ksi_state )); then
  export KITTY_SHELL_INTEGRATION=${KITTY_SHELL_INTEGRATION:-${KITTY_ZSH_INTEGRATION:-enabled}}
  autoload -Uz -- "$KITTY_INSTALLATION_DIR/shell-integration/zsh/kitty-integration"
  kitty-integration
  unfunction kitty-integration
fi

# Optional plugins: load once from the first matching package location.
for _zsh_dir in $_zsh_share_dirs; do
  if [[ -r $_zsh_dir/zsh-autosuggestions/zsh-autosuggestions.zsh ]]; then
    source "$_zsh_dir/zsh-autosuggestions/zsh-autosuggestions.zsh"
    bindkey '^ ' autosuggest-accept
    break
  fi
done

# Syntax highlighting must be the last sourced plugin, after custom widgets.
for _zsh_dir in $_zsh_share_dirs; do
  if [[ -r $_zsh_dir/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
    source "$_zsh_dir/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
    break
  fi
done
unset _zsh_dir _zsh_share_dirs
