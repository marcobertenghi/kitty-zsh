# Upstream projects and attribution

Applications, shell plugins and fonts are not vendored; their licences apply to
those separate installations.

| Component | Upstream |
| --- | --- |
| Kitty | [Official documentation](https://sw.kovidgoyal.net/kitty/) |
| Zsh | [zsh.org](https://www.zsh.org/) |
| Starship | [starship.rs](https://starship.rs/) |
| zoxide | [ajeetdsouza/zoxide](https://github.com/ajeetdsouza/zoxide) |
| fzf | [junegunn/fzf](https://github.com/junegunn/fzf) |
| fd | [sharkdp/fd](https://github.com/sharkdp/fd) |
| ripgrep | [BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) |
| bat | [sharkdp/bat](https://github.com/sharkdp/bat) |
| eza | [eza-community/eza](https://github.com/eza-community/eza) |
| zsh-autosuggestions | [zsh-users/zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) |
| zsh-syntax-highlighting | [zsh-users/zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) |
| Nerd Fonts | [ryanoasis/nerd-fonts](https://github.com/ryanoasis/nerd-fonts) |
| JetBrains Mono | [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono) |

## Bundled colour files

The three `kitty/*.auto.conf` files are copied from
[Rosé Pine for Kitty](https://github.com/rose-pine/kitty), retrieved 20 October 2026.
All three use `dist/rose-pine-moon.conf` so Moon stays selected regardless of the
desktop's appearance preference. Author metadata is preserved. Their MIT licence and
copyright notice are in [ROSE-PINE-LICENSE](../kitty/ROSE-PINE-LICENSE).

The Starship bar retains the existing segmented arrangement, with the Rose Pine
palette and portable context indicators. This project's own files are covered by
[its MIT licence](../LICENSE).

## Integration and configuration references

- [Kitty config](https://sw.kovidgoyal.net/kitty/conf/)
- [Manual shell integration](https://sw.kovidgoyal.net/kitty/shell-integration/#manual-shell-integration)
- [Automatic light/dark themes](https://sw.kovidgoyal.net/kitty/kittens/themes/)
- [SSH kitten](https://sw.kovidgoyal.net/kitty/kittens/ssh/)

Kitty's shell integration code is loaded from the installed application; it is not
copied into the runtime project. Development validation uses Kitty's real parser.
