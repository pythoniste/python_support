"""Fixtures partagées."""

import pytest
from inventaire.database import init_db
from inventaire.modeles import Portable


@pytest.fixture
def equipement():
    return Portable("Dell XPS", "SN001", "2025-01-15", ram_go=16)


@pytest.fixture
def con():
    c = init_db(":memory:")
    yield c
    c.close()
