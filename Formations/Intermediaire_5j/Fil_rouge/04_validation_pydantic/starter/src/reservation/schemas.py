"""Schémas Pydantic — étape 04 (starter).

TODO : implémenter SalleSchema, UtilisateurSchema, ReservationSchema.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class SalleSchema(BaseModel):
    # TODO : définir les champs
    ...


class UtilisateurSchema(BaseModel):
    # TODO : définir les champs
    ...


class ReservationSchema(BaseModel):
    # TODO : définir les champs + validators
    ...
