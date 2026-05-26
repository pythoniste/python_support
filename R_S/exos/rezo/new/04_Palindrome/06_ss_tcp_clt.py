"""Client TCP pour le serveur socketserver palindrome.

Une connexion par mot — le handler termine à chaque appel.
À utiliser avec 05_ss_tcp_srv.py.
"""
import socket


HOTE = "127.0.0.1"
PORT = 8808
BUFFER_SIZE = 1024

MOTS = [
    "mot",
    "anna",
    "Karine alla en Irak!",
    "stop",
]


def recv_ligne(sock, delim: bytes = b"\n") -> bytes:
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def interpreter(mot: str, reponse: str) -> None:
    if reponse == "PALINDROME":
        print(f"    Le mot {mot!r} est un palindrome.")
    elif reponse == "PAS_PALINDROME":
        print(f"    Le mot {mot!r} n'est pas un palindrome.")
    elif reponse == "ARRET":
        print(f"    Le serveur s'est arrêté ({mot!r}).")
    else:
        print(f"    Réponse inattendue : {reponse!r}")


def main() -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    for mot in MOTS:
        input(f"--- Entrée pour envoyer {mot!r}")
        with socket.socket(famille, type_, proto) as client:
            client.connect(sockaddr)
            client.sendall(mot.encode("utf-8") + b"\n")
            reponse = recv_ligne(client).decode("utf-8")
            interpreter(mot, reponse)


if __name__ == "__main__":
    main()
