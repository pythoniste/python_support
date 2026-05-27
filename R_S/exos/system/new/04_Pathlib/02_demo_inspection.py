#!/usr/bin/env python3
"""Demo : inspecter un chemin réel sur le disque.

À exécuter :  python3 02_demo_inspection.py

Le script crée un dossier temporaire autonome, y écrit deux fichiers
et un sous-dossier, puis applique les méthodes d'inspection :
- existence et type (is_file / is_dir / is_symlink) ;
- métadonnées (stat : taille, mtime) ;
- chemins utiles (cwd, home) ;
- différence absolute / resolve.

Tout est nettoyé automatiquement à la fin grâce au TemporaryDirectory.
"""
import tempfile
from datetime import datetime
from pathlib import Path


def main():
    print("Dossier courant (cwd) :", Path.cwd())
    print("Dossier personnel     :", Path.home())
    print()

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        # 1. Préparer un petit décor : un fichier et un sous-dossier.
        fichier = base / "notes.txt"
        fichier.write_text("ligne 1\nligne 2\n", encoding="utf-8")
        sous_dossier = base / "archives"
        sous_dossier.mkdir()

        # 2. Existence et type.
        print("fichier.exists()       :", fichier.exists())
        print("fichier.is_file()      :", fichier.is_file())
        print("fichier.is_dir()       :", fichier.is_dir())
        print("sous_dossier.is_dir()  :", sous_dossier.is_dir())
        print("fictif.exists()        :", (base / "absent").exists())
        print()

        # 3. Métadonnées via stat().
        infos = fichier.stat()
        mtime = datetime.fromtimestamp(infos.st_mtime)
        print("Taille  :", infos.st_size, "octets")
        print("Modifié :", mtime.isoformat(timespec="seconds"))
        print()

        # 4. absolute vs resolve : sur un chemin relatif construit à la main.
        relatif = Path("..") / fichier.name
        print("relatif             :", relatif)
        print("relatif.absolute()  :", relatif.absolute())   # garde '..'
        print("relatif.resolve()   :", relatif.resolve())    # canonique


if __name__ == "__main__":
    main()
