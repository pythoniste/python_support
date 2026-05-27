# 09_HTTP_client — Quatre clients HTTP en Python

Symétrique du dossier 08. On compare quatre façons d'**appeler** un
service HTTP depuis Python — du bas niveau stdlib jusqu'à l'async
moderne.

## Plan

| Fichier             | Bibliothèque             | Mode             |
|---------------------|--------------------------|------------------|
| `01_urllib.py`      | `urllib.request` (stdlib)| Sync, bas niveau |
| `02_http_client.py` | `http.client` (stdlib)   | Sync, encore plus bas |
| `03_requests_basic.py` | `requests`            | Sync, idiomatique |
| `04_requests_advanced.py` | `requests` (Session, auth, retries) | Sync |
| `05_httpx_sync.py`  | `httpx` sync             | Sync             |
| `06_httpx_async.py` | `httpx` async            | Async (coroutines) |

Tous ces clients interrogent un serveur public — par défaut
`https://httpbin.org/get` (un service qui renvoie la requête reçue).

## Comment exécuter

```
pip install requests httpx       # déjà présent sur la plupart des envs

python3 01_urllib.py
python3 03_requests_basic.py
python3 06_httpx_async.py
```

Pas besoin de lancer de serveur local — chaque script frappe une
URL publique (avec un fallback `httpbin.org` si la connectivité
fonctionne).

## Comparaison synthétique

| Critère                  | urllib    | http.client | requests       | httpx           |
|--------------------------|-----------|-------------|----------------|-----------------|
| Verbosité (lignes utiles)| 5         | 10          | **2**          | 2               |
| Sessions, cookies, retries | Manuel  | Manuel      | **Excellent**  | Excellent       |
| Sync                     | Oui       | Oui         | Oui            | Oui             |
| Async                    | Non       | Non         | Non            | **Oui**         |
| Standard 2026            |           |             | Sync           | **Sync + Async**|

**Recommandation** : **requests** pour le code synchrone simple.
**httpx** dès qu'il y a de l'async ou si on veut un client unique.
Les deux APIs sont quasi identiques — `httpx` est compatible
drop-in.

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur les clients HTTP.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
