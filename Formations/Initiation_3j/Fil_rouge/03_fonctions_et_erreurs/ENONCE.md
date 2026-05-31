# Étape 03 — Fonctions et gestion d'erreurs

## Contexte

Le code tient dans une grande boucle et ne gère pas les entrées invalides : un temps à « trente » crashe le programme. On découpe en fonctions et on gère les erreurs.

## Consignes

1. Extraire les opérations dans des fonctions typées :
   - `creer_recette(nom: str, ingredients: list[str], temps: int) -> dict`
   - `ajouter_recette(carnet: list[dict], recette: dict) -> None`
   - `formater_recette(recette: dict) -> str`
   - `saisir_recette() -> dict`
   - `afficher_carnet(carnet: list[dict]) -> None`
   - `main() -> None`
2. Créer une exception `RecetteInvalide(ValueError)`.
3. `creer_recette` doit valider : nom non vide, au moins 1 ingrédient, temps ≥ 1.
4. `saisir_recette` boucle tant que l'entrée est invalide.
5. Toutes les fonctions ont une docstring courte et des type hints.

## Attendus

```
Nom : 
❌ Le nom ne peut pas être vide.
Nom : Crêpes
Ingrédients (séparés par des virgules) : farine, œufs, lait
Temps (minutes) : trente
❌ Le temps doit être un nombre entier.
Temps (minutes) : 30
✅ Ajoutée !
```

## Critères d'acceptation

- [ ] Toutes les fonctions ont des type hints.
- [ ] `RecetteInvalide` hérite de `ValueError`.
- [ ] La saisie boucle proprement sur les entrées invalides.
- [ ] Aucun `except Exception:` fourre-tout.

## Temps estimé

1 h 30.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **Validation seulement dans la saisie** : si quelqu'un appelle `creer_recette(...)` programmatiquement, il doit aussi être protégé.
- **Oublier le `raise`** → l'erreur n'est pas signalée.
