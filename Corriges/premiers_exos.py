"""Corrigés des premiers exercices."""

import string


POETRY = """Je suis très émue de vous dire que j’ai
bien compris l’autre soir que vous aviez
toujours une envie folle de me faire
danser. Je garde le souvenir de votre
baiser et je voudrais bien que ce soit
là une preuve que je puisse être aimée
par vous. Je suis prête à vous montrer mon
affection toute désintéressée et sans cal-
cul, et si vous voulez me voir aussi
vous dévoiler sans artifice mon âme
toute nue, venez me faire une visite.
Nous causerons en amis, franchement.
Je vous prouverai que je suis la femme
sincère, capable de vous offrir l’affection
la plus profonde comme la plus étroite
amitié, en un mot la meilleure preuve
que vous puissiez rêver, puisque votre
âme est libre. Pensez que la solitude où j’ha-
bite est bien longue, bien dure et souvent
difficile. Ainsi en y songeant j’ai l’âme
grosse. Accourez donc vite et venez me la
faire oublier par l’amour où je veux me
mettre."""


def presque_carre(nombre: int) -> int:
    """
    Renvoie la multiplication du nombre précédent par le nombre suivant.
    Par exemple, pour 5, on multiplie 4 par 6. Pour 20, on multiplie 19 par 21

    >>> presque_carre(5)
    24
    >>> presque_carre(20)
    399
    """
    return (nombre - 1) * (nombre + 1)


def username_from_email(email: str) -> str:
    """
    Récupérer le nom d'utilisateur d'un email (partie avant l'arobase)

    >>> username_from_email("pythoniste@protonmail.com")
    'pythoniste'
    """
    return email[:email.index("@")]


def username_from_email_2(email: str) -> str:
    """
    Récupérer le nom d'utilisateur d'un email (partie avant l'arobase)

    >>> username_from_email_2("pythoniste@protonmail.com")
    'pythoniste'
    """
    return email.split("@")[0]


def triple_impair(debut: int, fin: int) -> list[int]:
    """
    Renvoie la liste de tous les multiples de trois, mais pas de deux entre début inclu et fin exclu

    >>> triple_impair(100, 120)
    [105, 111, 117]
    """
    result = []
    for nombre in range(debut, fin):
        if nombre % 3 == 0 and nombre % 2 == 1:
            result.append(nombre)
    return result


def triple_impair_2(debut: int, fin: int) -> list[int]:
    """
    Renvoie la liste de tous les multiples de trois, mais pas de deux entre début inclu et fin exclu

    >>> triple_impair_2(100, 120)
    [105, 111, 117]
    """
    return [nombre for nombre in range(debut, fin) if nombre % 3 == 0 and nombre % 2 == 1]


def aire_et_perimetre_rectangle(longueur: int, largeur: int) -> tuple[int, int]:
    """
    Renvoie l'aire et le périmètre du rectangle

    >>> aire_et_perimetre_rectangle(4, 5)
    (20, 18)
    """
    return longueur * largeur, (longueur + largeur) * 2


def nb_upper_letter(phrase: str) -> int:
    """
    Compter le nombre de lettres majuscules

    >>> nb_upper_letter("Ceci est un Exemple")
    2
    """
    compteur = 0
    for lettre in phrase:
        if lettre in string.ascii_uppercase:
            compteur += 1
    return compteur


def nb_upper_letter_2(phrase: str) -> int:
    """
    Compter le nombre de lettres majuscules

    >>> nb_upper_letter_2("Ceci est un Exemple")
    2
    """
    return len([lettre for lettre in phrase if lettre.isupper()])


def nb_occurrences(phrase: str) -> dict[str, int]:
    """
    Renvoie le nombre d'occurences de chaque lettre dans la phrase

    >>> nb_occurrences("OK OK...")
    {'.': 3, 'O': 2, 'K': 2, ' ': 1}
    """
    return {lettre: phrase.count(lettre) for lettre in set(phrase)}


def nb_occurrences_2(phrase: str) -> dict[str, int]:
    """
    Renvoie le nombre d'occurences de chaque lettre dans la phrase

    >>> nb_occurrences_2("OK OK...")
    {'.': 3, 'O': 2, 'K': 2, ' ': 1}
    """
    lettres = set(phrase)
    result = {}
    for lettre in lettres:
        result[lettre] = phrase.count(lettre)
    return result


def afficher_une_ligne_sur_deux(poetry: str) -> str:
    """
    Renvoie une ligne sur deux
    On peut tester avec https://www.poetica.fr/poeme-174/george-sand-lettre-par-aurore-dupin/

    >>> len(afficher_une_ligne_sur_deux(POETRY))
    443
    """
    return "\n".join(ligne for number, ligne in enumerate(poetry.split("\n")) if number % 2 == 0)


def est_palindrome(mot: str) -> bool:
    """
    Dit si un mot est un palindrome

    >>> est_palindrome("Anna")
    True
    >>> est_palindrome("Viviane")
    False
    """
    return mot.lower() == mot[::-1].lower()
