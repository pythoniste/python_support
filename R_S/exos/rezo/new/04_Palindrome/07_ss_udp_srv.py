"""Serveur UDP socketserver du service palindrome.

À utiliser avec 08_ss_udp_clt.py.
"""
import socketserver
import threading
from palindrome import est_palindrome


socketserver.UDPServer.allow_reuse_address = True

HOTE = "127.0.0.1"
PORT = 8808


class PalindromeHandler(socketserver.DatagramRequestHandler):

    def handle(self) -> None:
        # rfile contient l'ENTIER datagramme reçu — readline lit jusqu'à \n
        # ou jusqu'à la fin, selon ce qui vient en premier.
        ligne = self.rfile.readline().rstrip(b"\n").strip()
        mot = ligne.decode("utf-8", errors="replace")
        print(f"    Reçu de {self.client_address} : {mot!r}")
        if mot == "stop":
            self.wfile.write(b"ARRET")
            threading.Thread(
                target=self.server.shutdown, daemon=True
            ).start()
            return
        if est_palindrome(mot):
            self.wfile.write(b"PALINDROME")
        else:
            self.wfile.write(b"PAS_PALINDROME")


if __name__ == "__main__":
    with socketserver.UDPServer((HOTE, PORT), PalindromeHandler) as serveur:
        print(f"<<< Serveur palindrome (socketserver UDP) sur {(HOTE, PORT)}")
        serveur.serve_forever()
        print("<<< Serveur arrêté")
