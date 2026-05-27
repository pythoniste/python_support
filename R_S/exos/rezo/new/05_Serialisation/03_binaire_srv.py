"""Serveur TCP du service nombre aléatoire — encodage BINAIRE fixed-size.

Trames de 4 octets dans les deux sens (uint32 big-endian).
"""
import random
import socket
from encodage import pack_binaire, unpack_binaire, recv_exactement


HOTE = "127.0.0.1"
PORT = 8808


def traiter_client(connexion: socket.socket) -> None:
    try:
        while True:
            trame = recv_exactement(connexion, 4)
            max_value = unpack_binaire(trame)
            resultat = random.randint(0, max_value)
            connexion.sendall(pack_binaire(resultat))
    except ConnectionError:
        return                                          # client déconnecté


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur aléatoire (BINAIRE) sur {sockaddr}")
        while True:
            connexion, adresse = serveur.accept()
            with connexion:
                traiter_client(connexion)


if __name__ == "__main__":
    main()
