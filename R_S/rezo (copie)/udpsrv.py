#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur UDP utilisant socket
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


params = ('127.0.0.1', 8808)
BUFFER_SIZE = 1024  # default

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # , socket.SOCK_STREAM)
s.bind(params)
# Les lignes suivantes n'ont pas de sens en UDP:
# s.listen(1)
# conn, addr = s.accept()
# print('Connexion acceptée: %s' % str(addr))

while True:
    print("<<< En attente")
    # data = conn.recv(BUFFER_SIZE)
    data, addr = s.recvfrom(BUFFER_SIZE)
    print(">>> Reçu:", data, "from:", addr)
    if not data:
        break
    # conn.send(b"Bonjour " + data.strip() + b".\n")
    s.sendto(b"Bonjour " + data.strip() + b".\n", addr)
s.close()

