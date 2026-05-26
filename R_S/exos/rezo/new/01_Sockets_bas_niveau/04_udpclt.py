"""Client UDP minimal — à utiliser avec 03_udpsrv.py.

Démontre le cycle de vie d'un client UDP :
    socket() → sendto/recvfrom → close()

Pas de connect() : UDP n'est pas connexionnel, on envoie à l'adresse
directement. Une pause clavier précède chaque envoi pour observer
les échanges côté serveur.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024

MESSAGES = [b"World", b"Paul", b"Pierre"]


def main() -> None:
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_DGRAM
    )[0]

    with socket.socket(famille, type_, proto) as client:
        for message in MESSAGES:
            input(f"--- Entrée pour envoyer {message!r}")
            client.sendto(message, sockaddr)
            reponse, _ = client.recvfrom(BUFFER_SIZE)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
