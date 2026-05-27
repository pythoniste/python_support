# 08_HTTP_serveur — Frameworks HTTP en Python

Premier dossier de spécialité. On a vu Bottle au dossier 04 ;
on compare ici les **frameworks HTTP** les plus utilisés en
production, sur le même service trivial : un endpoint qui renvoie
l'heure actuelle au format ISO 8601.

## Plan

| Fichier             | Framework                  | Bibliothèque          |
|---------------------|----------------------------|-----------------------|
| `01_stdlib_http.py` | `http.server` (stdlib)     | stdlib                |
| `02_bottle.py`      | Bottle                     | `pip install bottle`  |
| `03_flask.py`       | Flask                      | `pip install flask`   |
| `04_fastapi.py`     | FastAPI                    | `pip install fastapi uvicorn` |

Le service expose :
- `GET /heure`           → `{"heure": "2026-05-26T14:00:00"}`
- `GET /heure/<format>`  → `{"heure": "<format spécifique>"}`

## Comment exécuter

Toutes les paires utilisent le port `8808`. Un seul serveur à la fois.

```
pip install bottle flask fastapi uvicorn

python3 01_stdlib_http.py    # ou 02, 03, 04

# Test :
curl http://127.0.0.1:8808/heure
curl http://127.0.0.1:8808/heure/locale
```

## Comparaison synthétique

| Critère              | stdlib       | Bottle        | Flask         | FastAPI            |
|----------------------|--------------|---------------|---------------|--------------------|
| Lignes utiles        | ~25          | ~10           | ~10           | ~10                |
| Routes par décorateur| Manuelle     | Oui           | Oui           | Oui                |
| Validation des types | Manuelle     | Basique       | Manuelle      | **Pydantic auto**  |
| Génération OpenAPI   | Non          | Plugin        | Plugin        | **Native**         |
| Async natif          | Non          | Non           | Sync (async possible) | **Oui**     |
| Production           | Évitable     | Petit         | Standard      | **Standard moderne** |

**Recommandation 2026** : **FastAPI** pour tout nouveau projet. Flask
si l'équipe a une dette technique. Bottle pour les scripts internes.
stdlib pour démontrer le fonctionnement (jamais en production).

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur les frameworks.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
