"""Service de réservation — étape 08 (starter).

TODO : implémenter ReservationService.
"""

from __future__ import annotations

from sqlalchemy import Engine
from sqlalchemy.orm import Session

from reservation.orm import Base


class ReservationService:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        Base.metadata.create_all(engine)

    def ajouter_salle(self, code: str, nom: str, capacite: int, type_salle: str) -> None:
        raise NotImplementedError

    def ajouter_utilisateur(self, email: str, nom: str, role: str = "user") -> None:
        raise NotImplementedError

    def reserver(self, salle_code: str, utilisateur_email: str, date: str, duree: int) -> int:
        raise NotImplementedError

    def annuler(self, reservation_id: int) -> bool:
        raise NotImplementedError

    def lister_reservations(self) -> list[dict]:
        raise NotImplementedError
