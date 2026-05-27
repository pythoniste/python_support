# Exercices pratiques — dossier 10_REST

Six ateliers pour pratiquer la conception REST.

---

## Atelier 1 — Filtrage et tri  ★
*Fichier de référence : 01_crud_stdlib.py ou 02_crud_fastapi.py*

Ajouter à `GET /todos` deux paramètres optionnels :
- `?fait=true` ou `?fait=false` : filtrer sur l'état ;
- `?tri=titre` : trier par titre alphabétique.

---

## Atelier 2 — Endpoint PATCH  ★★
*Fichier de référence : 02_crud_fastapi.py*

Ajouter `PATCH /todos/{id}` qui modifie partiellement un TODO (par
exemple ne changer que le champ `fait` sans toucher au `titre`).

**Indices** : Pydantic `TodoPatch` avec tous les champs optionnels
(`Optional[str] = None`).

---

## Atelier 3 — HATEOAS  ★★
*Fichier de référence : 02_crud_fastapi.py*

Ajouter à chaque réponse une section `_links` avec les actions
possibles :

```json
{"id": 1, "titre": "...",
 "_links": {"self": "/todos/1", "delete": "/todos/1", "modifier": "/todos/1"}}
```

HATEOAS = Hypermedia As The Engine Of Application State, la
contrainte la moins respectée de REST mais très utile en pratique.

---

## Atelier 4 — Pagination cursor-based  ★★★
*Fichier de référence : 04_pagination.py*

Implémenter une pagination par **curseur** : `?cursor=<dernier_id>`.
Le serveur renvoie 20 livres après ce curseur, plus un `prochain_cursor`.

**Avantages** : stable même si on insère/supprime des livres pendant
le parcours.

---

## Atelier 5 — Client testant tous les codes  ★★
*Fichiers de référence : 02_crud_fastapi.py + 05_erreurs.py*

Écrire un client `requests` qui :
1. POST un TODO → vérifier 201.
2. GET le TODO → vérifier 200.
3. POST le même → vérifier 409 (duplicata).
4. GET un id inexistant → vérifier 404.
5. POST avec JSON invalide → vérifier 422.
6. DELETE le TODO → vérifier 204.

---

## Atelier 6 — Migration v1 → v2  ★★★
*Fichier de référence : 03_versioning.py*

Étendre l'exemple v1/v2 avec un mécanisme de **deprecation** :
v1 répond avec l'en-tête `Deprecation: true` et `Sunset: <date>`.
Le client peut détecter et alerter. Ajouter aussi un endpoint v3
qui n'existe pas encore (404).
