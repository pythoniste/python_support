"""Client TCP du service nombre aléatoire — encodage TEXTE.

Demande 1000 tirages dans [0, MAX]. Affiche la moyenne pour vérifier
empiriquement l'uniformité (attendu ≈ MAX/2).
"""
import socket
from encodage import pack_texte, unpack_texte, recv_ligne


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
            client.sendall(pack_texte(MAX))
            nombres.append(unpack_texte(recv_ligne(client)))

    moyenne = sum(nombres) / N
    print(f"<<< {N} tirages dans [0, {MAX}]")
    print(f"    moyenne empirique : {moyenne:.3f}")
    print(f"    moyenne attendue  : {MAX / 2:.3f}")


if __name__ == "__main__":
    main()
