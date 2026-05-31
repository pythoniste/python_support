#!/usr/bin/python3
# -*- coding: utf-8 -*-


import random
import socketserver
from conv2 import int2bytes, bytes2int


PARAMS = ('127.0.0.1', 8809)


def generer_entier(max):
    return random.randint(0, max)


class RandomTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        max = bytes2int(self.rfile.readline().strip())
        resultat = generer_entier(max)
        self.wfile.write(int2bytes(resultat))

if __name__ == '__main__':
    server = socketserver.TCPServer(PARAMS, RandomTCPHandler)
    server.serve_forever()

