"""Chiffrement Fernet des fichiers de sortie.

A completer : implementer generate_key, encrypt_file, decrypt_file.
"""

from __future__ import annotations

from pathlib import Path


def generate_key() -> bytes:
    """Genere une cle Fernet."""
    # TODO : utiliser cryptography.fernet.Fernet.generate_key()
    ...


def encrypt_file(path: Path, key: bytes) -> Path:
    """Chiffre un fichier avec Fernet. Retourne le chemin du fichier .enc."""
    # TODO : lire, chiffrer, ecrire path.with_suffix(".enc")
    ...


def decrypt_file(path: Path, key: bytes) -> Path:
    """Dechiffre un fichier .enc. Retourne le chemin du fichier original."""
    # TODO : lire, dechiffrer, ecrire sans .enc
    ...
