"""Lecture et écriture d'un fichier INI avec configparser.

À exécuter :  python3 02_demo_ini.py

Observer :
- la création d'un INI d'exemple dans un dossier temporaire ;
- la lecture des sections et des valeurs ;
- la différence entre une valeur lue en chaîne et en type natif (getint, getboolean).
"""
import configparser
import tempfile
from pathlib import Path


CONTENU_INI = """\
[database]
host = localhost
port = 5432
ssl  = true

[server]
bind = 0.0.0.0
workers = 4
"""


def main():
    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "app.ini"
        chemin.write_text(CONTENU_INI, encoding="utf-8")

        config = configparser.ConfigParser()
        lus = config.read(chemin)
        print("Fichiers effectivement lus :", lus)

        # Lecture en chaîne (forme par défaut).
        print()
        print("host (str) :", repr(config["database"]["host"]))
        print("port (str) :", repr(config["database"]["port"]))

        # Lecture typée.
        port = config.getint("database", "port")
        ssl_on = config.getboolean("database", "ssl")
        workers = config.getint("server", "workers")
        print()
        print(f"port (int)     : {port!r}")
        print(f"ssl  (bool)    : {ssl_on!r}")
        print(f"workers (int)  : {workers!r}")

        # Parcourir toutes les sections.
        print()
        for nom in config.sections():
            print(f"[{nom}]")
            for cle, valeur in config[nom].items():
                print(f"  {cle} = {valeur}")


if __name__ == "__main__":
    main()
