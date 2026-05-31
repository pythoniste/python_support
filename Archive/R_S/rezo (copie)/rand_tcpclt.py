#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
from conv import int2bytes, bytes2int

PARAMS = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default
MAX = int2bytes(42) + b"\n"


nombres = []


for _ in range(1000):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(PARAMS)
    s.send(MAX)
    data = s.recv(BUFFER_SIZE)
    nombres.append(bytes2int(data))
    s.close()

print(nombres)
print("La moyenne est de %s" % (sum(nombres) / len(nombres)))

