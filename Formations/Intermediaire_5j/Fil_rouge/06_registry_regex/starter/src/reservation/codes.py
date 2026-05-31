"""Validation et extraction de codes de salles — étape 06 (starter).

TODO : implémenter valider_code, extraire_info, trouver_codes.
"""

from __future__ import annotations

import re

CODE_PATTERN = r"^(REU|FOR|AUD)-[A-Z]\d{3}$"


def valider_code(code: str) -> bool:
    raise NotImplementedError


def extraire_info(code: str) -> dict[str, str]:
    raise NotImplementedError


def trouver_codes(texte: str) -> list[str]:
    raise NotImplementedError
