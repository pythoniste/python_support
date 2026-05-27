#!/usr/bin/env python3
"""Demo : base64 — encoder, decoder, variante URL-safe.

A executer :  python3 05_demo_base64.py

Le script montre la forme standard, la forme URL-safe, le bourrage '=',
et un cas concret : embarquer un fichier binaire dans un JSON. Il
rappelle aussi que base64 N'EST PAS un chiffrement.
"""
import base64
import json
import secrets
import tempfile
from pathlib import Path


def main():
    # 1) base64 standard sur quelques octets.
    print("--- base64 standard ---")
    octets = b"\x01\x02\xff\xfe"
    encode = base64.b64encode(octets)         # bytes ASCII
    decode = base64.b64decode(encode)
    print("octets    :", octets)
    print("b64encode :", encode)
    print("b64decode :", decode)
    print("reversible:", decode == octets)

    # 2) Pour stocker dans un fichier texte, on convertit en str.
    print("--- str ASCII ---")
    texte = base64.b64encode(octets).decode("ascii")
    print(type(texte).__name__, texte)

    # 3) Variante URL-safe : '-' et '_' a la place de '+' et '/'.
    print("--- URL-safe ---")
    # Donnees choisies pour generer '+' et '/' en standard.
    donnees = bytes(range(255, 250, -1))     # \xff \xfe \xfd \xfc \xfb
    print("standard  :", base64.b64encode(donnees))
    print("urlsafe   :", base64.urlsafe_b64encode(donnees))

    # 4) Le bourrage '=' selon la longueur d'entree.
    print("--- bourrage = ---")
    for s in (b"abc", b"ab", b"a"):
        print(f"{s!r:>8} -> {base64.b64encode(s)!r}")

    # 5) base64 N'EST PAS un chiffrement : tout le monde peut decoder.
    print("--- pas un chiffrement ---")
    visible = base64.b64encode(b"mon mot de passe").decode("ascii")
    print("publie    :", visible)
    print("decode    :", base64.b64decode(visible))

    # 6) Cas concret : fichier binaire dans un JSON.
    print("--- fichier binaire dans un JSON ---")
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / "blob.bin"
        chemin.write_bytes(secrets.token_bytes(64))   # 64 octets aleatoires

        # Cote emetteur.
        with open(chemin, "rb") as f:
            contenu = f.read()
        payload = {"nom": chemin.name,
                   "contenu": base64.b64encode(contenu).decode("ascii")}
        message = json.dumps(payload)
        print("payload JSON (extrait) :", message[:80], "...")

        # Cote recepteur.
        recu = json.loads(message)
        retrouve = base64.b64decode(recu["contenu"])
        print("identique a l'original :", retrouve == contenu)


if __name__ == "__main__":
    main()
