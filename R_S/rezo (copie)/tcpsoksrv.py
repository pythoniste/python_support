#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socketserver
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import socketserver

params = ('127.0.0.1', 8808)

donnees = []


class ExampleTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.rfile.readline().strip()
        print('>>> Reçu: %s', data)
        self.wfile.write(b"Bonjour " + data + b".\n")


if __name__ == '__main__':
    server = socketserver.TCPServer(params, ExampleTCPHandler)
    server.serve_forever()

