"""Serveur TCP STATELESS — tous les paramètres en une requête JSON.

Format requête : {"capital": K, "taux": t, "duree": n}
Format réponse : {"mensualite": M}  ou  {"erreur": "..."}

Aucune mémoire entre requêtes côté serveur. Le protocole est
robuste : si le client meurt, rien à nettoyer.

À comparer avec 03_stateful_srv.py (même service, conception opposée).
"""
import json
import socket
from mensualite import calcul_mensualite


HOTE = "127.0.0.1"
PORT = 8808


def recv_ligne(sock, delim=b"\n"):
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def traiter_client(connexion):
    while True:
        ligne = recv_ligne(connexion)
        if not ligne:
            return
        try:
            req = json.loads(ligne)
            M = calcul_mensualite(
                req["capital"], req["taux"], req["duree"], arrondi=True
            )
            reponse = {"mensualite": M}
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            reponse = {"erreur": str(exc)}
        connexion.sendall(json.dumps(reponse).encode("utf-8") + b"\n")


def main():
    famille, type_, proto, _, sockaddr = socket.getaddrinfo(
        HOTE, PORT, type=socket.SOCK_STREAM
    )[0]
    with socket.socket(famille, type_, proto) as serveur:
        serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serveur.bind(sockaddr)
        serveur.listen(5)
        print(f"<<< Serveur mensualité STATELESS (JSON) sur {sockaddr}")
        while True:
            conn, _ = serveur.accept()
            with conn:
                traiter_client(conn)


if __name__ == "__main__":
    main()
