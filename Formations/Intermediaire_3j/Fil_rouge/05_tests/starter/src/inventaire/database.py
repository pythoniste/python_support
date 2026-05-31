"""Persistance SQL avec sqlite3."""

from __future__ import annotations

import sqlite3
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS equipements (
    numero_serie TEXT PRIMARY KEY,
    nom          TEXT NOT NULL,
    type_eq      TEXT NOT NULL,
    date_achat   TEXT NOT NULL,
    assigne_a    TEXT
);
"""


def init_db(chemin: Path | str = ":memory:") -> sqlite3.Connection:
    con = sqlite3.connect(str(chemin))
    con.row_factory = sqlite3.Row
    con.executescript(_SCHEMA)
    return con


def inserer_equipement(con: sqlite3.Connection, nom: str, numero_serie: str,
                       type_eq: str, date_achat: str) -> None:
    with con:
        con.execute(
            "INSERT INTO equipements (numero_serie, nom, type_eq, date_achat) VALUES (?, ?, ?, ?)",
            (numero_serie, nom, type_eq, date_achat),
        )


def lister_equipements(con: sqlite3.Connection) -> list[dict]:
    cur = con.execute("SELECT numero_serie, nom, type_eq, date_achat, assigne_a FROM equipements")
    return [dict(row) for row in cur.fetchall()]


def assigner_equipement(con: sqlite3.Connection, numero_serie: str, utilisateur: str) -> bool:
    with con:
        cur = con.execute(
            "UPDATE equipements SET assigne_a = ? WHERE numero_serie = ?",
            (utilisateur, numero_serie),
        )
        return cur.rowcount > 0


def supprimer_equipement(con: sqlite3.Connection, numero_serie: str) -> bool:
    with con:
        cur = con.execute("DELETE FROM equipements WHERE numero_serie = ?", (numero_serie,))
        return cur.rowcount > 0
