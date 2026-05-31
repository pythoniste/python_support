"""Persistance SQL avec sqlite3 — étape 07 (starter).

TODO : implémenter init_db et les fonctions CRUD.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path


def init_db(chemin: Path | str = ":memory:") -> sqlite3.Connection:
    """Crée la connexion et les tables si elles n'existent pas."""
    raise NotImplementedError


def inserer_salle(con: sqlite3.Connection, code: str, nom: str, capacite: int,
                  type_salle: str, equipements: list[str]) -> None:
    raise NotImplementedError


def lister_salles(con: sqlite3.Connection) -> list[dict]:
    raise NotImplementedError


def inserer_utilisateur(con: sqlite3.Connection, email: str, nom: str,
                        role: str = "user") -> None:
    raise NotImplementedError


def inserer_reservation(con: sqlite3.Connection, salle_code: str,
                        utilisateur_email: str, date: str,
                        duree_minutes: int) -> int:
    raise NotImplementedError


def lister_reservations(con: sqlite3.Connection) -> list[dict]:
    raise NotImplementedError


def supprimer_reservation(con: sqlite3.Connection, reservation_id: int) -> bool:
    raise NotImplementedError
