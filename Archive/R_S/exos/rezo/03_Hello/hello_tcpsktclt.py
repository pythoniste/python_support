#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket


params = ('127.0.0.1', 8809)
BUFFER_SIZE = 1024 # default

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(params)

messages = [
    b'World\n',
]

for m in messages:
    input("---\n\nEnvoi d'un message %s" % m)
    s.send(m)
    data = s.recv(BUFFER_SIZE)
    print("\t>>> {}".format(data))

s.close()

