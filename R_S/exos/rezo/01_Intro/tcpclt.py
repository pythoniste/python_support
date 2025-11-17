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


params = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(params)

s.send(b"World")
data = s.recv(BUFFER_SIZE)
print("\tDonnée récupérée du serveur : %s" % data)
input()
s.send(b"Vous")
data = s.recv(BUFFER_SIZE)
print("\tDonnée récupérée du serveur : %s" % data)
input()
s.send(b"stop")
data = s.recv(BUFFER_SIZE)
print("\tDonnée récupérée du serveur : %s" % data)

s.close()

