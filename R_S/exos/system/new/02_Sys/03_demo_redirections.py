#!/usr/bin/env python3
"""Demo : un script qui coopère avec les redirections du shell.

À exécuter sans redirection :

    python3 03_demo_redirections.py

Puis essayer ces variantes dans un shell :

    python3 03_demo_redirections.py > sortie.txt
        -> sortie.txt contient stdout ; stderr reste à l'écran.

    python3 03_demo_redirections.py 2> erreurs.txt
        -> stdout reste à l'écran ; erreurs.txt contient stderr.

    python3 03_demo_redirections.py > sortie.txt 2> erreurs.txt
        -> rien à l'écran ; les deux flux dans deux fichiers séparés.

    python3 03_demo_redirections.py > tout.txt 2>&1
        -> tout.txt contient les deux flux mélangés.

    python3 03_demo_redirections.py > /dev/null 2>&1 ; echo $?
        -> tout est jeté ; seul le code retour est conservé.

    python3 03_demo_redirections.py | tr a-z A-Z
        -> seul stdout passe dans tr ; stderr reste à l'écran.
"""
import sys


def main():
    # Trois lignes de "résultat" sur stdout : ce sont les données
    # utiles qu'un autre programme pourrait consommer.
    print("donnee_1")
    print("donnee_2")
    print("donnee_3")

    # Deux lignes de "journal" sur stderr : c'est pour l'utilisateur,
    # pas pour le programme d'aval.
    print("info : 3 donnees produites", file=sys.stderr)
    print("info : terminé", file=sys.stderr)

    # Code retour : 0 = succès. Le shell le récupère dans $?
    # même si stdout et stderr ont été redirigés.
    sys.exit(0)


if __name__ == "__main__":
    main()
