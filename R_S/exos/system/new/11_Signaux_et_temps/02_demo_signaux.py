#!/usr/bin/env python3
"""Demo : installer un handler de signal pour Ctrl+C.

À exécuter :  python3 02_demo_signaux.py

Le script boucle indéfiniment en affichant un point chaque seconde.
Taper Ctrl+C pour voir le handler s'exécuter, puis le programme sortir
proprement avec le code retour 0.

Note Windows : SIGINT (Ctrl+C) fonctionne ; SIGTERM est limité.
Rappel : SIGKILL et SIGSTOP ne peuvent jamais être interceptés.
"""
import signal
import sys
import time


stop_demande = False


def handler(signum, frame):
    """Appelé quand SIGINT (ou SIGTERM si dispo) arrive."""
    global stop_demande
    print()
    print(f"Signal {signum} reçu, arrêt propre en cours...")
    stop_demande = True


def main():
    # Installer le handler pour Ctrl+C.
    signal.signal(signal.SIGINT, handler)
    # Sous Windows, SIGTERM est absent ou différent ; on protège.
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, handler)

    print("Envoie Ctrl+C pour voir le handler s'exécuter.")
    print(f"(PID : {__import__('os').getpid()})")

    while not stop_demande:
        print(".", end="", flush=True)
        time.sleep(1)

    print("Sortie avec code retour 0.")
    sys.exit(0)


if __name__ == "__main__":
    main()
