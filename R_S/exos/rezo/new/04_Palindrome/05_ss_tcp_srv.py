"""Serveur TCP socketserver du service palindrome.

À utiliser avec 06_ss_tcp_clt.py.
"""
import socketserver
import threading
from palindrome import est_palindrome


socketserver.TCPServer.allow_reuse_address = True

HOTE = "127.0.0.1"
PORT = 8808


class PalindromeHandler(socketserver.StreamRequestHandler):

    def handle(self) -> None:
        ligne = self.rfile.readline().rstrip(b"\n")
        if not ligne:
            return
        mot = ligne.decode("utf-8", errors="replace")
        print(f"    Reçu de {self.client_address} : {mot!r}")
        if mot == "stop":
            self.wfile.write(b"ARRET\n")
            threading.Thread(
                target=self.server.shutdown, daemon=True
            ).start()
            return
        if est_palindrome(mot):
            self.wfile.write(b"PALINDROME\n")
        else:
            self.wfile.write(b"PAS_PALINDROME\n")


if __name__ == "__main__":
    with socketserver.TCPServer((HOTE, PORT), PalindromeHandler) as serveur:
        print(f"<<< Serveur palindrome (socketserver TCP) sur {(HOTE, PORT)}")
        serveur.serve_forever()
        print("<<< Serveur arrêté")
