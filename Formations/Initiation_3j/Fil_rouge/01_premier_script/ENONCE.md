# Étape 01 — Premier script

## Contexte

Première demi-journée : vous venez d'installer Python et écrit votre premier `print("Hello")`. Votre petit frère attend son carnet de recettes — commençons petit.

## Consignes

1. Créer un fichier `main.py`.
2. Écrire un programme qui :
   - demande le **nom** de la recette,
   - demande la **liste d'ingrédients** (une seule ligne, séparés par des virgules),
   - demande le **temps de préparation** en minutes (converti en `int`),
   - affiche un message de confirmation formaté.
3. Se lance avec `python main.py`.

## Attendus

```
$ python main.py
Nom : Crêpes
Ingrédients (séparés par des virgules) : farine, œufs, lait, beurre, sel
Temps (minutes) : 30
✅ Recette enregistrée : « Crêpes » — 5 ingrédients — 30 min
```

## Critères d'acceptation

- [ ] Le fichier `main.py` existe et se lance sans erreur.
- [ ] Le programme utilise **trois `input()`** séparés.
- [ ] Le temps est converti en `int`.
- [ ] Les ingrédients sont séparés avec `.split(",")` et comptés avec `len(...)`.
- [ ] Le message de confirmation utilise une **f-string**.

## Temps estimé

45 minutes.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **Oublier `int(...)` sur le temps** → chaîne au lieu d'un nombre, pas d'arithmétique possible.
- **`.split(",")` garde les espaces** → utiliser `[i.strip() for i in texte.split(",")]` pour nettoyer.
- **Liste vide** : si l'utilisateur tape juste une virgule, on peut se retrouver avec un ingrédient vide. On ignore pour l'instant, on traitera ça à l'étape 03.
