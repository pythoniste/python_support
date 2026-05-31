"""Étape 06 — Gestion des erreurs.

Ajoute trois exceptions personnalisées et valide les entrées avec
``creer_livre`` et ``ajouter_livre``. La saisie boucle tant que l'entrée
n'est pas valide.
"""

from datetime import date


class LivreInvalide(ValueError):
    """Données de livre invalides (titre, auteur, année, ISBN)."""


class LivreExistant(Exception):
    """ISBN déjà présent dans le catalogue."""


class CatalogueVide(Exception):
    """Catalogue vide : opération impossible."""


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
    """Ajoute un livre au catalogue. Lève LivreExistant si l'ISBN existe déjà."""
    for existant in catalogue:
        if existant["isbn"] == livre["isbn"]:
            raise LivreExistant(f"ISBN déjà présent : {livre['isbn']}")
    catalogue.append(livre)


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont titre ou auteur contient ``terme``."""
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
    """Trie une copie du catalogue selon 't', 'a' ou 'n'."""
    clefs = {
        "t": lambda livre: livre["titre"].casefold(),
        "a": lambda livre: livre["auteur"].casefold(),
        "n": lambda livre: livre["annee"],
    }
    if critere not in clefs:
        raise ValueError(f"Critère de tri inconnu : {critere!r}")
    return sorted(catalogue, key=clefs[critere])


def formater_livre(livre: dict) -> str:
    """Renvoie une chaîne formatée pour l'affichage d'un livre."""
    return (
        f"« {livre['titre']} » — {livre['auteur']} ({livre['annee']})\n"
        f"   ISBN : {livre['isbn']}   |   Ajouté le {livre['date_ajout']}"
    )


def afficher_menu() -> None:
    """Affiche le menu principal."""
    print()
    print("==== Bibliothèque ====")
    print("(1) Ajouter un livre")
    print("(2) Afficher tous les livres")
    print("(3) Compter les livres")
    print("(4) Rechercher")
    print("(q) Quitter")


def _saisir_champ(label: str, validateur) -> str | int:
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
    assert isinstance(titre, str)
    assert isinstance(auteur, str)
    assert isinstance(annee, int)
    assert isinstance(isbn, str)
    return creer_livre(titre, auteur, annee, isbn)


def afficher_catalogue(catalogue: list[dict]) -> None:
    """Affiche tous les livres du catalogue numérotés."""
    if not catalogue:
        print("« Aucun livre dans le catalogue. »")
        return
    for numero, livre in enumerate(catalogue, start=1):
        print(f"{numero}. {formater_livre(livre)}")


def main() -> None:
    """Boucle principale du gestionnaire de bibliothèque."""
    catalogue: list[dict] = []
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip().lower()
        if choix == "1":
            livre = saisir_livre()
            try:
                ajouter_livre(catalogue, livre)
            except LivreExistant as exc:
                print(f"❌ {exc}")
                continue
            print(f"✅ Ajouté le {livre['date_ajout']}.")
        elif choix == "2":
            if not catalogue:
                print("« Aucun livre dans le catalogue. »")
                continue
            critere = input("Trier par : (t)itre, (a)uteur, a(n)née : ").strip().lower()
            try:
                tries = trier(catalogue, critere)
            except ValueError as exc:
                print(f"❌ {exc}")
                continue
            afficher_catalogue(tries)
        elif choix == "3":
            total = len(catalogue)
            mot = "livre" if total < 2 else "livres"
            print(f"Le catalogue contient {total} {mot}.")
        elif choix == "4":
            terme = input("Rechercher : ").strip()
            try:
                resultats = rechercher(catalogue, terme)
            except CatalogueVide as exc:
                print(f"❌ {exc}")
                continue
            print(f"Résultats ({len(resultats)}) :")
            afficher_catalogue(resultats)
        elif choix == "q":
            print("À bientôt !")
            break
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    main()
