"""Tests des modèles — étape 09."""

import pytest

from reservation.modeles import (
    Reservation,
    Salle,
    SalleFormation,
    SalleReunion,
    Utilisateur,
)


def test_salle_creation():
    salle = Salle("Everest", 10, ["vidéo"])
    assert salle.nom == "Everest"
    assert salle.capacite == 10


def test_salle_nom_vide():
    with pytest.raises(ValueError):
        Salle("", 10)


def test_salle_eq():
    assert Salle("Everest", 10) == Salle("Everest", 20)


def test_salle_lt():
    assert Salle("A", 5) < Salle("B", 10)


def test_salle_reunion(salle_reunion):
    assert salle_reunion.visio is True
    assert isinstance(salle_reunion, Salle)


def test_salle_formation():
    s = SalleFormation("Labo", 20, nb_postes=15)
    assert s.nb_postes == 15


def test_utilisateur(utilisateur):
    assert utilisateur.nom == "Alice"
    assert utilisateur.email == "alice@test.fr"


def test_reservation(salle_reunion, utilisateur):
    resa = Reservation(salle_reunion, utilisateur, "2025-06-15T09:00", 60)
    assert resa.duree_minutes == 60
    assert "Everest" in str(resa)
