"""Tests des décorateurs — étape 05."""

import logging

import pytest

from reservation.decorateurs import autoriser, log_appel, timer
from reservation.modeles import Utilisateur


def test_log_appel(caplog):
    @log_appel
    def addition(a, b):
        return a + b

    with caplog.at_level(logging.DEBUG):
        result = addition(2, 3)
    assert result == 5
    assert "addition" in caplog.text


def test_timer(caplog):
    @timer
    def lente():
        total = 0
        for i in range(1000):
            total += i
        return total

    with caplog.at_level(logging.DEBUG):
        result = lente()
    assert result == 499500


def test_log_appel_preserve_name():
    @log_appel
    def ma_fonction():
        """Ma doc."""
        pass

    assert ma_fonction.__name__ == "ma_fonction"
    assert ma_fonction.__doc__ == "Ma doc."


def test_autoriser_admin():
    @autoriser(["admin"])
    def supprimer(user):
        return "supprimé"

    admin = Utilisateur("Admin", "admin@test.fr")
    admin.role = "admin"
    assert supprimer(admin) == "supprimé"


def test_autoriser_refuse():
    @autoriser(["admin"])
    def supprimer(user):
        return "supprimé"

    user = Utilisateur("Alice", "alice@test.fr")
    user.role = "user"
    with pytest.raises(PermissionError):
        supprimer(user)
