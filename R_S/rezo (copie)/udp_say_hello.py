#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client UDP utilisant le serveur réalisé avec socketserver
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
BUFFER_SIZE = 1024 # default

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

messages = [
	b'Paul\n',
	b'Pierre\n',
]

for m in messages:
	print("Envoi d'un message %s" % m)
	s.sendto(m, params)
	data = s.recv(BUFFER_SIZE)
	if len(data) == 0:
		print('\tPas de réponses')
	else:
		print('\tDonnée récupérée du serveur : %s' % data)
