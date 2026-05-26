"""Serveur UDP raw du service palindrome.

Pas de framing nécessaire — un datagramme = un mot. À utiliser avec
04_raw_udp_clt.py.
"""
import socket
from palindrome import est_palindrome


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_DGRAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        print(f"<<< Serveur palindrome (raw UDP) sur {sockaddr}")
        while True:
            data, addr = serveur.recvfrom(BUFFER_SIZE)
            mot = data.decode("utf-8", errors="replace").strip()
            print(f"    Reçu de {addr} : {mot!r}")
            if mot == "stop":
                serveur.sendto(b"ARRET", addr)
                print("<<< Arrêt du serveur demandé")
                return
            if est_palindrome(mot):
                serveur.sendto(b"PALINDROME", addr)
            else:
                serveur.sendto(b"PAS_PALINDROME", addr)


if __name__ == "__main__":
    main()
