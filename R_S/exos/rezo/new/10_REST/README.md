# 10_REST — Concevoir une API REST

REST (Representational State Transfer) n'est pas un protocole mais
un **style architectural** sur HTTP, formulé par Roy Fielding en
2000. Ce dossier illustre les principes sur un cas concret : une
API de gestion de TODOs (liste de tâches).

## Les six contraintes REST (rappel)

1. **Client-serveur** : séparation stricte.
2. **Stateless** : le serveur ne mémorise rien entre requêtes
   (dossier 06).
3. **Cacheable** : les réponses peuvent être mises en cache (HTTP).
4. **Interface uniforme** : URLs et méthodes HTTP standards.
5. **Système en couches** : intermédiaires (proxies, CDN) transparents.
6. **Code à la demande** *(optionnel)* : envoi de JS au client.

La contrainte la plus saillante au quotidien : **l'interface
uniforme**.

## Le contrat d'une API REST

| Méthode HTTP | Action            | Idempotente ? | Body ?    |
|--------------|-------------------|---------------|-----------|
| GET          | Lire              | Oui           | Non       |
| POST         | Créer             | **Non**       | Oui (data)|
| PUT          | Remplacer         | Oui           | Oui (data)|
| PATCH        | Modifier partiel  | Oui (en général) | Oui    |
| DELETE       | Supprimer         | Oui           | Non       |

## Plan

| Fichier                  | Concept REST                              |
|--------------------------|-------------------------------------------|
| `01_crud_stdlib.py`      | CRUD complet sur `http.server` (stdlib)   |
| `02_crud_fastapi.py`     | Même CRUD sur FastAPI (recommandé)        |
| `03_versioning.py`       | Versioning d'API (/v1, /v2)               |
| `04_pagination.py`       | Pagination des listes longues             |
| `05_erreurs.py`          | Codes HTTP et corps d'erreur cohérent     |

Toutes les paires utilisent le port `8808`.

```
pip install fastapi uvicorn       # pour 02 et au-delà

python3 01_crud_stdlib.py
```

Démonstration avec `curl` :

```
curl -X POST http://127.0.0.1:8808/todos \
     -H "Content-Type: application/json" \
     -d '{"titre": "Acheter du pain", "fait": false}'

curl http://127.0.0.1:8808/todos
curl http://127.0.0.1:8808/todos/1
curl -X DELETE http://127.0.0.1:8808/todos/1
```

## Anti-patterns à éviter

- **Verbes dans l'URL** : `/getUser/1`, `/deleteTodo/3`.
  → Préférer : `GET /users/1`, `DELETE /todos/3`.
- **Toujours 200 OK** : ne renvoyer que des 200 même en erreur.
  → Utiliser 201, 204, 400, 404, 409, 422, 500 selon le cas.
- **État dans le serveur** : sessions implicites entre requêtes.
  → Voir dossier 06. Mettre l'état dans un token côté client.
- **Plurals incohérents** : `/user/1` mais `/posts/5`.
  → Choisir une convention et s'y tenir (pluriel partout est plus
  fréquent).

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur REST.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
