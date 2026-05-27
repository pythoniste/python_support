#!/usr/bin/env python3
"""Demo : copier, déplacer et supprimer avec shutil.

À exécuter :  python3 02_demo_copier.py

Le script travaille intégralement dans un dossier temporaire qu'il
crée et nettoie lui-même. Aucun fichier de l'utilisateur n'est touché.

Observer :
- shutil.copy vs shutil.copy2 (métadonnées préservées ou non) ;
- shutil.copytree pour dupliquer un dossier entier ;
- shutil.move pour renommer ou déplacer ;
- shutil.rmtree qui détruit un dossier non vide (DANGER).
"""
import shutil
import tempfile
from pathlib import Path


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)

    # Préparer une mini-arborescence sous base/source.
    src = base / "source"
    src.mkdir()
    (src / "a.txt").write_text("contenu A")
    (src / "b.txt").write_text("contenu B")
    (src / "sous").mkdir()
    (src / "sous" / "c.txt").write_text("contenu C")

    # 1) shutil.copy : contenu seul.
    shutil.copy(src / "a.txt", base / "a_copie.txt")
    print("copy   :", (base / "a_copie.txt").read_text())

    # 2) shutil.copy2 : contenu + métadonnées (mtime, droits).
    shutil.copy2(src / "b.txt", base / "b_copie.txt")
    original = (src / "b.txt").stat().st_mtime
    copie = (base / "b_copie.txt").stat().st_mtime
    print(f"copy2  : mtime préservé ? {original == copie}")

    # 3) shutil.copytree : dossier entier (récursif).
    shutil.copytree(src, base / "duplicata")
    fichiers = sorted(p.name for p in (base / "duplicata").rglob("*"))
    print("tree   :", fichiers)

    # 4) shutil.move : renommer (même FS donc instantané).
    shutil.move(base / "a_copie.txt", base / "renomme.txt")
    print("move   : renomme.txt existe ?", (base / "renomme.txt").exists())

    # 5) shutil.rmtree : suppression récursive (DANGER en vrai).
    # Ici on est dans un dossier temporaire — pas de risque.
    cible = base / "duplicata"
    print("rmtree : suppression de", cible.name, "...")
    shutil.rmtree(cible)
    print("rmtree :", cible.name, "existe encore ?", cible.exists())

print("\nDossier temporaire supprimé proprement.")
