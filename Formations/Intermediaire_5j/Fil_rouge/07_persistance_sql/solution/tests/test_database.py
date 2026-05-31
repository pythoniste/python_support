"""Tests de la persistance SQL — étape 07."""

import pytest

from reservation.database import (
    init_db,
    inserer_reservation,
    inserer_salle,
    inserer_utilisateur,
    lister_reservations,
    lister_salles,
    supprimer_reservation,
)


@pytest.fixture
def con():
    c = init_db(":memory:")
    yield c
    c.close()


def test_init_db_cree_tables(con):
    cur = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row["name"] for row in cur.fetchall()}
    assert "salles" in tables
    assert "utilisateurs" in tables
    assert "reservations" in tables


def test_inserer_et_lister_salles(con):
    inserer_salle(con, "REU-A301", "Everest", 10, "reunion", ["vidéo"])
    salles = lister_salles(con)
    assert len(salles) == 1
    assert salles[0]["nom"] == "Everest"


def test_inserer_reservation(con):
    inserer_salle(con, "REU-A301", "Everest", 10, "reunion", [])
    inserer_utilisateur(con, "alice@test.fr", "Alice")
    rid = inserer_reservation(con, "REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert isinstance(rid, int)
    resas = lister_reservations(con)
    assert len(resas) == 1


def test_supprimer_reservation(con):
    inserer_salle(con, "REU-A301", "Everest", 10, "reunion", [])
    inserer_utilisateur(con, "alice@test.fr", "Alice")
    rid = inserer_reservation(con, "REU-A301", "alice@test.fr", "2025-06-15T09:00", 60)
    assert supprimer_reservation(con, rid) is True
    assert len(lister_reservations(con)) == 0
    assert supprimer_reservation(con, 9999) is False
