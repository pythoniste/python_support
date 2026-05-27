# 01 — Pourquoi `curses`

## 1.1 Le terminal a deux personnalités

Par défaut, un terminal fonctionne en **mode ligne** (en anglais
*cooked*, « cuit ») :

- les caractères tapés au clavier sont **bufferisés** par le système ;
- ils ne sont transmis au programme qu'à la **validation** par Entrée ;
- chaque touche tapée est immédiatement **renvoyée à l'écran**
  (c'est l'*écho*) ;
- la touche Backspace efface le caractère précédent **dans le tampon
  système**, avant que le programme ne voie quoi que ce soit.

C'est confortable pour `input()` : on récupère une ligne complète,
déjà corrigée par l'utilisateur, prête à l'emploi.

Mais ce mode interdit beaucoup de choses :

- réagir à **chaque touche** (impossible de capter une flèche avant
  Entrée) ;
- dessiner à un endroit précis de l'écran (`print` ne sait qu'aller à
  la ligne suivante) ;
- afficher un menu interactif, un éditeur, un jeu de plate-forme texte.

Pour cela, il faut basculer le terminal en **mode brut** (en anglais
*raw*) :

- chaque touche est transmise **immédiatement** au programme ;
- **aucun écho** automatique ;
- les touches spéciales (flèches, F1, etc.) deviennent lisibles ;
- c'est au programme de **redessiner** ce qu'il veut voir affiché.

## 1.2 `curses` : la bonne abstraction

Basculer manuellement le terminal en mode brut est fastidieux et
non portable (il faudrait appeler `termios.tcsetattr` avec des
constantes obscures). Heureusement, le module standard `curses` fait
tout cela pour nous, et plus encore.

`curses` permet de :

- basculer en mode brut **et** revenir au mode normal proprement ;
- découper l'écran en **fenêtres** indépendantes (objets `window`) ;
- écrire du texte à des **coordonnées** précises ;
- lire des touches y compris les **touches spéciales** ;
- gérer **couleurs**, gras, inversion vidéo, soulignement... ;
- détecter le **redimensionnement** de la fenêtre du terminal.

C'est la même bibliothèque que celle utilisée par `vim`, `htop`,
`mc`, `mutt`, `nano`, et la plupart des outils interactifs en
ligne de commande.

## 1.3 Disponibilité

| Système        | Disponibilité de `curses`                          |
|----------------|----------------------------------------------------|
| Linux          | Inclus dans la bibliothèque standard               |
| macOS          | Inclus dans la bibliothèque standard               |
| Windows natif  | **Non inclus** : `pip install windows-curses`      |
| Windows + WSL  | Inclus (c'est un Linux)                            |

Sous Windows natif, on installe `windows-curses` qui fournit l'API
attendue par-dessus la console Windows. **Ce paquet ne fait pas
partie de la stdlib** ; il sort du cadre strict du cours. La
solution recommandée est WSL.

## 1.4 Un vrai terminal, sinon rien

`curses` envoie au terminal des **séquences d'échappement** ANSI
(des suites de caractères de contrôle) pour déplacer le curseur,
colorer du texte, effacer une zone, etc. Pour que cela fonctionne,
il faut un terminal qui **interprète** ces séquences. C'est le cas
de :

- xterm, gnome-terminal, konsole, terminator, alacritty, kitty
  (Linux) ;
- Terminal.app, iTerm2 (macOS) ;
- Windows Terminal, ConEmu, WSL (Windows).

Mais ce n'est **pas** le cas de :

- la fenêtre « Run » de PyCharm (par défaut) ;
- IDLE ;
- les sorties capturées par les notebooks Jupyter ;
- une redirection vers un fichier (`python3 prog.py > sortie.txt`).

Dans ces environnements, soit le script plante, soit la sortie est
illisible. **Toujours** exécuter les démos de ce chapitre dans un
vrai terminal externe.

## À retenir

- Mode ligne (*cooked*) : ligne par ligne, écho automatique — c'est
  `print`/`input`.
- Mode brut (*raw*) : touche par touche, sans écho — c'est `curses`.
- `curses` est dans la stdlib sous Linux et macOS.
- Sous Windows : `pip install windows-curses` (hors stdlib) ou WSL.
- Toujours dans un vrai terminal externe, jamais dans la console
  d'un IDE qui n'émule pas l'ANSI.

## Démo

Exécuter `01_demo_intro.py` dans un terminal. Le programme prend
le contrôle de l'écran, affiche un message, attend une touche, puis
restaure le terminal.
