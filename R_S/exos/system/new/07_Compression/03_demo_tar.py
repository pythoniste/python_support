#!/usr/bin/env python3
"""Demo : créer, lister et extraire une archive .tar.gz.

À exécuter :  python3 03_demo_tar.py

Observer :
- tarfile.open(path, "w:gz") combine archivage et compression gzip ;
- .add(dossier) ajoute récursivement tout son contenu ;
- .getnames() liste les entrées sans extraire ;
- .extractall(..., filter="data") extrait de façon sûre.
"""
import tarfile
import tempfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)

        # Préparer une petite arborescence à archiver.
        projet = racine / "projet"
        (projet / "src").mkdir(parents=True)
        (projet / "src" / "main.py").write_text(
            "print('Bonjour')\n", encoding="utf-8")
        (projet / "README.md").write_text(
            "# Démo\n" * 50, encoding="utf-8")

        taille_brute = sum(p.stat().st_size
                           for p in projet.rglob("*") if p.is_file())

        # 1. Création de l'archive compressée en gzip.
        archive = racine / "projet.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(projet, arcname="projet")   # récursif

        taille_compr = archive.stat().st_size
        print(f"Contenu brut       : {taille_brute:>6} octets")
        print(f"Archive .tar.gz    : {taille_compr:>6} octets")

        # 2. Lister sans extraire.
        print("\nContenu interne :")
        with tarfile.open(archive, "r") as tar:
            for nom in tar.getnames():
                print(f"  - {nom}")

        # 3. Extraire avec un filtre sûr.
        sortie = racine / "extrait"
        with tarfile.open(archive, "r") as tar:
            tar.extractall(sortie, filter="data")

        print("\nFichiers extraits :")
        for chemin in sorted(sortie.rglob("*")):
            if chemin.is_file():
                rel = chemin.relative_to(sortie)
                print(f"  - {rel}")


if __name__ == "__main__":
    main()
