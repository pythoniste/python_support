# Étape 09 — Tests pytest

## Contexte

Le code est fonctionnel mais fragile : chaque modification peut casser quelque chose sans qu'on s'en aperçoive. On va écrire une **suite de tests complète** avec pytest, en utilisant les fixtures, le parametrize et les mocks.

## Consignes

1. Créer `tests/conftest.py` avec des **fixtures partagées** :
   - `salle_reunion` : une `SalleReunion` de test.
   - `utilisateur` : un `Utilisateur` de test.
   - `engine` : un `create_engine("sqlite:///:memory:")`.
   - `service` : un `ReservationService` prêt à l'emploi.

2. Créer `tests/test_modeles.py` : tests des modèles OO (au moins 6 tests).

3. Créer `tests/test_schemas.py` : tests Pydantic avec `@pytest.mark.parametrize` pour tester plusieurs cas invalides en un seul test.

4. Créer `tests/test_service.py` : tests du service ORM avec mocks (`monkeypatch` ou `unittest.mock.patch`).

5. Viser une **couverture > 80%** (optionnel : `pytest-cov`).

## Critères d'acceptation

- [ ] `conftest.py` existe avec au moins 3 fixtures.
- [ ] `@pytest.mark.parametrize` est utilisé au moins une fois.
- [ ] `monkeypatch` ou `unittest.mock` est utilisé au moins une fois.
- [ ] Au moins 15 tests au total.
- [ ] `pytest -v` est vert.

## Temps estimé

2 heures.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Fixtures trop couplées** : chaque fixture doit être indépendante. Utiliser `tmp_path` pour les fichiers.
- **Mock trop large** : ne mocker que ce qui est strictement nécessaire.
- **Oublier `yield` dans les fixtures** qui nécessitent un teardown (ex. fermer une connexion).
