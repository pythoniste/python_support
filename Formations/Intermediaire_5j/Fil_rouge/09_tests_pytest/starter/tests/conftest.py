"""Fixtures partagées — étape 09 (starter).

TODO : implémenter les fixtures.
"""

import pytest
from sqlalchemy import create_engine

from reservation.modeles import SalleReunion, Utilisateur
from reservation.service import ReservationService


@pytest.fixture
def salle_reunion():
    raise NotImplementedError


@pytest.fixture
def utilisateur():
    raise NotImplementedError


@pytest.fixture
def engine():
    raise NotImplementedError


@pytest.fixture
def service(engine):
    raise NotImplementedError
