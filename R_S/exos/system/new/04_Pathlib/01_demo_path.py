#!/usr/bin/env python3
"""Demo : construction et inspection « syntaxique » d'un Path.

À exécuter :  python3 01_demo_path.py

Observer :
- l'assemblage avec l'opérateur '/' ;
- la classe concrète (PosixPath ou WindowsPath) ;
- les attributs name, stem, suffix(es), parent, parents, parts ;
- les méthodes with_suffix / with_name qui renvoient un NOUVEAU Path.

Ce script ne lit pas le disque ; il manipule uniquement la forme des
chemins.
"""
from pathlib import Path


def main():
    # 1. Construction : à partir d'une chaîne, ou par assemblage.
    racine = Path("/tmp")
    fichier = racine / "donnees" / "rapport.tar.gz"
    print("Chemin construit :", fichier)
    print("Classe concrète  :", type(fichier).__name__)
    print()

    # 2. Attributs : les morceaux du chemin, sans calcul.
    print("name      :", fichier.name)        # rapport.tar.gz
    print("stem      :", fichier.stem)        # rapport.tar
    print("suffix    :", fichier.suffix)      # .gz
    print("suffixes  :", fichier.suffixes)    # ['.tar', '.gz']
    print("parent    :", fichier.parent)      # /tmp/donnees
    print("parts     :", fichier.parts)       # ('/', 'tmp', 'donnees', '...')
    print()

    # 3. parents : tous les ancêtres, du plus proche au plus lointain.
    print("Tous les parents :")
    for ancetre in fichier.parents:
        print("  -", ancetre)
    print()

    # 4. Modification : Path est immuable, on reconstruit.
    print("with_suffix('.zip')  ->", fichier.with_suffix(".zip"))
    print("with_name('autre')   ->", fichier.with_name("autre"))
    print("Original inchangé    ->", fichier)


if __name__ == "__main__":
    main()
