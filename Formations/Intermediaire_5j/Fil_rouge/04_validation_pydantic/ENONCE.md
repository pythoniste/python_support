# Étape 04 — Validation Pydantic

## Contexte

Les validations manuelles dans `__init__` deviennent lourdes. On migre les modèles vers **Pydantic v2** pour bénéficier de la validation automatique, de la sérialisation JSON et des validators personnalisés.

## Consignes

1. Créer `schemas.py` avec des modèles Pydantic :
   - `SalleSchema(BaseModel)` : `nom` (str, min 1 car), `capacite` (int, >= 1), `equipements` (list[str], défaut []).
   - `UtilisateurSchema(BaseModel)` : `nom` (str), `email` (EmailStr).
   - `ReservationSchema(BaseModel)` : `salle_nom` (str), `utilisateur_email` (str), `date` (datetime), `duree_minutes` (int, >= 15, <= 480).

2. Ajouter un `@field_validator` sur `ReservationSchema` :
   - `duree_minutes` doit être un multiple de 15.

3. Ajouter un `model_validator(mode="after")` :
   - La date ne doit pas être dans le passé.

4. Tester la sérialisation : `schema.model_dump_json()` et `SalleSchema.model_validate_json(...)`.

## Critères d'acceptation

- [ ] `SalleSchema`, `UtilisateurSchema`, `ReservationSchema` existent dans `schemas.py`.
- [ ] Les validateurs Pydantic lèvent `ValidationError` sur données invalides.
- [ ] La durée doit être un multiple de 15.
- [ ] La sérialisation JSON aller-retour fonctionne.
- [ ] Les tests passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`from pydantic import EmailStr`** nécessite `pydantic[email]` dans les dépendances.
- **`@field_validator` vs `@model_validator`** : le premier valide un champ isolé, le second accède au modèle entier.
- **`ValidationError` vs `ValueError`** : Pydantic lève `ValidationError`, pas `ValueError`.
