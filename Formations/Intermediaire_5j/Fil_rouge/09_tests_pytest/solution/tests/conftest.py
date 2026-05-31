"""Fixtures partagées pour la suite de tests."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from reservation.modeles import SalleReunion, Utilisateur
from reservation.service import ReservationService


@pytest.fixture
def salle_reunion() -> SalleReunion:
    return SalleReunion("Everest", 10, ["vidéoprojecteur"], visio=True)


@pytest.fixture
def utilisateur() -> Utilisateur:
    return Utilisateur("Alice", "alice@test.fr")


@pytest.fixture
def engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def service(engine: Engine) -> ReservationService:
    return ReservationService(engine)
