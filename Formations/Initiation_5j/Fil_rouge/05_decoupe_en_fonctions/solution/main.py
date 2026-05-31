"""Étape 05 — Découpe en fonctions avec type hints.

Refactoring pur : le comportement est identique à l'étape 04, mais le code
est réparti dans des fonctions à responsabilité unique avec des type hints
complets et des docstrings courtes.
"""

from datetime import date


def creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict:
    """Construit un dict représentant un livre avec sa date d'ajout."""
    return {
        "titre": titre,
        "auteur": auteur,
        "annee": annee,
        "isbn": isbn,
        "date_ajout": date.today().isoformat(),
    }


def ajouter_livre(catalogue: list[dict], livre: dict) -> None:
    """Ajoute un livre au catalogue (mutation en place)."""
    catalogue.append(livre)


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont titre ou auteur contient ``terme`` (case-insensitive)."""
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


def saisir_livre() -> dict:
    """Demande les informations d'un livre à l'utilisateur."""
    titre = input("Titre : ")
    auteur = input("Auteur : ")
    annee = int(input("Année : "))
    isbn = input("ISBN : ")
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
            ajouter_livre(catalogue, livre)
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
            if not catalogue:
                print("« Aucun livre dans le catalogue. »")
                continue
            terme = input("Rechercher : ").strip()
            resultats = rechercher(catalogue, terme)
            print(f"Résultats ({len(resultats)}) :")
            afficher_catalogue(resultats)
        elif choix == "q":
            print("À bientôt !")
            break
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    main()
