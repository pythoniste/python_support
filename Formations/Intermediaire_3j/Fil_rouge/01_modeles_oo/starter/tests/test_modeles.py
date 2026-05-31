"""Tests des modèles — étape 01."""

import pytest
from inventaire.modeles import Equipement, Portable, Ecran, Serveur


def test_equipement_creation():
    e = Equipement("Dell XPS", "SN001", "2025-01-15")
    assert e.nom == "Dell XPS"
    assert e.numero_serie == "SN001"


def test_portable_heritage():
    p = Portable("ThinkPad", "SN002", "2025-02-01", ram_go=16)
    assert isinstance(p, Equipement)
    assert p.ram_go == 16


def test_assigner_desassigner():
    e = Equipement("Dell XPS", "SN001", "2025-01-15")
    assert e.assigne_a is None
    e.assigner("Alice")
    assert e.assigne_a == "Alice"
    e.desassigner()
    assert e.assigne_a is None


def test_eq_sur_numero_serie():
    e1 = Equipement("Dell", "SN001", "2025-01-01")
    e2 = Equipement("HP", "SN001", "2025-06-01")
    assert e1 == e2


def test_hash():
    e1 = Equipement("Dell", "SN001", "2025-01-01")
    e2 = Equipement("HP", "SN001", "2025-06-01")
    assert len({e1, e2}) == 1
