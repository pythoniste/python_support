#!/usr/bin/python3
# -*- coding: utf-8 -*-


import random
import socketserver
from conv2 import bytes2int, bytes2float, float2bytes

PARAMS = ('127.0.0.1', 8808)


def calcul_mensualité(capital, taux_annuel, durée_en_mois, *, arrondi=False):
    """
    Calcul d'une mensualité:

    Paramètres :
    - capital en euros
    - un taux annuel (4.75% vaut 0.0475)
    - durée mensuelle (25 ans font 300 mois)
    - arrondi (booléen, obligatoirement nommé)

    Renvoie la mensualité en euros.

    >>> calcul_mensualité(200000, 4.75/100, 25*12)
    1140.234722762185
    >>> calcul_mensualité(200000, 4.75/100, 25*12, True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: calcul_mensualité() takes exactly 3 positional arguments (4 given)
    >>> calcul_mensualité(200000, 4.75/100, 25*12, arrondi=True)
    1140.23
    """
    resultat = capital * taux_annuel/12 / (1 - (1 + taux_annuel/12)**-durée_en_mois)
    return arrondi and round(resultat, 2) or resultat


class RandomUDPHandler(socketserver.DatagramRequestHandler):
    values = []
    def handle(self):
        if len(self.values) == 1:
            self.values.append(bytes2float(self.rfile.readline().strip()))
        else:
            self.values.append(bytes2int(self.rfile.readline().strip()))

        if len(self.values) == 3:
            resultat = calcul_mensualité(*self.values)
            self.values.clear()
            print(resultat, float2bytes(resultat))
            self.wfile.write(float2bytes(resultat))
        else:
            self.wfile.write(b"OK")


if __name__ == '__main__':
    server = socketserver.UDPServer(PARAMS, RandomUDPHandler)
    server.serve_forever()

