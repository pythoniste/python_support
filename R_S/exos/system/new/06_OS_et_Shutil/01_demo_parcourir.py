#!/usr/bin/env python3
"""Demo : parcourir une arborescence avec os et pathlib.

À exécuter :  python3 01_demo_parcourir.py

Le script crée son propre dossier temporaire, le peuple avec quelques
fichiers et sous-dossiers, puis affiche son contenu de quatre manières
différentes. Le dossier temporaire est automatiquement supprimé à la
sortie du with — rien n'est laissé sur le disque de l'utilisateur.
"""
import os
import tempfile
from pathlib import Path


def peupler(racine: Path) -> None:
    """Crée une petite arborescence de test sous racine."""
    (racine / "notes.txt").write_text("a")
    (racine / "rapport.md").write_text("b")
    sous = racine / "sous_dossier"
    sous.mkdir()
    (sous / "interne.txt").write_text("c")
    (sous / "interne.log").write_text("d")
    profond = sous / "encore_plus_bas"
    profond.mkdir()
    (profond / "fond.txt").write_text("e")


with tempfile.TemporaryDirectory() as tmp:
    racine = Path(tmp)
    peupler(racine)

    print("=== os.listdir (un seul niveau, str) ===")
    for nom in sorted(os.listdir(racine)):
        print(" ", nom)

    print("\n=== Path.iterdir (un seul niveau, Path) ===")
    for p in sorted(racine.iterdir()):
        print(" ", p.name, "(dossier)" if p.is_dir() else "(fichier)")

    print("\n=== os.walk (récursif, triplets) ===")
    for dirpath, dirnames, filenames in os.walk(racine):
        rel = Path(dirpath).relative_to(racine)
        print(f"  dans {rel or '.'} :")
        for d in sorted(dirnames):
            print("    sous-dossier :", d)
        for f in sorted(filenames):
            print("    fichier      :", f)

    print("\n=== Path.rglob('*.txt') (récursif, filtré) ===")
    for p in sorted(racine.rglob("*.txt")):
        print(" ", p.relative_to(racine))

# À la sortie du with, le dossier temporaire et tout son contenu
# sont supprimés automatiquement.
print("\nDossier temporaire supprimé proprement.")
