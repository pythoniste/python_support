"""Serveur TCP avec framing par préfixe de longueur.

Chaque message est précédé de 4 octets en big-endian indiquant la
longueur du payload qui suit. Le serveur lit le préfixe puis lit
exactement cette longueur, et répond avec le même protocole.

À utiliser avec 04_prefixe_clt.py.
"""
import socket
from aux_framing import envoyer_message_prefixe, recevoir_message_prefixe


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
        print(f"<<< Serveur (préfixe) en attente sur {sockaddr}")

        while True:
            connexion, adresse = serveur.accept()
            print(f">>> Connexion depuis {adresse}")
            with connexion:
                if not traiter_client(connexion):
                    print("<<< Arrêt du serveur demandé")
                    return


def traiter_client(connexion: socket.socket) -> bool:
    try:
        while True:
            message = recevoir_message_prefixe(connexion)
            print(f"    Reçu : {message!r}")
            if message == b"stop":
                envoyer_message_prefixe(connexion, b"Arret du serveur.")
                return False
            envoyer_message_prefixe(connexion, b"Bonjour " + message + b".")
    except ConnectionError:
        print("<<< Client déconnecté")
        return True


if __name__ == "__main__":
    main()
