"""Modèles SQLAlchemy ORM — étape 08 (starter).

TODO : définir Base, SalleORM, UtilisateurORM, ReservationORM.
"""

from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class SalleORM(Base):
    __tablename__ = "salles"
    # TODO : colonnes et relations
    ...


class UtilisateurORM(Base):
    __tablename__ = "utilisateurs"
    # TODO : colonnes et relations
    ...


class ReservationORM(Base):
    __tablename__ = "reservations"
    # TODO : colonnes et relations
    ...
