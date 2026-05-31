# Étape 02 — Validation Pydantic

## Contexte

Les validations manuelles deviennent lourdes. On migre vers Pydantic v2 pour la validation et la sérialisation.

## Consignes

1. Créer `schemas.py` avec `EquipementSchema(BaseModel)` : `nom`, `numero_serie`, `type_equipement` (Literal), `date_achat` (date), `assigne_a` (str | None).
2. Ajouter un `@field_validator` : le numéro de série doit correspondre au pattern `^[A-Z]{2}\d{6}$`.
3. Tester la sérialisation JSON aller-retour.

## Critères d'acceptation

- [ ] `EquipementSchema` existe avec validation.
- [ ] Le numéro de série est validé par regex.
- [ ] La sérialisation JSON fonctionne.
- [ ] Les tests passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.
