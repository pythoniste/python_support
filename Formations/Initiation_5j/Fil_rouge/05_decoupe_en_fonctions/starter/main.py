"""Étape 05 — Découpe en fonctions (starter).

À compléter : réorganiser le code de l'étape 04 en fonctions dédiées
avec type hints complets et docstrings.
"""

from datetime import date


def creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict:
    """Construit un dict représentant un livre."""
    raise NotImplementedError("étape 05 : implémenter creer_livre")


def ajouter_livre(catalogue: list[dict], livre: dict) -> None:
    """Ajoute un livre au catalogue (mutation en place)."""
    raise NotImplementedError("étape 05 : implémenter ajouter_livre")


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont titre ou auteur contient ``terme`` (case-insensitive)."""
    raise NotImplementedError("étape 05 : implémenter rechercher")


def trier(catalogue: list[dict], critere: str) -> list[dict]:
    """Trie une copie du catalogue selon le critère 't', 'a' ou 'n'."""
    raise NotImplementedError("étape 05 : implémenter trier")


def formater_livre(livre: dict) -> str:
    """Renvoie une chaîne formatée pour l'affichage d'un livre."""
    raise NotImplementedError("étape 05 : implémenter formater_livre")


def afficher_menu() -> None:
    """Affiche le menu principal."""
    raise NotImplementedError("étape 05 : implémenter afficher_menu")


def saisir_livre() -> dict:
    """Demande les informations d'un livre à l'utilisateur et renvoie un dict."""
    raise NotImplementedError("étape 05 : implémenter saisir_livre")


def afficher_catalogue(catalogue: list[dict]) -> None:
    """Affiche tous les livres du catalogue numérotés."""
    raise NotImplementedError("étape 05 : implémenter afficher_catalogue")


def main() -> None:
    """Boucle principale du gestionnaire de bibliothèque."""
    raise NotImplementedError("étape 05 : implémenter main")


if __name__ == "__main__":
    main()
