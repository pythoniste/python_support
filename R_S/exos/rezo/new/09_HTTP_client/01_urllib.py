"""Client HTTP — urllib.request (stdlib).

Le client le plus simple sans dépendance. Limites : pas de gestion
de session, pas de retries, pas de timeout par défaut, gestion
d'erreur via HTTPError seulement.
"""
import json
import urllib.request


URL = "https://httpbin.org/get?param=demo"


def main() -> None:
    with urllib.request.urlopen(URL, timeout=10) as reponse:
        donnees = json.loads(reponse.read().decode("utf-8"))
        print(f"Status      : {reponse.status}")
        print(f"URL appelée : {donnees['url']}")
        print(f"Paramètre   : {donnees.get('args', {}).get('param')}")


if __name__ == "__main__":
    main()
