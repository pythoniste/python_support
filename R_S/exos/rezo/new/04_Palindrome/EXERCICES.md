# Exercices pratiques — dossier 04_Palindrome

Huit ateliers qui consolident les acquis sur un cas métier unique :
détection de palindrome.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Réponse verbeuse  ★
*Fichier de référence : 01_raw_tcp_srv.py*

Modifier le serveur pour qu'il **inclue le mot reçu** dans sa réponse :
`Le mot 'anna' est un palindrome.\n` au lieu de `PALINDROME\n`.

Adapter `02_raw_tcp_clt.py` en conséquence (la fonction `interpreter`
n'a plus besoin du code, elle imprime directement la réponse).

**Indices**

- f-string côté serveur.
- Plus besoin de la fonction `interpreter` côté client.

---

## Atelier 2 — Validation d'entrée  ★
*Fichier de référence : 01_raw_tcp_srv.py*

Refuser les mots vides ou de longueur > 100 caractères. Réponse
d'erreur : `ERREUR_LONGUEUR\n` ou `ERREUR_VIDE\n`.

**Indices**

- Test après `decode` et avant `est_palindrome`.
- Le client doit ignorer ces erreurs ou les afficher comme telles.

---

## Atelier 3 — Tests unitaires de palindrome.py  ★
*Fichier de référence : palindrome.py*

Écrire un fichier `test_palindrome.py` avec **pytest** qui vérifie :

- Les palindromes simples : `"anna"`, `"kayak"`, `"radar"`.
- Les palindromes avec ponctuation et espaces.
- Les non-palindromes.
- La casse (insensibilité).
- Le cas limite : chaîne vide → palindrome trivialement vrai.

**Indices**

- `def test_xxx():` à la racine du fichier.
- `assert est_palindrome("anna")`.
- Lancer avec `pytest test_palindrome.py`.

---

## Atelier 4 — Endpoint `/reverse`  ★
*Fichier de référence : 09_bottle_palindrome.py*

Ajouter à Bottle un endpoint `GET /reverse/<mot>` qui renvoie le mot
**inversé** (sans nettoyage de la ponctuation) :

```
GET /reverse/anna           -> {"original": "anna", "inverse": "anna"}
GET /reverse/Hello          -> {"original": "Hello", "inverse": "olleH"}
```

**Indices**

- `mot[::-1]` retourne le slice inversé.
- Décorateur `@route("/reverse/<mot>")` supplémentaire.

---

## Atelier 5 — Compteur côté serveur  ★★
*Fichier de référence : 09_bottle_palindrome.py*

Maintenir un compteur global qui suit le nombre de palindromes
détectés et de non-palindromes. Exposer ces statistiques via un
nouvel endpoint :

```
GET /stats  ->  {"palindromes": 42, "non_palindromes": 17, "total": 59}
```

**Indices**

- Variables au niveau module ou dans un dict.
- Le compteur s'incrémente à chaque appel de `/palindrome/<mot>`.

---

## Atelier 6 — Client argparse  ★★
*Fichier de référence : 10_bottle_clt.py*

Modifier le client Bottle pour accepter le mot à tester en argument
de ligne de commande :

```
python3 atelier_06.py anna
    -> Le mot 'anna' est un palindrome.

python3 atelier_06.py "Karine alla en Irak"
    -> Le mot 'Karine alla en Irak' est un palindrome.
```

**Indices**

- `argparse.ArgumentParser`.
- `argument` positionnel `mot`.
- URL-encoder le mot (`requests` le fait automatiquement via
  `params=` ou `urllib.parse.quote`).

---

## Atelier 7 — Client universel  ★★★
*Tous les serveurs du dossier sont compatibles*

Écrire un **client universel** qui choisit son transport selon un
argument `--protocole {tcp,udp,bottle}` :

```
python3 atelier_07.py anna --protocole tcp
python3 atelier_07.py anna --protocole udp
python3 atelier_07.py anna --protocole bottle
```

Le mot et la réponse interprétée doivent être identiques quel que
soit le protocole.

**Indices**

- `argparse` avec `choices`.
- Trois fonctions séparées `via_tcp`, `via_udp`, `via_bottle`.
- Dispatching via un dictionnaire de fonctions ou un `match`.

---

## Atelier 8 — Test d'intégration automatisé  ★★★
*Tout le dossier*

Écrire un script `test_integration.py` qui :

1. Démarre **dans un thread** le serveur `05_ss_tcp_srv.py`
   (`socketserver.TCPServer` + `serve_forever`).
2. Envoie quelques mots de test via un client TCP.
3. Vérifie que les réponses correspondent à `est_palindrome`.
4. Arrête proprement le serveur (`server.shutdown()` depuis le
   thread principal — c'est légal ici parce que `serve_forever` est
   dans un autre thread).

**Indices**

- `import threading; threading.Thread(target=serveur.serve_forever).start()`
- Ce serveur tournera dans un thread daemon — il s'arrête avec le
  processus principal.
- Comparaison `assert reponse == "PALINDROME" if est_palindrome(mot)
  else "PAS_PALINDROME"`.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le dossier suivant — **`05_Sérialisation/`**
— reprend les bases du module 00/06 (boutisme) et les met en pratique
sur un service distinct (génération de nombres aléatoires), avec
plusieurs stratégies d'encodage côte à côte.
