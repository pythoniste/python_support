"""Serveur TCP du service nombre aléatoire — encodage JSON.

Chaque message est un objet JSON `{"valeur": n}` suivi de \\n.
Format extensible : on pourrait ajouter d'autres champs sans changer
le protocole de framing.
"""
import random
import socket
from encodage import pack_json, unpack_json, recv_ligne


HOTE = "127.0.0.1"
PORT = 8808


def traiter_client(connexion: socket.socket) -> None:
    while True:
        ligne = recv_ligne(connexion)
        if not ligne:
            return
        max_value = unpack_json(ligne)
        resultat = random.randint(0, max_value)
        connexion.sendall(pack_json(resultat))


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur aléatoire (JSON) sur {sockaddr}")
        while True:
            connexion, adresse = serveur.accept()
            with connexion:
                traiter_client(connexion)


if __name__ == "__main__":
    main()
