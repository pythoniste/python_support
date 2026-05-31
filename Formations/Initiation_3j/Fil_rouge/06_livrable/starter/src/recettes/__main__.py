"""Point d'entrée du package recettes — étape 06 (starter).

TODO : ajouter argparse et logging.
"""

from pathlib import Path

from recettes.carnet import ajouter_recette, charger, sauvegarder
from recettes.ui import afficher_carnet, afficher_menu, saisir_recette


def main() -> None:
    raise NotImplementedError("étape 06 : compléter main() avec argparse + logging")


if __name__ == "__main__":
    main()
