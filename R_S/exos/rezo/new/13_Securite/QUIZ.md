# Quiz — dossier 13_Securite

## Questions

**Q1.** Différence entre **HMAC** et un simple **hash** (`sha256`) ?
Pourquoi HMAC est-il préféré pour signer un message ?

**Q2.** Pourquoi utilise-t-on `hmac.compare_digest` plutôt que
`==` pour comparer des signatures ?

**Q3.** Que doit-on stocker en base pour un mot de passe : la
valeur en clair, son hash SHA-256, ou un hash via PBKDF2/bcrypt /
argon2 ? Pourquoi le dernier choix ?

**Q4.** En quoi un JWT est-il **"self-contained"** ? Quelle est la
contrepartie de cette propriété ?

**Q5.** Un JWT signé n'est PAS chiffré. Pourquoi ne peut-on pas
considérer un JWT comme "secret" ?

**Q6.** Quel pattern d'authentification recommandez-vous en 2026
pour une API REST publique ? Justifier.

---

## Réponses

**R1.** Un hash simple `sha256(message)` peut être recalculé par
n'importe qui : il prouve l'intégrité mais pas l'**origine**. HMAC
inclut un **secret partagé** dans le calcul : sha256(secret +
message) (en simplifiant). Sans le secret, on ne peut pas forger
une signature valide. HMAC prouve donc **intégrité ET origine**.

**R2.** Pour résister aux **timing attacks**. Un `==` Python sort
au premier octet différent — l'attaquant peut mesurer le temps de
réponse et deviner les octets un par un. `hmac.compare_digest`
compare en **temps constant** : même durée quel que soit
l'emplacement de la différence.

**R3.** **PBKDF2 / bcrypt / argon2** (par ordre croissant de
préférence). Raison : un hash SHA-256 est **rapide** — un GPU
calcule des milliards de hashes par seconde, donc une attaque par
dictionnaire est triviale. Les fonctions PBKDF2/bcrypt/argon2 sont
**volontairement lentes** (~100 ms par hash) avec un **sel
aléatoire** par utilisateur, rendant les attaques par dictionnaire
prohibitivement coûteuses.

**R4.** Un JWT contient **toutes les informations nécessaires** à
sa validation : identité, rôles, expiration, signature. Le serveur
n'a pas besoin d'appeler une base — la signature suffit pour la
confiance.

**Contrepartie : pas de révocation native.** Un JWT émis reste
valide jusqu'à son expiration. Solutions de contournement :
expiration courte (15 min) + refresh token, ou liste de tokens
révoqués côté serveur.

**R5.** Parce que le payload JWT est encodé en **base64 standard,
LISIBLE par n'importe qui**. La signature empêche la modification,
pas la lecture. Ne JAMAIS mettre de données sensibles (mot de
passe, données médicales, etc.) dans un JWT. Pour chiffrer, utiliser
JWE (JSON Web Encryption) — rarement nécessaire en pratique.

**R6.** **OAuth 2.0 + JWT comme access token, sur HTTPS.** Pourquoi :
(a) standard mature, supporté par tous les langages ; (b) le client
ne manipule jamais le mot de passe ; (c) scaling horizontal du
serveur de ressources (JWT auto-porteur) ; (d) intégration native
avec les identity providers (Google, Auth0, Keycloak…).
Implémentation simple : Authlib, FastAPI-Security, ou Auth0 SDK.
