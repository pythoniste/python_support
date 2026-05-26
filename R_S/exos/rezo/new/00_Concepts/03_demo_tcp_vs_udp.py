"""TCP vs UDP : la différence fondamentale, démontrée en deux essais.

À exécuter :  python3 03_demo_tcp_vs_udp.py

Observer :
- TCP exige une connexion → si personne n'écoute, on a une erreur immédiate.
- UDP est sans connexion → on peut envoyer dans le vide, le système
  d'exploitation accepte sans broncher.
"""
import socket


# Port choisi pour qu'aucun service n'y écoute (port 1 = tcpmux, jamais utilisé
# en pratique sur un poste de développement).
PORT_FERME = ("127.0.0.1", 1)


# 1. TCP : la connexion échoue si personne n'écoute.
print("[TCP] tentative de connexion à un port fermé...")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        s.connect(PORT_FERME)
        print("       connecté (inattendu)")
except (ConnectionRefusedError, OSError) as exc:
    print(f"       échec : {type(exc).__name__} — {exc}")

print()

# 2. UDP : l'envoi réussit toujours (« fire and forget »).
print("[UDP] envoi d'un datagramme vers le même port fermé...")
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        n = s.sendto(b"coucou", PORT_FERME)
        print(f"       {n} octets envoyés, aucune erreur signalée")
except OSError as exc:
    print(f"       échec : {type(exc).__name__} — {exc}")

print()
print("Numéros de protocole IANA :")
print(f"  TCP = {socket.getprotobyname('tcp')}")
print(f"  UDP = {socket.getprotobyname('udp')}")
