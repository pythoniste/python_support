# Exercices pratiques — dossier 13_Securite

Six ateliers sur l'authentification et l'intégrité.

---

## Atelier 1 — Webhook signé Github  ★★
*Fichier de référence : 01_hmac.py*

Github signe ses webhooks avec un header
`X-Hub-Signature-256: sha256=<hex>`. Écrire un middleware FastAPI
qui vérifie cette signature avant de traiter le corps. Tester avec
un faux webhook en local.

**Indices** : récupérer le corps brut (raw bytes) ; comparer avec
`compare_digest`.

---

## Atelier 2 — Vérifier la force d'un mot de passe  ★
*Fichier de référence : 02_password_hash.py*

Avant de hasher un mot de passe, vérifier qu'il fait au moins 12
caractères et contient majuscule + minuscule + chiffre + spécial.
Lever `ValueError` sinon.

---

## Atelier 3 — Migrer PBKDF2 → bcrypt  ★★
*Fichier de référence : 02_password_hash.py*

Refaire le module avec `bcrypt` (`pip install bcrypt`) au lieu de
PBKDF2. Comparer la facilité d'usage et les paramètres (bcrypt
gère le sel automatiquement).

---

## Atelier 4 — Token avec rôles (RBAC)  ★★
*Fichier de référence : 05_bearer_flow.py*

Ajouter une route `GET /finance` accessible uniquement aux
utilisateurs dont le rôle est `finance` ou `admin`. Tester avec
un utilisateur sans le rôle (403) et avec (200).

---

## Atelier 5 — Refresh token  ★★★
*Fichier de référence : 05_bearer_flow.py*

Implémenter un système à deux tokens : un access_token court
(15 min) et un refresh_token long (7 jours). Une route
`POST /refresh` échange le refresh_token contre un nouveau pair.

---

## Atelier 6 — Stockage et révocation  ★★★
*Fichier de référence : 05_bearer_flow.py*

Ajouter une route `POST /logout` qui ajoute le token courant à une
**liste noire** (un set en mémoire pour la démo, Redis en
production). Modifier `utilisateur_courant` pour rejeter les tokens
de la liste.

Note : c'est le contournement classique de la non-révocation des
JWT.
