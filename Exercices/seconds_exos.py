from datetime import datetime, date, time, timedelta
from random import choice


def calculer_age(date_naissance: date) -> int:
    """
    Calcule l'age à partir de la date de naissance

    >>> calculer_age(date(2000, 1, 1))
    24
    >>> calculer_age(date(2000, 12, 31))
    23
    """


def calculer_fin(heure_debut_reunion: time, duree_reunion: int | float) -> time:
    """
    Calcule l'heure de fin de réunion

    >>> calculer_fin(time(10, 0, 0), 1)
    datetime.time(11, 0)
    >>> calculer_fin(time(9, 30, 0), 2.5)
    datetime.time(12, 0)
    >>> calculer_fin(time(23, 30, 0), 2)
    datetime.time(1, 30)
    """


def common_ground(liste1: list[int], liste2: list[int]) -> list[int]:
    """
    Renvoie les éléments communs aux deux listes (ordonnés)

    >>> common_ground([1, 2, 3], [3, 4, 1, 5])
    [1, 3]
    """


def pierre_papier_ciseau(choix: str) -> str:
    """
    Jouer à Pierre, Papier, Ciseau
    >>> pierre_papier_ciseau("pierre")
    Vous avez gagné !
    >>> pierre_papier_ciseau("pierre")
    Vous avez perdu !
    >>> pierre_papier_ciseau("pierre")
    égalité !
    """


"""
Devinez le nombre
"""

"""
Générateur de mots de passe
Au moins 24 caractères dont au moins 3 minuscules, 3 majuscules, 3 chiffres, 2 caractères spéciaux.
"""
