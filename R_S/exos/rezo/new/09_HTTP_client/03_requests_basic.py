"""Client HTTP — requests (le standard sync).

`pip install requests`. Le code se réduit à 2 lignes. La méthode
.json() parse automatiquement la réponse.
"""
import requests


def main() -> None:
    r = requests.get("https://httpbin.org/get", params={"param": "demo"}, timeout=10)
    r.raise_for_status()
    print(f"Status   : {r.status_code}")
    print(f"URL      : {r.json()['url']}")
    print(f"Param    : {r.json()['args']['param']}")


if __name__ == "__main__":
    main()
