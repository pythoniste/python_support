"""Client HTTP — requests avec Session, retries, auth.

Trois patterns importants en production :
- Session : réutilise la connexion TCP (HTTP keep-alive) pour
  plusieurs requêtes consécutives → gain de RTT significatif ;
- HTTPAdapter avec Retry : retente automatiquement les erreurs
  transientes (5xx, timeouts) ;
- Authentification : Basic, Bearer, …
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def session_avec_retries() -> requests.Session:
    """Renvoie une Session configurée avec retries sur les codes 5xx."""
    s = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={"GET", "POST"},
    )
    adapter = HTTPAdapter(max_retries=retry)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def main() -> None:
    with session_avec_retries() as session:
        # Requête simple
        r = session.get("https://httpbin.org/get", timeout=10)
        print(f"GET simple : {r.status_code}")

        # Avec auth Basic
        r = session.get(
            "https://httpbin.org/basic-auth/user/passw0rd",
            auth=("user", "passw0rd"),
            timeout=10,
        )
        print(f"Basic auth : {r.status_code} -> {r.json()['authenticated']}")

        # POST JSON
        r = session.post(
            "https://httpbin.org/post",
            json={"cle": "valeur"},
            timeout=10,
        )
        print(f"POST JSON  : {r.status_code} -> {r.json()['json']}")


if __name__ == "__main__":
    main()
