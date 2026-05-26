# Exercices pratiques — dossier 03_Socketserver

Huit ateliers pour explorer la palette du module `socketserver`,
du simple changement de réponse à un serveur multi-clients.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Echo serveur  ★
*Fichier de référence : 01_tcpsrv.py*

Modifier le handler pour qu'il renvoie **exactement** le message reçu
(suivi de `\n`), sans préfixe « Bonjour » ni suffixe « . ».

**Indices**

- Une seule ligne à changer dans la méthode `handle()`.

---

## Atelier 2 — Compteur de connexions  ★
*Fichier de référence : 01_tcpsrv.py*

Ajouter au handler un **compteur de classe** qui s'incrémente à
chaque connexion acceptée. Inclure le numéro dans la réponse :
`b"Bonjour client #N : <data>.\n"`.

**Indices**

- Attribut de classe (pas d'instance) — il est partagé par toutes
  les instances créées par le framework.
- L'incrémenter dans `handle()`.

---

## Atelier 3 — Multi-message par connexion  ★★
*Fichier de référence : 01_tcpsrv.py*

Modifier le handler pour traiter **plusieurs messages dans la même
connexion**. Le client devra envoyer plusieurs lignes sans se
reconnecter, et le handler doit lire jusqu'à EOF.

Adapter aussi `02_tcpclt.py` pour envoyer 3 messages dans une seule
connexion ouverte.

**Indices**

- `while True` autour de `readline`, sortir si la ligne est vide.
- Côté client, ouvrir une seule fois la connexion, faire 3
  `sendall` / `recv_ligne`.

---

## Atelier 4 — BaseRequestHandler  ★★
*Fichier de référence : 01_tcpsrv.py*

Refaire le serveur avec `socketserver.BaseRequestHandler` au lieu de
`StreamRequestHandler`. On perd `rfile`/`wfile` ; on travaille
directement sur `self.request` (le socket brut), avec `recv`/`send`.

**Indices**

- `self.request` est le socket connecté au client.
- Pas de framing automatique : retomber sur un `recv` simple
  (suffisant pour un message court en local) ou réutiliser
  `recv_ligne`.

---

## Atelier 5 — ThreadingTCPServer  ★★
*Fichier de référence : 01_tcpsrv.py*

Activer le mode multi-clients via le mixin
`socketserver.ThreadingMixIn`. Tester en lançant **deux clients en
parallèle** (deux terminaux) : ils doivent être servis simultanément
et non l'un après l'autre.

**Indices**

- Définir une nouvelle classe :
  ```python
  class ServeurMultiClient(socketserver.ThreadingMixIn, socketserver.TCPServer):
      pass
  ```
- L'ordre d'héritage compte : mixin en premier.
- Ajouter un `time.sleep(2)` dans `handle()` pour rendre le
  parallélisme visible.

---

## Atelier 6 — Log fichier  ★
*Fichier de référence : 01_tcpsrv.py*

Écrire chaque message reçu dans un fichier `messages.log`
(append mode), avec horodatage et adresse du client.

**Indices**

- `from datetime import datetime` ; `datetime.now().isoformat()`.
- Ouvrir le fichier en mode `"a"` à chaque appel, ou en attribut de
  classe à l'init du serveur.

---

## Atelier 7 — Mot-clé stop via threading  ★★★
*Fichier de référence : 01_tcpsrv.py*

Réintroduire le mot-clé `stop` qui arrête proprement le serveur.
La difficulté : `self.server.shutdown()` ne peut pas être appelée
depuis `handle()` directement (deadlock). Il faut déléguer à un
thread auxiliaire.

**Indices**

- `import threading` ; `threading.Thread(target=self.server.shutdown).start()`
  juste avant que `handle()` retourne.
- Ne pas attendre la fin du thread — il fait son travail en
  arrière-plan.

---

## Atelier 8 — Protocole binaire préfixé via socketserver  ★★★
*À écrire de zéro à partir de 01_tcpsrv.py + 02_Framing/03_prefixe_srv.py*

Reprendre le protocole à préfixe de longueur de l'atelier
`02_Framing/03_prefixe_srv.py` et le réécrire avec
`BaseRequestHandler`. Le handler doit lire le préfixe `u32`
big-endian puis le payload, et répondre selon le même protocole.

**Indices**

- Hériter de `BaseRequestHandler` (pas StreamRequestHandler — on est
  en binaire à taille variable).
- Travailler sur `self.request.recv` directement.
- Importer ou réimplémenter `recv_exactement`, `envoyer_message_prefixe`,
  `recevoir_message_prefixe`.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le dossier suivant — **`04_Palindrome/`**
— met en pratique tout ce qu'on a vu sur un cas d'usage métier
(détection de palindrome), avec les quatre couches d'abstraction
(raw socket TCP, raw socket UDP, socketserver TCP, socketserver UDP).
