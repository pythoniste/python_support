#!/usr/bin/env python3
"""Demo : interpolation et format spec des f-strings.

À exécuter :  python3 02_demo_fstrings.py

Observer :
- l'interpolation de variables et d'expressions ;
- l'alignement (<>^) et la largeur ;
- la précision .2f et le séparateur de milliers ;
- le format de débogage {x=}.
"""
import math


def main():
    # 1) Interpolation simple.
    nom, age = "Ada", 36
    print(f"{nom} a {age} ans")

    # 2) Expression quelconque entre {} : appel de fonction, calcul, etc.
    print(f"Longueur du prénom : {len(nom)}")
    print(f"Dans 10 ans : {age + 10}")
    print(f"sqrt(2) = {math.sqrt(2):.4f}")

    # 3) Alignement et largeur.
    #    On utilise des crochets pour rendre la largeur visible à l'œil.
    print(f"[{'gauche':<10}]")    # [gauche    ]
    print(f"[{'droite':>10}]")    # [    droite]
    print(f"[{'centre':^10}]")    # [  centre  ]
    print(f"[{'rempli':*^10}]")   # [**rempli**]

    # 4) Précision et type pour les nombres.
    pi = math.pi
    print(f"pi brut       : {pi}")
    print(f"pi à 2 déc.   : {pi:.2f}")
    print(f"pi à 6 déc.   : {pi:.6f}")
    print(f"255 en binaire: {255:b}")
    print(f"255 en hex    : {255:x}")
    print(f"5 %           : {0.05:.1%}")

    # 5) Séparateur de milliers.
    n = 1234567
    print(f"{n:,}")     # 1,234,567
    print(f"{n:_}")     # 1_234_567

    # 6) Petit tableau aligné.
    articles = [("café", 1.5), ("croissant", 1.2), ("éclair", 3.45)]
    print()
    for nom_art, prix in articles:
        print(f"{nom_art:<12} {prix:>6.2f} €")

    # 7) Format de débogage : nom de l'expression ET valeur.
    x = 42
    print()
    print(f"{x=}")
    print(f"{x * 2=}")
    print(f"{math.pi=:.3f}")


if __name__ == "__main__":
    main()
