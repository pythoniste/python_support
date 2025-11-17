#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
from conv2 import int2bytes, float2bytes, bytes2float

PARAMS = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default
MAX = int2bytes(42) + b"\n"

capital, taux_annuel, durée_en_mois = 200000, 4.75/100, 25*12

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto(int2bytes(capital), PARAMS)
data = s.recv(BUFFER_SIZE)
print(data)
s.sendto(float2bytes(taux_annuel), PARAMS)
data = s.recv(BUFFER_SIZE)
print(data)
s.sendto(int2bytes(durée_en_mois), PARAMS)
data = s.recv(BUFFER_SIZE)
print(data)
print(bytes2float(data))

