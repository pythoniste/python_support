"""Générateur de certificat auto-signé pour les démos TLS locales.

`pip install cryptography`.

Crée deux fichiers dans le dossier courant :
    serveur.key  : clé privée RSA 2048 bits
    serveur.crt  : certificat X.509 auto-signé valable 365 jours

Ce certificat est valable pour CN=localhost et SAN=127.0.0.1.
Les clients devront soit l'accepter explicitement (verify=path),
soit désactiver la vérification (déconseillé sauf en démo).
"""
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def main():
    # 1. Génère une clé privée RSA.
    cle = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # 2. Construit le sujet et l'émetteur (= soi-même : auto-signé).
    sujet = emetteur = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Demo locale"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    # 3. Construit le certificat avec un SAN qui inclut 127.0.0.1.
    cert = (
        x509.CertificateBuilder()
        .subject_name(sujet)
        .issuer_name(emetteur)
        .public_key(cle.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.IPAddress(__import__("ipaddress").IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .sign(cle, hashes.SHA256())
    )

    # 4. Écrit la clé et le cert en PEM.
    Path("serveur.key").write_bytes(cle.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    ))
    Path("serveur.crt").write_bytes(cert.public_bytes(serialization.Encoding.PEM))

    print("Certificat auto-signé créé :")
    print(f"  serveur.crt — valide jusqu'au {cert.not_valid_after}")
    print(f"  serveur.key — clé privée RSA 2048")


if __name__ == "__main__":
    main()
