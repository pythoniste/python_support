#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
from conv2 import int2bytes, float2bytes, bytes2float

PARAMS = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default
MAX = int2bytes(42) + b"\n"

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        capital = int(input("Saisissez le capital"))
    except:
        pass
    else:
        break
s.sendto(int2bytes(capital), PARAMS)
data = s.recv(BUFFER_SIZE)
while True:
    try:
        taux_annuel = float(input("Saisissez le taux annuel"))
    except:
        pass
    else:
        break
s.sendto(float2bytes(taux_annuel), PARAMS)
data = s.recv(BUFFER_SIZE)
while True:
    try:
        durée_en_mois = int(input("Saisissez la durée en mois"))
    except:
        pass
    else:
        break
s.sendto(int2bytes(durée_en_mois), PARAMS)
data = s.recv(BUFFER_SIZE)
print(data)
print(bytes2float(data))

