"""Demo : basicConfig avec un fichier journal (dans un dossier temporaire).

À exécuter :  python3 02_demo_basicconfig.py

Observer :
- aucun message à l'écran : tout part dans le fichier ;
- le fichier contient la date, le niveau et le message ;
- le chemin du fichier est imprimé à la fin pour pouvoir l'inspecter.
"""
import logging
import tempfile
from pathlib import Path


FORMAT = "%(asctime)s %(levelname)-8s %(name)s : %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"


def main():
    # Fichier temporaire : créé dans /tmp (ou équivalent), nettoyage manuel.
    repertoire = Path(tempfile.mkdtemp(prefix="demo_logging_"))
    journal = repertoire / "app.log"

    logging.basicConfig(
        level=logging.DEBUG,
        filename=str(journal),
        filemode="w",          # "w" = on écrase à chaque exécution
        format=FORMAT,
        datefmt=DATEFMT,
    )

    logging.debug("démarrage de la fonction main")
    logging.info("traitement des données")
    logging.warning("valeur par défaut utilisée pour le paramètre X")
    logging.error("le fichier de configuration est introuvable")
    logging.critical("base de données injoignable, arrêt")

    # On affiche où regarder, depuis stdout cette fois-ci.
    print(f"Journal écrit dans : {journal}")
    print("Contenu :")
    print(journal.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
