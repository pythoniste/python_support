"""Descripteurs de validation reutilisables.

A completer : implementer Validated, RangeField, NonEmptyString, RegexField.
"""

from __future__ import annotations

import re
from abc import abstractmethod


class Validated:
    """Descripteur de base avec validation.

    Utilise __set_name__ pour connaitre le nom de l'attribut.
    Stocke la valeur dans instance.__dict__[self.name].
    """

    # TODO : implementer __set_name__, __get__, __set__
    # TODO : definir une methode abstraite validate(self, value)

    def __set_name__(self, owner: type, name: str) -> None:
        ...

    def __get__(self, instance: object, owner: type) -> object:
        ...

    def __set__(self, instance: object, value: object) -> None:
        ...

    @abstractmethod
    def validate(self, value: object) -> object:
        """Valide et retourne la valeur. Leve ValueError si invalide."""
        ...


class RangeField(Validated):
    """Verifie que la valeur est un nombre dans [min_val, max_val]."""

    def __init__(self, min_val: float, max_val: float) -> None:
        ...

    def validate(self, value: object) -> float:
        ...


class NonEmptyString(Validated):
    """Verifie que la valeur est un str non vide apres strip()."""

    def validate(self, value: object) -> str:
        ...


class RegexField(Validated):
    """Verifie qu'un str matche entierement un regex donne."""

    def __init__(self, pattern: str) -> None:
        ...

    def validate(self, value: object) -> str:
        ...
