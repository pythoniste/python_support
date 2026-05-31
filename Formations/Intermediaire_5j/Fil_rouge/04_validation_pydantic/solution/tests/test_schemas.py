"""Tests des schémas Pydantic — étape 04."""

from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from reservation.schemas import ReservationSchema, SalleSchema, UtilisateurSchema


def test_salle_schema_valide():
    s = SalleSchema(nom="Everest", capacite=10, equipements=["vidéo"])
    assert s.nom == "Everest"
    assert s.capacite == 10


def test_salle_schema_capacite_invalide():
    with pytest.raises(ValidationError):
        SalleSchema(nom="Everest", capacite=0)


def test_utilisateur_schema_valide():
    u = UtilisateurSchema(nom="Alice", email="alice@test.fr")
    assert u.nom == "Alice"


def test_utilisateur_schema_email_invalide():
    with pytest.raises(ValidationError):
        UtilisateurSchema(nom="Alice", email="pas-un-email")


def test_reservation_duree_multiple_15():
    futur = datetime.now() + timedelta(days=1)
    r = ReservationSchema(
        salle_nom="Everest",
        utilisateur_email="alice@test.fr",
        date=futur,
        duree_minutes=60,
    )
    assert r.duree_minutes == 60


def test_reservation_duree_pas_multiple_15():
    futur = datetime.now() + timedelta(days=1)
    with pytest.raises(ValidationError):
        ReservationSchema(
            salle_nom="Everest",
            utilisateur_email="alice@test.fr",
            date=futur,
            duree_minutes=25,
        )


def test_salle_json_round_trip():
    s = SalleSchema(nom="Everest", capacite=10)
    json_str = s.model_dump_json()
    s2 = SalleSchema.model_validate_json(json_str)
    assert s == s2
