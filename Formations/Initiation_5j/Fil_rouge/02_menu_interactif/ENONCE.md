# Étape 02 — Menu interactif

## Contexte

À l'étape 01, le programme saisit **un seul** livre puis se termine. C'est frustrant — votre grand-père veut en saisir plusieurs à la suite. On va donc mettre en place une **boucle principale** avec un menu.

## Consignes

1. Reprendre le code de l'étape 01 (ou partir du `starter/`).
2. Mettre en place une **boucle principale** qui affiche le menu suivant :
   ```
   ==== Bibliothèque ====
   (1) Ajouter un livre
   (2) Afficher tous les livres
   (q) Quitter
   Votre choix :
   ```
3. Stocker les livres dans une **liste** (globale au script pour l'instant, on modulariera plus tard).
4. Chaque livre est un **tuple `(titre, auteur, annee)`** pour cette étape.
5. Quand l'utilisateur choisit `(2)`, afficher tous les livres avec leur numéro de ligne :
   ```
   1. « Le Petit Prince » — Antoine de Saint-Exupéry (1943)
   2. « 1984 » — George Orwell (1949)
   ```
6. Si la liste est vide, afficher `« Aucun livre dans le catalogue. »`.
7. Si l'utilisateur entre un choix inconnu, afficher un message d'erreur et redemander.
8. Quitter proprement avec `(q)`.

## Attendus

Exemple d'exécution :

```
==== Bibliothèque ====
(1) Ajouter un livre
(2) Afficher tous les livres
(q) Quitter
Votre choix : 1
Titre : Le Petit Prince
Auteur : Antoine de Saint-Exupéry
Année : 1943
✅ Ajouté !

==== Bibliothèque ====
...
Votre choix : 2
1. « Le Petit Prince » — Antoine de Saint-Exupéry (1943)

==== Bibliothèque ====
...
Votre choix : q
À bientôt !
```

## Critères d'acceptation

- [ ] Une boucle `while True` (ou équivalent) gère le menu.
- [ ] Les livres sont stockés dans une liste Python.
- [ ] Chaque livre est un tuple de **trois éléments** (titre, auteur, année).
- [ ] L'affichage numérote les livres à partir de 1 (indice : `enumerate(start=1)`).
- [ ] Un choix inconnu ne plante **pas** le programme.
- [ ] La commande `q` sort proprement avec `break`.

## Temps estimé

1 heure.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **Oublier `break`** pour sortir de la boucle → le programme ne se termine jamais.
- **`input()` retourne une chaîne** → comparer avec `"q"`, pas avec `q` sans guillemets.
- **Enumerate à partir de 0** → pour un humain, on compte à partir de 1. Utiliser `enumerate(livres, start=1)`.
- **Mélanger `break` et `continue`** : `break` sort de la boucle, `continue` saute à l'itération suivante.
