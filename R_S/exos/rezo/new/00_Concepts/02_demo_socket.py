"""Inspection d'un socket : il a un descripteur OS comme un fichier.

À exécuter :  python3 02_demo_socket.py

Observer :
- le numéro de descripteur (fileno) — un simple entier ;
- les trois caractéristiques (famille, type, proto) ;
- la libération automatique du descripteur à la sortie du `with`.
"""
import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Descripteur OS (fileno) :", s.fileno())
    print("Famille  :", s.family.name)   # AddressFamily.AF_INET
    print("Type     :", s.type.name)     # SocketKind.SOCK_STREAM
    print("Proto    :", s.proto)         # 0 (TCP par défaut)
    print("Bloquant :", s.getblocking())
    print("Timeout  :", s.gettimeout())  # None = pas de timeout

# À la sortie du with, le descripteur est libéré.
# Si on imprimait s.fileno() ici, on aurait -1 (socket fermé).
print()
print("Après le with, fileno =", s.fileno(), "(socket fermé)")
