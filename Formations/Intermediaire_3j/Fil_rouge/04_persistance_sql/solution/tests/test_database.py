"""Tests SQL — étape 04."""

import pytest
from inventaire.database import (init_db, inserer_equipement, lister_equipements,
                                  assigner_equipement, supprimer_equipement)


@pytest.fixture
def con():
    c = init_db(":memory:")
    yield c
    c.close()


def test_init_db(con):
    cur = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    assert "equipements" in tables


def test_inserer_et_lister(con):
    inserer_equipement(con, "Dell XPS", "SN001", "portable", "2025-01-15")
    eqs = lister_equipements(con)
    assert len(eqs) == 1
    assert eqs[0]["nom"] == "Dell XPS"


def test_assigner(con):
    inserer_equipement(con, "Dell XPS", "SN001", "portable", "2025-01-15")
    assert assigner_equipement(con, "SN001", "Alice") is True


def test_supprimer(con):
    inserer_equipement(con, "Dell XPS", "SN001", "portable", "2025-01-15")
    assert supprimer_equipement(con, "SN001") is True
    assert len(lister_equipements(con)) == 0
