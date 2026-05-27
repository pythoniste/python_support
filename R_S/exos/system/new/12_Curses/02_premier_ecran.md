# 02 — Premier écran avec `curses.wrapper`

## 2.1 Pourquoi `curses.wrapper`

`curses` modifie l'état du terminal au démarrage : il efface l'écran,
cache le curseur, désactive l'écho, passe en mode brut. Si le
programme se termine **proprement**, il restaure tout. Si en revanche
une exception **non rattrapée** survient en cours de route, le
terminal reste dans un état cassé : on tape mais rien ne s'affiche,
ou bien on voit les caractères de contrôle bruts. Il faut alors
quitter à l'aveugle et taper `reset` pour récupérer.

`curses.wrapper(fonction)` règle ce problème. Il :

1. initialise `curses` ;
2. crée la fenêtre principale (`stdscr`, *standard screen*) ;
3. appelle la `fonction` en lui passant `stdscr` ;
4. **quoi qu'il arrive** — fin normale ou exception — restaure le
   terminal proprement ;
5. si une exception a eu lieu, la **relance** une fois le terminal
   remis d'aplomb, pour qu'on puisse lire la trace.

C'est l'équivalent d'un `try/finally` géant, mais offert clé en main.
**Toujours** passer par `wrapper` en début de carrière `curses`.

## 2.2 La structure canonique

```python
import curses


def main(stdscr):
    # tout le code curses va ici
    stdscr.addstr(0, 0, "Bonjour, monde !")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
```

C'est la **forme à connaître par coeur**. On la verra dans toutes les
démos et tous les corrigés du chapitre.

## 2.3 Les quatre méthodes essentielles

### `addstr(y, x, texte)` — écrire du texte

Écrit `texte` à la position `(y, x)` de la fenêtre :

```python
stdscr.addstr(5, 10, "ici à la ligne 5, colonne 10")
```

**Attention** : l'ordre est `(y, x)` et **pas** `(x, y)`. C'est
l'opposé de ce qu'on a en mathématiques, mais c'est l'ordre logique
en informatique : « la ligne d'abord, puis la colonne ». L'origine
`(0, 0)` est en **haut à gauche**, et `y` augmente vers le **bas**.

### `refresh()` — rendre visible à l'écran

Pour des raisons de performance, `addstr` ne dessine pas
**immédiatement**. Il met à jour une copie interne de l'écran.
L'appel à `refresh()` envoie effectivement le contenu au terminal.

Règle pratique : **un `refresh` après une série de `addstr`**, jamais
entre chaque.

### `getch()` — lire une touche

Lit **un** caractère (ou une touche spéciale) au clavier. Bloquant
par défaut : le programme attend qu'on tape.

```python
touche = stdscr.getch()
if touche == ord("q"):
    return    # quitte le programme
```

`getch` renvoie un **entier** : le code ASCII pour les touches
classiques, un code spécial (`curses.KEY_UP`, etc.) pour les flèches
et compagnie. La fonction `ord("q")` donne le code de la lettre `q`.

### `clear()` — effacer la fenêtre

Efface tout le contenu, prêt à redessiner. À utiliser à chaque tour
de boucle dans une animation, ou lors d'un redimensionnement.

## 2.4 Le squelette d'une boucle d'événements

La plupart des programmes `curses` suivent toujours le même schéma :

```python
import curses


def main(stdscr):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Appuyer sur q pour quitter.")
        stdscr.refresh()

        touche = stdscr.getch()
        if touche == ord("q"):
            break


if __name__ == "__main__":
    curses.wrapper(main)
```

Boucle : **effacer, dessiner, rafraîchir, attendre une touche, agir**.
C'est tout. Le reste du chapitre raffine ce squelette : couleurs,
positionnement, gestion du redimensionnement.

## À retenir

- Toujours passer par `curses.wrapper(main)` : il restaure le
  terminal même en cas d'exception.
- La fonction principale reçoit `stdscr`, la fenêtre par défaut.
- Coordonnées en `(y, x)`, origine en haut à gauche, `y` croît vers
  le bas.
- `addstr(y, x, texte)` écrit, `refresh()` rend visible.
- `getch()` lit une touche (entier).
- `clear()` efface avant de redessiner.

## Démo

Exécuter `02_demo_addstr.py`.
