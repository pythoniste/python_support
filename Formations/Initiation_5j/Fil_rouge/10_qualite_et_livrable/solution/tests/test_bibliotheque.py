"""Tests pytest du gestionnaire de bibliothèque."""

from datetime import date
from pathlib import Path

import pytest

from bibliotheque.catalogue import (
    ajouter_livre,
    charger_csv,
    charger_json,
    creer_livre,
    rechercher,
    sauvegarder_csv,
    sauvegarder_json,
    trier,
)
from bibliotheque.exceptions import CatalogueVide, LivreExistant, LivreInvalide


def _exemple() -> dict:
    return creer_livre("1984", "George Orwell", 1949, "9780451524935")


def test_creer_livre_valide():
    livre = _exemple()
    assert livre["titre"] == "1984"
    assert livre["auteur"] == "George Orwell"
    assert livre["annee"] == 1949
    assert livre["isbn"] == "9780451524935"
    assert livre["date_ajout"] == date.today().isoformat()


def test_creer_livre_invalide_leve_exception():
    with pytest.raises(LivreInvalide):
        creer_livre("1984", "George Orwell", 3000, "9780451524935")
    with pytest.raises(LivreInvalide):
        creer_livre("", "George Orwell", 1949, "9780451524935")
    with pytest.raises(LivreInvalide):
        creer_livre("1984", "George Orwell", 1949, "123")


def test_ajouter_livre_duplicate():
    catalogue: list[dict] = []
    livre = _exemple()
    ajouter_livre(catalogue, livre)
    with pytest.raises(LivreExistant):
        ajouter_livre(catalogue, _exemple())


def test_rechercher_case_insensitive():
    catalogue = [_exemple()]
    assert len(rechercher(catalogue, "ORWELL")) == 1
    assert len(rechercher(catalogue, "orwell")) == 1
    assert len(rechercher(catalogue, "1984")) == 1
    assert len(rechercher(catalogue, "dickens")) == 0


def test_rechercher_catalogue_vide_leve_exception():
    with pytest.raises(CatalogueVide):
        rechercher([], "orwell")


def test_trier_par_annee():
    catalogue = [
        creer_livre("1984", "George Orwell", 1949, "9780451524935"),
        creer_livre("Le Petit Prince", "A. de Saint-Exupéry", 1943, "9782070612758"),
    ]
    tries = trier(catalogue, "n")
    assert tries[0]["annee"] == 1943
    assert tries[1]["annee"] == 1949


def test_sauvegarder_charger_json_round_trip(tmp_path: Path):
    catalogue = [
        creer_livre("1984", "George Orwell", 1949, "9780451524935"),
        creer_livre("Le Petit Prince", "A. de Saint-Exupéry", 1943, "9782070612758"),
    ]
    fichier = tmp_path / "catalogue.json"
    sauvegarder_json(catalogue, fichier)
    recharge = charger_json(fichier)
    assert recharge == catalogue


def test_sauvegarder_charger_csv_round_trip(tmp_path: Path):
    catalogue = [
        creer_livre("1984", "George Orwell", 1949, "9780451524935"),
    ]
    fichier = tmp_path / "catalogue.csv"
    sauvegarder_csv(catalogue, fichier)
    recharge = charger_csv(fichier)
    assert recharge == catalogue
    assert isinstance(recharge[0]["annee"], int)
