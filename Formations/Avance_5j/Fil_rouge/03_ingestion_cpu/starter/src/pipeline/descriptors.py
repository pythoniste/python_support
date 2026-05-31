"""Descripteurs de validation reutilisables (solution etapes 01-02)."""

from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any


class Validated:
    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(self, instance: object, owner: type) -> Any:
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance: object, value: Any) -> None:
        value = self.validate(value)
        instance.__dict__[self.name] = value

    @abstractmethod
    def validate(self, value: Any) -> Any: ...


class RangeField(Validated):
    def __init__(self, min_val: float, max_val: float) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value: Any) -> float:
        if not isinstance(value, (int, float)):
            raise ValueError(f"{self.name}: {value!r} n'est pas un nombre")
        val = float(value)
        if val < self.min_val or val > self.max_val:
            raise ValueError(f"{self.name}: {val} hors de [{self.min_val}, {self.max_val}]")
        return val


class NonEmptyString(Validated):
    def validate(self, value: Any) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{self.name}: la chaine est vide ou n'est pas un str")
        return value


class RegexField(Validated):
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self._compiled = re.compile(pattern)

    def validate(self, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError(f"{self.name}: {value!r} n'est pas un str")
        if not self._compiled.fullmatch(value):
            raise ValueError(f"{self.name}: {value!r} ne matche pas {self.pattern}")
        return value
