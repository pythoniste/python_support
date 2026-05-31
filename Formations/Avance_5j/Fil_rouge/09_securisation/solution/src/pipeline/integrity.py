"""Integrite des fichiers : hachage et HMAC."""

from __future__ import annotations

import hashlib
import hmac as hmac_mod
from pathlib import Path

_BLOCK_SIZE = 8192


def compute_file_hash(path: Path, algorithm: str = "sha256") -> str:
    """Calcule le hash d'un fichier par blocs."""
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        while block := f.read(_BLOCK_SIZE):
            h.update(block)
    return h.hexdigest()


def compute_hmac(data: bytes, key: bytes) -> str:
    """Calcule un HMAC-SHA256."""
    return hmac_mod.new(key, data, hashlib.sha256).hexdigest()


def verify_hmac(data: bytes, key: bytes, expected: str) -> bool:
    """Verifie un HMAC en temps constant."""
    computed = compute_hmac(data, key)
    return hmac_mod.compare_digest(computed, expected)


def create_manifest(directory: Path) -> dict[str, str]:
    """Cree un dict {filename: sha256_hash} pour tous les fichiers."""
    manifest: dict[str, str] = {}
    for p in sorted(directory.iterdir()):
        if p.is_file():
            manifest[p.name] = compute_file_hash(p)
    return manifest


def verify_manifest(directory: Path, manifest: dict[str, str]) -> list[str]:
    """Retourne la liste des fichiers dont le hash ne correspond pas."""
    bad: list[str] = []
    for name, expected_hash in manifest.items():
        p = directory / name
        if not p.exists():
            bad.append(name)
        elif compute_file_hash(p) != expected_hash:
            bad.append(name)
    return bad
