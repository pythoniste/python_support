"""Étape 03 — Fonctions et erreurs (starter).

À compléter : découper le code en fonctions typées et ajouter
``RecetteInvalide`` pour les entrées fautives.
"""


class RecetteInvalide(ValueError):
    """Données de recette invalides."""


def creer_recette(nom: str, ingredients: list[str], temps: int) -> dict:
    raise NotImplementedError


def ajouter_recette(carnet: list[dict], recette: dict) -> None:
    raise NotImplementedError


def formater_recette(recette: dict) -> str:
    raise NotImplementedError


def saisir_recette() -> dict:
    raise NotImplementedError


def afficher_carnet(carnet: list[dict]) -> None:
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
