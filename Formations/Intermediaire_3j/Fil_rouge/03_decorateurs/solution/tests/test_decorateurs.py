"""Tests des décorateurs — étape 03."""

import logging
from inventaire.decorateurs import log_action, timer


def test_log_action(caplog):
    @log_action
    def ajouter(x, y):
        return x + y

    with caplog.at_level(logging.DEBUG):
        assert ajouter(2, 3) == 5
    assert "ajouter" in caplog.text


def test_timer(caplog):
    @timer
    def calcul():
        return sum(range(1000))

    with caplog.at_level(logging.DEBUG):
        assert calcul() == 499500


def test_preserve_name():
    @log_action
    def ma_func():
        """Doc."""
    assert ma_func.__name__ == "ma_func"
