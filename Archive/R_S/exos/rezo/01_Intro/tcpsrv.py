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

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(params)
s.listen(1)

print("<<< En attente")

conn, addr = s.accept()
print("Connexion acceptée: %s" % str(addr))

while True:
    print("<<< Traitement donnée")
    data = conn.recv(BUFFER_SIZE)
    print(">>> Reçu: ", data)
    if not data:
        conn.close()
        break
    if data == b"stop":
        print("Arrêt du serveur")
        conn.close()
        s.close()
        break
    conn.send(b"Bonjour " + data.strip() + b".\n")

