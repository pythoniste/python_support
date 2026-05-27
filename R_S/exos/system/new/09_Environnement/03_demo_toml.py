"""Lecture d'un fichier TOML avec tomllib (Python 3.11+).

À exécuter :  python3 03_demo_toml.py

Observer :
- l'ouverture en mode binaire ("rb") exigée par tomllib ;
- les types Python natifs renvoyés (int, list, dict imbriqués) ;
- la structure typique d'un pyproject.toml.
"""
import sys
import tempfile
import tomllib
from pathlib import Path


CONTENU_TOML = """\
[project]
name = "mon-paquet"
version = "1.0.0"
requires-python = ">=3.11"
keywords = ["demo", "config", "toml"]

[project.urls]
homepage = "https://example.org"
"""


def main():
    if sys.version_info < (3, 11):
        print("Ce script nécessite Python 3.11 ou plus récent.", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as dossier:
        chemin = Path(dossier) / "pyproject.toml"
        chemin.write_text(CONTENU_TOML, encoding="utf-8")

        # Ouverture en mode BINAIRE — exigée par tomllib.load.
        with open(chemin, "rb") as f:
            data = tomllib.load(f)

        # data est un dict aux types Python natifs.
        print("type(data)              :", type(data).__name__)
        print("data['project']['name'] :", data["project"]["name"])
        print("version                 :", data["project"]["version"])
        print("keywords (list)         :", data["project"]["keywords"])
        print("type(keywords)          :", type(data["project"]["keywords"]).__name__)
        print("homepage                :", data["project"]["urls"]["homepage"])


if __name__ == "__main__":
    main()
