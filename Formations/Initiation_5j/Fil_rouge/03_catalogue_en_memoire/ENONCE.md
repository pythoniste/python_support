# Étape 03 — Catalogue en mémoire

## Contexte

Les tuples, c'est bien pour deux-trois informations, mais votre grand-père veut aussi noter l'**ISBN** (le code-barres) et la **date d'ajout** au catalogue. Ça commence à faire beaucoup d'informations — on va donc passer à des **dictionnaires**, plus lisibles et plus souples.

## Consignes

1. Reprendre le code de l'étape 02.
2. Chaque livre devient désormais un **dictionnaire** avec les clés suivantes :
   - `"titre"` (str)
   - `"auteur"` (str)
   - `"annee"` (int)
   - `"isbn"` (str, 13 caractères, on ne valide pas encore)
   - `"date_ajout"` (str au format ISO, rempli automatiquement)
3. Utiliser `datetime.date.today().isoformat()` pour la date d'ajout (le programme la remplit, pas l'utilisateur).
4. Adapter l'affichage du catalogue pour inclure l'ISBN et la date d'ajout.
5. Ajouter une nouvelle option de menu : `(3) Afficher le nombre total de livres`.

## Attendus

Exemple :

```
==== Bibliothèque ====
(1) Ajouter un livre
(2) Afficher tous les livres
(3) Compter les livres
(q) Quitter
Votre choix : 1
Titre : 1984
Auteur : George Orwell
Année : 1949
ISBN : 9780451524935
✅ Ajouté le 2026-04-14.

Votre choix : 2
1. « 1984 » — George Orwell (1949)
   ISBN : 9780451524935   |   Ajouté le 2026-04-14

Votre choix : 3
Le catalogue contient 1 livre.
```

## Critères d'acceptation

- [ ] Chaque livre est un `dict` avec les 5 clés listées.
- [ ] La date d'ajout est remplie **automatiquement** par le programme.
- [ ] Le comptage affiche `"livre"` ou `"livres"` selon le pluriel (≥ 2).
- [ ] L'affichage reste propre même avec plusieurs livres.

## Temps estimé

1 h 30.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **Oublier l'import `from datetime import date`** en haut du fichier.
- **Dict vs tuple** : `livre["titre"]` et non `livre[0]`.
- **Accord pluriel** : un petit `if` suffit, mais c'est un détail qui compte pour l'utilisateur.
