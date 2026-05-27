#!/usr/bin/env python3
"""Demo : conversion de type, choix fermé, nargs, default, metavar.

À exécuter :

    python3 02_demo_types.py 3 4 5
    python3 02_demo_types.py 3 4 5 --operation produit
    python3 02_demo_types.py 3 4 5 --operation somme --precision 2
    python3 02_demo_types.py 3 4 abc       # erreur : "abc" n'est pas un float
    python3 02_demo_types.py --operation xor  # erreur : choix invalide
    python3 02_demo_types.py --help

Observer :
- les valeurs sont converties en `float` ; un mauvais argument
  déclenche un message d'erreur lisible (code retour 2) ;
- `nargs="+"` rend `nombres` toujours non vide ;
- `metavar="N"` change l'étiquette dans l'aide.
"""
import argparse
from functools import reduce


def main():
    parser = argparse.ArgumentParser(
        prog="demo_types",
        description="Combine plusieurs nombres par une opération donnée.",
    )
    parser.add_argument(
        "nombres",
        type=float,
        nargs="+",                       # au moins un nombre
        metavar="N",
        help="liste des nombres à combiner",
    )
    parser.add_argument(
        "--operation", "-o",
        choices=["somme", "produit", "max"],
        default="somme",
        help="opération à appliquer (par défaut : somme)",
    )
    parser.add_argument(
        "--precision", "-p",
        type=int,
        default=3,
        help="nombre de décimales dans l'affichage (par défaut : 3)",
    )

    args = parser.parse_args()

    if args.operation == "somme":
        resultat = sum(args.nombres)
    elif args.operation == "produit":
        resultat = reduce(lambda a, b: a * b, args.nombres, 1.0)
    else:  # max
        resultat = max(args.nombres)

    print(f"{args.operation}({args.nombres}) = {resultat:.{args.precision}f}")


if __name__ == "__main__":
    main()
