#!/usr/bin/env python3
"""Demo : texte vs binaire, BOM UTF-8 et errors=replace.

À exécuter :  python3 03_demo_binaire.py

Le script écrit le même contenu sous trois formes différentes dans un
dossier temporaire, puis le relit en mode texte et en mode binaire pour
mettre en évidence ce qui change vraiment.
"""
import tempfile
from pathlib import Path


BOM_UTF8 = b"\xef\xbb\xbf"


def main():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)

        # 1) Texte simple : un mot avec accent.
        chemin_txt = base / "cafe.txt"
        with open(chemin_txt, "w", encoding="utf-8") as f:
            f.write("cafe accentue : cafe\n")
            # On force volontairement un accent.
            f.write("avec accent : café\n")

        # Relecture en texte : on récupère des str.
        with open(chemin_txt, "r", encoding="utf-8") as f:
            contenu_texte = f.read()
        print("--- mode texte ---")
        print(type(contenu_texte).__name__, repr(contenu_texte))

        # Relecture en binaire : on récupère des bytes.
        with open(chemin_txt, "rb") as f:
            contenu_octets = f.read()
        print("--- mode binaire ---")
        print(type(contenu_octets).__name__, contenu_octets)

        # 2) Fichier avec BOM UTF-8 (typique sous Windows).
        chemin_bom = base / "avec_bom.txt"
        with open(chemin_bom, "wb") as f:
            f.write(BOM_UTF8 + "hello\n".encode("utf-8"))

        # Lu en utf-8 strict : le BOM est conservé comme caractère.
        with open(chemin_bom, "r", encoding="utf-8") as f:
            avec_bom = f.read()
        # Lu en utf-8-sig : le BOM est consommé silencieusement.
        with open(chemin_bom, "r", encoding="utf-8-sig") as f:
            sans_bom = f.read()
        print("--- BOM ---")
        print("utf-8     :", repr(avec_bom))
        print("utf-8-sig :", repr(sans_bom))

        # 3) Octets invalides + errors="replace".
        chemin_casse = base / "casse.txt"
        with open(chemin_casse, "wb") as f:
            f.write(b"bonjour \xff\xfe monde\n")  # \xff\xfe invalides en UTF-8

        with open(chemin_casse, "r", encoding="utf-8",
                  errors="replace") as f:
            recupere = f.read()
        print("--- errors=replace ---")
        print(repr(recupere))


if __name__ == "__main__":
    main()
