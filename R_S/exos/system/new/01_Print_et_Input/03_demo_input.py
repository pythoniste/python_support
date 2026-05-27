#!/usr/bin/env python3
"""Demo : lire au clavier, convertir, valider, masquer un mot de passe.

À exécuter :  python3 03_demo_input.py

Trois invites s'enchaînent :
1. un prénom (chaîne libre) ;
2. un entier (relance tant que ce n'est pas un entier) ;
3. un mot de passe (saisie masquée via getpass).

Le script est interactif : il faut taper les réponses au clavier.
"""
import getpass


def lire_entier(invite):
    """Lit un entier, redemande tant que la saisie est invalide."""
    while True:
        saisie = input(invite)
        try:
            return int(saisie)
        except ValueError:
            print("  -> ce n'est pas un entier, réessaye.")


def main():
    # 1) Lecture d'une chaîne brute.
    prenom = input("Quel est ton prénom ? ")
    print(f"Bonjour {prenom} !")

    # 2) Lecture d'un entier avec validation.
    age = lire_entier("Quel est ton âge (entier) ? ")
    print(f"Dans 10 ans, tu auras {age + 10} ans.")

    # 3) Lecture masquée d'un mot de passe : rien ne s'affiche pendant
    #    la frappe. On ne montre que la longueur, pas le contenu.
    mdp = getpass.getpass("Mot de passe (ne s'affichera pas) : ")
    print(f"Tu as tapé {len(mdp)} caractère(s).")


if __name__ == "__main__":
    main()
