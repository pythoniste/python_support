# Exercices pratiques — dossier 12_Curses

Une fois les quatre modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Tous les ateliers doivent être lancés dans un **vrai terminal** et
utiliser **`curses.wrapper`** pour la fonction principale. Sous
Windows natif, `pip install windows-curses` est requis (hors stdlib) ;
la solution recommandée reste WSL.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Hello, monde centré  ★
*Module 02 — premier écran, et module 04 — centrage*

Écrire un script `atelier_01.py` qui affiche `Hello, monde !` exactement
au **centre horizontal et vertical** de l'écran, et quitte à la
pression de la touche `q`.

**Indices**

- `stdscr.getmaxyx()` donne `(hauteur, largeur)`.
- `y = hauteur // 2`, `x = (largeur - len(texte)) // 2`.
- Boucle `while True` avec `getch()` et `if touche == ord("q"): break`.

**Comportement attendu**

À l'exécution : le terminal devient plein écran, le message apparaît
pile au centre. Tout autre touche que `q` est ignorée. À l'appui sur
`q`, le programme rend la main et restaure le terminal.

---

## Atelier 2 — Compteur de touches  ★★
*Modules 02 et 03 — boucle d'événements, attributs*

Écrire un script `atelier_02.py` qui affiche un **compteur** au centre
de l'écran. À chaque appui sur n'importe quelle touche autre que `q`,
le compteur est incrémenté de 1 et le nouveau total est ré-affiché.
La touche `q` quitte.

**Bonus** : afficher la dernière touche pressée (sous forme d'entier)
en bas de l'écran, en gras.

**Indices**

- Variable `compteur = 0` initialisée avant la boucle.
- `stdscr.clear()` à chaque itération avant de redessiner.
- Pour afficher en gras : `stdscr.addstr(y, x, texte, curses.A_BOLD)`.

---

## Atelier 3 — Menu navigable  ★★
*Modules 03 et 04 — attributs, touches spéciales*

Écrire un script `atelier_03.py` qui affiche une **liste verticale**
de quatre choix, par exemple :

```
  Nouveau fichier
  Ouvrir
  Enregistrer
  Quitter
```

L'item **sélectionné** est affiché en `curses.A_REVERSE`. Les flèches
**haut** et **bas** déplacent la sélection (sans dépasser les bornes).
La touche **Entrée** (ou la touche `Q` sur l'item « Quitter ») met fin
au programme et affiche, **après** restauration du terminal, l'item
qui était sélectionné.

**Indices**

- Liste `items = ["Nouveau fichier", "Ouvrir", "Enregistrer", "Quitter"]`.
- Index courant `selection = 0`.
- À chaque tour, boucler sur `enumerate(items)` et appliquer
  `A_REVERSE` quand `i == selection`.
- Touches : `curses.KEY_UP`, `curses.KEY_DOWN`, code `10` ou
  `curses.KEY_ENTER` pour la validation.
- Stocker le résultat dans une variable, puis l'**imprimer après** la
  sortie de `curses.wrapper`.

---

## Atelier 4 — Horloge plein écran  ★★★
*Module 04 — boucle non bloquante*

Écrire un script `atelier_04.py` qui affiche l'heure courante au
format `HH:MM:SS` au centre de l'écran, **mise à jour chaque seconde**.
La touche `q` quitte ; un redimensionnement recentre l'heure.

**Indices**

- `stdscr.timeout(1000)` rend `getch()` non bloquant pendant 1000 ms.
- `getch` renvoie `-1` si rien n'a été tapé pendant le délai.
- `time.strftime("%H:%M:%S")` donne l'heure formatée.
- Toujours `stdscr.clear()` + redessiner + `refresh()` à chaque
  itération.
- Penser à traiter `curses.KEY_RESIZE`.

**Bonus** : afficher l'heure en grand en utilisant chaque chiffre sur
plusieurs lignes (police ASCII art simple). Non requis pour la
correction de l'atelier.

---

## Atelier 5 — Tableau de bord deux colonnes  ★★★
*Tous modules*

Écrire un script `atelier_05.py` qui découpe l'écran en deux colonnes :

- à **gauche**, une liste verticale d'au moins cinq éléments (par
  exemple des noms de fichiers fictifs), avec l'élément sélectionné
  en `A_REVERSE` ;
- à **droite**, une zone de **détail** qui affiche des informations
  sur l'élément sélectionné (par exemple : son index, sa longueur,
  une description fictive).

Les flèches haut/bas déplacent la sélection ; `q` quitte ; un
redimensionnement adapte la disposition (la frontière se replace au
milieu de la largeur courante).

**Indices**

- Calculer `frontiere = largeur // 2` à chaque redessin.
- Écrire les éléments de la liste à `x = 2`, le détail à
  `x = frontiere + 2`.
- Pour tracer une ligne verticale de séparation, on peut écrire le
  caractère `|` à `x = frontiere` sur chaque ligne.
- Penser à `KEY_RESIZE` pour relire `getmaxyx()` et recalculer.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on dispose de toutes les briques pour
écrire un **véritable outil interactif** en pur Python : un mini
éditeur, un explorateur de fichiers, un client de messagerie, un
gestionnaire de tâches plein écran. La progression naturelle est de
remplacer les listes statiques par des données réelles (lues sur
disque, sur le réseau, etc.) — et de **réutiliser** les chapitres
précédents du cours pour les obtenir.
