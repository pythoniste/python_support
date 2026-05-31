"""Métier et persistance du carnet — étape 05 (starter).

À compléter : copier les fonctions de l'étape 04.
Aucun ``print`` ni ``input`` ici.
"""


class RecetteInvalide(ValueError):
    """Données de recette invalides."""


def creer_recette(nom: str, ingredients: list[str], temps: int) -> dict:
    raise NotImplementedError


def ajouter_recette(carnet: list[dict], recette: dict) -> None:
    raise NotImplementedError


def sauvegarder(carnet: list[dict], chemin) -> None:
    raise NotImplementedError


def charger(chemin) -> list[dict]:
    raise NotImplementedError
