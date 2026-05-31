"""Exceptions métier du gestionnaire de bibliothèque."""


class LivreInvalide(ValueError):
    """Données de livre invalides (titre, auteur, année, ISBN)."""


class LivreExistant(Exception):
    """ISBN déjà présent dans le catalogue."""


class CatalogueVide(Exception):
    """Le catalogue est vide : opération impossible."""
