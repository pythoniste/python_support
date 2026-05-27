"""Client LENT — envoie 5 messages avec 0,3 s entre chacun.

Simule un client réaliste qui ne peut pas tout envoyer instantanément.
Cumulé sur 5 messages, une session dure ~1,5 s.

Usage :  python3 05_clt_lent.py [libelle]
"""
import socket
import sys
import time


HOTE = "127.0.0.1"
PORT = 8808
N_MESSAGES = 5
ATTENTE = 0.3


def main(libelle: str = "C") -> None:
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    debut = time.perf_counter()
    with socket.socket(famille, type_, proto) as client:
        client.connect(sockaddr)
        for i in range(1, N_MESSAGES + 1):
            msg = f"{libelle}#{i}\n".encode("utf-8")
            client.sendall(msg)
            reponse = client.recv(1024).rstrip(b"\n")
            print(f"  [{libelle}] envoyé {msg.rstrip()!r:>10s} reçu {reponse!r}")
            time.sleep(ATTENTE)
    duree = time.perf_counter() - debut
    print(f"[{libelle}] durée totale : {duree:.2f} s")


if __name__ == "__main__":
    libelle = sys.argv[1] if len(sys.argv) > 1 else "C"
    main(libelle)
