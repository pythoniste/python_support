"""Modèles SQLAlchemy ORM pour le système de réservation."""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class SalleORM(Base):
    __tablename__ = "salles"

    code: Mapped[str] = mapped_column(String(10), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    capacite: Mapped[int] = mapped_column(Integer, nullable=False)
    type_salle: Mapped[str] = mapped_column(String(20), nullable=False)

    reservations: Mapped[list[ReservationORM]] = relationship(back_populates="salle")

    def __repr__(self) -> str:
        return f"SalleORM(code={self.code!r}, nom={self.nom!r}, capacite={self.capacite})"


class UtilisateurORM(Base):
    __tablename__ = "utilisateurs"

    email: Mapped[str] = mapped_column(String(200), primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="user")

    reservations: Mapped[list[ReservationORM]] = relationship(back_populates="utilisateur")

    def __repr__(self) -> str:
        return f"UtilisateurORM(email={self.email!r}, nom={self.nom!r})"


class ReservationORM(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    salle_code: Mapped[str] = mapped_column(ForeignKey("salles.code"), nullable=False)
    utilisateur_email: Mapped[str] = mapped_column(
        ForeignKey("utilisateurs.email"), nullable=False
    )
    date: Mapped[str] = mapped_column(String(30), nullable=False)
    duree_minutes: Mapped[int] = mapped_column(Integer, nullable=False)

    salle: Mapped[SalleORM] = relationship(back_populates="reservations")
    utilisateur: Mapped[UtilisateurORM] = relationship(back_populates="reservations")

    def __repr__(self) -> str:
        return (
            f"ReservationORM(id={self.id}, salle={self.salle_code!r}, "
            f"date={self.date!r}, duree={self.duree_minutes})"
        )
