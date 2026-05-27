#!/usr/bin/env python3
"""Demo : store_true, store_false, count, append.

À exécuter :

    python3 03_demo_actions.py
    python3 03_demo_actions.py -v
    python3 03_demo_actions.py -vvv
    python3 03_demo_actions.py --sans-couleur
    python3 03_demo_actions.py -vv --inclure a --inclure b --inclure c
    python3 03_demo_actions.py --help

Observer :
- `-v` peut être répété et est compté ;
- `--couleur` vaut True par défaut, faux quand `--sans-couleur` est passé ;
- `--inclure` peut être répété, chaque occurrence ajoute à la liste ;
- `--brouillon` est un simple booléen.
"""
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="demo_actions",
        description="Démonstre store_true, store_false, count et append.",
    )
    parser.add_argument(
        "-v", "--verbeux",
        action="count",
        default=0,
        help="augmente le niveau de verbosité (répétable : -v, -vv, -vvv)",
    )
    parser.add_argument(
        "--brouillon",
        action="store_true",
        help="signale que la sortie est un brouillon",
    )
    parser.add_argument(
        "--sans-couleur",
        dest="couleur",
        action="store_false",
        help="désactive l'affichage en couleur (par défaut : activé)",
    )
    parser.add_argument(
        "--inclure",
        action="append",
        default=[],
        metavar="MOTIF",
        help="ajoute un motif à inclure (répétable)",
    )

    args = parser.parse_args()

    print(f"Verbosité : {args.verbeux}")
    print(f"Brouillon : {args.brouillon}")
    print(f"Couleur   : {args.couleur}")
    print(f"Inclure   : {args.inclure}")

    # Exemple d'utilisation du compteur de verbosité.
    if args.verbeux >= 1:
        print("[INFO]  niveau 1 atteint")
    if args.verbeux >= 2:
        print("[DEBUG] niveau 2 atteint")
    if args.verbeux >= 3:
        print("[TRACE] niveau 3 atteint")


if __name__ == "__main__":
    main()
