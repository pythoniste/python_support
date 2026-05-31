"""Logique métier du catalogue — étape 07 (starter).

À compléter : reprendre les fonctions de l'étape 06 sans les impressions.
Aucun ``print`` ni ``input`` ici.
"""

from datetime import date

from bibliotheque.exceptions import CatalogueVide, LivreExistant, LivreInvalide


def creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict:
    """Construit un livre validé."""
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def ajouter_livre(catalogue: list[dict], livre: dict) -> None:
    """Ajoute un livre au catalogue."""
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont le titre ou l'auteur contient ``terme``."""
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")


def trier(catalogue: list[dict], critere: str) -> list[dict]:
    """Trie une copie du catalogue selon 't', 'a' ou 'n'."""
    raise NotImplementedError("étape 07 : copier depuis l'étape 06")
