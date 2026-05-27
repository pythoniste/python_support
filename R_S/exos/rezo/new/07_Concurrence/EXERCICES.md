# Exercices pratiques — dossier 07_Concurrence

Huit ateliers explorant les différentes formes de concurrence.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Compter les threads actifs  ★
*Fichier de référence : 02_thread_srv.py*

Ajouter au handler un affichage du **nombre de threads actifs** au
moment où un client se connecte et au moment où il se déconnecte.
Lancer le test de charge à 3 clients et observer le pic à 3.

**Indices**

- `threading.active_count()` retourne le nombre total de threads
  (y compris le main).
- L'affichage se fait dans `handle()`, début et fin.

---

## Atelier 2 — Timestamps dans les logs  ★
*Fichier de référence : 02_thread_srv.py*

Préfixer chaque ligne de log par un horodatage millisecondes. Lancer
le test de charge et **observer l'entrelacement** des messages de
différents clients (les threads ne progressent pas par lots).

**Indices**

- `from datetime import datetime ; datetime.now().strftime("%H:%M:%S.%f")[:-3]`.
- Fonction utilitaire `log(message)` qui préfixe avant chaque print.

---

## Atelier 3 — Limiter le nombre de threads  ★★
*Fichier de référence : 02_thread_srv.py*

Limiter le nombre de threads simultanés à **5** via un
`threading.Semaphore(5)`. Au-delà, les clients attendent qu'un
slot se libère avant d'être servis.

Tester avec 10 clients en parallèle : observer que 5 sont traités
en même temps, puis les 5 suivants.

**Indices**

- `semaphore = threading.Semaphore(5)`.
- Dans `handle()` : `with semaphore: ...`.
- Lancer 10 clients en parallèle (adapter `06_charge_test.py`).

---

## Atelier 4 — Asyncio : `gather` sur plusieurs tâches  ★★
*Fichier de référence : 04_asyncio_srv.py + client*

Écrire un client **asyncio** qui ouvre 10 connexions en parallèle
via `asyncio.gather`, chacune envoyant 3 messages. Mesurer le temps
total — comparer avec le test de charge à 3 clients via subprocess.

**Indices**

- `asyncio.open_connection(host, port)` retourne `(reader, writer)`.
- `await asyncio.gather(*[client_async(i) for i in range(10)])`.
- Chaque coroutine fait son propre flux d'écriture/lecture.

---

## Atelier 5 — Asyncio avec timeout  ★★
*Fichier de référence : 04_asyncio_srv.py*

Ajouter un timeout de **2 secondes** à chaque `readline()` côté
serveur. Si le client est trop lent, le serveur ferme la connexion
proprement avec un message `b"TIMEOUT\n"`.

**Indices**

- `asyncio.wait_for(reader.readline(), timeout=2.0)`.
- Attraper `asyncio.TimeoutError`.

---

## Atelier 6 — Chat broadcast avec asyncio  ★★★
*Fichier de référence : 04_asyncio_srv.py*

Construire un serveur de **chat** : chaque message reçu d'un client
est **diffusé à tous les autres clients** connectés.

**Indices**

- Liste globale (`set`) des writers actifs.
- À l'arrivée d'un message, itérer sur la liste et écrire à chacun
  (sauf l'émetteur).
- Au départ d'un client, retirer son writer de la liste.

---

## Atelier 7 — Selectors : multiplexer aussi l'écriture  ★★★
*Fichier de référence : 03_selectors_srv.py*

Le serveur selectors actuel utilise `sendall` (qui peut bloquer si
le buffer d'écriture est plein). Refaire avec `EVENT_WRITE` : la
réponse est mise en buffer côté serveur, et envoyée par tranches
quand le selecteur signale que le socket est prêt à écrire.

**Indices**

- `sel.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data)`.
- Data devient un objet qui contient à la fois les callbacks et le
  buffer d'écriture en attente.

---

## Atelier 8 — Benchmark systématique  ★★★
*Fichiers de référence : les 4 serveurs*

Écrire un script qui mesure le temps total de traitement de N
clients lents pour N ∈ {3, 30, 300} sur les 4 serveurs. Tabuler.

**Indices**

- Boucle qui lance le serveur en subprocess, puis les N clients
  via `asyncio.gather` (plus rapide que subprocess pour 300 clients).
- Attention à ulimit pour 300 clients (file descriptors).
- L'itératif sera lent ; arrêter à 30 si besoin.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le cursus continue vers les sujets
de spécialité : `08_HTTP_serveur/` (Flask/FastAPI), `09_HTTP_client/`,
`10_REST/`, `11_TLS/`, `12_WebSockets/`, `13_Securite/`. Aucun de
ces sujets ne se comprend pleinement sans les fondations posées
dans les dossiers 00 à 07.
