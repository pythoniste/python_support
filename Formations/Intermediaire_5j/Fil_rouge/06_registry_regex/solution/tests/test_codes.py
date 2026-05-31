"""Tests des codes et du registre — étape 06."""

import pytest

from reservation.codes import extraire_info, trouver_codes, valider_code
from reservation.modeles import Salle, SalleReunion
from reservation.registry import SalleRegistry


def test_valider_code_valide():
    assert valider_code("REU-A301") is True
    assert valider_code("FOR-B102") is True
    assert valider_code("AUD-C999") is True


def test_valider_code_invalide():
    assert valider_code("XXX-A301") is False
    assert valider_code("REU-a301") is False
    assert valider_code("REU-A30") is False
    assert valider_code("") is False


def test_extraire_info():
    info = extraire_info("REU-A301")
    assert info == {"type": "REU", "batiment": "A", "numero": "301"}


def test_extraire_info_invalide():
    with pytest.raises(ValueError):
        extraire_info("INVALIDE")


def test_trouver_codes():
    texte = "Réservez REU-A301 ou FOR-B102 pour demain."
    codes = trouver_codes(texte)
    assert codes == ["REU-A301", "FOR-B102"]


def test_registry_enregistrer_obtenir():
    reg = SalleRegistry()
    salle = SalleReunion("Everest", 10, visio=True)
    reg.enregistrer("REU-A301", salle)
    assert reg.obtenir("REU-A301") is salle


def test_registry_code_invalide():
    reg = SalleRegistry()
    salle = Salle("Test", 5)
    with pytest.raises(ValueError):
        reg.enregistrer("INVALIDE", salle)


def test_registry_lister():
    reg = SalleRegistry()
    reg.enregistrer("REU-A301", SalleReunion("Everest", 10))
    reg.enregistrer("FOR-B102", Salle("Labo", 20))
    assert len(reg.lister()) == 2
