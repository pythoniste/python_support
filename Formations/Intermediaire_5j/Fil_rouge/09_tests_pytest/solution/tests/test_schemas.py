"""Tests Pydantic avec parametrize — étape 09."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from reservation.schemas import ReservationSchema, SalleSchema, UtilisateurSchema


def test_salle_schema_valide():
    s = SalleSchema(nom="Everest", capacite=10)
    assert s.nom == "Everest"


@pytest.mark.parametrize(
    "nom, capacite",
    [
        ("", 10),       # nom vide
        ("X", 0),       # capacité 0
        ("X", -5),      # capacité négative
    ],
)
def test_salle_schema_invalide(nom, capacite):
    with pytest.raises(ValidationError):
        SalleSchema(nom=nom, capacite=capacite)


@pytest.mark.parametrize(
    "duree",
    [10, 25, 7, 100],
)
def test_reservation_duree_pas_multiple_15(duree):
    futur = datetime.now() + timedelta(days=1)
    with pytest.raises(ValidationError):
        ReservationSchema(
            salle_nom="Everest",
            utilisateur_email="a@b.fr",
            date=futur,
            duree_minutes=duree,
        )


def test_reservation_duree_valide():
    futur = datetime.now() + timedelta(days=1)
    r = ReservationSchema(
        salle_nom="Everest",
        utilisateur_email="a@b.fr",
        date=futur,
        duree_minutes=60,
    )
    assert r.duree_minutes == 60


def test_utilisateur_email_invalide():
    with pytest.raises(ValidationError):
        UtilisateurSchema(nom="Alice", email="pas-email")
