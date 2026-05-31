#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de client TCP utilisant le serveur socketserver
"""


import socket


params = ("127.0.0.1", 8819)
BUFFER_SIZE = 1024 # default

messages = [
    "mot",
    "anna",
    "Karine alla en Irak!",
    "#",
]

for m in messages:
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Le mot '%s' " % m, end="")
    s.sendto(m.encode("utf-8"), params)
    data, _ = s.recvfrom(BUFFER_SIZE)
    if len(data) == 0:
        print("n'est pas parvenu jusqu'au serveur")
    elif data == b"T":
        print("est un palindrome")
    elif data == b"F":
        print("n'est pas un palindrome")
    elif data == b"S":
        print("a permis d'arrêter le serveur")
    else:
        print("n'a pas été compris par le serveur qui a renvoyé la réponse: %s" % data)
    input()
s.close()

