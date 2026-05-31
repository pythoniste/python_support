"""Étape 06 — Gestion des erreurs (starter).

À compléter : ajouter les exceptions personnalisées LivreInvalide,
LivreExistant, CatalogueVide. Valider les entrées dans creer_livre
et ajouter_livre. Faire boucler saisir_livre tant que l'entrée est
invalide.
"""

from datetime import date


class LivreInvalide(ValueError):
    """Données de livre invalides (titre, auteur, année, ISBN)."""


class LivreExistant(Exception):
    """ISBN déjà présent dans le catalogue."""


class CatalogueVide(Exception):
    """Catalogue vide."""


# TODO : reprendre les fonctions de l'étape 05 et :
#   - valider les arguments dans creer_livre (titre/auteur non vides,
#     année entre 800 et today().year+1, ISBN 13 chiffres)
#   - vérifier l'unicité de l'ISBN dans ajouter_livre
#   - faire boucler saisir_livre sur LivreInvalide
