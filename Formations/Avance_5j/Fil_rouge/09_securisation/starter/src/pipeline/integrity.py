"""Integrite des fichiers : hachage et HMAC.

A completer : implementer les fonctions de hachage et de manifeste.
"""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
from pathlib import Path


def compute_file_hash(path: Path, algorithm: str = "sha256") -> str:
    """Calcule le hash d'un fichier par blocs. Retourne le digest hex."""
    # TODO : lire par blocs de 8 Ko, retourner hexdigest
    ...


def compute_hmac(data: bytes, key: bytes) -> str:
    """Calcule un HMAC-SHA256."""
    # TODO : hmac.new avec sha256
    ...


def verify_hmac(data: bytes, key: bytes, expected: str) -> bool:
    """Verifie un HMAC en temps constant."""
    # TODO : hmac.compare_digest
    ...


def create_manifest(directory: Path) -> dict[str, str]:
    """Cree un dict {filename: sha256_hash} pour tous les fichiers."""
    # TODO : iterer sur les fichiers du repertoire
    ...


def verify_manifest(directory: Path, manifest: dict[str, str]) -> list[str]:
    """Retourne la liste des fichiers dont le hash ne correspond pas."""
    # TODO : comparer chaque fichier avec le manifeste
    ...
