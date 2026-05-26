"""Logique métier partagée par les cinq variantes du service palindrome.

Un module unique, importé par les serveurs et par les tests.
Ne contient AUCUN code réseau.
"""
import string


def est_palindrome(mot: str) -> bool:
    """Indique si `mot` est un palindrome.

    Insensible à la casse, aux espaces et à la ponctuation.

    >>> est_palindrome("anna")
    True
    >>> est_palindrome("Karine alla en Irak")
    True
    >>> est_palindrome("Esope reste ici et se repose")
    True
    >>> est_palindrome("Hello")
    False
    """
    mot = mot.lower()
    for c in string.whitespace + string.punctuation:
        mot = mot.replace(c, "")
    return mot == mot[::-1]


if __name__ == "__main__":
    cas = [
        "mot",
        "anna",
        "Karine alla en Irak!",
        "Esope reste ici et se repose",
        "Hello",
        "kayak",
    ]
    for mot in cas:
        verdict = "PALINDROME" if est_palindrome(mot) else "pas palindrome"
        print(f"  {mot!r:40s} -> {verdict}")
