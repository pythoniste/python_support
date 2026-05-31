"""Tests des modèles — étape 01."""

import pytest

from reservation.modeles import Reservation, Salle, Utilisateur


def test_salle_creation():
    salle = Salle("Everest", 10, ["vidéoprojecteur"])
    assert salle.nom == "Everest"
    assert salle.capacite == 10
    assert salle.equipements == ["vidéoprojecteur"]


def test_salle_nom_vide_leve_erreur():
    with pytest.raises(ValueError):
        Salle("", 10)


def test_salle_capacite_negative_leve_erreur():
    with pytest.raises(ValueError):
        Salle("Test", -1)


def test_salle_a_equipement():
    salle = Salle("Everest", 10, ["Vidéoprojecteur", "Tableau blanc"])
    assert salle.a_equipement("vidéoprojecteur") is True
    assert salle.a_equipement("TABLEAU BLANC") is True
    assert salle.a_equipement("micro") is False


def test_salle_str():
    salle = Salle("Everest", 10)
    assert "Everest" in str(salle)
    assert "10" in str(salle)


def test_utilisateur_creation():
    user = Utilisateur("Alice", "alice@test.fr")
    assert user.nom == "Alice"
    assert user.email == "alice@test.fr"


def test_utilisateur_nom_vide_leve_erreur():
    with pytest.raises(ValueError):
        Utilisateur("", "a@b.fr")


def test_reservation_creation():
    salle = Salle("Everest", 10)
    user = Utilisateur("Alice", "alice@test.fr")
    resa = Reservation(salle, user, "2025-06-15T09:00", 60)
    assert resa.salle is salle
    assert resa.utilisateur is user
    assert resa.duree_minutes == 60


def test_reservation_duree_invalide():
    salle = Salle("Everest", 10)
    user = Utilisateur("Alice", "alice@test.fr")
    with pytest.raises(ValueError):
        Reservation(salle, user, "2025-06-15T09:00", 0)
