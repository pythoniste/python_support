# Exercices pratiques — dossier 06_Etat_et_protocole

Huit ateliers sur la conception du protocole.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Tests de `mensualite.py`  ★
*Fichier de référence : mensualite.py*

Écrire `test_mensualite.py` avec **pytest** qui vérifie :

- le cas standard `(200_000, 0.0475, 300) → 1140.23 €` ;
- le cas taux nul `(50_000, 0, 60) → 833.33 €` ;
- les exceptions sur valeurs invalides (durée ≤ 0, capital < 0,
  taux < 0).

**Indices**

- `pytest.approx(1140.23, rel=1e-3)` pour les comparaisons de floats.
- `with pytest.raises(ValueError):` pour tester les exceptions.

---

## Atelier 2 — Validation étendue  ★
*Fichier de référence : 01_stateless_srv.py*

Étendre la validation côté serveur stateless :

- refuser un capital > 100 000 000 (limite arbitraire) ;
- refuser un taux > 0.5 (50% annuel) ;
- refuser une durée > 1200 mois (100 ans).

Retourner `{"erreur": "<message clair>"}` pour chaque cas.

---

## Atelier 3 — Échéancier complet  ★★
*Fichier de référence : mensualite.py*

Ajouter une fonction `calcul_echeancier(capital, taux, duree)` qui
renvoie la **liste détaillée mois par mois** : pour chaque mois, le
montant remboursé en intérêts vs en capital, et le capital restant
dû. Au mois 1, presque tout est intérêts ; au dernier mois, presque
tout est capital.

**Indices**

- Intérêts du mois N = capital restant × taux/12.
- Capital remboursé du mois N = mensualité − intérêts.
- Capital restant = capital précédent − capital remboursé.

---

## Atelier 4 — Endpoint REST `/echeancier`  ★★
*Fichier de référence : 05_rest_srv.py*

Exposer la fonction `calcul_echeancier` via un nouvel endpoint
Bottle :

```
GET /echeancier/<capital:int>/<taux:float>/<duree:int>
```

Retour : `{"echeancier": [{"mois": 1, "interets": ..., "capital_rembourse": ...,
"restant": ...}, ...]}`.

---

## Atelier 5 — Mesure des round-trips  ★★
*Fichiers de référence : paires stateless et stateful*

Écrire un script qui mesure, sur N=100 calculs de mensualité, le
**nombre total de round-trips réseau** consommés par chaque
protocole :

- Stateless : 1 requête + 1 réponse par calcul = 100 round-trips.
- Stateful : 3 envois + 3 réponses + 1 connexion par calcul ≈ 400.
- REST : idem stateless.

Et mesurer le **temps total**.

**Indices**

- Compter et mesurer côté client uniquement.
- `time.perf_counter()` autour de la boucle.

---

## Atelier 6 — Client REST argparse  ★
*Fichier de référence : 06_rest_clt.py*

Modifier le client REST pour accepter capital, taux, durée en
arguments de ligne de commande :

```
python3 atelier_06.py 200000 0.0475 300
    -> mensualité = 1140.23 €
```

**Indices**

- `argparse` avec 3 arguments positionnels.
- Conversion des types directement par argparse.

---

## Atelier 7 — Multi-emprunts en batch  ★★★
*Fichier de référence : 05_rest_srv.py*

Ajouter un endpoint `POST /batch` qui accepte un JSON contenant une
**liste d'emprunts** à calculer et renvoie une liste de résultats :

```
POST /batch
{"demandes": [{"capital": ..., "taux": ..., "duree": ...}, ...]}

réponse :
{"resultats": [{"mensualite": ...}, ...]}
```

**Indices**

- `from bottle import request, route`.
- `request.json` pour accéder au corps POST.
- Endpoint avec `method="POST"`.

---

## Atelier 8 — Cache côté serveur  ★★★
*Fichier de référence : 05_rest_srv.py*

Ajouter un cache simple côté serveur (un dictionnaire indexé par
`(capital, taux, duree)`) qui mémorise les calculs déjà faits.
Ajouter dans la réponse un champ booléen `"cache_hit": true|false`.
Tester en envoyant deux fois la même requête.

**Indices**

- Dictionnaire au niveau module.
- Clé = tuple `(capital, taux, duree)`.
- Le calcul de mensualité est déterministe — le cache est sûr.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le dossier suivant — **`07_Concurrence/`**
— traite la question du multi-client en parallèle, du serveur
itératif jusqu'à `asyncio`.
