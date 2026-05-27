# 13_Securite — Authentification et intégrité

Dernier dossier du cursus. On a vu **comment** parler sur le réseau ;
on aborde ici **avec qui** on parle (authentification) et **comment
vérifier** que ce qui arrive n'a pas été altéré (intégrité).

TLS (dossier 11) protège le **transport** : confidentialité et
intégrité **en transit**. Ce dossier complète au niveau
**applicatif** : qui appelle, avec quels droits, et comment vérifier
qu'un message stocké ou retransmis est authentique.

## Plan

| Fichier              | Sujet                                                      |
|----------------------|------------------------------------------------------------|
| `01_hmac.py`         | HMAC : intégrité d'un message + secret partagé             |
| `02_password_hash.py`| Hash de mot de passe avec sel (PBKDF2)                     |
| `03_basic_auth.py`   | HTTP Basic Auth (à éviter sauf en HTTPS interne)           |
| `04_jwt.py`          | JWT : token signé self-contained (`pip install pyjwt`)     |
| `05_bearer_flow.py`  | Flow complet : login → token → requête authentifiée        |

## Concepts traités

- **HMAC** : signature symétrique. Émetteur et récepteur partagent
  un secret. Permet de prouver que le message vient bien de quelqu'un
  qui connaît le secret. Utilisé partout : webhooks Github/Stripe,
  AWS Signature v4.
- **Hash de mot de passe** : on **ne stocke jamais** un mot de
  passe en clair. On stocke un hash dérivé via une fonction lente
  (PBKDF2, bcrypt, scrypt, argon2) avec sel aléatoire par utilisateur.
- **HTTP Basic** : login/password en base64 dans l'en-tête
  `Authorization`. **Obsolète seul** (toujours en HTTPS), survie
  pour les services internes.
- **Bearer tokens** : `Authorization: Bearer <token>`. Standard
  moderne ; le token est typiquement un JWT.
- **JWT** : JSON Web Token. Un objet signé, **self-contained** :
  contient l'identité et les claims, vérifiable sans appel à une
  base. Standard RFC 7519.

## Dépendances

```bash
pip install cryptography pyjwt requests
```

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sécurité.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
