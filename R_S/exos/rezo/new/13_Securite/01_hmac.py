"""HMAC — Hash-based Message Authentication Code.

Démo pédagogique : on signe un message avec un secret partagé, on
le vérifie côté récepteur. Toute altération du message ou usage
d'une mauvaise clé est détecté.

C'est le pattern derrière :
- les webhooks Github / Stripe / Twilio (header X-Hub-Signature) ;
- AWS Signature v4 ;
- les cookies signés Flask (`itsdangerous`).
"""
import hashlib
import hmac
import secrets


def signer(secret: bytes, message: bytes) -> str:
    """Renvoie un hex digest HMAC-SHA256."""
    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def verifier(secret: bytes, message: bytes, signature: str) -> bool:
    """Vérifie la signature en temps constant (résistance au timing attack)."""
    attendu = signer(secret, message)
    return hmac.compare_digest(attendu, signature)


if __name__ == "__main__":
    secret = b"ma_super_cle_secrete"

    # 1. Signer un message
    message = b"Transfert de 100 EUR vers Alice"
    sig = signer(secret, message)
    print(f"Message   : {message!r}")
    print(f"Signature : {sig}")

    # 2. Vérification réussie
    assert verifier(secret, message, sig)
    print("Vérification message original : OK")

    # 3. Vérification échoue si le message a été altéré
    message_altere = b"Transfert de 1000 EUR vers Alice"
    assert not verifier(secret, message_altere, sig)
    print("Vérification message altéré   : DETECTE")

    # 4. Vérification échoue avec mauvais secret
    assert not verifier(b"mauvaise_cle", message, sig)
    print("Vérification mauvaise clé     : DETECTE")

    # 5. Bonne pratique : générer le secret avec secrets.token_bytes
    nouveau_secret = secrets.token_bytes(32)
    print(f"\nNouveau secret (256 bits) : {nouveau_secret.hex()}")
