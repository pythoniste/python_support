"""Client HTTP — http.client (stdlib, encore plus bas niveau).

Permet de voir tous les détails du protocole : ligne de requête,
en-têtes, corps. urllib s'appuie en interne sur http.client.
"""
import http.client
import json


HOTE = "httpbin.org"
CHEMIN = "/get?param=demo"


def main() -> None:
    conn = http.client.HTTPSConnection(HOTE, timeout=10)
    try:
        conn.request("GET", CHEMIN, headers={"User-Agent": "demo-client"})
        reponse = conn.getresponse()
        print(f"Status   : {reponse.status} {reponse.reason}")
        print("En-têtes :")
        for nom, valeur in reponse.getheaders()[:3]:
            print(f"  {nom}: {valeur}")
        corps = json.loads(reponse.read().decode("utf-8"))
        print(f"URL      : {corps['url']}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
