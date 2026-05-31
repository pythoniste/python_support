"""Point d'entrée : ``python -m bibliotheque``."""

from pathlib import Path

from bibliotheque.catalogue import (
    ajouter_livre,
    charger_csv,
    charger_json,
    rechercher,
    sauvegarder_csv,
    sauvegarder_json,
    trier,
)
from bibliotheque.exceptions import CatalogueVide, LivreExistant
from bibliotheque.ui import afficher_catalogue, afficher_menu, saisir_livre


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
        elif choix == "5":
            chemin = Path(input("Chemin : ").strip())
            fmt = input("Format : (c)sv, (j)son : ").strip().lower()
            try:
                if fmt == "c":
                    sauvegarder_csv(catalogue, chemin)
                elif fmt == "j":
                    sauvegarder_json(catalogue, chemin)
                else:
                    print(f"❌ Format inconnu : {fmt!r}")
                    continue
            except OSError as exc:
                print(f"❌ Erreur d'écriture : {exc}")
                continue
            print(f"✅ {len(catalogue)} livres sauvegardés dans {chemin}")
        elif choix == "6":
            chemin = Path(input("Chemin : ").strip())
            try:
                if chemin.suffix == ".csv":
                    catalogue = charger_csv(chemin)
                elif chemin.suffix == ".json":
                    catalogue = charger_json(chemin)
                else:
                    print(f"❌ Extension non reconnue : {chemin.suffix}")
                    continue
            except (FileNotFoundError, ValueError) as exc:
                print(f"❌ {exc}")
                continue
            print(f"✅ {len(catalogue)} livres chargés depuis {chemin}")
        elif choix == "q":
            print("À bientôt !")
            break
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    main()
