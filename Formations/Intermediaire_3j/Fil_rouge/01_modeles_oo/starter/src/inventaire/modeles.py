"""Modèles métier — étape 01 (starter).

TODO : implémenter Equipement, Portable, Ecran, Serveur.
"""

from __future__ import annotations


class Equipement:
    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 assigne_a: str | None = None):
        raise NotImplementedError

    def assigner(self, nom_utilisateur: str) -> None:
        raise NotImplementedError

    def desassigner(self) -> None:
        raise NotImplementedError


class Portable(Equipement):
    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 ram_go: int, **kwargs):
        raise NotImplementedError


class Ecran(Equipement):
    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 taille_pouces: float, **kwargs):
        raise NotImplementedError


class Serveur(Equipement):
    def __init__(self, nom: str, numero_serie: str, date_achat: str,
                 nb_cpu: int, **kwargs):
        raise NotImplementedError
