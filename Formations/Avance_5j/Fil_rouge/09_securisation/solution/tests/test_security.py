"""Tests pour l'integrite et le chiffrement."""

from pathlib import Path

import pytest

from pipeline.crypto import decrypt_file, encrypt_file, generate_key
from pipeline.integrity import (
    compute_file_hash,
    compute_hmac,
    create_manifest,
    verify_hmac,
    verify_manifest,
)


@pytest.fixture()
def sample_file(tmp_path: Path) -> Path:
    p = tmp_path / "data.txt"
    p.write_text("hello world")
    return p


@pytest.fixture()
def sample_dir(tmp_path: Path) -> Path:
    d = tmp_path / "outbox"
    d.mkdir()
    (d / "a.json").write_text('{"temp": 22.5}')
    (d / "b.json").write_text('{"temp": 18.3}')
    return d


class TestIntegrity:
    def test_compute_file_hash(self, sample_file: Path) -> None:
        h = compute_file_hash(sample_file)
        assert len(h) == 64

    def test_compute_hmac(self) -> None:
        h = compute_hmac(b"hello", b"secret")
        assert isinstance(h, str)

    def test_verify_hmac_correct(self) -> None:
        h = compute_hmac(b"hello", b"secret")
        assert verify_hmac(b"hello", b"secret", h) is True

    def test_verify_hmac_wrong(self) -> None:
        h = compute_hmac(b"hello", b"secret")
        assert verify_hmac(b"hello", b"wrong_key", h) is False

    def test_create_and_verify_manifest(self, sample_dir: Path) -> None:
        manifest = create_manifest(sample_dir)
        assert len(manifest) == 2
        assert verify_manifest(sample_dir, manifest) == []

    def test_manifest_detects_modification(self, sample_dir: Path) -> None:
        manifest = create_manifest(sample_dir)
        (sample_dir / "a.json").write_text("modified")
        assert "a.json" in verify_manifest(sample_dir, manifest)


class TestCrypto:
    def test_encrypt_decrypt_roundtrip(self, sample_file: Path) -> None:
        key = generate_key()
        original = sample_file.read_bytes()
        enc_path = encrypt_file(sample_file, key)
        assert enc_path.suffix == ".enc"
        dec_path = decrypt_file(enc_path, key)
        assert dec_path.read_bytes() == original

    def test_encrypted_file_is_different(self, sample_file: Path) -> None:
        key = generate_key()
        original = sample_file.read_bytes()
        enc_path = encrypt_file(sample_file, key)
        assert enc_path.read_bytes() != original
