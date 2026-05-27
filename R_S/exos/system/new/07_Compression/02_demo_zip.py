#!/usr/bin/env python3
"""Demo : créer, lister et extraire une archive ZIP.

À exécuter :  python3 02_demo_zip.py

Observer :
- write(path, arcname) ajoute un fichier du disque ;
- writestr(name, donnees) ajoute du contenu venu de la mémoire ;
- namelist() liste les entrées sans extraire ;
- extractall() restaure l'arborescence dans un dossier cible.
"""
import tempfile
import zipfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)

        # Préparer deux fichiers d'entrée.
        (racine / "rapport.txt").write_text(
            "Compte rendu\n" * 200, encoding="utf-8")
        sous_dossier = racine / "medias"
        sous_dossier.mkdir()
        (sous_dossier / "note.txt").write_text(
            "Pense-bête\n", encoding="utf-8")

        # 1. Création de l'archive.
        archive = racine / "documents.zip"
        with zipfile.ZipFile(archive, "w",
                             compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(racine / "rapport.txt", arcname="rapport.txt")
            zf.write(sous_dossier / "note.txt",
                     arcname="medias/note.txt")
            # Contenu généré en mémoire (pas de fichier source).
            zf.writestr("genere.txt", "Contenu en mémoire\n")

        print(f"Archive créée : {archive.name} "
              f"({archive.stat().st_size} octets)")

        # 2. Lister sans extraire.
        print("\nContenu interne :")
        with zipfile.ZipFile(archive, "r") as zf:
            for nom in zf.namelist():
                print(f"  - {nom}")

        # 3. Extraire dans un dossier dédié.
        sortie = racine / "extrait"
        with zipfile.ZipFile(archive, "r") as zf:
            zf.extractall(sortie)

        print("\nFichiers extraits :")
        for chemin in sorted(sortie.rglob("*")):
            if chemin.is_file():
                rel = chemin.relative_to(sortie)
                print(f"  - {rel}  ({chemin.stat().st_size} octets)")


if __name__ == "__main__":
    main()
