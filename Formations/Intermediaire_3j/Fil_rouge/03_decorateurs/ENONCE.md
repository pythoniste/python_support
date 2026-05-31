# Étape 03 — Décorateurs

## Contexte

On ajoute du logging automatique et de la mesure de performance avec des décorateurs.

## Consignes

1. Créer `decorateurs.py` avec `@log_action` et `@timer` (comme Intermédiaire 5j étape 05).
2. Utiliser `functools.wraps`.
3. Appliquer sur les fonctions critiques du métier.

## Critères d'acceptation

- [ ] `@log_action` et `@timer` existent.
- [ ] `functools.wraps` préserve `__name__` et `__doc__`.
- [ ] Les tests passent.

## Temps estimé

1 h.

## Solution

Voir `solution/`.
