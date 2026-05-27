# 04 — `secrets` et `hmac` : générer et signer

## 4.1 Pourquoi pas `random` ?

Le module `random` de la bibliothèque standard est un générateur
**pseudo-aléatoire** orienté simulation. Sa graine peut être devinée à
partir d'observations successives, et le standard Python n'en fait pas
mystère : sa documentation indique explicitement de **ne pas l'utiliser
pour la cryptographie**.

```python
# À NE JAMAIS FAIRE pour un token, un mot de passe, une clé...
import random
token = "".join(random.choices("0123456789abcdef", k=32))
```

Pour tout ce qui doit être imprévisible — token de session, clé d'API,
mot de passe temporaire, identifiant de panier… — on utilise le module
**`secrets`**, qui s'appuie sur le générateur cryptographique du
système d'exploitation.

## 4.2 Générer un secret avec `secrets`

| Fonction                       | Renvoie                                  |
|--------------------------------|------------------------------------------|
| `secrets.token_hex(n)`         | Chaîne hex de `2n` caractères            |
| `secrets.token_urlsafe(n)`     | Chaîne ASCII URL-safe (`-`, `_`, alpha)  |
| `secrets.token_bytes(n)`       | `bytes` brut de longueur `n`             |
| `secrets.randbelow(n)`         | Entier dans `[0, n)`                     |
| `secrets.choice(seq)`          | Élément tiré dans une séquence           |

```python
import secrets

print(secrets.token_hex(16))       # 32 caractères hex
print(secrets.token_urlsafe(16))   # ~22 caractères URL-safe
print(secrets.token_bytes(16))     # 16 octets bruts
print(secrets.randbelow(1000))     # 0..999
print(secrets.choice(["alpha", "beta", "gamma"]))
```

L'argument `n` est un **nombre d'octets**, pas un nombre de
caractères. `token_hex(16)` produit une chaîne de **32** caractères
hex parce que chaque octet donne 2 caractères. Pour un token de
session « solide », 16 à 32 octets sont la norme.

## 4.3 Comparaison à temps constant

Un `==` classique entre deux chaînes ou deux `bytes` s'arrête au
**premier octet qui diffère**. Un attaquant qui mesure le temps de
réponse peut, en théorie, deviner un secret caractère par caractère.
Pour comparer un secret reçu à un secret attendu, on utilise donc
`secrets.compare_digest`, qui prend **toujours le même temps** quelle
que soit la position de la divergence :

```python
import secrets

attendu = "abc123"
recu = "abc999"
if secrets.compare_digest(attendu, recu):
    print("OK")
else:
    print("Refuse")
```

À utiliser pour comparer : tokens, clés d'API, signatures, empreintes
de mots de passe. Pour deux chaînes « banales » qui ne sont pas des
secrets, le `==` ordinaire reste de mise.

## 4.4 Signer un message avec `hmac`

**HMAC** (*Hash-based Message Authentication Code*) répond à la
question : « ce message a-t-il été envoyé par quelqu'un qui possède la
même clé que moi, et n'a-t-il pas été modifié en route ? ».

On choisit une fonction de hachage (généralement `sha256`), une **clé
secrète** partagée entre l'émetteur et le récepteur, et on calcule la
signature du message :

```python
import hmac, hashlib

cle = b"ma-cle-secrete-32-octets-...."   # connue des deux cotes
message = b"transfert:100eur:bob"

signature = hmac.new(cle, message, hashlib.sha256).hexdigest()
print(signature)
```

Pour **vérifier** côté récepteur, on recalcule la signature et on
compare avec `hmac.compare_digest` (équivalent de
`secrets.compare_digest`, propre au module `hmac`) :

```python
attendue = hmac.new(cle, message, hashlib.sha256).hexdigest()
if hmac.compare_digest(attendue, signature):
    print("Message authentique")
else:
    print("Message altere ou signature invalide")
```

## 4.5 Cas d'usage

| Besoin                                  | Outil                              |
|-----------------------------------------|------------------------------------|
| Identifiant de session web              | `secrets.token_urlsafe(32)`        |
| Clé d'API à donner à un client          | `secrets.token_hex(32)`            |
| Clé symétrique brute (32 octets)        | `secrets.token_bytes(32)`          |
| Vérifier un webhook GitHub / Stripe…    | `hmac.new(cle, payload, sha256)`   |
| Vérifier un mot de passe haché          | `hmac.compare_digest(...)`         |
| Tirer un élément au sort dans une liste | `secrets.choice(liste)`            |

Les services qui envoient des **webhooks** signent presque toujours
leur charge utile avec HMAC-SHA256 ; le serveur récepteur recalcule la
signature et la compare avec celle reçue dans un en-tête. C'est
exactement le motif vu en 4.4.

## À retenir

- Pour un secret, **jamais** `random` — toujours `secrets`.
- `secrets.token_hex / token_urlsafe / token_bytes` couvrent 99 % des
  besoins ; l'argument `n` est un **nombre d'octets**.
- `secrets.compare_digest` (ou `hmac.compare_digest`) pour comparer
  deux secrets : temps constant, à l'abri du timing.
- `hmac.new(cle, message, hashlib.sha256).hexdigest()` signe un
  message ; on vérifie en recalculant et en comparant.
- Pour stocker un mot de passe, ni `hashlib.sha256` ni `hmac` : il
  faut une fonction lente (`scrypt`, `pbkdf2_hmac`).

## Démo

Exécuter `04_demo_secrets_et_hmac.py`.
