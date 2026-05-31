# Étape 03 — Typage complet

## Contexte

Le code fonctionne mais `mypy --strict` affiche des dizaines d'erreurs. On va ajouter un typage moderne (PEP 604, PEP 695) et un `Protocol` pour les objets « réservables ».

## Consignes

1. Ajouter des **type hints** sur toutes les fonctions et méthodes (paramètres + retour).
2. Utiliser la syntaxe moderne : `int | None` au lieu de `Optional[int]`, `list[str]` au lieu de `List[str]`.
3. Créer un `Protocol` nommé `Reservable` dans `protocols.py` :
   ```python
   class Reservable(Protocol):
       nom: str
       capacite: int
   ```
4. Modifier les fonctions qui acceptent une salle pour qu'elles acceptent un `Reservable`.
5. `mypy --strict src/` doit passer sans erreur.

## Critères d'acceptation

- [ ] Toutes les fonctions ont des type hints (paramètres + retour).
- [ ] `from __future__ import annotations` en tête de chaque module.
- [ ] `Reservable` est un `Protocol` dans `protocols.py`.
- [ ] `mypy --strict src/` ne produit aucune erreur.
- [ ] Les tests existants passent toujours.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`Optional[X]` vs `X | None`** : les deux fonctionnent, mais `X | None` est la syntaxe moderne recommandée.
- **Oublier `from __future__ import annotations`** : nécessaire pour évaluer les annotations de manière paresseuse.
- **`Protocol` avec méthodes vs attributs** : les attributs dans un `Protocol` doivent être déclarés comme annotations de classe.
