"""Tests complets de l'inventaire — étape 05."""

import pytest
from pydantic import ValidationError

from inventaire.modeles import Equipement, Portable, Ecran
from inventaire.schemas import EquipementSchema
from inventaire.database import inserer_equipement, lister_equipements, assigner_equipement


def test_equipement_creation(equipement):
    assert equipement.nom == "Dell XPS"
    assert equipement.ram_go == 16


def test_equipement_assigner(equipement):
    equipement.assigner("Alice")
    assert equipement.assigne_a == "Alice"


def test_equipement_desassigner(equipement):
    equipement.assigner("Alice")
    equipement.desassigner()
    assert equipement.assigne_a is None


def test_equipement_eq():
    e1 = Equipement("A", "SN001", "2025-01-01")
    e2 = Equipement("B", "SN001", "2025-06-01")
    assert e1 == e2


@pytest.mark.parametrize("nom,ns", [("", "SN001"), ("Dell", "")])
def test_equipement_invalide(nom, ns):
    with pytest.raises(ValueError):
        Equipement(nom, ns, "2025-01-01")


def test_schema_valide():
    e = EquipementSchema(nom="Dell", numero_serie="AB123456",
                         type_equipement="portable", date_achat="2025-01-15")
    assert e.nom == "Dell"


@pytest.mark.parametrize("ns", ["abc", "123", "ABCD", "AB12345"])
def test_schema_numero_serie_invalide(ns):
    with pytest.raises(ValidationError):
        EquipementSchema(nom="Dell", numero_serie=ns,
                         type_equipement="portable", date_achat="2025-01-15")


def test_db_inserer_lister(con):
    inserer_equipement(con, "Dell", "SN001", "portable", "2025-01-15")
    eqs = lister_equipements(con)
    assert len(eqs) == 1


def test_db_assigner(con):
    inserer_equipement(con, "Dell", "SN001", "portable", "2025-01-15")
    assert assigner_equipement(con, "SN001", "Alice") is True


def test_ecran():
    e = Ecran("Samsung", "SN003", "2025-03-01", taille_pouces=27.0)
    assert e.taille_pouces == 27.0
    assert isinstance(e, Equipement)
