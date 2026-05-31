"""Chiffrement Fernet des fichiers de sortie."""

from __future__ import annotations

from pathlib import Path

from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Genere une cle Fernet."""
    return Fernet.generate_key()


def encrypt_file(path: Path, key: bytes) -> Path:
    """Chiffre un fichier avec Fernet. Retourne le chemin du fichier .enc."""
    f = Fernet(key)
    data = path.read_bytes()
    encrypted = f.encrypt(data)
    enc_path = path.with_suffix(path.suffix + ".enc")
    enc_path.write_bytes(encrypted)
    return enc_path


def decrypt_file(path: Path, key: bytes) -> Path:
    """Dechiffre un fichier .enc. Retourne le chemin du fichier original."""
    f = Fernet(key)
    data = path.read_bytes()
    decrypted = f.decrypt(data)
    # Retirer le .enc du nom
    original_name = path.name
    if original_name.endswith(".enc"):
        original_name = original_name[:-4]
    dec_path = path.parent / original_name
    dec_path.write_bytes(decrypted)
    return dec_path
