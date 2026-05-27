# Exercices pratiques — dossier 08_HTTP_serveur

Six ateliers explorant les frameworks HTTP.

---

## Atelier 1 — Endpoint `/uptime` (stdlib)  ★
*Fichier de référence : 01_stdlib_http.py*

Ajouter un endpoint `GET /uptime` qui renvoie le temps écoulé depuis
le démarrage du serveur, au format `{"uptime_secondes": ...}`.

**Indices** : `time.perf_counter()` au démarrage, différence à
chaque requête.

---

## Atelier 2 — Endpoint POST `/echo` (Flask)  ★
*Fichier de référence : 03_flask.py*

Ajouter `POST /echo` qui renvoie le corps JSON reçu, augmenté d'un
horodatage.

**Indices** : `request.json`, `methods=["POST"]`.

---

## Atelier 3 — Validation Pydantic (FastAPI)  ★★
*Fichier de référence : 04_fastapi.py*

Définir un modèle Pydantic `Personne` (nom: str, age: int ≥ 0).
Ajouter `POST /personnes` qui accepte ce modèle et renvoie un
greeting. Tester via /docs avec des données valides puis invalides.

**Indices** : `from pydantic import BaseModel, Field` ; `age: int =
Field(ge=0)`.

---

## Atelier 4 — Middleware de log (FastAPI)  ★★
*Fichier de référence : 04_fastapi.py*

Ajouter un middleware qui logge la méthode, l'URL et le temps de
réponse pour chaque requête. Tester en lançant plusieurs curl.

**Indices** : `@app.middleware("http")` avec `async def`.

---

## Atelier 5 — Serveur multi-framework (★★★)
*Fichiers de référence : tous*

Modifier les 4 serveurs pour qu'ils écoutent sur des ports
**différents** (8801, 8802, 8803, 8804). Écrire un script qui les
démarre tous en subprocess et envoie une requête à chacun pour
vérifier que tous fonctionnent identiquement.

---

## Atelier 6 — Performance comparative (★★★)
*Fichiers de référence : tous*

Mesurer le **débit** (requêtes/seconde) de chacun des 4 serveurs
avec `ab` (Apache bench) ou un client Python en boucle. Tabuler.

**Indices** : `ab -n 1000 -c 10 http://127.0.0.1:8808/heure` ;
ou client Python avec `requests` en boucle ; ou `httpx.AsyncClient`
en parallèle.
