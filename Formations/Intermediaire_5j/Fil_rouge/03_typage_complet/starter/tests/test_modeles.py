"""Tests des modèles — étape 03."""

import pytest

from reservation.modeles import (
    Reservation,
    Salle,
    SalleFormation,
    SalleReunion,
    Utilisateur,
)
from reservation.protocols import Reservable


def test_salle_creation() -> None:
    salle = Salle("Everest", 10, ["vidéoprojecteur"])
    assert salle.nom == "Everest"
    assert salle.capacite == 10


def test_salle_is_reservable() -> None:
    salle = Salle("Everest", 10)
    assert isinstance(salle, Reservable)


def test_salle_reunion_is_reservable() -> None:
    s = SalleReunion("Everest", 10, visio=True)
    assert isinstance(s, Reservable)


def test_reservation_creation() -> None:
    salle = Salle("Everest", 10)
    user = Utilisateur("Alice", "alice@test.fr")
    resa = Reservation(salle, user, "2025-06-15T09:00", 60)
    assert resa.duree_minutes == 60
