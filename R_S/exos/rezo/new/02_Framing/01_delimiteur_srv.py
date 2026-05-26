"""Serveur TCP avec framing par délimiteur ('\\n').

Chaque message est terminé par '\\n'. Le serveur lit ligne par ligne
via `recv_ligne` (cf. aux_framing.py), et répond ligne par ligne.

Le mot-clé `stop` arrête le serveur.

À utiliser avec 02_delimiteur_clt.py.
"""
import socket
from aux_framing import recv_ligne


HOTE = "127.0.0.1"
PORT = 8808


def main() -> None:
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]

    with socket.socket(famille, type_, proto) as serveur:
        # Autorise le rebind immédiat sur un port en TIME_WAIT (pratique
        # en développement, lorsqu'on redémarre souvent le serveur).
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur (délimiteur) en attente sur {sockaddr}")

        while True:
            connexion, adresse = serveur.accept()
            print(f">>> Connexion depuis {adresse}")
            with connexion:
                if not traiter_client(connexion):
                    print("<<< Arrêt du serveur demandé")
                    return


def traiter_client(connexion: socket.socket) -> bool:
    while True:
        ligne = recv_ligne(connexion)
        if not ligne:
            print("<<< Client déconnecté")
            return True
        print(f"    Reçu : {ligne!r}")
        if ligne == b"stop":
            connexion.sendall(b"Arret du serveur.\n")
            return False
        connexion.sendall(b"Bonjour " + ligne + b".\n")


if __name__ == "__main__":
    main()
