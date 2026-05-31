"""Modèles métier — étape 03 (starter).

TODO : ajouter les type hints manquants pour que mypy --strict passe.
Copie de la solution étape 02. Les annotations sont partiellement présentes.
"""

from __future__ import annotations


class Salle:
    def __init__(self, nom: str, capacite: int, equipements: list[str] | None = None):
        if not nom or not nom.strip():
            raise ValueError("Le nom de la salle ne peut pas être vide.")
        if capacite < 1:
            raise ValueError("La capacité doit être ≥ 1.")
        self.nom = nom.strip()
        self.capacite = capacite
        self.equipements: list[str] = equipements if equipements is not None else []

    def a_equipement(self, nom: str) -> bool:
        nom_cf = nom.casefold()
        return any(e.casefold() == nom_cf for e in self.equipements)

    @classmethod
    def from_dict(cls, data: dict) -> Salle:  # TODO: typer data plus finement
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
    def __init__(
        self,
        nom: str,
        capacite: int,
        equipements: list[str] | None = None,
        *,
        visio: bool = False,
    ):
        super().__init__(nom, capacite, equipements)
        self.visio = visio

    def __str__(self) -> str:
        visio_str = ", visio" if self.visio else ""
        return f"Salle de réunion {self.nom} ({self.capacite} places{visio_str})"

    def __repr__(self) -> str:
        return (
            f"SalleReunion(nom={self.nom!r}, capacite={self.capacite}, "
            f"equipements={self.equipements!r}, visio={self.visio})"
        )


class SalleFormation(Salle):
    def __init__(
        self,
        nom: str,
        capacite: int,
        equipements: list[str] | None = None,
        *,
        nb_postes: int = 0,
    ):
        super().__init__(nom, capacite, equipements)
        self.nb_postes = nb_postes

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
    def __init__(self, nom: str, email: str):
        if not nom or not nom.strip():
            raise ValueError("Le nom de l'utilisateur ne peut pas être vide.")
        if not email or "@" not in email:
            raise ValueError("L'email est invalide.")
        self.nom = nom.strip()
        self.email = email.strip()

    def __str__(self) -> str:
        return f"{self.nom} <{self.email}>"

    def __repr__(self) -> str:
        return f"Utilisateur(nom={self.nom!r}, email={self.email!r})"


class Reservation:
    def __init__(
        self, salle: Salle, utilisateur: Utilisateur, date: str, duree_minutes: int
    ):
        if not date or not date.strip():
            raise ValueError("La date ne peut pas être vide.")
        if duree_minutes < 1:
            raise ValueError("La durée doit être ≥ 1 minute.")
        self.salle = salle
        self.utilisateur = utilisateur
        self.date = date.strip()
        self.duree_minutes = duree_minutes

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
