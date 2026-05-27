#!/usr/bin/env python3
"""Demo : inspecter sys.argv et choisir un code retour via sys.exit.

À exécuter :

    python3 01_demo_argv.py
    python3 01_demo_argv.py alpha beta 42
    python3 01_demo_argv.py --erreur

Observer :
- argv[0] est toujours présent (le nom du script lui-même) ;
- les autres éléments sont les arguments fournis, en str ;
- sys.exit("message") écrit sur stderr et sort en 1.

Vérifier ensuite `echo $?` dans le shell pour voir le code retour.
"""
import sys


def main():
    # argv est une liste de chaînes. Le tout premier élément est le script.
    print("Nombre d'éléments dans argv :", len(sys.argv))
    print("argv[0] (nom du script)     :", sys.argv[0])

    # Les vrais arguments commencent à l'indice 1.
    arguments_utilisateur = sys.argv[1:]
    print("Arguments utilisateur       :", arguments_utilisateur)

    # Démonstration du raccourci sys.exit("message") : si on passe
    # --erreur, on simule un échec en une seule ligne.
    if "--erreur" in arguments_utilisateur:
        # Cette ligne écrit sur stderr ET sort avec le code retour 1.
        sys.exit("Erreur simulée : le mode --erreur a été demandé.")

    # Cas nominal : on liste les arguments un par un.
    for indice, valeur in enumerate(arguments_utilisateur, start=1):
        print(f"  argument {indice} : {valeur!r}")

    # Sortie explicite avec un code retour de succès.
    # sys.exit() sans argument fait la même chose.
    sys.exit(0)


if __name__ == "__main__":
    main()
