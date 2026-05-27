# 04 — Redimensionnement et touches spéciales

## 4.1 Touches spéciales

Quand on appuie sur une touche **non imprimable** (flèche,
F1...F12, Backspace, Insert, Page Up...), `getch()` ne renvoie pas
le code ASCII d'un caractère mais une **constante** définie dans
`curses` :

| Constante           | Touche                |
|---------------------|-----------------------|
| `curses.KEY_UP`     | Flèche haut           |
| `curses.KEY_DOWN`   | Flèche bas            |
| `curses.KEY_LEFT`   | Flèche gauche         |
| `curses.KEY_RIGHT`  | Flèche droite         |
| `curses.KEY_ENTER`  | Entrée (pavé numérique)|
| `curses.KEY_BACKSPACE` | Backspace          |
| `curses.KEY_F1` ... `curses.KEY_F12` | Touches de fonction |
| `curses.KEY_RESIZE` | Redimensionnement de la fenêtre |

Pour les **touches ordinaires**, on compare au code retourné par
`ord(...)`. Pour les **touches spéciales**, on compare aux
constantes. Boucle typique :

```python
touche = stdscr.getch()
if touche == ord("q"):
    break
elif touche == curses.KEY_UP:
    curseur_y -= 1
elif touche == curses.KEY_DOWN:
    curseur_y += 1
elif touche == 10 or touche == curses.KEY_ENTER:
    # Entrée (touche principale) : code 10 sous Linux.
    valider()
```

Note : la touche Entrée du clavier principal renvoie souvent `10`
(saut de ligne) plutôt que `KEY_ENTER`. Tester les deux est une
bonne pratique.

## 4.2 Connaître la taille de l'écran

À tout moment, on peut lire les dimensions de la fenêtre courante :

```python
hauteur, largeur = stdscr.getmaxyx()    # (lignes, colonnes)
```

Ou via les variables globales :

```python
curses.LINES    # nombre de lignes
curses.COLS     # nombre de colonnes
```

Les deux donnent la même information ; `getmaxyx` est préféré car
il fonctionne sur n'importe quelle fenêtre, pas seulement `stdscr`.

**Attention** : ces valeurs sont une **photo** prise à un instant.
Si l'utilisateur agrandit ou réduit la fenêtre du terminal, il
faudra les relire.

## 4.3 Centrer un texte

Le calcul classique pour centrer une chaîne `s` dans une fenêtre
de taille `(hauteur, largeur)` :

```python
y = hauteur // 2
x = (largeur - len(s)) // 2
stdscr.addstr(y, x, s)
```

On divise par `2` avec `//` (division entière) pour avoir des
coordonnées entières.

## 4.4 Réagir au redimensionnement

Si la fenêtre du terminal est redimensionnée par l'utilisateur,
`curses` envoie une « pseudo-touche » `curses.KEY_RESIZE` lors du
prochain `getch`. Le programme doit alors :

1. relire la nouvelle taille avec `getmaxyx()` ;
2. **effacer** l'écran avec `clear()` ;
3. **recalculer** les positions ;
4. **redessiner** tout le contenu.

Squelette robuste :

```python
def dessiner(stdscr):
    stdscr.clear()
    hauteur, largeur = stdscr.getmaxyx()
    message = "Coucou"
    y = hauteur // 2
    x = max(0, (largeur - len(message)) // 2)
    stdscr.addstr(y, x, message)
    stdscr.refresh()


def main(stdscr):
    dessiner(stdscr)
    while True:
        touche = stdscr.getch()
        if touche == ord("q"):
            break
        elif touche == curses.KEY_RESIZE:
            dessiner(stdscr)
```

Le `max(0, ...)` évite une coordonnée **négative** si le terminal
devient plus étroit que le texte.

## 4.5 Bordures de l'écran : un piège

Écrire dans le **coin bas-droit** d'une fenêtre lève une exception
`curses.error`. C'est un héritage historique : le curseur avance
d'une case après chaque caractère, et la dernière case n'a pas de
case suivante. Solutions :

- ne pas dessiner sur la toute dernière position ;
- ou bien encadrer l'`addstr` dans un `try/except curses.error:
  pass` (la chaîne sera tronquée mais le programme survivra) ;
- ou bien utiliser `stdscr.addnstr(y, x, texte, largeur - x - 1)`
  pour borner la longueur.

## 4.6 Boucle bloquante ou non bloquante

Par défaut, `getch()` **bloque** jusqu'à ce qu'une touche soit
pressée. Pour des animations (horloge, jeux), on rend l'attente
**temporisée** avec :

```python
stdscr.timeout(1000)    # attendre au maximum 1000 ms
touche = stdscr.getch()
if touche == -1:
    pass    # aucune touche pendant le délai : on continue
```

Si rien n'est tapé pendant le délai, `getch` renvoie `-1`. On peut
alors mettre à jour l'affichage et reboucler.

## À retenir

- Touches ordinaires : `ord("q")`. Touches spéciales : `curses.KEY_*`.
- `getmaxyx()` donne `(hauteur, largeur)` de la fenêtre.
- `curses.KEY_RESIZE` signale un redimensionnement ; il faut effacer
  et redessiner.
- Le coin bas-droit lève `curses.error` : prévoir une marge.
- `stdscr.timeout(ms)` rend `getch` non bloquant ; il renvoie `-1`
  en cas de délai dépassé.

## Démo

Exécuter `04_demo_resize.py` puis redimensionner la fenêtre du
terminal pour voir le texte se recentrer.
