# Étape 08 — SQLAlchemy ORM

## Contexte

Le code `sqlite3` fonctionne mais est verbeux. On migre vers **SQLAlchemy 2** pour bénéficier d'un ORM déclaratif, de relations automatiques et d'une syntaxe plus pythonique.

## Consignes

1. Créer `orm.py` avec les modèles SQLAlchemy :
   - `SalleORM`, `UtilisateurORM`, `ReservationORM` héritant de `DeclarativeBase`.
   - Relations : `ReservationORM.salle` et `ReservationORM.utilisateur`.
   - `SalleORM.reservations` (relation inverse).

2. Créer `service.py` avec une classe `ReservationService` :
   - `__init__(self, engine: Engine)` : crée les tables.
   - `ajouter_salle(...)`, `ajouter_utilisateur(...)`, `reserver(...)`, `annuler(id)`, `lister_reservations()`.
   - Utiliser des `Session` avec context manager.

3. Le module `database.py` (sqlite3) reste disponible comme alternative.

## Critères d'acceptation

- [ ] Les 3 modèles ORM existent avec relations.
- [ ] `ReservationService` fonctionne via `Session`.
- [ ] `create_engine("sqlite:///:memory:")` est utilisé dans les tests.
- [ ] Les tests passent.

## Temps estimé

2 heures.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`DeclarativeBase` vs `declarative_base()`** : SQLAlchemy 2 recommande `class Base(DeclarativeBase): pass`.
- **Oublier `Session.commit()`** dans le context manager.
- **Mapping circulaire** : utiliser `back_populates` plutôt que `backref`.
