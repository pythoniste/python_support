"""Serveur TCP raw du service palindrome — framing par délimiteur.

À utiliser avec 02_raw_tcp_clt.py.
"""
import socket
from palindrome import est_palindrome


HOTE = "127.0.0.1"
PORT = 8808


def recv_ligne(sock, delim: bytes = b"\n") -> bytes:
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def traiter_client(connexion: socket.socket) -> bool:
    while True:
        ligne = recv_ligne(connexion).decode("utf-8", errors="replace")
        if not ligne:
            return True                                 # déconnexion
        print(f"    Reçu : {ligne!r}")
        if ligne == "stop":
            connexion.sendall(b"ARRET\n")
            return False                                # arrêt demandé
        if est_palindrome(ligne):
            connexion.sendall(b"PALINDROME\n")
        else:
            connexion.sendall(b"PAS_PALINDROME\n")


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur palindrome (raw TCP) sur {sockaddr}")
        while True:
            conn, addr = serveur.accept()
            print(f">>> Connexion depuis {addr}")
            with conn:
                if not traiter_client(conn):
                    print("<<< Arrêt du serveur demandé")
                    return


if __name__ == "__main__":
    main()
