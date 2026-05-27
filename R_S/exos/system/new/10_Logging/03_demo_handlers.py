"""Demo : un logger, deux destinations.

À exécuter :  python3 03_demo_handlers.py

Observer :
- DEBUG et INFO ne s'affichent **que** dans le fichier ;
- WARNING, ERROR, CRITICAL apparaissent **aussi** sur la console ;
- le logger est nommé d'après le module (__name__).
"""
import logging
import tempfile
from pathlib import Path


def construire_logger(chemin_fichier: Path) -> logging.Logger:
    """Configure un logger avec deux handlers (fichier + console)."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)   # le logger laisse tout passer

    # Handler fichier : tout, format complet.
    fichier = logging.FileHandler(chemin_fichier, mode="w", encoding="utf-8")
    fichier.setLevel(logging.DEBUG)
    fichier.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-8s %(name)s : %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    logger.addHandler(fichier)

    # Handler console : WARNING+, format plus court.
    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter(
        "[console] %(levelname)-8s : %(message)s"
    ))
    logger.addHandler(console)

    return logger


def main():
    repertoire = Path(tempfile.mkdtemp(prefix="demo_handlers_"))
    journal = repertoire / "app.log"

    logger = construire_logger(journal)

    logger.debug("ouverture de la base")
    logger.info("requête traitée en 12 ms")
    logger.warning("quota proche de la limite")
    logger.error("requête refusée par le serveur")
    logger.critical("perte du lien réseau")

    print()
    print(f"Journal complet écrit dans : {journal}")
    print("Contenu du fichier :")
    print(journal.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
