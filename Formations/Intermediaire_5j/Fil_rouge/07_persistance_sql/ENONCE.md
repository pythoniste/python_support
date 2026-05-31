# Étape 07 — Persistance SQL

## Contexte

Les données vivent en mémoire et disparaissent à chaque redémarrage. On va les persister dans une base **SQLite** avec le module `sqlite3` de la bibliothèque standard.

## Consignes

1. Créer `database.py` avec :
   - `init_db(chemin: Path) -> sqlite3.Connection` : crée les tables si elles n'existent pas.
   - Tables : `salles` (code, nom, capacite, type_salle, equipements_json), `utilisateurs` (email, nom, role), `reservations` (id, salle_code, utilisateur_email, date, duree_minutes).
   - Fonctions CRUD : `inserer_salle`, `lister_salles`, `inserer_utilisateur`, `inserer_reservation`, `lister_reservations`, `supprimer_reservation`.

2. Toutes les requêtes doivent utiliser des **requêtes paramétrées** (`?` placeholders) pour éviter l'injection SQL.

3. Utiliser `with connexion:` pour les transactions.

4. Stocker `equipements` comme JSON sérialisé dans une colonne texte.

## Critères d'acceptation

- [ ] `init_db` crée les 3 tables.
- [ ] Les CRUD fonctionnent (insert + select + delete).
- [ ] Les requêtes sont paramétrées (pas de f-string dans le SQL).
- [ ] `with connexion:` est utilisé pour les transactions.
- [ ] Les tests passent avec une base en mémoire (`:memory:`).

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Injection SQL** : ne jamais utiliser `f"SELECT ... WHERE nom = '{nom}'"`. Toujours `?`.
- **Oublier `connexion.commit()`** : les données ne sont pas persistées. Avec `with connexion:`, le commit est automatique.
- **JSON dans SQLite** : stocker les listes comme JSON (`json.dumps`) et les recharger avec `json.loads`.
