"""Tests des modèles — étape 02."""

import pytest

from reservation.modeles import (
    Reservation,
    Salle,
    SalleFormation,
    SalleReunion,
    Utilisateur,
)


# --- Tests étape 01 (régression) ---

def test_salle_creation():
    salle = Salle("Everest", 10, ["vidéoprojecteur"])
    assert salle.nom == "Everest"
    assert salle.capacite == 10


def test_utilisateur_creation():
    user = Utilisateur("Alice", "alice@test.fr")
    assert user.nom == "Alice"


# --- Tests étape 02 ---

def test_salle_reunion():
    s = SalleReunion("Everest", 10, ["vidéoprojecteur"], visio=True)
    assert s.visio is True
    assert isinstance(s, Salle)
    assert "visio" in str(s).lower() or "réunion" in str(s).lower()


def test_salle_formation():
    s = SalleFormation("Labo", 20, ["tableau"], nb_postes=15)
    assert s.nb_postes == 15
    assert isinstance(s, Salle)
    assert "15" in str(s) or "postes" in str(s).lower()


def test_salle_eq():
    s1 = Salle("Everest", 10)
    s2 = Salle("Everest", 20)
    assert s1 == s2  # même nom


def test_salle_lt():
    s1 = Salle("Petite", 5)
    s2 = Salle("Grande", 20)
    assert s1 < s2
    assert sorted([s2, s1]) == [s1, s2]


def test_salle_hash():
    s1 = Salle("Everest", 10)
    s2 = Salle("Everest", 20)
    assert hash(s1) == hash(s2)
    assert len({s1, s2}) == 1


def test_salle_from_dict():
    data = {"nom": "Everest", "capacite": 10, "equipements": ["vidéo"]}
    salle = Salle.from_dict(data)
    assert salle.nom == "Everest"
    assert salle.capacite == 10
