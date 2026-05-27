# Quiz — dossier 08_HTTP_serveur

## Questions

**Q1.** Pourquoi évite-t-on `http.server.BaseHTTPRequestHandler` en
production ?

**Q2.** Différences principales entre Bottle, Flask et FastAPI ?

**Q3.** FastAPI génère automatiquement une documentation OpenAPI.
Quelle URL ouvre cette documentation ?

**Q4.** Pourquoi est-il recommandé d'utiliser `gunicorn` ou
`uvicorn` plutôt que le serveur de développement intégré de Flask
ou FastAPI ?

**Q5.** Flask `@app.route` vs FastAPI `@app.get` — différence
fonctionnelle ?

**Q6.** FastAPI utilise **Pydantic** pour la validation. Quel
avantage par rapport à valider à la main ?

---

## Réponses

**R1.** Trois raisons : (a) **aucune gestion de routes** (tout le
parsing d'URL est manuel) ; (b) **mono-thread par défaut** (1 client
à la fois) ; (c) **aucun support de middleware** (auth, logging,
CORS, etc.). C'est utile pour comprendre le bas niveau, jamais pour
servir des clients réels.

**R2.** **Bottle** : tient en un seul fichier, zéro dépendance,
minimal. Petits scripts internes. **Flask** : standard historique,
écosystème énorme (Flask-SQLAlchemy, Flask-Login, …), sync par
défaut. **FastAPI** : moderne, async natif, validation Pydantic,
OpenAPI auto. Standard 2026 pour les nouveaux projets.

**R3.** `http://127.0.0.1:8808/docs` (Swagger UI) ou `/redoc`
(ReDoc). Disponible immédiatement, sans configuration.

**R4.** Le serveur de dev est **mono-thread, mono-process**, sans
optimisation, sans reload propre. Gunicorn (sync) ou uvicorn (async)
gèrent : plusieurs workers, redémarrage gracieux, signaux,
intégration avec systemd, journalisation, etc. Indispensable pour
servir du trafic réel.

**R5.** Aucune différence sémantique sur le routage. La différence
est dans l'**inférence de type** : FastAPI lit les annotations
(`format: str`) pour valider et documenter. Flask se contente du
chemin URL.

**R6.** Avec Pydantic : (a) **validation automatique** à l'entrée
(types, contraintes, JSON schema) ; (b) **erreur 422** structurée
si invalide ; (c) **documentation incluse** dans /docs. Sans :
chaque endpoint réécrit son validateur, avec risque d'oubli.
