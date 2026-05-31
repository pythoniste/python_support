"""Modèles métier — étape 02 (starter).

TODO : ajouter SalleReunion, SalleFormation, surcharge d'opérateurs, from_dict.
"""

from __future__ import annotations


class Salle:
    """Une salle de l'entreprise."""

    def __init__(self, nom: str, capacite: int, equipements: list[str] | None = None):
        if not nom or not nom.strip():
            raise ValueError("Le nom de la salle ne peut pas être vide.")
        if capacite < 1:
            raise ValueError("La capacité doit être ≥ 1.")
        self.nom = nom.strip()
        self.capacite = capacite
        self.equipements = equipements if equipements is not None else []

    def a_equipement(self, nom: str) -> bool:
        nom_cf = nom.casefold()
        return any(e.casefold() == nom_cf for e in self.equipements)

    # TODO : __eq__, __lt__, __hash__

    # TODO : from_dict (classmethod)

    def __str__(self) -> str:
        return f"Salle {self.nom} ({self.capacite} places)"

    def __repr__(self) -> str:
        return (
            f"Salle(nom={self.nom!r}, capacite={self.capacite}, "
            f"equipements={self.equipements!r})"
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


# TODO : class SalleReunion(Salle): ...
# TODO : class SalleFormation(Salle): ...
