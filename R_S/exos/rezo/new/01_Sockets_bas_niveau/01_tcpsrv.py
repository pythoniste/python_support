"""Serveur TCP minimal.

Démontre le cycle de vie d'un serveur TCP :
    socket() → bind() → listen() → accept() → recv/send → close()

Le serveur écoute sur 127.0.0.1:8808. Pour chaque client qui se
connecte, il répond "Bonjour <data>." à chaque message reçu. Le
mot-clé "stop" arrête le serveur.

Limites volontaires :
- un seul client à la fois (concurrence traitée plus tard) ;
- recv(BUFFER_SIZE) suppose que les messages arrivent en un bloc —
  vrai en local sur messages courts, faux en général (voir module
  00/05 sur le framing).
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024


def main() -> None:
    # Résolution de l'adresse via getaddrinfo (cf. module 00/01).
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]

    with socket.socket(famille, type_, proto) as serveur:
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur TCP en attente sur {sockaddr}")

        while True:
            connexion, adresse_client = serveur.accept()
            print(f">>> Connexion acceptée depuis {adresse_client}")
            with connexion:
                if not traiter_client(connexion):
                    print("<<< Arrêt du serveur demandé")
                    return


def traiter_client(connexion: socket.socket) -> bool:
    """Boucle d'échanges avec un client. Renvoie False pour arrêter le serveur."""
    while True:
        data = connexion.recv(BUFFER_SIZE)
        if not data:
            print("<<< Client déconnecté")
            return True
        print(f"    Reçu : {data!r}")
        if data.strip() == b"stop":
            connexion.sendall(b"Arret du serveur.\n")
            return False
        connexion.sendall(b"Bonjour " + data.strip() + b".\n")


if __name__ == "__main__":
    main()
