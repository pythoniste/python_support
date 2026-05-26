"""Client TCP minimal — à utiliser avec 01_tcpsrv.py.

Démontre le cycle de vie d'un client TCP :
    socket() → connect() → send/recv → close()

Trois échanges sont enchaînés avec une pause clavier entre chacun,
pour observer le dialogue côté serveur. Le dernier message ("stop")
arrête le serveur.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024

MESSAGES = [b"World", b"Vous", b"stop"]


def main() -> None:
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]

    with socket.socket(famille, type_, proto) as client:
        client.connect(sockaddr)
        print(f"<<< Connecté à {sockaddr}")

        for message in MESSAGES:
            input(f"--- Entrée pour envoyer {message!r}")
            client.sendall(message)
            reponse = client.recv(BUFFER_SIZE)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
