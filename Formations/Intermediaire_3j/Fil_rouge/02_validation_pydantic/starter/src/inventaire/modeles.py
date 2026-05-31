"""Modèles métier de l'inventaire IT."""

from __future__ import annotations


class Equipement:
    """Un équipement informatique."""

    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 assigne_a: str | None = None) -> None:
        if not nom or not nom.strip():
            raise ValueError("Le nom ne peut pas être vide.")
        if not numero_serie or not numero_serie.strip():
            raise ValueError("Le numéro de série ne peut pas être vide.")
        self.nom: str = nom.strip()
        self.numero_serie: str = numero_serie.strip()
        self.date_achat: str = date_achat.strip()
        self.assigne_a: str | None = assigne_a

    def assigner(self, nom_utilisateur: str) -> None:
        """Assigne l'équipement à un utilisateur."""
        self.assigne_a = nom_utilisateur

    def desassigner(self) -> None:
        """Retire l'assignation."""
        self.assigne_a = None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equipement):
            return NotImplemented
        return self.numero_serie == other.numero_serie

    def __hash__(self) -> int:
        return hash(self.numero_serie)

    def __str__(self) -> str:
        assignation = f" -> {self.assigne_a}" if self.assigne_a else ""
        return f"{self.nom} [{self.numero_serie}]{assignation}"

    def __repr__(self) -> str:
        return f"Equipement(nom={self.nom!r}, numero_serie={self.numero_serie!r})"


class Portable(Equipement):
    """Ordinateur portable."""

    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 ram_go: int, **kwargs) -> None:
        super().__init__(nom, numero_serie, date_achat, **kwargs)
        self.ram_go: int = ram_go

    def __str__(self) -> str:
        return f"Portable {self.nom} [{self.numero_serie}] ({self.ram_go} Go RAM)"


class Ecran(Equipement):
    """Écran."""

    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 taille_pouces: float, **kwargs) -> None:
        super().__init__(nom, numero_serie, date_achat, **kwargs)
        self.taille_pouces: float = taille_pouces

    def __str__(self) -> str:
        return f"Écran {self.nom} [{self.numero_serie}] ({self.taille_pouces}\")"


class Serveur(Equipement):
    """Serveur."""

    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 nb_cpu: int, **kwargs) -> None:
        super().__init__(nom, numero_serie, date_achat, **kwargs)
        self.nb_cpu: int = nb_cpu

    def __str__(self) -> str:
        return f"Serveur {self.nom} [{self.numero_serie}] ({self.nb_cpu} CPUs)"
