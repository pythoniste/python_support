#!/usr/bin/env python3
"""Demo : un script Python qui se présente lui-même.

À exécuter :  python3 01_demo_programme.py
Ou bien, après `chmod +x 01_demo_programme.py` :  ./01_demo_programme.py

Observer :
- la valeur de __name__ quand on lance le fichier directement ;
- le chemin de l'interpréteur python3 utilisé ;
- la version exacte de Python sous laquelle on tourne.
"""
import sys


def presentation():
    """Affiche quelques informations sur l'exécution courante."""
    print("Nom du module en cours :", __name__)
    print("Interpréteur utilisé   :", sys.executable)
    print("Version de Python      :", sys.version.split()[0])
    print("Arguments reçus        :", sys.argv)


# Le garde ci-dessous : ce bloc ne s'exécute que si le fichier est
# lancé directement (et pas s'il est importé depuis un autre module).
if __name__ == "__main__":
    presentation()
    print()
    print("Astuce : essayer aussi `python3 -i 01_demo_programme.py`")
    print("         pour rester dans le REPL après l'exécution.")
