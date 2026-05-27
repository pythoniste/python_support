"""Serveur HTTP minimal — stdlib uniquement (http.server).

À éviter en production : il faut gérer routes, parsing, sérialisation
JSON à la main. C'est néanmoins la base de tous les frameworks.
"""
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


HOTE = "127.0.0.1"
PORT = 8808


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        chemin = parsed.path

        if chemin == "/heure":
            self._json({"heure": datetime.now().isoformat()})
        elif chemin.startswith("/heure/"):
            fmt = chemin[len("/heure/"):]
            if fmt == "locale":
                self._json({"heure": datetime.now().strftime("%c")})
            elif fmt == "epoch":
                self._json({"heure": int(datetime.now().timestamp())})
            else:
                self._json({"erreur": f"format inconnu : {fmt!r}"}, status=400)
        else:
            self._json({"erreur": "not found"}, status=404)

    def _json(self, donnees: dict, status: int = 200) -> None:
        corps = json.dumps(donnees).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def log_message(self, format, *args):
        # Silence les logs verbeux par défaut.
        print(f"  [{self.address_string()}] {format % args}")


if __name__ == "__main__":
    with HTTPServer((HOTE, PORT), Handler) as serveur:
        print(f"<<< Serveur stdlib sur {(HOTE, PORT)}")
        serveur.serve_forever()
