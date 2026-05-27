"""Couleurs et attributs curses.

À exécuter dans un vrai terminal :  python3 03_demo_couleurs.py

Observer :
- chaque couleur est utilisée comme premier plan, sur fond noir ;
- on combine A_BOLD et A_REVERSE pour démontrer les attributs ;
- la paire 0 (blanc sur noir) est réservée et non modifiable.

Appuyer sur n'importe quelle touche pour quitter.
"""
import curses


COULEURS = [
    ("NOIR",    curses.COLOR_BLACK),
    ("ROUGE",   curses.COLOR_RED),
    ("VERT",    curses.COLOR_GREEN),
    ("JAUNE",   curses.COLOR_YELLOW),
    ("BLEU",    curses.COLOR_BLUE),
    ("MAGENTA", curses.COLOR_MAGENTA),
    ("CYAN",    curses.COLOR_CYAN),
    ("BLANC",   curses.COLOR_WHITE),
]


def main(stdscr):
    # Activer le mode couleur (wrapper l'a souvent déjà fait).
    curses.start_color()

    # Vérification utile en cas de terminal monochrome.
    if not curses.has_colors():
        stdscr.addstr(0, 0, "Ce terminal n'a pas de couleur.")
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(0, 0, "Les huit couleurs standard de curses :")

    # On déclare une paire par couleur, en commençant au numéro 1.
    for numero, (nom, couleur) in enumerate(COULEURS, start=1):
        curses.init_pair(numero, couleur, curses.COLOR_BLACK)
        stdscr.addstr(numero + 1, 4, f"Paire {numero} : {nom}",
                      curses.color_pair(numero))

    # Démonstration des attributs combinés.
    stdscr.addstr(11, 0, "Attributs (combinés avec | ) :")
    stdscr.addstr(12, 4, "GRAS",     curses.A_BOLD)
    stdscr.addstr(13, 4, "INVERSE",  curses.A_REVERSE)
    stdscr.addstr(14, 4, "ROUGE GRAS",
                  curses.color_pair(2) | curses.A_BOLD)

    stdscr.addstr(16, 0, "Appuyer sur une touche pour quitter.")
    stdscr.refresh()
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
