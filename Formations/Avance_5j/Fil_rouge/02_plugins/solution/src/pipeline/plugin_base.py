"""Systeme de plugins par __init_subclass__."""

from __future__ import annotations

from abc import abstractmethod

from pipeline.models import SensorReading


class TransformPlugin:
    """Classe de base pour les plugins de transformation.

    Chaque sous-classe doit declarer un attribut de classe `name: str`.
    L'enregistrement est automatique via __init_subclass__.
    """

    _registry: dict[str, type[TransformPlugin]] = {}

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name"):
            raise TypeError(
                f"Le plugin {cls.__name__} doit declarer un attribut de classe 'name'"
            )
        if cls.name in TransformPlugin._registry:
            raise ValueError(
                f"Un plugin avec le nom {cls.name!r} existe deja "
                f"({TransformPlugin._registry[cls.name].__name__})"
            )
        TransformPlugin._registry[cls.name] = cls

    @abstractmethod
    def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
        """Transforme une liste de lectures."""
        ...

    @classmethod
    def get_plugin(cls, name: str) -> type[TransformPlugin]:
        """Retrouve un plugin par son nom. Leve KeyError si inconnu."""
        if name not in cls._registry:
            raise KeyError(f"Plugin {name!r} inconnu. Disponibles : {list(cls._registry)}")
        return cls._registry[name]

    @classmethod
    def list_plugins(cls) -> list[str]:
        """Liste les noms de plugins disponibles."""
        return sorted(cls._registry.keys())
