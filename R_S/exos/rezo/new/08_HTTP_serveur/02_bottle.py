"""Serveur HTTP — Bottle.

`pip install bottle`. Microframework en UN fichier de la stdlib
Python (bottle.py), aucune dépendance. Pratique pour les scripts
internes, vu en dossier 04.
"""
from datetime import datetime
from bottle import route, run


@route("/heure")
def heure():
    return {"heure": datetime.now().isoformat()}


@route("/heure/<format>")
def heure_format(format: str):
    if format == "locale":
        return {"heure": datetime.now().strftime("%c")}
    if format == "epoch":
        return {"heure": int(datetime.now().timestamp())}
    return {"erreur": f"format inconnu : {format!r}"}


if __name__ == "__main__":
    run(host="127.0.0.1", port=8808)
