"""Affichage et saisie — toutes les fonctions print/input vivent ici."""

from bibliotheque.catalogue import creer_livre
from bibliotheque.exceptions import LivreInvalide
from datetime import date


def afficher_menu() -> None:
    """Affiche le menu principal."""
    print()
    print("==== Bibliothèque ====")
    print("(1) Ajouter un livre")
    print("(2) Afficher tous les livres")
    print("(3) Compter les livres")
    print("(4) Rechercher")
    print("(q) Quitter")


def formater_livre(livre: dict) -> str:
    """Renvoie une chaîne formatée pour l'affichage d'un livre."""
    return (
        f"« {livre['titre']} » — {livre['auteur']} ({livre['annee']})\n"
        f"   ISBN : {livre['isbn']}   |   Ajouté le {livre['date_ajout']}"
    )


def afficher_catalogue(catalogue: list[dict]) -> None:
    """Affiche tous les livres du catalogue numérotés."""
    if not catalogue:
        print("« Aucun livre dans le catalogue. »")
        return
    for numero, livre in enumerate(catalogue, start=1):
        print(f"{numero}. {formater_livre(livre)}")


def _saisir_champ(label: str, validateur):
    """Boucle jusqu'à obtenir une valeur acceptée par ``validateur``."""
    while True:
        brut = input(f"{label} : ")
        try:
            return validateur(brut)
        except LivreInvalide as exc:
            print(f"❌ {exc}")


def saisir_livre() -> dict:
    """Demande les informations d'un livre en bouclant sur chaque champ."""

    def valider_titre(x: str) -> str:
        if not x.strip():
            raise LivreInvalide("Le titre ne peut pas être vide.")
        return x.strip()

    def valider_auteur(x: str) -> str:
        if not x.strip():
            raise LivreInvalide("L'auteur ne peut pas être vide.")
        return x.strip()

    def valider_annee(x: str) -> int:
        try:
            n = int(x)
        except ValueError:
            raise LivreInvalide("L'année doit être un nombre entier.") from None
        annee_max = date.today().year + 1
        if n < 800 or n > annee_max:
            raise LivreInvalide(f"L'année doit être entre 800 et {annee_max}.")
        return n

    def valider_isbn(x: str) -> str:
        if not (len(x) == 13 and x.isdigit()):
            raise LivreInvalide("L'ISBN doit faire 13 chiffres.")
        return x

    titre = _saisir_champ("Titre", valider_titre)
    auteur = _saisir_champ("Auteur", valider_auteur)
    annee = _saisir_champ("Année", valider_annee)
    isbn = _saisir_champ("ISBN", valider_isbn)
    return creer_livre(titre, auteur, annee, isbn)
