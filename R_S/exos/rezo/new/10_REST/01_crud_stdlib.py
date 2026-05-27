"""CRUD complet via http.server (stdlib).

Démontre les patterns REST sans dépendance externe. À comparer avec
02_crud_fastapi.py qui fait la même chose 3 fois plus court.

Routes :
    GET    /todos          → liste tous les TODO
    POST   /todos          → crée un TODO  (renvoie 201 + le nouvel objet)
    GET    /todos/<id>     → renvoie un TODO  (404 si absent)
    PUT    /todos/<id>     → remplace        (404 si absent)
    DELETE /todos/<id>     → supprime        (204 si OK, 404 si absent)
"""
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer


HOTE = "127.0.0.1"
PORT = 8808

todos: dict[int, dict] = {}
prochain_id = 1


class Handler(BaseHTTPRequestHandler):

    def do_GET(self) -> None:
        if self.path == "/todos":
            self._json(200, list(todos.values()))
            return
        m = re.match(r"^/todos/(\d+)$", self.path)
        if m:
            tid = int(m.group(1))
            if tid not in todos:
                self._json(404, {"erreur": "todo absent"})
                return
            self._json(200, todos[tid])
            return
        self._json(404, {"erreur": "route inconnue"})

    def do_POST(self) -> None:
        global prochain_id
        if self.path != "/todos":
            self._json(404, {"erreur": "route inconnue"})
            return
        donnees = self._lire_corps()
        if donnees is None or "titre" not in donnees:
            self._json(400, {"erreur": "champ titre requis"})
            return
        todo = {"id": prochain_id, "titre": donnees["titre"], "fait": donnees.get("fait", False)}
        todos[prochain_id] = todo
        prochain_id += 1
        self._json(201, todo)

    def do_PUT(self) -> None:
        m = re.match(r"^/todos/(\d+)$", self.path)
        if not m:
            self._json(404, {"erreur": "route inconnue"})
            return
        tid = int(m.group(1))
        if tid not in todos:
            self._json(404, {"erreur": "todo absent"})
            return
        donnees = self._lire_corps()
        if donnees is None or "titre" not in donnees:
            self._json(400, {"erreur": "champ titre requis"})
            return
        todos[tid] = {"id": tid, "titre": donnees["titre"], "fait": donnees.get("fait", False)}
        self._json(200, todos[tid])

    def do_DELETE(self) -> None:
        m = re.match(r"^/todos/(\d+)$", self.path)
        if not m:
            self._json(404, {"erreur": "route inconnue"})
            return
        tid = int(m.group(1))
        if tid not in todos:
            self._json(404, {"erreur": "todo absent"})
            return
        del todos[tid]
        self.send_response(204)
        self.end_headers()

    # --- helpers ---

    def _lire_corps(self) -> dict | None:
        longueur = int(self.headers.get("Content-Length", "0"))
        if longueur == 0:
            return None
        try:
            return json.loads(self.rfile.read(longueur))
        except json.JSONDecodeError:
            return None

    def _json(self, status: int, donnees) -> None:
        corps = json.dumps(donnees).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def log_message(self, format, *args):
        print(f"  [{self.address_string()}] {format % args}")


if __name__ == "__main__":
    with HTTPServer((HOTE, PORT), Handler) as serveur:
        print(f"<<< CRUD stdlib sur {(HOTE, PORT)}")
        serveur.serve_forever()
