"""Schémas Pydantic pour l'inventaire IT."""

from __future__ import annotations

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class EquipementSchema(BaseModel):
    """Schéma de validation d'un équipement."""

    nom: str = Field(min_length=1)
    numero_serie: str
    type_equipement: Literal["portable", "ecran", "serveur", "imprimante", "autre"]
    date_achat: date
    assigne_a: str | None = None

    @field_validator("numero_serie")
    @classmethod
    def valider_numero_serie(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{2}\d{6}$", v):
            raise ValueError("Le numéro de série doit correspondre au format XX999999.")
        return v
