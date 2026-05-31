"""Service de réservation utilisant SQLAlchemy ORM."""

from __future__ import annotations

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from reservation.orm import Base, ReservationORM, SalleORM, UtilisateurORM


class ReservationService:
    """Couche service pour les opérations de réservation."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        Base.metadata.create_all(engine)

    def ajouter_salle(self, code: str, nom: str, capacite: int, type_salle: str) -> None:
        """Ajoute une salle dans la base."""
        with Session(self.engine) as session:
            salle = SalleORM(code=code, nom=nom, capacite=capacite, type_salle=type_salle)
            session.add(salle)
            session.commit()

    def ajouter_utilisateur(self, email: str, nom: str, role: str = "user") -> None:
        """Ajoute un utilisateur dans la base."""
        with Session(self.engine) as session:
            user = UtilisateurORM(email=email, nom=nom, role=role)
            session.add(user)
            session.commit()

    def reserver(
        self, salle_code: str, utilisateur_email: str, date: str, duree: int
    ) -> int:
        """Crée une réservation et renvoie son id."""
        with Session(self.engine) as session:
            resa = ReservationORM(
                salle_code=salle_code,
                utilisateur_email=utilisateur_email,
                date=date,
                duree_minutes=duree,
            )
            session.add(resa)
            session.commit()
            session.refresh(resa)
            return resa.id

    def annuler(self, reservation_id: int) -> bool:
        """Annule une réservation. Renvoie True si trouvée."""
        with Session(self.engine) as session:
            resa = session.get(ReservationORM, reservation_id)
            if resa is None:
                return False
            session.delete(resa)
            session.commit()
            return True

    def lister_reservations(self) -> list[dict]:
        """Liste toutes les réservations."""
        with Session(self.engine) as session:
            stmt = select(ReservationORM)
            resas = session.scalars(stmt).all()
            return [
                {
                    "id": r.id,
                    "salle_code": r.salle_code,
                    "utilisateur_email": r.utilisateur_email,
                    "date": r.date,
                    "duree_minutes": r.duree_minutes,
                }
                for r in resas
            ]
