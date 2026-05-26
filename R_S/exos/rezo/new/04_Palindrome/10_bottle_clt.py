"""Client HTTP du service palindrome — utilise `requests`.

À utiliser avec 09_bottle_palindrome.py.

Premier client qui n'écrit AUCUN code réseau : tout est dans
`requests.get`. C'est la valeur ajoutée du REST/HTTP : le client
parle un protocole standard, l'API utilise un format standard
(JSON), et l'écriture est trivialement portable.
"""
import requests


URL = "http://127.0.0.1:8808/palindrome/{}"

MOTS = [
    "mot",
    "anna",
    "Karine alla en Irak",
    "Esope reste ici et se repose",
]


def main() -> None:
    for mot in MOTS:
        reponse = requests.get(URL.format(mot))
        data = reponse.json()
        verdict = "est" if data["est_palindrome"] else "n'est pas"
        print(f"    Le mot {data['mot']!r} {verdict} un palindrome.")


if __name__ == "__main__":
    main()
