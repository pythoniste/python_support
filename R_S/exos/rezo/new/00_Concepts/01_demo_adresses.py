"""Inspection des adresses : nom d'hôte, IP locale, résolution DNS.

À exécuter :  python3 01_demo_adresses.py

Observer :
- le nom d'hôte de la machine ;
- la (ou les) adresse(s) IP associée(s) ;
- la liste renvoyée par getaddrinfo pour un nom public.
"""
import socket


# 1. Le nom de cette machine
print("Nom d'hôte local :", socket.gethostname())

# 2. Une IP associée à ce nom (méthode « naïve », IPv4 uniquement)
print("IP locale        :", socket.gethostbyname(socket.gethostname()))
print()

# 3. La méthode à privilégier : getaddrinfo
#    Elle renvoie une liste de tuples (famille, type, proto, canonname, sockaddr)
#    et gère IPv4 ET IPv6.
print("Résolution de example.com :")
hostname = input("Résolution d'un site de votre choix ? ")
for info in socket.getaddrinfo(hostname, 80, type=socket.SOCK_STREAM):
    famille, _type, _proto, _canon, sockaddr = info
    nom_famille = "IPv4" if famille == socket.AF_INET else "IPv6"
    print(f"  {nom_famille:5s} -> {sockaddr}")
