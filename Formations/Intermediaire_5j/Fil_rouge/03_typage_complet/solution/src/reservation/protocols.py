"""Protocols structurels pour le système de réservation."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Reservable(Protocol):
    """Tout objet ayant un nom et une capacité peut être réservé."""

    nom: str
    capacite: int
