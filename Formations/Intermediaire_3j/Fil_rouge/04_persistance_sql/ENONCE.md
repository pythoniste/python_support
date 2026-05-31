# Étape 04 — Persistance SQL

## Contexte

On persiste l'inventaire dans une base SQLite.

## Consignes

1. Créer `database.py` avec `init_db`, `inserer_equipement`, `lister_equipements`, `assigner_equipement`, `supprimer_equipement`.
2. Requêtes paramétrées uniquement.
3. Utiliser `with connexion:` pour les transactions.

## Critères d'acceptation

- [ ] `init_db` crée la table `equipements`.
- [ ] Les CRUD fonctionnent.
- [ ] Pas de f-string dans le SQL.
- [ ] Les tests passent avec `:memory:`.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.
