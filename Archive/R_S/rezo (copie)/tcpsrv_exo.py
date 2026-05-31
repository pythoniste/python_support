#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socket
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import socket


params = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default

donnees = []

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(params)
s.listen(1)

print("<<< En attente")

conn, addr = s.accept()
print("Connexion acceptée: %s" % str(addr))

while True:
    print("<<< Traitement donnée")
    data = conn.recv(BUFFER_SIZE).strip()

    if not data:
        conn.close()
        break
    elif data == b"stop":
        print("Arrêt du serveur")
        conn.close()
        s.close()
        break
    elif data == b"*":
        print("Renvoi de la dernière valeur", end="")
        if donnees:
            print(donnees[-1])
            conn.send(donnees[-1])
        else:
            print("Pas encore de valeurs")
            conn.send("Pas encore de valeurs")
    else:
        print("enregistrement de la valeur", data)
        donnees.append(data)
        conn.send(b"Donnees '" + data.strip() + b"' enregistree.\n")

