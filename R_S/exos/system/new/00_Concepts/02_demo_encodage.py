#!/usr/bin/env python3
"""Demo : str, bytes, et l'encodage UTF-8 par défaut.

À exécuter :  python3 02_demo_encodage.py

Observer :
- l'encodage par défaut de stdout ;
- la conversion str -> bytes via .encode() ;
- la conversion bytes -> str via .decode() ;
- le fait que les caractères non-ASCII occupent plusieurs octets.
"""
import sys


def main():
    # 1) L'encodage de sortie déclaré par l'interpréteur.
    print("Encodage de stdout :", sys.stdout.encoding)
    print()

    # 2) Un texte avec des caractères non-ASCII.
    texte = "Café — 2,50 €"
    print("Texte (str)   :", texte)
    print("Longueur str  :", len(texte), "caractères")

    # 3) Encodage en UTF-8 (bytes).
    octets = texte.encode("utf-8")
    print("Octets (bytes):", octets)
    print("Longueur bytes:", len(octets), "octets")
    print()

    # 4) Décodage retour : on retrouve le texte original.
    retour = octets.decode("utf-8")
    print("Décodage retour :", retour)
    print("Égal au départ  :", retour == texte)

    # 5) Que se passe-t-il si on tente un encodage incompatible ?
    try:
        texte.encode("ascii")
    except UnicodeEncodeError as exc:
        print()
        print("Encodage en ASCII impossible :", exc)


if __name__ == "__main__":
    main()
