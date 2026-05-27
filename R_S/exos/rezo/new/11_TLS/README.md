# 11_TLS — Chiffrer les communications

Tout ce qu'on a vu jusqu'ici passe **en clair sur le réseau**.
Wireshark capture les mots de passe, les API keys, le JSON métier.
Sur Internet, c'est impensable. TLS (Transport Layer Security)
résout le problème.

## Trois garanties TLS

1. **Confidentialité** : chiffrement symétrique de bout en bout
   (clé de session négociée par le handshake).
2. **Intégrité** : MAC sur chaque enregistrement, détecte les
   modifications en transit.
3. **Authentification (du serveur, et optionnellement du client)**
   par certificats X.509 signés par une autorité de confiance (CA).

HTTPS = HTTP sur TLS. WSS = WebSocket sur TLS.

## Plan

| Fichier               | Sujet                                                  |
|-----------------------|--------------------------------------------------------|
| `01_https_client.py`  | Client HTTPS avec `requests` (parfait pour servers publics) |
| `02_generer_cert.py`  | Générer un certificat auto-signé via `cryptography`   |
| `03_tls_srv.py`       | Serveur TCP TLS minimal (stdlib `ssl`)                |
| `04_tls_clt.py`       | Client TCP TLS qui parle au serveur ci-dessus         |
| `05_bottle_tls.py`    | Bottle en HTTPS (avec cert auto-signé)                |

## Avant de lancer les paires locales

Les paires 3, 4, 5 utilisent un **certificat auto-signé** créé par
le script 02 :

```bash
pip install cryptography requests
python3 02_generer_cert.py             # crée serveur.crt + serveur.key
python3 03_tls_srv.py                  # terminal 1
python3 04_tls_clt.py                  # terminal 2 (échange chiffré)
```

Un certificat auto-signé est **rejeté par défaut** par les
clients (warning "verify failed"). On contourne en passant le
chemin du cert au client (`verify=...`).

## Quand utiliser quoi en 2026

- **Service public** : Let's Encrypt + un reverse proxy
  (nginx/caddy/traefik) qui terminate TLS. Le code Python ne voit
  que du HTTP en clair sur localhost.
- **Service interne** : certificats internes (mTLS) générés par
  une CA d'entreprise.
- **Pour démonstration / labo** : certificats auto-signés, ce que
  fait ce dossier.

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur TLS.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
