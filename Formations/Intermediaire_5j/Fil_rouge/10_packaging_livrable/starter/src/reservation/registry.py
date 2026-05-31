"""Registre centralisé des salles."""

from __future__ import annotations

import re

from reservation.codes import valider_code
from reservation.modeles import Salle


class SalleRegistry:
    """Registre centralisé des salles avec validation des codes."""

    def __init__(self) -> None:
        self._salles: dict[str, Salle] = {}

    def enregistrer(self, code: str, salle: Salle) -> None:
        """Enregistre une salle sous un code validé."""
        if not valider_code(code):
            raise ValueError(f"Code de salle invalide : {code!r}")
        self._salles[code] = salle

    def obtenir(self, code: str) -> Salle:
        """Récupère une salle par son code."""
        if code not in self._salles:
            raise KeyError(f"Salle inconnue : {code!r}")
        return self._salles[code]

    def lister(self) -> list[tuple[str, Salle]]:
        """Liste toutes les salles enregistrées."""
        return list(self._salles.items())

    def rechercher(self, pattern: str) -> list[tuple[str, Salle]]:
        """Recherche les salles dont le code correspond au pattern regex."""
        regex = re.compile(pattern)
        return [(code, salle) for code, salle in self._salles.items() if regex.search(code)]
