#!/usr/bin/env python3
"""Demo : tempfile — dossier temporaire, fichier nomme, ecriture atomique.

A executer :  python3 01_demo_tempfile.py

Le script montre les trois formes utiles : TemporaryDirectory (nettoyage
automatique), NamedTemporaryFile (acces au chemin via .name), et un
motif d'ecriture atomique avec os.replace. Il pointe aussi le piege
classique : mkdtemp ne nettoie rien.
"""
import os
import tempfile
from pathlib import Path


def main():
    # 1) Ou le systeme range-t-il les fichiers temporaires ?
    print("--- gettempdir ---")
    print(tempfile.gettempdir())

    # 2) TemporaryDirectory : la forme par defaut, avec nettoyage.
    print("--- TemporaryDirectory ---")
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        (base / "essai.txt").write_text("hello\n", encoding="utf-8")
        print("dossier :", base)
        print("contenu :", list(base.iterdir()))
    # Ici, le dossier n'existe plus du tout.
    print("dossier supprime :", not base.exists())

    # 3) NamedTemporaryFile : on a un chemin via f.name.
    print("--- NamedTemporaryFile ---")
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                     suffix=".txt", delete=True) as f:
        f.write("contenu jetable\n")
        f.flush()
        print("chemin :", f.name)
        print("existe pendant le with :", Path(f.name).exists())
    print("existe apres le with :", Path(f.name).exists())

    # 4) Ecriture atomique : on ecrit dans un fichier temporaire du
    # MEME dossier que la destination, puis on renomme.
    print("--- ecriture atomique ---")
    with tempfile.TemporaryDirectory() as tmp:
        destination = Path(tmp) / "rapport.txt"
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                         dir=destination.parent,
                                         delete=False) as f:
            f.write("contenu final\n")
            nom_tmp = f.name
        os.replace(nom_tmp, destination)
        print("destination :", destination.read_text(encoding="utf-8").strip())

    # 5) mkdtemp : DANGER, pas de nettoyage automatique. On nettoie a
    # la main pour la demo, mais le piege est de l'oublier.
    print("--- mkdtemp (DANGER) ---")
    chemin = tempfile.mkdtemp()
    print("cree   :", chemin)
    os.rmdir(chemin)
    print("supprime manuellement.")


if __name__ == "__main__":
    main()
