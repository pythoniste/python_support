"""Serveur ECHO — version ITÉRATIVE (un client à la fois).

Le `accept()` n'est appelé que **après** la déconnexion du client
courant. Si un client lent monopolise la connexion, tout le monde
attend dans la file de listen().

C'est notre BASELINE de comparaison.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808


def traiter(connexion: socket.socket, adresse) -> None:
    print(f">>> Client {adresse} connecté")
    with connexion, connexion.makefile("rwb") as flux:
        for ligne in flux:
            ligne = ligne.rstrip(b"\n")
            if not ligne:
                break
            print(f"    [{adresse[1]}] -> {ligne!r}")
            flux.write(b"ECHO " + ligne + b"\n")
            flux.flush()
    print(f"<<< Client {adresse} déconnecté")


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur ITÉRATIF sur {sockaddr}")
        while True:
            connexion, adresse = serveur.accept()
            traiter(connexion, adresse)                 # bloque la boucle


if __name__ == "__main__":
    main()
