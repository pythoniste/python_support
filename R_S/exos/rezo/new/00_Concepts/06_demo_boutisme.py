"""Boutisme : observer la différence d'encodage entre big et little endian.

À exécuter :  python3 06_demo_boutisme.py

Observer :
- les mêmes octets prennent un sens différent selon le boutisme choisi ;
- d'où la nécessité d'une convention partagée entre émetteur et récepteur.
"""
import struct
import sys


print("Boutisme natif de cette machine :", sys.byteorder)
print()

# 1. Encoder la même valeur avec deux conventions
n = 1
print(f"Valeur encodée : {n}")
print(f"  big-endian    : {n.to_bytes(4, 'big').hex()}")
print(f"  little-endian : {n.to_bytes(4, 'little').hex()}")
print(f"  struct !I     : {struct.pack('!I', n).hex()}  (! = network = big)")
print(f"  struct <I     : {struct.pack('<I', n).hex()}")
print()

# 2. Démontrer concrètement le risque : mêmes octets, interprétations différentes
octets = bytes.fromhex("0a000000")
print(f"Octets bruts reçus : {octets.hex()}")
print(f"  lu en big-endian    : {int.from_bytes(octets, 'big')}")
print(f"  lu en little-endian : {int.from_bytes(octets, 'little')}")
print()
print("Mêmes octets sur le câble, deux nombres complètement différents.")
print("D'où l'importance d'une convention partagée — par défaut, big-endian.")
