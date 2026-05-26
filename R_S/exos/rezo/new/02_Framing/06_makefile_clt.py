"""Client TCP utilisant socket.makefile().

À utiliser avec 05_makefile_srv.py.

Noter le `flush()` après chaque `write()` — sans lui, les octets
restent dans le buffer Python et ne partent jamais sur le socket.
"""
import socket


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

        with client.makefile("rwb") as flux:
            for message in MESSAGES:
                input(f"--- Entrée pour envoyer {message!r}")
                flux.write(message + b"\n")
                flux.flush()
                reponse = flux.readline().rstrip(b"\n")
                print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
