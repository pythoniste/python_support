"""Serveur ECHO — version SELECTORS (multiplexage I/O).

Un seul thread, plusieurs sockets surveillés simultanément par
`selectors.DefaultSelector()` (epoll sous Linux, kqueue sous BSD,
select sous Windows).

Le code utilise des **callbacks** : pour chaque événement signalé
par le sélecteur, on appelle la fonction associée.

C'est ce qui se passe en dessous de asyncio.
"""
import selectors
import socket


HOTE = "127.0.0.1"
PORT = 8808

sel = selectors.DefaultSelector()


def accepter(serveur: socket.socket) -> None:
    """Callback invoqué quand le socket d'écoute a une connexion entrante."""
    conn, addr = serveur.accept()
    print(f">>> Client {addr} connecté (fd={conn.fileno()})")
    conn.setblocking(False)
    # On enregistre le nouveau socket pour les lectures.
    sel.register(conn, selectors.EVENT_READ, lire)


def lire(conn: socket.socket) -> None:
    """Callback invoqué quand un client connecté a des données prêtes."""
    addr = conn.getpeername()
    data = conn.recv(4096)
    if not data:
        print(f"<<< Client {addr} déconnecté")
        sel.unregister(conn)
        conn.close()
        return
    # Découpage simple par ligne (le client envoie '\n' à la fin de chaque message).
    for ligne in data.split(b"\n"):
        if ligne:
            print(f"    [{addr[1]}] -> {ligne!r}")
            conn.sendall(b"ECHO " + ligne + b"\n")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind((HOTE, PORT))
        serveur.listen(5)
        serveur.setblocking(False)
        sel.register(serveur, selectors.EVENT_READ, accepter)

        print(f"<<< Serveur SELECTORS sur {(HOTE, PORT)}")
        while True:
            for key, _ in sel.select():
                callback = key.data
                callback(key.fileobj)


if __name__ == "__main__":
    main()
