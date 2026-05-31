"""Point d'entrée CLI du package recettes.

Installé comme ``recettes`` via ``[project.scripts]``.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from recettes.carnet import ajouter_recette, charger, sauvegarder
from recettes.ui import afficher_carnet, afficher_menu, saisir_recette

logger = logging.getLogger("recettes")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="recettes",
        description="Carnet de recettes de votre petit frère.",
    )
    parser.add_argument(
        "--charger",
        type=Path,
        default=None,
        metavar="FICHIER",
        help="Charge un carnet JSON au démarrage",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Active les logs de debug",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée CLI."""
    args = _parser().parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    carnet: list[dict] = []
    if args.charger is not None:
        try:
            carnet = charger(args.charger)
            print(f"Chargement : {len(carnet)} recettes depuis {args.charger}")
        except (FileNotFoundError, ValueError) as exc:
            logger.warning("Chargement initial echoue : %s", exc)
            print(f"Erreur : {exc}")

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip().lower()
        if choix == "1":
            try:
                recette = saisir_recette()
            except Exception as exc:
                print(f"Erreur : {exc}")
                continue
            ajouter_recette(carnet, recette)
            print(f"Recette ajoutee : {recette['nom']}")
        elif choix == "2":
            afficher_carnet(carnet)
        elif choix == "3":
            chemin = Path(input("Chemin du fichier : ").strip())
            try:
                sauvegarder(carnet, chemin)
            except OSError as exc:
                logger.warning("Erreur d'ecriture : %s", exc)
                print(f"Erreur : {exc}")
                continue
            print(f"{len(carnet)} recettes sauvegardees dans {chemin}")
        elif choix == "4":
            chemin = Path(input("Chemin du fichier : ").strip())
            try:
                carnet = charger(chemin)
            except (FileNotFoundError, ValueError) as exc:
                logger.warning("Chargement echoue : %s", exc)
                print(f"Erreur : {exc}")
                continue
            print(f"{len(carnet)} recettes chargees depuis {chemin}")
        elif choix == "q":
            print("A bientot !")
            return 0
        else:
            print(f"Choix inconnu : {choix!r}")


if __name__ == "__main__":
    raise SystemExit(main())
