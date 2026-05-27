#!/usr/bin/env python3
"""Demo : platform — connaitre la machine et adapter un message.

A executer :  python3 02_demo_platform.py

Le script affiche les six informations utiles, puis montre un
branchement classique selon l'OS detecte.
"""
import platform
import sys


def message_accueil(systeme):
    """Renvoie un message d'accueil adapte a l'OS detecte."""
    if systeme == "Linux":
        return "Bonjour ! Detecte Linux : on est sur un Unix-like."
    if systeme == "Darwin":
        return "Bonjour ! Detecte macOS (noyau Darwin)."
    if systeme == "Windows":
        return "Bonjour ! Detecte Windows."
    return f"OS inconnu ({systeme}), on continuera sans adaptation."


def main():
    # 1) Les six fonctions a connaitre.
    print("--- informations machine ---")
    print("OS         :", platform.system())
    print("Release    :", platform.release())
    print("Version    :", platform.version())
    print("Machine    :", platform.machine())
    print("Node       :", platform.node())
    print("Python     :", platform.python_version())

    # 2) 64 bits ou 32 bits cote Python ?
    print("--- Python 64 bits ? ---")
    print("sys.maxsize > 2**32 :", sys.maxsize > 2**32)

    # 3) Adapter un message d'accueil selon l'OS.
    print("--- accueil adapte ---")
    print(message_accueil(platform.system()))

    # 4) En-tete de rapport de bug : a copier-coller tel quel.
    print("--- en-tete rapport de bug ---")
    print(f"OS      : {platform.system()} {platform.release()}")
    print(f"Arch    : {platform.machine()}")
    print(f"Machine : {platform.node()}")
    print(f"Python  : {platform.python_version()} ({sys.executable})")


if __name__ == "__main__":
    main()
