# Étape 02 — Menu et liste de recettes en mémoire

## Contexte

À l'étape 01, on saisit **une seule** recette. On va mettre en place une boucle principale avec un menu pour en saisir plusieurs et les lister.

## Consignes

1. Reprendre le code de l'étape 01.
2. Mettre en place une boucle avec le menu suivant :
   ```
   ==== Carnet de recettes ====
   (1) Ajouter une recette
   (2) Lister les recettes
   (q) Quitter
   ```
3. Stocker les recettes dans une **liste de dictionnaires**. Chaque recette est un dict :
   ```python
   {"nom": "Crêpes", "ingredients": [...], "temps": 30}
   ```
4. Option `(2)` : lister toutes les recettes numérotées avec leurs infos.
5. Si la liste est vide : afficher `« Aucune recette dans le carnet. »`.
6. Un choix inconnu affiche une erreur et retourne au menu.

## Attendus

```
Votre choix : 1
Nom : Crêpes
Ingrédients (séparés par des virgules) : farine, œufs, lait
Temps (minutes) : 30
✅ Ajoutée !

Votre choix : 2
1. « Crêpes » — 30 min
   Ingrédients : farine, œufs, lait
```

## Critères d'acceptation

- [ ] Une boucle `while True` gère le menu.
- [ ] Les recettes sont stockées dans une liste de dicts.
- [ ] L'affichage utilise `enumerate(start=1)`.
- [ ] `q` quitte proprement avec `break`.

## Temps estimé

1 h.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **Oublier le `break`** → boucle infinie.
- **Comparer à `q` sans guillemets** → `NameError`.
