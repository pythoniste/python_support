"""Modèles métier du système de réservation — étape 03 (typage complet)."""

from __future__ import annotations

from typing import Any


class Salle:
    """Une salle de l'entreprise."""

    def __init__(self, nom: str, capacite: int, equipements: list[str] | None = None) -> None:
        if not nom or not nom.strip():
            raise ValueError("Le nom de la salle ne peut pas être vide.")
        if capacite < 1:
            raise ValueError("La capacité doit être ≥ 1.")
        self.nom: str = nom.strip()
        self.capacite: int = capacite
        self.equipements: list[str] = equipements if equipements is not None else []

    def a_equipement(self, nom: str) -> bool:
        """Vérifie si la salle possède un équipement (case-insensitive)."""
        nom_cf = nom.casefold()
        return any(e.casefold() == nom_cf for e in self.equipements)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Salle:
        """Crée une salle depuis un dictionnaire."""
        return cls(
            nom=data["nom"],
            capacite=data["capacite"],
            equipements=data.get("equipements", []),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Salle):
            return NotImplemented
        return self.nom == other.nom

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Salle):
            return NotImplemented
        return self.capacite < other.capacite

    def __hash__(self) -> int:
        return hash(self.nom)

    def __str__(self) -> str:
        return f"Salle {self.nom} ({self.capacite} places)"

    def __repr__(self) -> str:
        return (
            f"Salle(nom={self.nom!r}, capacite={self.capacite}, "
            f"equipements={self.equipements!r})"
        )


class SalleReunion(Salle):
    """Salle de réunion, éventuellement équipée de visioconférence."""

    def __init__(
        self,
        nom: str,
        capacite: int,
        equipements: list[str] | None = None,
        *,
        visio: bool = False,
    ) -> None:
        super().__init__(nom, capacite, equipements)
        self.visio: bool = visio

    def __str__(self) -> str:
        visio_str = ", visio" if self.visio else ""
        return f"Salle de réunion {self.nom} ({self.capacite} places{visio_str})"

    def __repr__(self) -> str:
        return (
            f"SalleReunion(nom={self.nom!r}, capacite={self.capacite}, "
            f"equipements={self.equipements!r}, visio={self.visio})"
        )


class SalleFormation(Salle):
    """Salle de formation avec postes informatiques."""

    def __init__(
        self,
        nom: str,
        capacite: int,
        equipements: list[str] | None = None,
        *,
        nb_postes: int = 0,
    ) -> None:
        super().__init__(nom, capacite, equipements)
        self.nb_postes: int = nb_postes

    def __str__(self) -> str:
        return (
            f"Salle de formation {self.nom} ({self.capacite} places, "
            f"{self.nb_postes} postes)"
        )

    def __repr__(self) -> str:
        return (
            f"SalleFormation(nom={self.nom!r}, capacite={self.capacite}, "
            f"equipements={self.equipements!r}, nb_postes={self.nb_postes})"
        )


class Utilisateur:
    """Un utilisateur du système de réservation."""

    def __init__(self, nom: str, email: str) -> None:
        if not nom or not nom.strip():
            raise ValueError("Le nom de l'utilisateur ne peut pas être vide.")
        if not email or "@" not in email:
            raise ValueError("L'email est invalide.")
        self.nom: str = nom.strip()
        self.email: str = email.strip()

    def __str__(self) -> str:
        return f"{self.nom} <{self.email}>"

    def __repr__(self) -> str:
        return f"Utilisateur(nom={self.nom!r}, email={self.email!r})"


class Reservation:
    """Une réservation de salle."""

    def __init__(
        self, salle: Salle, utilisateur: Utilisateur, date: str, duree_minutes: int
    ) -> None:
        if not date or not date.strip():
            raise ValueError("La date ne peut pas être vide.")
        if duree_minutes < 1:
            raise ValueError("La durée doit être ≥ 1 minute.")
        self.salle: Salle = salle
        self.utilisateur: Utilisateur = utilisateur
        self.date: str = date.strip()
        self.duree_minutes: int = duree_minutes

    def __str__(self) -> str:
        return (
            f"Réservation {self.salle.nom} par {self.utilisateur.nom} "
            f"le {self.date} ({self.duree_minutes} min)"
        )

    def __repr__(self) -> str:
        return (
            f"Reservation(salle={self.salle!r}, utilisateur={self.utilisateur!r}, "
            f"date={self.date!r}, duree_minutes={self.duree_minutes})"
        )
