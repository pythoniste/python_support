"""Serveur UDP minimal.

Démontre le cycle de vie d'un serveur UDP :
    socket() → bind() → recvfrom/sendto → close()

Pas de listen(), pas de accept() — UDP n'est pas connexionnel.
À chaque datagramme reçu, le serveur répond "Bonjour <data>."

Limites volontaires :
- pas d'arrêt propre (interrompre avec Ctrl-C) ;
- pas de gestion d'erreur (datagramme malformé, etc.).
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024


def main() -> None:
    famille, type_, proto, _canon, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_DGRAM
    )[0]

    with socket.socket(famille, type_, proto) as serveur:
        serveur.bind(sockaddr)
        print(f"<<< Serveur UDP en attente sur {sockaddr}")

        while True:
            data, adresse_client = serveur.recvfrom(BUFFER_SIZE)
            print(f">>> Reçu de {adresse_client} : {data!r}")
            if not data:
                continue
            serveur.sendto(b"Bonjour " + data.strip() + b".\n", adresse_client)


if __name__ == "__main__":
    main()
