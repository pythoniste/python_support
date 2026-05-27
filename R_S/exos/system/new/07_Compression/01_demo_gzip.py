#!/usr/bin/env python3
"""Demo : compresser un fichier seul avec gzip, bz2 et lzma.

À exécuter :  python3 01_demo_gzip.py

Observer :
- les trois modules exposent la même API `open(path, mode)` ;
- la taille du fichier compressé varie selon l'algorithme ;
- gzip est rapide, lzma compresse mieux.

Tout se passe dans un dossier temporaire, supprimé en fin d'exécution.
"""
import bz2
import gzip
import lzma
import tempfile
from pathlib import Path


# Données très répétitives -> excellent taux de compression.
DONNEES = ("Bonjour le monde.\n" * 5000).encode("utf-8")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)

        # On écrit d'abord le fichier d'origine.
        original = racine / "donnees.txt"
        original.write_bytes(DONNEES)
        taille_origine = original.stat().st_size

        print(f"Fichier original         : {taille_origine:>8} octets")

        # Trois modules, trois extensions, même API.
        cibles = [
            (gzip, racine / "donnees.txt.gz"),
            (bz2,  racine / "donnees.txt.bz2"),
            (lzma, racine / "donnees.txt.xz"),
        ]

        for module, chemin in cibles:
            with module.open(chemin, "wb") as sortie:
                sortie.write(DONNEES)

            taille = chemin.stat().st_size
            ratio = 100 * taille / taille_origine
            print(f"  -> {chemin.name:<20} {taille:>8} octets "
                  f"({ratio:5.1f} % de l'original)")

        # Vérification : on relit et on compare octet à octet.
        print()
        print("Vérification (lecture + comparaison) :")
        for module, chemin in cibles:
            with module.open(chemin, "rb") as entree:
                relu = entree.read()
            etat = "OK" if relu == DONNEES else "ERREUR"
            print(f"  {chemin.name:<20} -> {etat}")


if __name__ == "__main__":
    main()
