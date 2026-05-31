"""Fixtures partagées."""

import pytest
from sqlalchemy import create_engine

from reservation.service import ReservationService


@pytest.fixture
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def service(engine):
    return ReservationService(engine)
