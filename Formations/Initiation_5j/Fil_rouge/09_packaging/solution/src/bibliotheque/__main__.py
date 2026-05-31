"""Point d'entrée CLI du package bibliotheque.

Installé comme ``bibliotheque`` via ``[project.scripts]``.
"""

from __future__ import annotations

import argparse
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


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bibliotheque",
        description="Gestionnaire de bibliothèque personnelle.",
    )
    parser.add_argument(
        "--charger",
        type=Path,
        default=None,
        metavar="FICHIER",
        help="Charge un catalogue au démarrage",
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="json",
        help="Format par défaut pour les sauvegardes (défaut: json)",
    )
    return parser


def _charger_depuis(chemin: Path) -> list[dict]:
    if chemin.suffix == ".csv":
        return charger_csv(chemin)
    if chemin.suffix == ".json":
        return charger_json(chemin)
    raise ValueError(f"Extension non reconnue : {chemin.suffix}")


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI."""
    args = _parser().parse_args(argv)
    catalogue: list[dict] = []
    if args.charger is not None:
        try:
            catalogue = _charger_depuis(args.charger)
            print(f"✅ {len(catalogue)} livres chargés depuis {args.charger}")
        except (FileNotFoundError, ValueError) as exc:
            print(f"❌ {exc}")

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
            fmt = input(f"Format [{args.format}] : ").strip().lower() or args.format[0]
            try:
                if fmt in ("c", "csv"):
                    sauvegarder_csv(catalogue, chemin)
                elif fmt in ("j", "json"):
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
                catalogue = _charger_depuis(chemin)
            except (FileNotFoundError, ValueError) as exc:
                print(f"❌ {exc}")
                continue
            print(f"✅ {len(catalogue)} livres chargés depuis {chemin}")
        elif choix == "q":
            print("À bientôt !")
            return 0
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    raise SystemExit(main())
