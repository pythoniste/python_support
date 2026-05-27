"""Hashing de mots de passe — PBKDF2 (stdlib).

NE JAMAIS stocker un mot de passe en clair. On stocke (sel + hash)
issu d'une fonction LENTE pour rendre les attaques par dictionnaire
coûteuses.

Algorithmes recommandés (2026, par ordre de préférence) :
1. argon2id (`pip install argon2-cffi`)
2. bcrypt (`pip install bcrypt`)
3. scrypt (stdlib `hashlib.scrypt`)
4. PBKDF2 (stdlib `hashlib.pbkdf2_hmac`) — utilisé ici pour rester
   en stdlib pure, mais argon2 ou bcrypt sont préférables en
   production.
"""
import hashlib
import hmac
import secrets


# Paramètres PBKDF2 — un compromis sécurité / performance.
ALGO = "sha256"
ITERATIONS = 200_000
LONGUEUR_SEL = 16


def hasher_password(mot_de_passe: str) -> str:
    """Renvoie une chaîne 'algo$iter$sel$hash' prête à stocker en base."""
    sel = secrets.token_bytes(LONGUEUR_SEL)
    derive = hashlib.pbkdf2_hmac(ALGO, mot_de_passe.encode("utf-8"), sel, ITERATIONS)
    return f"{ALGO}${ITERATIONS}${sel.hex()}${derive.hex()}"


def verifier_password(mot_de_passe: str, hash_stocke: str) -> bool:
    """Vérifie un mot de passe contre un hash stocké."""
    algo, iterations, sel_hex, hash_hex = hash_stocke.split("$")
    sel = bytes.fromhex(sel_hex)
    derive = hashlib.pbkdf2_hmac(
        algo, mot_de_passe.encode("utf-8"), sel, int(iterations)
    )
    # Comparaison en temps constant
    return hmac.compare_digest(derive.hex(), hash_hex)


if __name__ == "__main__":
    motpasse = "monSuperMotDePasse42!"

    stocke = hasher_password(motpasse)
    print(f"Hash stocké : {stocke}")
    print(f"  (longueur : {len(stocke)} caractères)")

    assert verifier_password(motpasse, stocke)
    print("Vérification bon mot de passe     : OK")

    assert not verifier_password("essai", stocke)
    print("Vérification mauvais mot de passe : REJETE")

    # Deux hash du même mot de passe doivent être DIFFÉRENTS (sels aléatoires).
    autre = hasher_password(motpasse)
    assert stocke != autre
    print("Deux hashes du même password sont différents (sels aléatoires).")
