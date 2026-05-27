#!/usr/bin/env python3
"""Demo : secrets pour generer, hmac pour signer.

A executer :  python3 04_demo_secrets_et_hmac.py

Le script genere differents tokens avec secrets, signe un message avec
HMAC-SHA256, verifie la signature avec compare_digest, et illustre une
detection de falsification.
"""
import hashlib
import hmac
import secrets


def main():
    # 1) Generation de secrets : trois formes utiles.
    print("--- secrets ---")
    print("token_hex(16)     :", secrets.token_hex(16))
    print("token_urlsafe(16) :", secrets.token_urlsafe(16))
    print("token_bytes(16)   :", secrets.token_bytes(16))
    print("randbelow(1000)   :", secrets.randbelow(1000))
    print("choice(...)       :",
          secrets.choice(["alpha", "beta", "gamma"]))

    # 2) Comparaison a temps constant. Pour deux tokens, on
    # n'utilise PAS '==' mais secrets.compare_digest.
    print("--- compare_digest ---")
    attendu = "abc123"
    print("attendu == 'abc123' :",
          secrets.compare_digest(attendu, "abc123"))
    print("attendu == 'abc999' :",
          secrets.compare_digest(attendu, "abc999"))

    # 3) Signature HMAC-SHA256 d'un message.
    print("--- HMAC-SHA256 ---")
    cle = secrets.token_bytes(32)            # cle partagee
    message = b"transfert:100eur:bob"

    signature = hmac.new(cle, message, hashlib.sha256).hexdigest()
    print("message   :", message)
    print("signature :", signature)

    # 4) Verification cote recepteur.
    recalculee = hmac.new(cle, message, hashlib.sha256).hexdigest()
    if hmac.compare_digest(recalculee, signature):
        print("verification : OK (message authentique)")
    else:
        print("verification : KO")

    # 5) Falsification : le message change, la signature ne suit plus.
    print("--- detection de falsification ---")
    message_falsifie = b"transfert:9999eur:bob"
    recalculee = hmac.new(cle, message_falsifie,
                          hashlib.sha256).hexdigest()
    if hmac.compare_digest(recalculee, signature):
        print("verification : OK (ne devrait pas arriver)")
    else:
        print("verification : KO (signature ne correspond pas)")


if __name__ == "__main__":
    main()
