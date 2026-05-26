"""Serveur UDP avec socketserver.UDPServer + DatagramRequestHandler.

Même principe qu'en TCP : un handler par datagramme reçu. self.rfile
est un BytesIO contenant le datagramme entier (pas de framing UDP
nécessaire — les frontières sont préservées par le protocole).

À comparer avec 01_Sockets_bas_niveau/03_udpsrv.py (version raw socket).

Pour arrêter : Ctrl-C.
"""
import socketserver


# Autorise le rebind immédiat sur un port en TIME_WAIT.
socketserver.UDPServer.allow_reuse_address = True

HOTE = "127.0.0.1"
PORT = 8808


class BonjourHandler(socketserver.DatagramRequestHandler):
    """Une instance par datagramme reçu."""

    def handle(self) -> None:
        ligne = self.rfile.readline().rstrip(b"\n")
        print(f"    Reçu de {self.client_address} : {ligne!r}")
        self.wfile.write(b"Bonjour " + ligne + b".\n")


if __name__ == "__main__":
    with socketserver.UDPServer((HOTE, PORT), BonjourHandler) as serveur:
        print(f"<<< Serveur UDPServer en attente sur {(HOTE, PORT)}")
        print("    (Ctrl-C pour arrêter)")
        serveur.serve_forever()
