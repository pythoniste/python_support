"""Client TCP minimal — à utiliser avec 01_tcpsrv.py.

Le serveur traite UNE requête par connexion (le handler se termine et
ferme la connexion). Le client doit donc se reconnecter pour chaque
message — pattern classique des serveurs socketserver.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024

MESSAGES = [b"World", b"Vous", b"Final"]


def recv_ligne(sock, delim: bytes = b"\n") -> bytes:
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def main() -> None:
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]

    for message in MESSAGES:
        input(f"--- Entrée pour envoyer {message!r}")
        with socket.socket(famille, type_, proto) as client:
            client.connect(sockaddr)
            client.sendall(message + b"\n")
            reponse = recv_ligne(client)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
