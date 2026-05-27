# Exercices pratiques — dossier 12_WebSockets

Six ateliers WebSocket. `pip install websockets`.

---

## Atelier 1 — Echo avec horodatage  ★
*Fichier de référence : 01_echo_srv.py*

Modifier le serveur pour préfixer chaque réponse par
`[HH:MM:SS]`.

---

## Atelier 2 — Heartbeat (ping/pong)  ★★
*Fichier de référence : 01_echo_srv.py*

Configurer le serveur pour envoyer un ping automatique toutes les
10 secondes ; déconnecter le client qui ne répond pas dans les 5 s
suivantes.

**Indices** : paramètres `ping_interval=10, ping_timeout=5` de
`websockets.serve`.

---

## Atelier 3 — Chat avec pseudo persistant  ★★
*Fichier de référence : 03_chat_srv.py*

Le premier message reçu de chaque client est son **pseudo**.
Le serveur l'enregistre et l'utilise dans tous les broadcasts qui
suivent (au lieu de l'adresse IP).

---

## Atelier 4 — Compteur de connectés en temps réel  ★★
*Fichier de référence : 03_chat_srv.py*

Diffuser à chaque arrivée/départ un message
`{"connectés": N}` sous forme JSON. Le client HTML met à jour un
indicateur en haut de la page.

---

## Atelier 5 — WS sécurisé (wss://)  ★★★
*Fichiers de référence : 01_echo_srv.py + cert du dossier 11*

Faire passer le serveur en `wss://` (WebSocket sur TLS).
Réutiliser le cert auto-signé du dossier 11.

**Indices** : `websockets.serve(..., ssl=contexte)` où contexte est
un `ssl.SSLContext`.

---

## Atelier 6 — Salons multiples  ★★★
*Fichier de référence : 03_chat_srv.py*

Permettre plusieurs salons via le chemin de connexion :
`ws://.../chat/general`, `ws://.../chat/dev`. Le broadcast ne se
fait qu'à l'intérieur d'un salon.

**Indices** : `websockets.serve` passe `path` au handler ; on
indexe `clients` par salon.
