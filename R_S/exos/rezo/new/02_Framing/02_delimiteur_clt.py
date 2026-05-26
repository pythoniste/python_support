"""Client TCP avec framing par délimiteur ('\\n').

À utiliser avec 01_delimiteur_srv.py. Chaque message est terminé
par '\\n'. La réponse est lue ligne par ligne via `recv_ligne`.
"""
import socket
from aux_framing import recv_ligne


HOTE = "127.0.0.1"
PORT = 8808

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
            client.sendall(message + b"\n")             # délimiteur en queue
            reponse = recv_ligne(client)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
