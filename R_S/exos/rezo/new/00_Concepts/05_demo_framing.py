"""Le problème du framing, démontré sans avoir besoin d'un serveur tiers.

socket.socketpair() crée deux sockets STREAM connectés dans le même
processus. Ils ont exactement les mêmes propriétés de flux qu'un TCP/IPv4.

À exécuter :  python3 05_demo_framing.py

Observer :
- trois envois distincts arrivent en un seul recv() ;
- on ne peut PAS retrouver les frontières d'origine sans délimiteur ;
- la fonction recv_exactement compense les recv() partiels.
"""
import socket


# --- 1. Les frontières disparaissent ------------------------------------
emetteur, recepteur = socket.socketpair()

emetteur.send(b"Bonjour ")
emetteur.send(b"le ")
emetteur.send(b"monde !")
emetteur.close()  # signale la fin de l'envoi

print("Côté récepteur, un seul recv(100) :")
print("  ", recepteur.recv(100))
# -> b'Bonjour le monde !'
#    Les 3 frontières d'envoi ont DISPARU.

recepteur.close()


# --- 2. La fonction canonique : lire exactement N octets ----------------
print()
print("Solution canonique : la fonction recv_exactement")
print("-" * 50)


def recv_exactement(sock, n):
    """Lit exactement n octets, en bouclant sur les recv() partiels."""
    morceaux = []
    restant = n
    while restant:
        bloc = sock.recv(restant)
        if not bloc:
            raise ConnectionError("Connexion fermée prématurément")
        morceaux.append(bloc)
        restant -= len(bloc)
    return b"".join(morceaux)


a, b = socket.socketpair()
a.send(b"ABCDEFGHIJ")
print("recv_exactement(b, 5) =", recv_exactement(b, 5))  # b'ABCDE'
print("recv_exactement(b, 5) =", recv_exactement(b, 5))  # b'FGHIJ'

a.close()
b.close()
