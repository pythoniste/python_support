# Quiz de validation — dossier 12_Curses

Six questions courtes pour vérifier qu'on a saisi l'essentiel. Les
réponses se trouvent en fin de document — tenter d'y répondre **sans**
consulter au préalable.

## Questions

**Q1.** En quoi le mode « brut » (raw) d'un terminal diffère-t-il du
mode « cuit » (cooked), et pourquoi `curses` a-t-il besoin du mode
brut ?

**Q2.** À quoi sert `curses.wrapper(main)`, et quel serait le risque
concret de s'en passer ?

**Q3.** Lire le code suivant et indiquer ce qui ne va pas :

```python
stdscr.addstr(10, 5, "Coucou")
```

Quel est précisément le rôle des nombres `10` et `5` ? Et ce code,
écrit dans une fonction principale appelée par `curses.wrapper`,
suffit-il à voir le texte s'afficher ?

**Q4.** Pour afficher du texte rouge sur fond noir avec `curses`,
quelles sont les **trois étapes** dans l'ordre, et pourquoi
`curses.COLOR_RED` ne peut-il pas être passé directement à `addstr` ?

**Q5.** Le programme suivant fonctionne, mais il a un défaut quand
l'utilisateur agrandit la fenêtre du terminal. Lequel, et comment le
corriger ?

```python
def main(stdscr):
    hauteur, largeur = stdscr.getmaxyx()
    stdscr.addstr(hauteur // 2, largeur // 2 - 3, "Coucou")
    stdscr.refresh()
    while stdscr.getch() != ord("q"):
        pass
```

**Q6.** Pour faire une horloge plein écran qui se met à jour chaque
seconde, on ne peut pas se contenter d'un `getch()` bloquant. Quelle
méthode `curses` permet de rendre `getch()` non bloquant avec un
délai donné, et que renvoie `getch()` lorsque le délai expire sans
qu'aucune touche n'ait été pressée ?

---

## Réponses

**R1.** En mode **cuit**, le système bufferise les caractères tapés
ligne par ligne et n'en transmet le contenu au programme qu'à
l'appui sur Entrée ; chaque touche est en outre **renvoyée à
l'écran** automatiquement (écho). En mode **brut**, chaque touche
est transmise **immédiatement** au programme, **sans écho**, et les
touches spéciales (flèches, F1...) deviennent lisibles. `curses` a
besoin du mode brut pour réagir touche par touche et dessiner
lui-même ce qui apparaît à l'écran.

**R2.** `curses.wrapper(main)` initialise `curses`, appelle `main`
en lui passant `stdscr`, puis **restaure le terminal d'origine
quoi qu'il arrive** — fin normale ou exception non rattrapée — avant
de relancer l'exception pour qu'on puisse lire la trace. Sans
`wrapper`, une exception laisse le terminal en mode brut sans écho :
on ne voit plus ce qu'on tape, et il faut taper `reset` à l'aveugle
pour récupérer.

**R3.** L'ordre est `(y, x)` : `10` est la **ligne** (depuis le
haut) et `5` la **colonne** (depuis la gauche). Ce code seul ne
suffit **pas** à voir le texte : `curses` bufferise les
modifications. Il faut un `stdscr.refresh()` après les `addstr` pour
que le texte apparaisse effectivement à l'écran.

**R4.** Les trois étapes :

1. activer la couleur avec `curses.start_color()` (souvent déjà fait
   par `wrapper`) ;
2. déclarer une paire avec
   `curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)` ;
3. passer `curses.color_pair(1)` en quatrième argument :
   `stdscr.addstr(y, x, "texte", curses.color_pair(1))`.

`curses.COLOR_RED` est juste un **numéro de couleur** ; ce n'est pas
un attribut prêt à l'emploi. Seul un appel à `color_pair(n)` (où la
paire `n` a été préalablement déclarée par `init_pair`) renvoie un
attribut utilisable.

**R5.** La taille `(hauteur, largeur)` est **lue une seule fois** au
démarrage. Si l'utilisateur redimensionne la fenêtre, le texte reste
à l'ancienne position et n'est plus centré. Correction : capter
`curses.KEY_RESIZE` dans la boucle d'événements et, à chaque
réception, ré-appeler `stdscr.clear()`, relire `getmaxyx()`,
recalculer les coordonnées et redessiner.

**R6.** `stdscr.timeout(ms)` rend `getch()` non bloquant : il attend
au maximum `ms` millisecondes. Si rien n'est tapé, `getch()` renvoie
**`-1`**. Pour une horloge à la seconde, on utilise
`stdscr.timeout(1000)` ; à chaque retour, qu'on ait reçu une touche
ou `-1`, on redessine l'heure et on reboucle.
