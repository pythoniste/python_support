"""
Ce fichier contient le corrigé pour l'exercice sur la manipulation d'objets.
"""

from datetime import date
from functools import total_ordering


@total_ordering
class Person:
    """Représente une personne."""

    def __init__(self, prenom, nom, date_naissance):
        """Initialisateur."""
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance

    @property
    def email(self):
        return f"{self.prenom}.{self.nom}@exemple.fr".lower()

    @property
    def age(self):
        return (date.today() - self.date_naissance).days // 365

    def __eq__(self, other):
        return self.date_naissance == other.date_naissance

    def __lt__(self, other):
        return self.date_naissance > other.date_naissance


john = Person("John", "Doe", date(1995, 1, 1))
jane = Person("Jane", "Doe", date(1995, 12, 31))

assert john.age == 29
assert jane.age == 28
assert john.email == "john.doe@exemple.fr"
assert jane.email == "jane.doe@exemple.fr"
assert john > jane
