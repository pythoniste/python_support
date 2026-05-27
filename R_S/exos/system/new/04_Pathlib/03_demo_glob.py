#!/usr/bin/env python3
"""Demo : parcourir et filtrer une arborescence avec iterdir / glob / rglob.

À exécuter :  python3 03_demo_glob.py

Le script crée un dossier temporaire avec une mini-arborescence :

    racine/
        a.py
        b.py
        notes.txt
        sub/
            c.py
            d.md

Puis il montre :
- iterdir  : un seul niveau, sans filtre ;
- glob     : un seul niveau, avec motif (*.py, [a-c]*.py) ;
- rglob    : récursif, équivalent à glob('**/...').
"""
import tempfile
from pathlib import Path


def preparer(racine: Path) -> None:
    """Crée la petite arborescence décrite dans le docstring."""
    (racine / "a.py").write_text("# a\n")
    (racine / "b.py").write_text("# b\n")
    (racine / "notes.txt").write_text("texte\n")
    sub = racine / "sub"
    sub.mkdir()
    (sub / "c.py").write_text("# c\n")
    (sub / "d.md").write_text("# d\n")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)
        preparer(racine)

        print("Contenu direct (iterdir) :")
        for entree in sorted(racine.iterdir()):
            marque = "/" if entree.is_dir() else " "
            print(f"  [{marque}] {entree.name}")
        print()

        print("Motif '*.py' (glob, un seul niveau) :")
        for p in sorted(racine.glob("*.py")):
            print("  -", p.relative_to(racine))
        print()

        print("Motif '[a-c]*.py' (jeu de caractères) :")
        for p in sorted(racine.glob("[a-c]*.py")):
            print("  -", p.relative_to(racine))
        print()

        print("Motif '*.py' récursif (rglob) :")
        for p in sorted(racine.rglob("*.py")):
            print("  -", p.relative_to(racine))


if __name__ == "__main__":
    main()
