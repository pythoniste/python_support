"""Interface utilisateur — étape 07 (starter).

À compléter : afficher le menu, saisir un livre, afficher le catalogue.
Toutes les fonctions ``print``/``input`` vivent ici.
"""

from bibliotheque.catalogue import creer_livre
from bibliotheque.exceptions import LivreInvalide


def afficher_menu() -> None:
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def saisir_livre() -> dict:
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def formater_livre(livre: dict) -> str:
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def afficher_catalogue(catalogue: list[dict]) -> None:
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")
