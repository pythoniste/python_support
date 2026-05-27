#!/usr/bin/env python3
"""Demo : modes d'écriture w / a / x, et trois méthodes pour écrire.

À exécuter :  python3 02_demo_ecrire.py

Le script crée tous ses fichiers dans un dossier temporaire, puis
réaffiche leur contenu pour observer la différence entre les modes et
entre write/writelines/print.
"""
import tempfile
from pathlib import Path


def afficher(titre, chemin):
    print(f"--- {titre} ---")
    with open(chemin, "r", encoding="utf-8") as f:
        print(f.read(), end="")
    print()


def main():
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "notes.txt"

        # Mode "w" : on écrase ce qu'il y avait. write() n'ajoute
        # pas de \n automatique : à nous de l'inclure.
        with open(chemin, "w", encoding="utf-8") as f:
            f.write("premiere ligne\n")
            f.write("seconde ligne\n")
        afficher("apres mode w", chemin)

        # Mode "a" : on ajoute à la fin sans rien toucher.
        with open(chemin, "a", encoding="utf-8") as f:
            f.write("troisieme ligne (ajoutee)\n")
        afficher("apres mode a", chemin)

        # writelines() écrit une liste de chaînes brutes : pas de \n
        # ajouté non plus.
        chemin_lettres = Path(tmp) / "lettres.txt"
        with open(chemin_lettres, "w", encoding="utf-8") as f:
            f.writelines(["alpha\n", "beta\n", "gamma\n"])
        afficher("writelines()", chemin_lettres)

        # print(file=f) ajoute le \n comme à l'écran : souvent le
        # plus lisible.
        chemin_print = Path(tmp) / "via_print.txt"
        with open(chemin_print, "w", encoding="utf-8") as f:
            print("ligne via print", file=f)
            print(f"valeur formatee : {42 * 2}", file=f)
        afficher("print(file=f)", chemin_print)

        # Mode "x" : refus d'écraser un fichier existant.
        try:
            with open(chemin, "x", encoding="utf-8") as f:
                f.write("ne sera jamais ecrit\n")
        except FileExistsError as e:
            print("Mode x sur fichier existant -> FileExistsError :", e)


if __name__ == "__main__":
    main()
