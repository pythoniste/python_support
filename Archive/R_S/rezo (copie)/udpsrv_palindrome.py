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


import sys

import string
import socket


def est_palindrome(chaine):
    chaine = chaine.lower()
    for c in string.whitespace + string.punctuation:
        chaine = chaine.replace(c, "")
    return chaine == chaine[::-1]


params = ('127.0.0.1', 8819)
BUFFER_SIZE = 1024 # default

donnees = {}

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(params)

while True:
    print("<<< Traitement donnée")
    data, addr = s.recvfrom(BUFFER_SIZE)
    print('Connexion acceptée: %s' % str(addr))
    print(">>> Reçu: ", data)
    if data == b"#":
        print("Arrêt du serveur")
        s.sendto(b'S', addr)
        s.close()
        sys.exit()
    data = data.decode("utf-8")
    if est_palindrome(data):
        s.sendto(b'T', addr)
    else:
        s.sendto(b'F', addr)

