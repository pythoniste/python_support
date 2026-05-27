"""Trois stratégies de sérialisation d'un entier non négatif.

Chaque stratégie expose un couple symétrique (pack, unpack).
Le module ne contient AUCUN code réseau — juste l'encodage.
"""
import json
import struct


# --- Stratégie 1 — texte ---------------------------------------------------

def pack_texte(n: int) -> bytes:
    """int -> b'42\\n' (lisible, framing par \\n)."""
    return str(n).encode("utf-8") + b"\n"


def unpack_texte(data: bytes) -> int:
    """b'42' (sans \\n final) -> 42."""
    return int(data.rstrip(b"\n").decode("utf-8"))


# --- Stratégie 2 — binaire fixed-size (4 octets, big-endian) ---------------

def pack_binaire(n: int) -> bytes:
    """int -> b'\\x00\\x00\\x00\\x2A' (taille fixe 4 octets, sans signe)."""
    return struct.pack("!I", n)


def unpack_binaire(data: bytes) -> int:
    """b'\\x00\\x00\\x00\\x2A' -> 42 (suppose exactement 4 octets)."""
    return struct.unpack("!I", data)[0]


# --- Stratégie 3 — JSON ----------------------------------------------------

def pack_json(n: int) -> bytes:
    """int -> b'{\"valeur\": 42}\\n' (extensible, framing par \\n)."""
    return json.dumps({"valeur": n}).encode("utf-8") + b"\n"


def unpack_json(data: bytes) -> int:
    """b'{\"valeur\": 42}' -> 42."""
    return json.loads(data.rstrip(b"\n"))["valeur"]


# --- Helpers framing -------------------------------------------------------

def recv_ligne(sock, delim: bytes = b"\n") -> bytes:
    """Lit jusqu'au délimiteur (exclu) — pour les encodages textuel et JSON."""
    morceaux = []
    while True:
        octet = sock.recv(1)
        if not octet or octet == delim:
            return b"".join(morceaux)
        morceaux.append(octet)


def recv_exactement(sock, n: int) -> bytes:
    """Lit exactement n octets — pour l'encodage binaire fixed-size."""
    morceaux = []
    restant = n
    while restant:
        bloc = sock.recv(restant)
        if not bloc:
            raise ConnectionError(f"Connexion fermée à {n - restant}/{n}")
        morceaux.append(bloc)
        restant -= len(bloc)
    return b"".join(morceaux)


if __name__ == "__main__":
    # Démo : encoder et décoder 42 de trois façons.
    for nom, pack, unpack in [
        ("texte  ", pack_texte, unpack_texte),
        ("binaire", pack_binaire, unpack_binaire),
        ("json   ", pack_json, unpack_json),
    ]:
        encode = pack(42)
        decode = unpack(encode.rstrip(b"\n") if nom != "binaire" else encode)
        print(f"{nom} : {len(encode):3d} octets  {encode!r:40s} -> {decode}")
