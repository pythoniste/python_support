"""Client UDP raw pour le serveur palindrome.

À utiliser avec 03_raw_udp_srv.py.
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
        HOTE, PORT, type=socket.SOCK_DGRAM
    )[0]
    with socket.socket(famille, type_, proto) as client:
        for mot in MOTS:
            input(f"--- Entrée pour envoyer {mot!r}")
            client.sendto(mot.encode("utf-8"), sockaddr)
            reponse, _ = client.recvfrom(BUFFER_SIZE)
            interpreter(mot, reponse.decode("utf-8"))


if __name__ == "__main__":
    main()
