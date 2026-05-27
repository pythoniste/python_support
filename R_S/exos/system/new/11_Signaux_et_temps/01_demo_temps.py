#!/usr/bin/env python3
"""Demo : mesurer une durée, afficher l'heure et formater une date.

À exécuter :  python3 01_demo_temps.py

Observer :
- la durée mesurée par time.monotonic (chronomètre) ;
- l'instant courant donné par datetime.now ;
- le formatage et le parsing via strftime / strptime.
"""
import time
from datetime import datetime, timedelta


def main():
    # 1. Mesurer une durée : utiliser une horloge monotone.
    print("Mesure d'une pause de 1,5 seconde...")
    debut = time.monotonic()
    time.sleep(1.5)
    duree = time.monotonic() - debut
    print(f"Durée écoulée : {duree:.3f} s")
    print()

    # 2. Instant courant : on utilise datetime.
    maintenant = datetime.now()
    print("Heure courante :", maintenant)
    print("  année :", maintenant.year)
    print("  heure :", maintenant.hour)
    print()

    # 3. Formater une date en chaîne lisible.
    texte = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    print("Format ISO compact :", texte)

    # 4. Parser une chaîne pour retrouver un datetime.
    relu = datetime.strptime(texte, "%Y-%m-%d %H:%M:%S")
    print("Relu via strptime  :", relu)

    # 5. Arithmétique : datetime + timedelta = nouveau datetime.
    plus_tard = maintenant + timedelta(minutes=10)
    print("Dans 10 minutes    :", plus_tard.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()
