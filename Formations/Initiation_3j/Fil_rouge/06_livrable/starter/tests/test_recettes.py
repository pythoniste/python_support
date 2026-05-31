"""Tests pytest du carnet de recettes — étape 06 (starter).

TODO : implémenter les 4 tests demandés dans ENONCE.md.
"""

import pytest

from recettes.carnet import (
    RecetteInvalide,
    ajouter_recette,
    charger,
    creer_recette,
    sauvegarder,
)


def test_creer_recette_valide():
    raise NotImplementedError


def test_creer_recette_nom_vide_leve_exception():
    raise NotImplementedError


def test_sauvegarder_charger_round_trip(tmp_path):
    raise NotImplementedError


def test_ajouter_recette_incremente():
    raise NotImplementedError
