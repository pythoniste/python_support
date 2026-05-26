"""Cycle de vie d'un socket : visualiser les états successifs.

À exécuter :  python3 04_demo_cycle_de_vie.py

Observer :
- l'adresse vide tant qu'on n'a pas appelé bind() ;
- l'adresse réelle attribuée après bind() (port choisi par l'OS via 0) ;
- le fait que UDP n'a ni listen() ni accept().
"""
import socket


print("=== Serveur TCP ===\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp:
    print("État 1 — socket() : descripteur créé, pas encore attaché")
    print("         getsockname() =", tcp.getsockname())

    tcp.bind(("127.0.0.1", 0))  # 0 = port libre choisi par l'OS
    print("\nÉtat 2 — bind() : adresse locale attribuée")
    print("         getsockname() =", tcp.getsockname())

    tcp.listen(5)
    print("\nÉtat 3 — listen(5) : socket en attente de clients")
    print("         (un appel à accept() bloquerait ici jusqu'à connexion)")


print("\n\n=== Serveur UDP ===\n")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
    udp.bind(("127.0.0.1", 0))
    print("État unique — bind() : prêt à recevoir des datagrammes")
    print("              getsockname() =", udp.getsockname())
    print("              Pas de listen() ni de accept() en UDP.")
