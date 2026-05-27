# Exercices pratiques — dossier 09_HTTP_client

Six ateliers sur les clients HTTP.

---

## Atelier 1 — Mesure du gain Session  ★
*Fichier de référence : requests*

Faire 10 requêtes GET successives à `https://httpbin.org/get`,
une fois sans `Session`, une fois avec `Session`. Comparer le temps
total.

**Indices** : `time.perf_counter` ; `requests.Session()`.

---

## Atelier 2 — Téléchargement de fichier (streaming)  ★★
*Fichier de référence : requests*

Télécharger un fichier de grande taille (ex.
`https://httpbin.org/bytes/1048576`) sans tout charger en mémoire :
utiliser `stream=True` et `iter_content`.

**Indices** : `with open("fichier", "wb") as f: for chunk in
r.iter_content(8192): f.write(chunk)`.

---

## Atelier 3 — Retries avec backoff  ★★
*Fichier de référence : 04_requests_advanced.py*

Tester le retry en frappant `https://httpbin.org/status/500` : la
session doit retenter 3 fois avec un backoff croissant.

**Indices** : ajouter un endpoint qui renvoie 500. Logger chaque
tentative via un Logger sur urllib3.

---

## Atelier 4 — Async 50 URLs en parallèle  ★★★
*Fichier de référence : 06_httpx_async.py*

Lancer 50 requêtes en parallèle vers `https://httpbin.org/get` avec
un `asyncio.Semaphore(10)` pour limiter à 10 requêtes simultanées.
Mesurer le temps total et constater l'écart avec 50 requêtes en
série.

---

## Atelier 5 — Client REST avec authentification Bearer  ★★
*Fichier de référence : requests*

Construire un client qui s'authentifie avec un token Bearer fictif
sur `https://httpbin.org/bearer`. Vérifier les codes 200 (token
fourni) vs 401 (token absent).

**Indices** : `headers={"Authorization": "Bearer xxx"}` ou
`auth=` custom.

---

## Atelier 6 — Comparaison 4 clients  ★★★
*Fichiers de référence : tous*

Écrire un script qui mesure le temps moyen sur 20 requêtes pour
les 4 approches : urllib, http.client, requests sans session,
requests avec session, httpx sync, httpx async. Tabuler.
