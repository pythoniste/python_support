"""Systeme de plugins par __init_subclass__.

A completer : implementer TransformPlugin avec auto-enregistrement.
"""

from __future__ import annotations

from abc import abstractmethod

from pipeline.models import SensorReading


class TransformPlugin:
    """Classe de base pour les plugins de transformation.

    Chaque sous-classe doit declarer un attribut de classe `name: str`.
    L'enregistrement est automatique via __init_subclass__.
    """

    _registry: dict[str, type[TransformPlugin]] = {}

    # TODO : implementer __init_subclass__ pour auto-enregistrer les sous-classes
    # TODO : verifier que `name` est defini et unique

    @abstractmethod
    def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
        """Transforme une liste de lectures."""
        ...

    @classmethod
    def get_plugin(cls, name: str) -> type[TransformPlugin]:
        """Retrouve un plugin par son nom."""
        ...

    @classmethod
    def list_plugins(cls) -> list[str]:
        """Liste les noms de plugins disponibles."""
        ...
