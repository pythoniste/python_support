"""Serveur TCP STATEFUL — accumule les 3 paramètres au fil des messages.

Protocole :
    Client → "<capital>\\n"      Serveur → "OK_CAPITAL\\n"
    Client → "<taux>\\n"         Serveur → "OK_TAUX\\n"
    Client → "<duree>\\n"        Serveur → "<mensualite>\\n"

L'état (les valeurs reçues) vit dans la fonction traiter_client,
donc **par connexion**. C'est la connexion TCP qui borne la session.

FRAGILE : si le client meurt entre les messages, l'état est perdu.
Si la séquence est désordonnée, le résultat est faux silencieusement.

À comparer avec 01_stateless_srv.py — même service, opposé en design.
"""
import socket
from mensualite import calcul_mensualite


HOTE = "127.0.0.1"
PORT = 8808


def recv_ligne(sock, delim=b"\n"):
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def traiter_client(connexion):
    # État de cette session = variables locales de la fonction.
    msg = recv_ligne(connexion)
    if not msg:
        return
    capital = float(msg)
    connexion.sendall(b"OK_CAPITAL\n")

    msg = recv_ligne(connexion)
    if not msg:
        print("    Client a abandonné après le capital — session perdue")
        return
    taux = float(msg)
    connexion.sendall(b"OK_TAUX\n")

    msg = recv_ligne(connexion)
    if not msg:
        print("    Client a abandonné après le taux — session perdue")
        return
    duree = int(msg)

    M = calcul_mensualite(capital, taux, duree, arrondi=True)
    connexion.sendall(f"{M}\n".encode("utf-8"))
    print(f"    K={capital} t={taux} n={duree} -> {M}")


def main():
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur mensualité STATEFUL sur {sockaddr}")
        while True:
            conn, addr = serveur.accept()
            print(f">>> Session avec {addr}")
            with conn:
                traiter_client(conn)


if __name__ == "__main__":
    main()
