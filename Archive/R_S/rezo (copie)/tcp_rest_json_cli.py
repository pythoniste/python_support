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
import json


params = ('127.0.0.1', 8809)
BUFFER_SIZE = 1024 # default

messages = [
    {"method": "add", "values": [4, 2, 7] },
    {"method": "sub", "values": [4, 2] },
    {"method": "mul", "values": [4, 2] },
    {"method": "truediv", "values": [4, 2] },
    {"method": "mul", "values": [4, 2, 6] },
]

for m in messages:
    print("Envoi des données %s" % m)
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(params)
    s.send(json.dumps(m).encode("utf8") + b'\n')
    data = s.recv(BUFFER_SIZE)
    print('\tDonnée récupérée du serveur : %s' % data)
    s.close()

