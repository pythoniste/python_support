#!/usr/bin/env python3
"""Demo : un parser minimal avec un positionnel et un optionnel.

À exécuter :

    python3 01_demo_parser.py Ada
    python3 01_demo_parser.py Ada --salutation Salut
    python3 01_demo_parser.py Ada -s Coucou
    python3 01_demo_parser.py            # erreur : nom manquant
    python3 01_demo_parser.py --help     # aide générée automatiquement

Observer :
- le positionnel `nom` est obligatoire ;
- l'optionnel `--salutation` vaut "Bonjour" par défaut (defaut explicite) ;
- `argparse` produit lui-même un message d'usage et une page d'aide.
"""
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="demo_parser",
        description="Salue quelqu'un par son prénom.",
    )
    parser.add_argument(
        "nom",
        help="prénom de la personne à saluer",
    )
    parser.add_argument(
        "--salutation", "-s",
        default="Bonjour",
        help="formule de salutation (par défaut : Bonjour)",
    )

    args = parser.parse_args()

    # `args` est un Namespace : un simple conteneur d'attributs.
    print(f"{args.salutation}, {args.nom}")


if __name__ == "__main__":
    main()
