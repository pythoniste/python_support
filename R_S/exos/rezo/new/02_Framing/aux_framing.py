"""Utilitaires de framing TCP, repris partout dans le dossier.

Quatre fonctions :
- recv_exactement(sock, n)              : lit exactement n octets
- recv_ligne(sock, delim=b"\\n")        : lit jusqu'au délimiteur (exclu)
- envoyer_message_prefixe(sock, msg)    : envoi avec préfixe de longueur
- recevoir_message_prefixe(sock)        : réception avec préfixe de longueur
"""
import socket
import struct


def recv_exactement(sock: socket.socket, n: int) -> bytes:
    """Lit exactement n octets, en bouclant sur les recv() partiels.

    Lève ConnectionError si la connexion ferme avant d'avoir tout reçu.
    """
    morceaux: list[bytes] = []
    restant = n
    while restant:
        bloc = sock.recv(restant)
        if not bloc:
            raise ConnectionError(
                f"Connexion fermée après {n - restant} octets sur {n} attendus"
            )
        morceaux.append(bloc)
        restant -= len(bloc)
    return b"".join(morceaux)


def recv_ligne(sock: socket.socket, delimiteur: bytes = b"\n") -> bytes:
    """Lit octet par octet jusqu'au délimiteur (exclu).

    Retourne b"" si la connexion ferme avant la première lecture.
    Version pédagogique simple : cf. atelier 5 pour une version
    bufferisée plus efficace.
    """
    morceaux: list[bytes] = []
    while True:
        octet = sock.recv(1)
        if not octet:
            return b"".join(morceaux)
        if octet == delimiteur:
            return b"".join(morceaux)
        morceaux.append(octet)


def envoyer_message_prefixe(sock: socket.socket, message: bytes) -> None:
    """Envoie un message précédé de sa longueur (4 octets, network byte order)."""
    sock.sendall(struct.pack("!I", len(message)) + message)


def recevoir_message_prefixe(sock: socket.socket) -> bytes:
    """Lit un message à partir de son préfixe de longueur."""
    (longueur,) = struct.unpack("!I", recv_exactement(sock, 4))
    return recv_exactement(sock, longueur)
