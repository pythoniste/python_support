#!/usr/bin/env python3
"""Demo : tous les paramètres de print() en action.

À exécuter :  python3 01_demo_print.py

Observer :
- l'effet de sep et end ;
- l'écriture sur stderr ;
- l'effet de flush=True sur l'apparition progressive d'une ligne.
"""
import sys
import time


def main():
    # 1) sep : changer ce qui sépare les valeurs.
    print("a", "b", "c")               # a b c       (espace par défaut)
    print("a", "b", "c", sep="-")      # a-b-c
    print("a", "b", "c", sep="")       # abc
    print("a", "b", "c", sep="\n")     # une valeur par ligne

    # 2) end : changer ce qui termine la ligne.
    print("---")
    print("sans saut", end=" | ")
    print("collé sur la même ligne")

    # 3) file : viser stderr au lieu de stdout.
    #    Depuis un terminal, les deux flux s'affichent ensemble,
    #    mais on peut les rediriger séparément avec > et 2>.
    print("Resultat utile (stdout)")
    print("Avertissement (stderr)", file=sys.stderr)

    # 4) flush : forcer l'affichage immédiat, avant le saut de ligne.
    #    Sans flush=True, on verrait "Chargement... OK" d'un seul coup
    #    parce que le tampon n'est vidé qu'au saut de ligne final.
    print("Chargement", end="", flush=True)
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print(" OK")


if __name__ == "__main__":
    main()
