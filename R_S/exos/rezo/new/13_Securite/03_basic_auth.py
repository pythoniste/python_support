"""HTTP Basic Auth — démonstration côté serveur.

Le client envoie `Authorization: Basic base64(user:password)`. Le
serveur décode et vérifie.

À utiliser UNIQUEMENT en HTTPS (sinon le mot de passe transite en
clair en base64 trivial à décoder).

Pour les services modernes : préférer Bearer (JWT) — fichiers 04, 05.
"""
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer


HOTE = "127.0.0.1"
PORT = 8808

# En production : table d'utilisateurs avec mots de passe HASHÉS
# (cf. 02_password_hash.py). Ici, simplifié.
UTILISATEURS = {
    "alice": "passw0rd",
    "bob": "secret",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        auth = self.headers.get("Authorization", "")
        utilisateur = self._verifier(auth)

        if utilisateur is None:
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="zone protégée"')
            self.end_headers()
            self.wfile.write(b"Authentification requise")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"Bonjour {utilisateur}".encode("utf-8"))

    def _verifier(self, header: str) -> str | None:
        if not header.startswith("Basic "):
            return None
        try:
            decode = base64.b64decode(header[6:]).decode("utf-8")
            user, _, motpasse = decode.partition(":")
        except Exception:
            return None
        if UTILISATEURS.get(user) == motpasse:
            return user
        return None

    def log_message(self, format, *args):
        print(f"  [{self.address_string()}] {format % args}")


if __name__ == "__main__":
    print(f"<<< Basic Auth sur {(HOTE, PORT)}")
    print("    Test :")
    print("      curl -u alice:passw0rd http://127.0.0.1:8808/")
    print("      curl -u alice:wrong    http://127.0.0.1:8808/")
    HTTPServer((HOTE, PORT), Handler).serve_forever()
