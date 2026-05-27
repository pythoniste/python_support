"""JWT — JSON Web Token (`pip install pyjwt`).

Un JWT est un objet auto-porteur signé :
    <header en base64>.<payload en base64>.<signature>

- Header : type d'algorithme.
- Payload : claims (identité utilisateur, expiration, etc.).
- Signature : HMAC ou signature asymétrique sur (header + payload).

Avantage : le serveur peut vérifier le token **sans appeler une
base** — la signature suffit. Idéal pour le scaling horizontal.
"""
import datetime
import jwt


SECRET = "remplace-moi-par-un-vrai-secret-de-256-bits"


def emettre(utilisateur: str, ttl_minutes: int = 60) -> str:
    """Émet un JWT pour `utilisateur`, valide ttl_minutes minutes."""
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": utilisateur,                             # subject
        "iat": maintenant,                              # issued at
        "exp": maintenant + datetime.timedelta(minutes=ttl_minutes),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verifier(token: str) -> dict:
    """Décode et vérifie. Lève une exception si invalide / expiré."""
    return jwt.decode(token, SECRET, algorithms=["HS256"])


if __name__ == "__main__":
    # 1. Émission
    token = emettre("alice")
    print(f"Token émis :\n  {token}\n")

    # 2. Inspection (sans vérifier la signature)
    print("Payload (lisible, non chiffré) :")
    print(f"  {jwt.decode(token, options={'verify_signature': False})}\n")

    # 3. Vérification d'un token valide
    print(f"Vérification valide : {verifier(token)}\n")

    # 4. Vérification d'un token altéré
    altere = token[:-1] + ("a" if token[-1] != "a" else "b")
    try:
        verifier(altere)
    except jwt.InvalidSignatureError as exc:
        print(f"Vérification altéré : REJETE ({exc})")
