"""Service REST de calcul de mensualité via Bottle.

Endpoint :
    GET /mensualite/<capital:int>/<taux:float>/<duree:int>
    -> JSON {"capital": K, "taux": t, "duree": n, "mensualite": M}

REST = stateless par essence. Chaque requête est autonome ; aucune
mémoire serveur entre appels.

Démo curl :
    curl http://127.0.0.1:8808/mensualite/200000/0.0475/300

À comparer avec 01_stateless_srv.py — même philosophie,
encapsulation HTTP en plus.
"""
from bottle import route, run
from mensualite import calcul_mensualite


HOTE = "127.0.0.1"
PORT = 8808


@route("/mensualite/<capital:int>/<taux:float>/<duree:int>")
def endpoint(capital: int, taux: float, duree: int):
    try:
        M = calcul_mensualite(capital, taux, duree, arrondi=True)
        return {
            "capital": capital,
            "taux": taux,
            "duree": duree,
            "mensualite": M,
        }
    except ValueError as exc:
        return {"erreur": str(exc)}


if __name__ == "__main__":
    run(host=HOTE, port=PORT)
