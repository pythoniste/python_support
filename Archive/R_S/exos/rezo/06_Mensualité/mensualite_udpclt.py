#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket

PARAMS = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default

capital, taux_annuel, durée_en_mois = 200000, 4.75/100, 25*12

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto("|".join(str(e) for e in (capital, taux_annuel, durée_en_mois)).encode("utf-8"), PARAMS)
data = s.recv(BUFFER_SIZE)
print(data.decode("utf-8"))

