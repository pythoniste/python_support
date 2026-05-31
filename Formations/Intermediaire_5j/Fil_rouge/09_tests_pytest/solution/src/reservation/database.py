"""Persistance SQL avec sqlite3."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

_SCHEMA = """
CREATE TABLE IF NOT EXISTS salles (
    code         TEXT PRIMARY KEY,
    nom          TEXT NOT NULL,
    capacite     INTEGER NOT NULL,
    type_salle   TEXT NOT NULL,
    equipements_json TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS utilisateurs (
    email TEXT PRIMARY KEY,
    nom   TEXT NOT NULL,
    role  TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS reservations (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    salle_code         TEXT NOT NULL REFERENCES salles(code),
    utilisateur_email  TEXT NOT NULL REFERENCES utilisateurs(email),
    date               TEXT NOT NULL,
    duree_minutes      INTEGER NOT NULL
);
"""


def init_db(chemin: Path | str = ":memory:") -> sqlite3.Connection:
    """Crée la connexion et les tables si elles n'existent pas."""
    con = sqlite3.connect(str(chemin))
    con.row_factory = sqlite3.Row
    con.executescript(_SCHEMA)
    return con


def inserer_salle(
    con: sqlite3.Connection,
    code: str,
    nom: str,
    capacite: int,
    type_salle: str,
    equipements: list[str],
) -> None:
    """Insère une salle dans la base."""
    with con:
        con.execute(
            "INSERT INTO salles (code, nom, capacite, type_salle, equipements_json) "
            "VALUES (?, ?, ?, ?, ?)",
            (code, nom, capacite, type_salle, json.dumps(equipements, ensure_ascii=False)),
        )


def lister_salles(con: sqlite3.Connection) -> list[dict]:
    """Liste toutes les salles."""
    cur = con.execute("SELECT code, nom, capacite, type_salle, equipements_json FROM salles")
    return [
        {
            "code": row["code"],
            "nom": row["nom"],
            "capacite": row["capacite"],
            "type_salle": row["type_salle"],
            "equipements": json.loads(row["equipements_json"]),
        }
        for row in cur.fetchall()
    ]


def inserer_utilisateur(
    con: sqlite3.Connection, email: str, nom: str, role: str = "user"
) -> None:
    """Insère un utilisateur."""
    with con:
        con.execute(
            "INSERT INTO utilisateurs (email, nom, role) VALUES (?, ?, ?)",
            (email, nom, role),
        )


def inserer_reservation(
    con: sqlite3.Connection,
    salle_code: str,
    utilisateur_email: str,
    date: str,
    duree_minutes: int,
) -> int:
    """Insère une réservation et renvoie son id."""
    with con:
        cur = con.execute(
            "INSERT INTO reservations (salle_code, utilisateur_email, date, duree_minutes) "
            "VALUES (?, ?, ?, ?)",
            (salle_code, utilisateur_email, date, duree_minutes),
        )
        return cur.lastrowid  # type: ignore[return-value]


def lister_reservations(con: sqlite3.Connection) -> list[dict]:
    """Liste toutes les réservations."""
    cur = con.execute(
        "SELECT id, salle_code, utilisateur_email, date, duree_minutes FROM reservations"
    )
    return [dict(row) for row in cur.fetchall()]


def supprimer_reservation(con: sqlite3.Connection, reservation_id: int) -> bool:
    """Supprime une réservation par id. Renvoie True si trouvée."""
    with con:
        cur = con.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        return cur.rowcount > 0
