"""Client TCP STATEFUL — 3 messages successifs par emprunt.

Pour chaque emprunt : ouverture de connexion, envoi en 3 étapes,
fermeture. Chaque emprunt nécessite donc 4 round-trips réseau au
lieu de 1 dans la version stateless.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808

DEMANDES = [
    (200_000, 0.0475, 300, "Achat principal"),
    (100_000, 0.03,   240, "Investissement locatif"),
    (50_000,  0.0,    60,  "Prêt familial"),
]


def recv_ligne(sock, delim=b"\n"):
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def calculer(capital, taux, duree, sockaddr, famille, type_, proto):
    with socket.socket(famille, type_, proto) as client:
        client.connect(sockaddr)
        client.sendall(f"{capital}\n".encode("utf-8"))
        recv_ligne(client)                              # ack capital
        client.sendall(f"{taux}\n".encode("utf-8"))
        recv_ligne(client)                              # ack taux
        client.sendall(f"{duree}\n".encode("utf-8"))
        return recv_ligne(client).decode("utf-8")


def main():
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    for capital, taux, duree, libelle in DEMANDES:
        M = calculer(capital, taux, duree, sockaddr, famille, type_, proto)
        print(f"  [{libelle:25s}] mensualité = {M:>10s} €")


if __name__ == "__main__":
    main()
