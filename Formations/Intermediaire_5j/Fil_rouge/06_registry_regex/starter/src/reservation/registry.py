"""Registre de salles — étape 06 (starter).

TODO : implémenter SalleRegistry.
"""

from __future__ import annotations

from reservation.modeles import Salle


class SalleRegistry:
    """Registre centralisé des salles."""

    def __init__(self) -> None:
        self._salles: dict[str, Salle] = {}

    def enregistrer(self, code: str, salle: Salle) -> None:
        raise NotImplementedError

    def obtenir(self, code: str) -> Salle:
        raise NotImplementedError

    def lister(self) -> list[tuple[str, Salle]]:
        raise NotImplementedError

    def rechercher(self, pattern: str) -> list[tuple[str, Salle]]:
        raise NotImplementedError
