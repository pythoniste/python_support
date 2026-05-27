"""Centrer du texte et suivre le redimensionnement.

À exécuter dans un vrai terminal :  python3 04_demo_resize.py

Observer :
- le texte est centré horizontalement et verticalement ;
- redimensionner la fenêtre du terminal (à la souris ou Ctrl + - / +) :
  le texte se replace au centre, et la taille affichée se met à jour ;
- la touche KEY_RESIZE est délivrée à chaque changement de taille.

Appuyer sur q pour quitter.
"""
import curses


def dessiner(stdscr):
    """Efface l'écran, recalcule la position centrée et redessine."""
    stdscr.clear()
    hauteur, largeur = stdscr.getmaxyx()

    titre = "Hello, monde !"
    info = f"Taille actuelle : {hauteur} lignes x {largeur} colonnes"
    aide = "Redimensionner la fenetre, puis q pour quitter."

    # Position centrée pour chaque ligne, avec max(0, ...) en garde-fou.
    y_centre = hauteur // 2
    stdscr.addstr(y_centre - 1, max(0, (largeur - len(titre)) // 2),
                  titre, curses.A_BOLD)
    stdscr.addstr(y_centre + 1, max(0, (largeur - len(info)) // 2),
                  info)
    stdscr.addstr(y_centre + 3, max(0, (largeur - len(aide)) // 2),
                  aide)

    stdscr.refresh()


def main(stdscr):
    dessiner(stdscr)
    while True:
        touche = stdscr.getch()
        if touche == ord("q"):
            break
        elif touche == curses.KEY_RESIZE:
            # L'utilisateur a changé la taille du terminal : on redessine.
            dessiner(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
