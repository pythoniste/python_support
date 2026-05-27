#!/usr/bin/env python3
"""Demo : quatre manières de lire un même fichier texte.

À exécuter :  python3 01_demo_lire.py

Le script crée son propre fichier d'exemple dans un dossier temporaire,
puis le lit successivement avec read(), readline(), readlines() et par
itération. Le dossier est supprimé automatiquement à la sortie.
"""
import tempfile
from pathlib import Path


CONTENU = "roses are red\nviolets are blue\nsugar is sweet\n"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "poeme.txt"

        # Préparation : on écrit un petit fichier de trois lignes.
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(CONTENU)

        # 1) read() : tout d'un coup.
        with open(chemin, "r", encoding="utf-8") as f:
            tout = f.read()
        print("--- read() ---")
        print(repr(tout))

        # 2) readline() : à la demande, ligne par ligne.
        print("--- readline() x2 ---")
        with open(chemin, "r", encoding="utf-8") as f:
            print(repr(f.readline()))
            print(repr(f.readline()))

        # 3) readlines() : toutes les lignes en mémoire.
        with open(chemin, "r", encoding="utf-8") as f:
            lignes = f.readlines()
        print("--- readlines() ---")
        print(lignes)

        # 4) Itération : la forme à privilégier.
        print("--- for ligne in f ---")
        with open(chemin, "r", encoding="utf-8") as f:
            for ligne in f:
                # rstrip("\n") retire le saut de ligne final.
                print(ligne.rstrip("\n"))


if __name__ == "__main__":
    main()
