#!/usr/bin/env python3
"""Demo : hashlib — empreintes en RAM et empreinte d'un fichier par blocs.

A executer :  python3 03_demo_hashlib.py

Le script calcule l'empreinte d'une chaine de plusieurs facons, puis
genere un fichier dans un dossier temporaire et le hache par blocs de
4 Kio. Il montre aussi la sensibilite : un seul octet change suffit a
modifier toute l'empreinte.
"""
import hashlib
import tempfile
from pathlib import Path


TAILLE_BLOC = 4096   # 4 Kio


def sha256_fichier(chemin):
    """Calcule le SHA-256 d'un fichier par blocs (memoire constante)."""
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        while True:
            bloc = f.read(TAILLE_BLOC)
            if not bloc:           # b"" = fin de fichier
                break
            h.update(bloc)
    return h.hexdigest()


def main():
    # 1) Forme en deux temps : update() puis hexdigest().
    print("--- sha256 d'une chaine ---")
    h = hashlib.sha256()
    h.update(b"hello ")
    h.update(b"world")
    print(h.hexdigest())

    # 2) Sensibilite : un octet change, toute l'empreinte change.
    print("--- sensibilite ---")
    a = hashlib.sha256(b"hello world").hexdigest()
    b = hashlib.sha256(b"hello worle").hexdigest()    # 1 octet de moins
    print("hello world :", a)
    print("hello worle :", b)
    print("identiques  :", a == b)

    # 3) Quatre algorithmes sur le meme message.
    print("--- md5 / sha1 / sha256 / sha512 ---")
    msg = b"empreinte de demo"
    for nom in ("md5", "sha1", "sha256", "sha512"):
        h = hashlib.new(nom)
        h.update(msg)
        print(f"{nom:7s} ({h.digest_size*8} bits) : {h.hexdigest()}")

    # 4) Empreinte d'un fichier par blocs de 4 Kio.
    print("--- sha256 d'un fichier ---")
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "echantillon.txt"
        # On ecrit ~100 Kio de donnees pour faire plusieurs blocs.
        with open(chemin, "wb") as f:
            for i in range(2500):
                f.write(f"ligne {i}\n".encode("utf-8"))

        empreinte = sha256_fichier(chemin)
        print("fichier   :", chemin.name,
              "(", chemin.stat().st_size, "octets )")
        print("sha256    :", empreinte)

        # 5) Comparaison de deux fichiers via leur empreinte.
        copie = Path(tmp) / "copie.txt"
        copie.write_bytes(chemin.read_bytes())
        print("memes ?   :", sha256_fichier(chemin) == sha256_fichier(copie))


if __name__ == "__main__":
    main()
