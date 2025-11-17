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

params = ('127.0.0.1', 8809)

donnees = []


class ExampleTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.rfile.readline().strip()
        print(type(data))

        if data == b"stop":
            print("Arrêt du serveur")
            # self.server.shutdown()  # Se met en attente ici
            # self.server.server_close()  # pas le bon endroit
        elif data == b"*":
            print("Renvoi de la dernière valeur", end="")
            if donnees:
                print(donnees[-1])
                self.wfile.write(donnees[-1])
            else:
                print("Pas encore de valeurs")
                self.wfile.write("Pas encore de valeurs")
        else:
            print("enregistrement de la valeur", data)
            donnees.append(data)
            self.wfile.write(b"Donnees '" + data.strip() + b"' enregistree.\n")


if __name__ == '__main__':
    server = socketserver.TCPServer(params, ExampleTCPHandler)
    server.serve_forever()

