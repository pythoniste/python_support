"""Client TCP avec framing par préfixe de longueur.

À utiliser avec 03_prefixe_srv.py.
"""
import socket
from aux_framing import envoyer_message_prefixe, recevoir_message_prefixe


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
            envoyer_message_prefixe(client, message)
            reponse = recevoir_message_prefixe(client)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
