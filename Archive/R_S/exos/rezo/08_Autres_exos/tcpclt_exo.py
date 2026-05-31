#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client TCP utilisant serveur socket
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


params = ("127.0.0.1", 8809)
BUFFER_SIZE = 1024 # default

while True:
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(params)
    saisie = input("Saisissez ce qu'il faut envoyer au serveur")
    s.send(saisie.encode("utf8") + b"\n")
    data = s.recv(BUFFER_SIZE)
    print("\tDonnée récupérée du serveur >>> %s" % data)
    if not data:
        break
    s.close()

