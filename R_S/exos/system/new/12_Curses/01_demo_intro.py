"""Premier contact avec curses : prendre le contrôle du terminal.

À exécuter dans un vrai terminal :  python3 01_demo_intro.py

Observer :
- l'écran est effacé et passe en mode plein écran ;
- aucun écho des touches : on tape mais rien ne s'affiche tout seul ;
- la fonction main reçoit stdscr (la fenêtre principale) ;
- à la sortie, curses.wrapper restaure le terminal d'origine.

Appuyer sur n'importe quelle touche pour quitter.
"""
import curses


def main(stdscr):
    # On efface l'écran avant de dessiner.
    stdscr.clear()

    # Un texte à la position (ligne 0, colonne 0).
    stdscr.addstr(0, 0, "Bonjour, curses !")

    # Un autre texte plus bas, pour montrer qu'on positionne où on veut.
    stdscr.addstr(2, 0, "Appuyer sur une touche pour quitter.")

    # Sans refresh, rien ne s'affiche : curses bufferise.
    stdscr.refresh()

    # getch bloque jusqu'à une touche pressée.
    stdscr.getch()


if __name__ == "__main__":
    # wrapper initialise curses, appelle main, et restaure le terminal
    # même en cas d'exception non rattrapée.
    curses.wrapper(main)
