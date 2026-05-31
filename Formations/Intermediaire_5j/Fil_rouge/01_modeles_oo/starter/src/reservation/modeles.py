"""Modèles métier — étape 01 (starter).

TODO : implémenter Salle, Utilisateur, Reservation.
"""

from __future__ import annotations


class Salle:
    def __init__(self, nom: str, capacite: int, equipements: list[str] | None = None):
        raise NotImplementedError

    def a_equipement(self, nom: str) -> bool:
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Utilisateur:
    def __init__(self, nom: str, email: str):
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Reservation:
    def __init__(
        self, salle: Salle, utilisateur: Utilisateur, date: str, duree_minutes: int
    ):
        raise NotImplementedError

    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
