#!/usr/bin/env python3
"""Demo : écrire sur stdout et stderr, et choisir un code retour.

À exécuter :  python3 03_demo_flux.py

Essayer ensuite les redirections suivantes dans un shell :

    python3 03_demo_flux.py > sortie.txt
        -> seul stderr s'affiche à l'écran ; sortie.txt contient stdout.

    python3 03_demo_flux.py 2> erreurs.txt
        -> seul stdout s'affiche ; erreurs.txt contient stderr.

    python3 03_demo_flux.py > sortie.txt 2> erreurs.txt
        -> rien à l'écran ; les deux flux sont rangés séparément.

    python3 03_demo_flux.py ; echo "Code retour : $?"
        -> affiche 0 (succès) à la fin.
"""
import sys


def main():
    # Sortie normale : le résultat du programme.
    print("Ligne 1 sur stdout (résultat utile)")
    print("Ligne 2 sur stdout (résultat utile)")

    # Sortie d'erreur : journaux, progression, avertissements.
    print("Info : traitement en cours...", file=sys.stderr)
    print("Info : terminé.", file=sys.stderr)

    # On peut aussi écrire directement via les objets fichier.
    sys.stdout.write("Ligne 3 sur stdout (via sys.stdout.write)\n")
    sys.stderr.write("Avertissement via sys.stderr.write\n")

    # Code retour explicite : 0 = succès.
    # On pourrait aussi appeler sys.exit(0), ou ne rien faire du tout.
    sys.exit(0)


if __name__ == "__main__":
    main()
