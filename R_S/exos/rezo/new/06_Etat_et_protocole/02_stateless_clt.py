"""Client TCP STATELESS — chaque demande tient en UNE requête JSON.

Trois emprunts traités dans la même connexion, chacun en 1 aller-retour.
"""
import json
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


def main():
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as client:
        client.connect(sockaddr)
        for capital, taux, duree, libelle in DEMANDES:
            req = {"capital": capital, "taux": taux, "duree": duree}
            client.sendall(json.dumps(req).encode("utf-8") + b"\n")
            rep = json.loads(recv_ligne(client))
            if "mensualite" in rep:
                print(f"  [{libelle:25s}] mensualité = {rep['mensualite']:>10.2f} €")
            else:
                print(f"  [{libelle:25s}] erreur : {rep.get('erreur')}")


if __name__ == "__main__":
    main()
