"""Tests Pydantic — étape 02."""

import pytest
from pydantic import ValidationError
from inventaire.schemas import EquipementSchema


def test_equipement_valide():
    e = EquipementSchema(nom="Dell XPS", numero_serie="AB123456",
                         type_equipement="portable", date_achat="2025-01-15")
    assert e.nom == "Dell XPS"


def test_numero_serie_invalide():
    with pytest.raises(ValidationError):
        EquipementSchema(nom="Dell", numero_serie="invalide",
                         type_equipement="portable", date_achat="2025-01-15")


def test_json_round_trip():
    e = EquipementSchema(nom="Dell XPS", numero_serie="AB123456",
                         type_equipement="portable", date_achat="2025-01-15")
    j = e.model_dump_json()
    e2 = EquipementSchema.model_validate_json(j)
    assert e == e2
