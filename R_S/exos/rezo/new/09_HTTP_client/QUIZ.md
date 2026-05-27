# Quiz — dossier 09_HTTP_client

## Questions

**Q1.** Trois raisons pour lesquelles on évite `urllib.request` en
faveur de `requests` dans le code applicatif ?

**Q2.** Que fait une `requests.Session()` qu'une succession d'appels
`requests.get(...)` ne fait pas ?

**Q3.** Pourquoi est-il important de définir un `timeout` sur
chaque requête HTTP ?

**Q4.** Quand un `Retry` automatique est-il une **mauvaise** idée ?

**Q5.** Différence pratique entre `httpx.Client` et
`httpx.AsyncClient` ?

**Q6.** Que se passe-t-il si on lance 100 requêtes httpx async en
parallèle vers le même serveur ? Risque-t-on de le saturer ?

---

## Réponses

**R1.** (a) **Verbosité** : 5 lignes vs 2 ; (b) **pas de session**
(perte du keep-alive entre requêtes) ; (c) **pas de retries
automatiques** ; (d) gestion d'erreur via HTTPError seulement (pas
d'exception sur les 4xx par défaut sans `raise_for_status()`).

**R2.** Une `Session` (a) **réutilise les connexions TCP** (HTTP
keep-alive) : 1 handshake au lieu de N ; (b) persiste les **cookies**
entre requêtes ; (c) permet de partager des en-têtes par défaut
(`session.headers`) ; (d) permet d'attacher un `HTTPAdapter` avec
des retries personnalisés.

**R3.** Sans timeout, `requests.get(...)` peut **bloquer
indéfiniment** si le serveur ne répond pas. Pour un worker web ou
un job qui doit terminer, c'est inacceptable. Convention : timeout
de 5–30 s selon le contexte. Toujours.

**R4.** Quand la requête est **non idempotente** (POST qui crée une
ressource, paiement, envoi d'email…). Retenter peut créer des
doublons. Par défaut, `Retry` ne retente que les méthodes
idempotentes (GET, HEAD, OPTIONS, PUT, DELETE). Vérifier avant
d'ajouter POST à `allowed_methods`.

**R5.** `Client` est synchrone (`with ... :`) ; `AsyncClient` est
asynchrone (`async with ... :`, `await`). Sémantique identique,
seul l'environnement d'exécution change.

**R6.** Risque réel. httpx async limite par défaut à **100
connexions simultanées par hôte** (configurable via `Limits`). Au
delà, les requêtes attendent une connexion libre. Pour vraiment
ne pas saturer, utiliser un `asyncio.Semaphore` côté client.
