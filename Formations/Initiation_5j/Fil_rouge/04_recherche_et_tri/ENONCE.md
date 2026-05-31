# Étape 04 — Recherche et tri

## Contexte

Le catalogue grossit. Votre grand-père veut pouvoir **chercher un livre** sans tout lister, et **trier** l'affichage par titre ou par année. On va mettre en place ces deux fonctionnalités.

## Consignes

1. Reprendre le code de l'étape 03.
2. Ajouter l'option de menu `(4) Rechercher` qui demande une chaîne de recherche et affiche tous les livres dont le **titre ou l'auteur** contient cette chaîne (**sans tenir compte de la casse**).
3. Modifier l'option `(2) Afficher` pour demander un **critère de tri** :
   ```
   Trier par : (t)itre, (a)uteur, a(n)née
   ```
   et afficher les livres triés selon ce critère.
4. Le tri doit être **stable** (deux livres identiques sur le critère gardent leur ordre d'entrée).
5. La recherche doit trouver par exemple « orwell » dans « George Orwell » (majuscules/minuscules indifférentes).

## Attendus

```
Votre choix : 4
Rechercher : orwell
Résultats (1) :
1. « 1984 » — George Orwell (1949)

Votre choix : 2
Trier par : (t)itre, (a)uteur, a(n)née : n
1. « 1984 » — George Orwell (1949)
2. « Le Petit Prince » — Antoine de Saint-Exupéry (1943)
```

## Critères d'acceptation

- [ ] La recherche est **case-insensitive** (indice : `.lower()` ou `.casefold()`).
- [ ] La recherche cherche dans le titre **et** l'auteur.
- [ ] Le tri utilise `sorted()` avec un paramètre `key=` (lambda ou `operator.itemgetter`).
- [ ] Le tri ne **modifie pas** la liste originale (utiliser `sorted`, pas `list.sort`).
- [ ] Un critère de tri inconnu affiche un message d'erreur et retourne au menu.

## Temps estimé

1 h 30.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **`casefold()` vs `lower()`** : `casefold()` est plus robuste pour Unicode (ex. allemand `ß`). Pour du texte français c'est équivalent.
- **`list.sort()` modifie en place** et retourne `None`. `sorted()` retourne une nouvelle liste.
- **Lambda vs itemgetter** : les deux marchent, `itemgetter` est légèrement plus rapide et plus lisible pour du tri multi-clé.
