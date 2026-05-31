"""Validation et extraction de codes de salles."""

from __future__ import annotations

import re

CODE_PATTERN = r"^(REU|FOR|AUD)-[A-Z]\d{3}$"
_CODE_RE = re.compile(CODE_PATTERN)
_CODE_FINDALL = re.compile(r"((?:REU|FOR|AUD)-[A-Z]\d{3})")


def valider_code(code: str) -> bool:
    """Vérifie si un code de salle est valide."""
    return bool(_CODE_RE.match(code))


def extraire_info(code: str) -> dict[str, str]:
    """Extrait type, bâtiment et numéro d'un code de salle."""
    m = _CODE_RE.match(code)
    if not m:
        raise ValueError(f"Code de salle invalide : {code!r}")
    type_salle = m.group(1)
    reste = code[4:]  # après "REU-"
    return {
        "type": type_salle,
        "batiment": reste[0],
        "numero": reste[1:],
    }


def trouver_codes(texte: str) -> list[str]:
    """Trouve tous les codes de salles dans un texte libre."""
    return _CODE_FINDALL.findall(texte)
