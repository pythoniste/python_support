"""Tests pytest du carnet de recettes."""

from pathlib import Path

import pytest

from recettes.carnet import (
    RecetteInvalide,
    ajouter_recette,
    charger,
    creer_recette,
    sauvegarder,
)


def _exemple() -> dict:
    return creer_recette("Crepes", ["farine", "oeufs", "lait"], 20)


def test_creer_recette_valide():
    recette = _exemple()
    assert recette["nom"] == "Crepes"
    assert recette["ingredients"] == ["farine", "oeufs", "lait"]
    assert recette["temps"] == 20


def test_creer_recette_nom_vide_leve_exception():
    with pytest.raises(RecetteInvalide):
        creer_recette("", ["farine"], 10)
    with pytest.raises(RecetteInvalide):
        creer_recette("   ", ["farine"], 10)


def test_sauvegarder_charger_round_trip(tmp_path: Path):
    carnet = [
        creer_recette("Crepes", ["farine", "oeufs", "lait"], 20),
        creer_recette("Gateau", ["farine", "beurre", "sucre"], 45),
    ]
    fichier = tmp_path / "carnet.json"
    sauvegarder(carnet, fichier)
    recharge = charger(fichier)
    assert recharge == carnet


def test_ajouter_recette_incremente():
    carnet: list[dict] = []
    recette = _exemple()
    ajouter_recette(carnet, recette)
    assert len(carnet) == 1
    assert carnet[0]["nom"] == "Crepes"
    ajouter_recette(carnet, creer_recette("Tarte", ["pommes", "pate"], 30))
    assert len(carnet) == 2
