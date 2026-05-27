# 03 — Couleurs et attributs

## 3.1 Le modèle « paires de couleurs »

`curses` ne raisonne pas en termes de couleur unique mais en
**paires** : une couleur de **premier plan** (le texte) et une
couleur de **fond**. Chaque paire est identifiée par un **numéro
entier** strictement positif que l'on choisit soi-même.

Le rituel est toujours le même :

1. activer les couleurs avec `curses.start_color()` (`wrapper`
   l'appelle déjà pour nous dans la plupart des cas) ;
2. déclarer chaque paire avec
   `curses.init_pair(numero, premier_plan, fond)` ;
3. récupérer l'attribut correspondant avec `curses.color_pair(numero)` ;
4. passer cet attribut en **quatrième argument** d'`addstr`.

## 3.2 Les couleurs disponibles

Huit couleurs standard, garanties sur tout terminal couleur :

| Constante           | Couleur   |
|---------------------|-----------|
| `curses.COLOR_BLACK`   | Noir   |
| `curses.COLOR_RED`     | Rouge  |
| `curses.COLOR_GREEN`   | Vert   |
| `curses.COLOR_YELLOW`  | Jaune  |
| `curses.COLOR_BLUE`    | Bleu   |
| `curses.COLOR_MAGENTA` | Magenta|
| `curses.COLOR_CYAN`    | Cyan   |
| `curses.COLOR_WHITE`   | Blanc  |

Certains terminaux modernes supportent 256 couleurs ou plus, mais
ces huit constantes sont le **plus petit dénominateur commun** : on
s'y limite pour rester portable.

## 3.3 Un exemple complet

```python
import curses


def main(stdscr):
    # 1. Activer la couleur (souvent déjà fait par wrapper).
    curses.start_color()

    # 2. Déclarer deux paires.
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)

    # 3. Récupérer les attributs.
    rouge_sur_noir = curses.color_pair(1)
    noir_sur_jaune = curses.color_pair(2)

    # 4. Les utiliser dans addstr.
    stdscr.addstr(0, 0, "Texte rouge sur fond noir", rouge_sur_noir)
    stdscr.addstr(2, 0, "Texte noir sur fond jaune", noir_sur_jaune)
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
```

## 3.4 Les attributs

En plus des couleurs, `curses` propose des **attributs de style**
qu'on peut combiner avec une couleur via l'opérateur `|` (OU
binaire) :

| Constante           | Effet                          |
|---------------------|--------------------------------|
| `curses.A_NORMAL`   | Style normal (par défaut)      |
| `curses.A_BOLD`     | Gras                           |
| `curses.A_UNDERLINE`| Souligné                       |
| `curses.A_REVERSE`  | Vidéo inverse (premier plan et fond échangés) |
| `curses.A_BLINK`    | Clignotant (souvent ignoré)    |
| `curses.A_DIM`      | Atténué                        |

Combinaison typique :

```python
attr = curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE
stdscr.addstr(5, 5, "Rouge gras souligné", attr)
```

`A_REVERSE` est particulièrement utile pour signaler l'**élément
sélectionné** dans un menu, sans avoir à définir une paire de
couleurs dédiée :

```python
stdscr.addstr(y, x, "Item sélectionné", curses.A_REVERSE)
```

## 3.5 Pièges courants

- **Oublier `init_pair`** : si la paire 1 n'a jamais été déclarée,
  `color_pair(1)` ne plantera pas mais n'affichera aucune couleur.
- **Numéro de paire à 0** : la paire 0 est **réservée** (blanc sur
  noir, non modifiable). Toujours commencer à 1.
- **Confondre couleur et paire** : `COLOR_RED` n'est **pas** un
  attribut prêt à l'emploi pour `addstr`. Il faut passer par
  `init_pair` puis `color_pair`.
- **Terminal monochrome** : `curses.has_colors()` répond `False`. On
  peut le tester avant de définir des paires pour avoir un repli
  propre.

## À retenir

- Une **paire** = une couleur de premier plan + une couleur de fond.
- Workflow : `start_color` -> `init_pair(n, fg, bg)` ->
  `color_pair(n)` -> 4e argument d'`addstr`.
- Huit couleurs standard, paire 0 réservée.
- Attributs combinables avec `|` : `A_BOLD`, `A_REVERSE`, etc.
- `A_REVERSE` est l'astuce pour mettre en évidence un élément
  sélectionné sans définir de paire.

## Démo

Exécuter `03_demo_couleurs.py`.
