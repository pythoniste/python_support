

def presque_carre(nombre):
    """
    Renvoie la multiplication du nombre précédent par le nombre suivant.
    Par exemple, pour 5, on multiplie 4 par 6. Pour 20, on multiplie 19 par 21

    >>> presque_carre(5)
    24
    >>> presque_carre(20)
    399
    """


assert presque_carre(5) == 24
assert presque_carre(20) == 399


def username_from_email(email):
    """
    Récupérer le username d'un email (partie avant l'arobase)

    >>> username_from_email("pythoniste@protonmail.com")
    pythoniste
    """


def triple_impair(debut, fin):
    """
    Renvoie la liste de tous les nombres multiples de trois, mais pas de deux entre début inclu et fin exclu

    >>> triple_impair(100, 110)
    [105, 111, 117]
    """


def aire_et_perimetre_rectangle(longueur, largeur):
    """
    Renvoie l'aire et le périmètre du rectangle

    >>> aire_et_perimetre_rectangle(4, 5)
    20, 18
    """


def nb_upper_letter(phrase):
    """
    compter le nombre de lettres majuscules

    >>> nb_upper_letter("Ceci est un Exemple")
    2
    """


def nb_occurences(phrase):
    """
    Renvoie le nombre d'occurences de chaque lettre dans la phrase

    >>> nb_occurences("OK OK...")
    {"O": 2, "K": 2, ".": 3, " ": 1}
    """


def afficher_une_ligne_sur_deux(poeme):
    """
    Renvoie une ligne sur deux
    On peut tester avec https://www.poetica.fr/poeme-174/george-sand-lettre-par-aurore-dupin/

    >>> afficher_une_ligne_sur_deux("Truc\nMachin\nChose")
    "Truc\nChose"
    """


def est_palindrome(mot):
    """
    Dit si un mot est un palindrome

    >>> est_palindrome("Anna")
    True
    >>> est_palindrome("Viviane")
    False
    """
