"""Serveur HTTP — Flask.

`pip install flask`. Framework historique, écosystème mature.
Modèle synchrone par défaut, async ajouté en 2.0+.
"""
from datetime import datetime
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/heure")
def heure():
    return jsonify({"heure": datetime.now().isoformat()})


@app.route("/heure/<format>")
def heure_format(format: str):
    if format == "locale":
        return jsonify({"heure": datetime.now().strftime("%c")})
    if format == "epoch":
        return jsonify({"heure": int(datetime.now().timestamp())})
    return jsonify({"erreur": f"format inconnu : {format!r}"}), 400


if __name__ == "__main__":
    # En production : utiliser gunicorn / waitress, pas le serveur de dev.
    app.run(host="127.0.0.1", port=8808, debug=False)
