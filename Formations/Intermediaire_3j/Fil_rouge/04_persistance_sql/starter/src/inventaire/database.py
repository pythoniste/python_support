"""Persistance SQL — étape 04 (starter).

TODO : implémenter init_db et les fonctions CRUD.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


def init_db(chemin: Path | str = ":memory:") -> sqlite3.Connection:
    raise NotImplementedError


def inserer_equipement(con: sqlite3.Connection, nom: str, numero_serie: str,
                       type_eq: str, date_achat: str) -> None:
    raise NotImplementedError


def lister_equipements(con: sqlite3.Connection) -> list[dict]:
    raise NotImplementedError


def assigner_equipement(con: sqlite3.Connection, numero_serie: str,
                        utilisateur: str) -> bool:
    raise NotImplementedError


def supprimer_equipement(con: sqlite3.Connection, numero_serie: str) -> bool:
    raise NotImplementedError
