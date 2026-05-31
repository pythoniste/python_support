"""Exceptions métier du gestionnaire de bibliothèque.

À compléter : les classes sont là mais doivent hériter correctement.
"""


class LivreInvalide(ValueError):
    """Données de livre invalides."""


class LivreExistant(Exception):
    """ISBN déjà présent dans le catalogue."""


class CatalogueVide(Exception):
    """Le catalogue est vide."""
