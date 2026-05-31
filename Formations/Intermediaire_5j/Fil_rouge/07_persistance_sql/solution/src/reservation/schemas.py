"""Schémas Pydantic pour la validation et la sérialisation."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class SalleSchema(BaseModel):
    """Schéma de validation d'une salle."""

    nom: str = Field(min_length=1)
    capacite: int = Field(ge=1)
    equipements: list[str] = Field(default_factory=list)


class UtilisateurSchema(BaseModel):
    """Schéma de validation d'un utilisateur."""

    nom: str = Field(min_length=1)
    email: EmailStr


class ReservationSchema(BaseModel):
    """Schéma de validation d'une réservation."""

    salle_nom: str = Field(min_length=1)
    utilisateur_email: str
    date: datetime
    duree_minutes: int = Field(ge=15, le=480)

    @field_validator("duree_minutes")
    @classmethod
    def duree_multiple_de_15(cls, v: int) -> int:
        """La durée doit être un multiple de 15 minutes."""
        if v % 15 != 0:
            msg = f"La durée doit être un multiple de 15 (reçu : {v})."
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def date_pas_dans_le_passe(self) -> ReservationSchema:
        """La date de réservation ne doit pas être dans le passé."""
        if self.date < datetime.now():
            msg = "La date de réservation ne peut pas être dans le passé."
            raise ValueError(msg)
        return self
