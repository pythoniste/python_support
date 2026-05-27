"""Positionnement de texte avec addstr(y, x, ...).

À exécuter dans un vrai terminal :  python3 02_demo_addstr.py

Observer :
- l'ordre des coordonnées est (y, x), pas (x, y) ;
- l'origine (0, 0) est en haut à gauche ;
- y augmente vers le bas ;
- un seul refresh à la fin suffit pour rendre tout visible.

Appuyer sur q pour quitter.
"""
import curses


def main(stdscr):
    stdscr.clear()

    # On écrit du texte à des coordonnées variées.
    stdscr.addstr(0, 0, "(0, 0) coin haut-gauche")
    stdscr.addstr(1, 4, "(1, 4) decale de 4 colonnes")
    stdscr.addstr(3, 0, "(3, 0) trois lignes plus bas")
    stdscr.addstr(5, 10, "(5, 10) au milieu de la zone")
    stdscr.addstr(7, 0, "Astuce : (y, x) = (ligne, colonne)")
    stdscr.addstr(9, 0, "Appuyer sur q pour quitter.")

    # Un seul refresh : tout apparaît d'un coup.
    stdscr.refresh()

    # Boucle d'événements minimale : on attend la touche q.
    while True:
        touche = stdscr.getch()
        if touche == ord("q"):
            break


if __name__ == "__main__":
    curses.wrapper(main)
