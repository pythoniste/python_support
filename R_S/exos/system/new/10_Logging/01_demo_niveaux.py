"""Demo : les cinq niveaux de logging et l'effet du seuil.

À exécuter :  python3 01_demo_niveaux.py

Observer :
- avec un seuil INFO, les messages DEBUG sont masqués ;
- avec un seuil WARNING, INFO et DEBUG disparaissent à leur tour ;
- la sortie va sur stderr (rediriger 2> pour le vérifier).
"""
import logging


def emettre_les_cinq():
    """Envoie un message à chacun des cinq niveaux."""
    logging.debug("Détail interne pour le développeur")
    logging.info("Étape normale du programme")
    logging.warning("Comportement inattendu mais non bloquant")
    logging.error("Une opération a échoué")
    logging.critical("Échec grave, le programme va peut-être s'arrêter")


def main():
    print("--- Seuil = WARNING (défaut si aucun appel à basicConfig) ---")
    # Par défaut, seuls WARNING et au-dessus passent.
    emettre_les_cinq()

    print("\n--- Seuil = INFO ---")
    # force=True : on remplace la configuration précédente.
    logging.basicConfig(level=logging.INFO, force=True,
                        format="%(levelname)-8s : %(message)s")
    emettre_les_cinq()

    print("\n--- Seuil = DEBUG ---")
    logging.basicConfig(level=logging.DEBUG, force=True,
                        format="%(levelname)-8s : %(message)s")
    emettre_les_cinq()


if __name__ == "__main__":
    main()
