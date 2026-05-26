"""Service HTTP/REST du palindrome via Bottle.

Endpoint :
    GET /palindrome/<mot>  ->  JSON {"mot": "...", "est_palindrome": bool}

À utiliser avec 10_bottle_clt.py (ou directement avec curl).

Démo avec curl :
    curl http://127.0.0.1:8808/palindrome/anna
    curl 'http://127.0.0.1:8808/palindrome/Karine%20alla%20en%20Irak'

Pour arrêter : Ctrl-C (Bottle ne fournit pas de mot-clé d'arrêt en
mode dev).
"""
from bottle import route, run
from palindrome import est_palindrome


HOTE = "127.0.0.1"
PORT = 8808


@route("/palindrome/<mot>")
def palindrome_endpoint(mot: str):
    return {
        "mot": mot,
        "est_palindrome": est_palindrome(mot),
    }


if __name__ == "__main__":
    run(host=HOTE, port=PORT)
