#!/usr/bin/env python3
"""Demo : lire stdin et écrire sur stdout / stderr, détecter un tty.

À exécuter en mode interactif :

    python3 02_demo_flux.py
    (taper quelques lignes, puis Ctrl+D pour terminer l'entrée)

À exécuter avec une entrée venant d'un pipe :

    echo "ligne 1\\nligne 2\\nligne 3" | python3 02_demo_flux.py

À exécuter avec un fichier en entrée :

    python3 02_demo_flux.py < /etc/hostname

Observer :
- la détection automatique tty / pipe via isatty() ;
- l'itération ligne à ligne sur sys.stdin ;
- la séparation stdout (résultat) / stderr (info).
"""
import sys


def main():
    # On informe l'utilisateur sur stderr : ce n'est pas un résultat,
    # c'est un message de journal.
    if sys.stdin.isatty():
        print("Entrée : terminal interactif.", file=sys.stderr)
        print("Taper du texte, puis Ctrl+D pour terminer.", file=sys.stderr)
    else:
        print("Entrée : pipe ou fichier (non interactif).", file=sys.stderr)

    # Lecture ligne à ligne. Cette boucle s'arrête à la fin du flux :
    # Ctrl+D au clavier, ou fin du fichier / du producteur amont.
    nb_lignes = 0
    nb_caracteres = 0
    for ligne in sys.stdin:
        nb_lignes += 1
        nb_caracteres += len(ligne)
        # On retire le saut de ligne final pour un affichage propre.
        ligne_propre = ligne.rstrip("\n")
        # Résultat utile : sur stdout, pour pouvoir le rediriger.
        print(f"[{nb_lignes:>3}] {ligne_propre}")

    # Résumé : on choisit stderr car c'est de l'info, pas de la donnée.
    print(
        f"Total : {nb_lignes} ligne(s), {nb_caracteres} caractère(s).",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
