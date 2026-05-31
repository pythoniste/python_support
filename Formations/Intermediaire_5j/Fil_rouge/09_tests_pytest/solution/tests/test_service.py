"""Tests du service avec mocks — étape 09."""

from unittest.mock import MagicMock, patch

import pytest

from reservation.service import ReservationService


def test_reserver(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert isinstance(rid, int)


def test_annuler(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    rid = service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert service.annuler(rid) is True
    assert service.annuler(9999) is False


def test_lister_vide(service):
    assert service.lister_reservations() == []


def test_lister_apres_reservation(service):
    service.ajouter_salle("REU-A301", "Everest", 10, "reunion")
    service.ajouter_utilisateur("alice@test.fr", "Alice")
    service.reserver("REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    resas = service.lister_reservations()
    assert len(resas) == 1
    assert resas[0]["salle_code"] == "REU-A301"


def test_service_avec_mock_engine():
    """Démontre l'utilisation de mock pour isoler le service."""
    mock_engine = MagicMock()
    mock_engine.begin = MagicMock()
    with patch("reservation.service.Base.metadata.create_all"):
        svc = ReservationService(mock_engine)
    assert svc.engine is mock_engine
