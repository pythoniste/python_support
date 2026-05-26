"""Client UDP minimal — à utiliser avec 03_udpsrv.py."""
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
            client.sendto(message + b"\n", sockaddr)
            reponse, _ = client.recvfrom(BUFFER_SIZE)
            print(f"    Réponse : {reponse!r}")


if __name__ == "__main__":
    main()
