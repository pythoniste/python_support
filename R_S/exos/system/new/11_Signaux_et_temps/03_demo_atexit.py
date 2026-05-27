#!/usr/bin/env python3
"""Demo : ordre LIFO des fonctions atexit.

À exécuter :  python3 03_demo_atexit.py

Observer :
- les trois fonctions sont enregistrées dans l'ordre A, B, C ;
- à la sortie, elles s'exécutent dans l'ordre inverse : C, B, A ;
- atexit tourne aussi sur sys.exit(...) (sortie normale).

Pour vérifier qu'os._exit court-circuite atexit, décommenter la ligne
correspondante en bas du main : aucune des trois fonctions ne sera
appelée.
"""
import atexit
import os
import sys


def nettoyer(nom):
    print(f"  -> nettoyage {nom}")


def main():
    print("Enregistrement de trois fonctions de nettoyage.")
    atexit.register(nettoyer, "A (enregistré en premier)")
    atexit.register(nettoyer, "B (enregistré en deuxième)")
    atexit.register(nettoyer, "C (enregistré en dernier)")

    print("Travail simulé du programme...")
    print("Sortie via sys.exit(0) : atexit va s'exécuter.")
    sys.exit(0)

    # Décommenter pour voir qu'os._exit saute atexit :
    # os._exit(0)


if __name__ == "__main__":
    main()
