"""Client HTTPS basique — requests.

Pas de configuration TLS particulière : `requests` vérifie le
certificat du serveur contre les CA système (paquet `certifi`).
"""
import requests


URL = "https://www.example.com"


def main():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    print(f"Status     : {r.status_code}")
    print(f"Protocole  : {r.url.split(':')[0]}")
    # request.Response expose le certificat distant via les headers ou
    # via la connexion urllib3 sous-jacente.
    print(f"Server     : {r.headers.get('Server', '?')}")
    print(f"Taille     : {len(r.content)} octets reçus chiffrés puis déchiffrés.")


if __name__ == "__main__":
    main()
