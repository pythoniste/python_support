"""Tests ORM — étape 08."""

import pytest
from sqlalchemy import create_engine

from reservation.service import ReservationService


@pytest.fixture
def service():
    engine = create_engine("sqlite:///:memory:")
    return ReservationService(engine)


def test_ajouter_salle(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")


def test_reserver(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert isinstance(rid, int)


def test_lister_reservations(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    resas = service.lister_reservations()
    assert len(resas) == 1


def test_annuler(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert service.annuler(rid) is True
    assert len(service.lister_reservations()) == 0
