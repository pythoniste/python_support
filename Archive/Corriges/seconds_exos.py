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
    today = date.today()
    diff = today - date_naissance
    return diff.days // 365


def calculer_age_2(date_naissance: date) -> int:
    """
    Calcule l'age à partir de la date de naissance

    >>> calculer_age(date(2000, 1, 1))
    24
    >>> calculer_age(date(2000, 12, 31))
    23
    """
    return (date.today() - date_naissance).days // 365


# print(calculer_age(date(2009, 7, 11)))
# print(calculer_age_2(date(2009, 7, 11)))


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
    datetime_debut = datetime.combine(date.today(), heure_debut_reunion)
    datetime_fin = datetime_debut + timedelta(seconds=duree_reunion * 3600)
    return datetime_fin.time()


# print(calculer_fin(time(10, 0, 0), 1))
# print(calculer_fin(time(9, 30, 0), 2.5))
# print(calculer_fin(time(23, 30, 0), 2))


def common_ground(liste1: list[int], liste2: list[int]) -> list[int]:
    """
    Renvoie les éléments communs aux deux listes (ordonnés)

    >>> common_ground([1, 2, 3], [3, 4, 1, 5])
    [1, 3]
    """
    return sorted(set(liste1) & set(liste2))


def pierre_feuille_ciseaux(choix: str) -> str:
    """
    Jouer à Pierre, Papier, Ciseau
    >>> pierre_feuille_ciseaux("pierre")
    Vous avez gagné !
    >>> pierre_feuille_ciseaux("feuille")
    Vous avez perdu !
    >>> pierre_feuille_ciseaux("ciseaux")
    égalité !
    """
    univers = ["pierre", "feuille", "ciseaux"]
    if choix not in univers:
        return "Ce choix n'est pas correct."

    choix_ordinateur = choice(univers)
    print(choix_ordinateur)
    result = (univers.index(choix) - univers.index(choix_ordinateur)) % 3
    if result == 0:
        return "égalité !"
    if result == 1:
        return "Vous avez gagné !"
    return "Vous avez perdu !"
