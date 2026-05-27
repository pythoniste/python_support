"""Bottle en HTTPS via cherrypy / waitress / wsgiref + SSL.

`pip install bottle cheroot`.

Bottle utilise par défaut wsgiref qui ne gère pas TLS. On passe
par cheroot (extrait de CherryPy) pour avoir un serveur WSGI TLS.

NB : en production, on **terminate** TLS dans nginx/traefik plutôt
que dans le code Python. Cet exemple sert uniquement à montrer que
c'est possible.
"""
from bottle import Bottle, run


app = Bottle()


@app.route("/")
def index():
    return {"protocole": "HTTPS", "message": "Bonjour TLS"}


if __name__ == "__main__":
    # Méthode simple via cheroot :
    from cheroot.wsgi import Server
    from cheroot.ssl.builtin import BuiltinSSLAdapter

    serveur = Server(("127.0.0.1", 8443), app)
    serveur.ssl_adapter = BuiltinSSLAdapter(
        certificate="serveur.crt",
        private_key="serveur.key",
    )
    print("<<< Bottle HTTPS sur https://127.0.0.1:8443")
    print("    Test : curl -k https://127.0.0.1:8443/")
    try:
        serveur.start()
    except KeyboardInterrupt:
        serveur.stop()
