# Exercices pratiques — dossier 05_Serialisation

Huit ateliers explorant les choix d'encodage en pratique.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Tests de `encodage.py`  ★
*Fichier de référence : encodage.py*

Écrire `test_encodage.py` avec **pytest** qui vérifie que chaque
couple `pack_*` / `unpack_*` est symétrique (`unpack(pack(n)) == n`)
sur quelques valeurs : `0`, `1`, `42`, `255`, `65535`, `2**32-1`.

**Indices**

- Trois fonctions de test, une par stratégie.
- `pytest.mark.parametrize` pour itérer sur les valeurs.

---

## Atelier 2 — Mesure de taille  ★
*Fichier de référence : encodage.py*

Écrire un script qui simule **1000 tirages** avec `max=42` et calcule,
pour chacun des trois encodages, le **nombre total d'octets**
émis + reçus sur le réseau. Comparer avec une règle de trois sur la
taille du payload « 42 ».

**Indices**

- `len(pack_texte(42))`, etc.
- Ne pas exécuter de réseau — c'est de l'arithmétique pure.

---

## Atelier 3 — Encodage des floats  ★★
*Fichier de référence : encodage.py*

Ajouter au module `encodage.py` trois couples
`pack_float_*` / `unpack_float_*` (texte, binaire, JSON) pour les
nombres flottants. Tester avec `3.14`, `-0.5`, `1e10`.

**Indices**

- Texte : `str(f)` puis `float()`.
- Binaire : `struct.pack("!d", f)` (double 8 octets).
- JSON : déjà supporté nativement — `json.dumps({"valeur": 3.14})`.

---

## Atelier 4 — JSON multi-champs  ★★
*Fichiers de référence : 05_json_srv.py + 06_json_clt.py*

Étendre le service JSON pour que le client envoie deux champs en
une requête (`{"max": 42, "tirages": 5}`) et reçoive une **liste**
de tirages (`{"resultats": [3, 17, 22, 8, 41]}`).

**Indices**

- Côté serveur, lire les deux champs puis générer la liste.
- Côté client, itérer sur la liste reçue.
- Comparer la quantité d'échanges réseau avec la version "un tirage =
  un échange" : un seul aller-retour vs `N`.

---

## Atelier 5 — Validation côté serveur  ★
*Fichier de référence : 03_binaire_srv.py*

Le serveur binaire reçoit un `uint32`. Si un client triché envoie
0xFFFFFFFF (= 4 294 967 295), `random.randint(0, max)` peut être
très lent. Refuser les `max > 1 000 000` en renvoyant la valeur
spéciale `0xFFFFFFFF` comme code d'erreur.

**Indices**

- Test simple `if max_value > 1_000_000:`.
- Documenter la convention de la valeur d'erreur dans le code.

---

## Atelier 6 — Mesure de débit  ★★
*Fichiers de référence : les trois paires*

Mesurer le **temps total** pour 10 000 tirages avec chacune des trois
paires. Tabuler : nombre d'octets par tirage, temps total,
tirages/seconde, octets/seconde.

**Indices**

- `time.perf_counter()` autour de la boucle de 10 000 tirages.
- Lancer le serveur correspondant entre chaque mesure.
- Sur localhost, le CPU domine ; sur un vrai réseau, la taille de
  payload dominerait — bonne occasion d'en discuter.

---

## Atelier 7 — Compression gzip  ★★
*Fichier de référence : encodage.py*

Ajouter une **quatrième stratégie** : JSON compressé avec gzip.
Mesurer la taille pour quelques valeurs (42, 1234567890, une chaîne
de 1000 caractères) ; conclure sur quand la compression vaut son
surcoût CPU.

**Indices**

- `import gzip; gzip.compress(b"...")` / `gzip.decompress(b"...")`.
- Préfixer la trame par sa longueur (4 octets) pour faciliter le
  framing — sans cela, le délimiteur `\n` pourrait apparaître dans
  le flux compressé.

---

## Atelier 8 — Binaire à préfixe de longueur  ★★
*Fichier de référence : encodage.py*

Le binaire fixed-size de 4 octets limite à `2³² − 1`. Implémenter un
encodage binaire **à préfixe de longueur** :

```
[longueur u8][octets entier en big-endian]
```

Cela permet de transporter des entiers arbitrairement grands.

**Indices**

- Côté pack : encoder l'entier avec `(n.bit_length() + 7) // 8`
  octets, préfixer par cette taille sur 1 octet.
- Côté unpack : lire 1 octet → taille → `recv_exactement(sock,
  taille)` → `int.from_bytes(..., "big")`.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le dossier suivant — **`06_Etat_et_protocole/`**
— reprend le service de calcul de mensualité (du repo original
06_Mensualité) avec un protocole **à plusieurs champs** et un état
serveur persistant entre requêtes.
