"""Client TCP du service nombre aléatoire — encodage BINAIRE fixed-size."""
import socket
from encodage import pack_binaire, unpack_binaire, recv_exactement


HOTE = "127.0.0.1"
PORT = 8808
MAX = 42
N = 1000


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    nombres = []
    with socket.socket(famille, type_, proto) as client:
        client.connect(sockaddr)
        for _ in range(N):
            client.sendall(pack_binaire(MAX))
            nombres.append(unpack_binaire(recv_exactement(client, 4)))

    moyenne = sum(nombres) / N
    print(f"<<< {N} tirages dans [0, {MAX}]")
    print(f"    moyenne empirique : {moyenne:.3f}")
    print(f"    moyenne attendue  : {MAX / 2:.3f}")


if __name__ == "__main__":
    main()
