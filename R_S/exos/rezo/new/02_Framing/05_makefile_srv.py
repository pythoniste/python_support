"""Serveur TCP utilisant socket.makefile().

`makefile("rwb")` retourne un objet file-like binaire qui encapsule
recv/send et fournit `readline()`/`write()` avec bufferisation.

C'est la base sur laquelle reposent `socketserver.StreamRequestHandler`
(dossier 03) et beaucoup de protocoles textuels (HTTP, SMTP, IRC…).

Sémantique de framing : délimiteur '\\n' (héritée de readline).

À utiliser avec 06_makefile_clt.py.
"""
import socket


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
        print(f"<<< Serveur (makefile) en attente sur {sockaddr}")

        while True:
            connexion, adresse = serveur.accept()
            print(f">>> Connexion depuis {adresse}")
            with connexion, connexion.makefile("rwb") as flux:
                if not traiter_client(flux):
                    print("<<< Arrêt du serveur demandé")
                    return


def traiter_client(flux) -> bool:
    while True:
        ligne = flux.readline().rstrip(b"\n")
        if not ligne:
            print("<<< Client déconnecté")
            return True
        print(f"    Reçu : {ligne!r}")
        if ligne == b"stop":
            flux.write(b"Arret du serveur.\n")
            flux.flush()
            return False
        flux.write(b"Bonjour " + ligne + b".\n")
        flux.flush()                                    # indispensable !


if __name__ == "__main__":
    main()
