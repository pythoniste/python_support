"""Logique métier pure du catalogue de livres.

Ce module ne connaît **ni** l'affichage **ni** la saisie. Il ne doit
contenir aucun ``print`` ou ``input``.
"""

from datetime import date

from bibliotheque.exceptions import CatalogueVide, LivreExistant, LivreInvalide


def creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict:
    """Construit un livre validé. Lève LivreInvalide en cas de donnée fautive."""
    if not titre or not titre.strip():
        raise LivreInvalide("Le titre ne peut pas être vide.")
    if not auteur or not auteur.strip():
        raise LivreInvalide("L'auteur ne peut pas être vide.")
    annee_max = date.today().year + 1
    if not isinstance(annee, int) or annee < 800 or annee > annee_max:
        raise LivreInvalide(f"L'année doit être entre 800 et {annee_max}.")
    if not (isinstance(isbn, str) and len(isbn) == 13 and isbn.isdigit()):
        raise LivreInvalide("L'ISBN doit faire 13 chiffres.")
    return {
        "titre": titre.strip(),
        "auteur": auteur.strip(),
        "annee": annee,
        "isbn": isbn,
        "date_ajout": date.today().isoformat(),
    }


def ajouter_livre(catalogue: list[dict], livre: dict) -> None:
    """Ajoute un livre au catalogue. Lève LivreExistant si l'ISBN est déjà là."""
    for existant in catalogue:
        if existant["isbn"] == livre["isbn"]:
            raise LivreExistant(f"ISBN déjà présent : {livre['isbn']}")
    catalogue.append(livre)


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont titre ou auteur contient ``terme`` (case-insensitive)."""
    if not catalogue:
        raise CatalogueVide("Le catalogue est vide.")
    terme_cf = terme.casefold()
    return [
        livre
        for livre in catalogue
        if terme_cf in livre["titre"].casefold()
        or terme_cf in livre["auteur"].casefold()
    ]


def trier(catalogue: list[dict], critere: str) -> list[dict]:
    """Trie une copie du catalogue selon 't' (titre), 'a' (auteur) ou 'n' (année)."""
    clefs = {
        "t": lambda livre: livre["titre"].casefold(),
        "a": lambda livre: livre["auteur"].casefold(),
        "n": lambda livre: livre["annee"],
    }
    if critere not in clefs:
        raise ValueError(f"Critère de tri inconnu : {critere!r}")
    return sorted(catalogue, key=clefs[critere])
