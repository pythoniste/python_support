#!/usr/bin/python3
# -*- coding: utf-8 -*-


import socket
import argparse
from conv2 import int2bytes, float2bytes, bytes2float

PARAMS = ("127.0.0.1", 8808)
BUFFER_SIZE = 1024 # default
MAX = int2bytes(42) + b"\n"

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def proxy_client(args):
    s.sendto(int2bytes(args.capital), PARAMS)
    data = s.recv(BUFFER_SIZE)
    s.sendto(float2bytes(args.taux), PARAMS)
    data = s.recv(BUFFER_SIZE)
    s.sendto(int2bytes(args.duree), PARAMS)
    data = s.recv(BUFFER_SIZE)
    print(data)
    print(bytes2float(data))

parser = argparse.ArgumentParser(
    prog = 'emprunt',
    description = """Programme permettant d'effectuer des calculs sur des emprunts par un appel réseau""",
    epilog = """Réalisé pour le livre Programmation système avec Python"""
)

parser.add_argument(
    'capital',
    help = """capital en euros""",
    type = int,
)
parser.add_argument(
    'taux',
    help = """un taux annuel en pourcentage""",
    type = float,
)
parser.add_argument(
    'duree',
    help = """Durée en années""",
    type = int,
)
parser.set_defaults(func=proxy_client)

args = parser.parse_args()

print("Here we go")
args.func(args)

