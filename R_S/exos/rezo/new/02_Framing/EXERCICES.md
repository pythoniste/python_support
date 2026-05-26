# Exercices pratiques — dossier 02_Framing

Huit ateliers pour consolider les trois stratégies de framing.

Chaque atelier indique :

- le ou les fichiers de référence ;
- une difficulté de ★ à ★★★ ;
- des indices pour démarrer.

Les corrigés sont dans `CORRIGES/`.

---

## Atelier 1 — Echo à délimiteur  ★
*Fichier de référence : 01_delimiteur_srv.py*

Transformer le serveur en pur echo : renvoyer exactement le message
reçu (suivi du délimiteur `\n`), sauf pour `stop` qui doit toujours
arrêter le serveur.

**Indices**
- Une seule ligne à changer dans `traiter_client`.
- Penser à conserver le `\n` en queue de réponse pour que le client
  puisse lire avec `recv_ligne`.

---

## Atelier 2 — Délimiteur configurable  ★
*Fichiers de référence : 01_delimiteur_srv.py + 02_delimiteur_clt.py*

Modifier la paire pour utiliser `b"|"` (pipe) comme délimiteur au
lieu de `b"\n"`. Vérifier que tout fonctionne identiquement.

**Indices**
- `recv_ligne` a déjà un paramètre `delimiteur`.
- Côté envoi, remplacer le suffixe `b"\n"` par `b"|"` à chaque
  `sendall`.

---

## Atelier 3 — Limite anti-DoS  ★★
*Fichier de référence : aux_framing.py (fonction recv_ligne)*

Ajouter à `recv_ligne` un paramètre `taille_max` (entier, défaut
8192) : si on atteint cette taille sans avoir vu le délimiteur,
lever `ValueError`. Cela protège contre un client malveillant qui
n'envoie jamais de délimiteur et fait gonfler la mémoire du serveur.

**Indices**
- Compter au fur et à mesure.
- Tester avec un client qui n'envoie pas le délimiteur (par exemple
  `client.sendall(b"x" * 10000)` puis `time.sleep(60)`).

---

## Atelier 4 — Multi-champs typés  ★★
*Fichiers de référence : 03_prefixe_srv.py + 04_prefixe_clt.py*

Modifier la paire pour que le client envoie **trois valeurs à la
fois** : `(nom: bytes, age: uint8, taille_cm: uint16)`. Le serveur
les désérialise et répond
`b"Bonjour <nom>, <age> ans, <taille> cm."`.

**Indices**
- Format de message complet :
  `[longueur_nom u32][nom bytes][age u8][taille u16]`
- `struct.pack("!IBH", len(nom), age, taille)` pour la partie fixe.
- Côté serveur : lire les 4 octets de longueur du nom, puis le nom,
  puis 3 octets pour age + taille.

---

## Atelier 5 — `recv_ligne` bufferisé  ★★★
*Fichier de référence : aux_framing.py*

Écrire une **classe** `LecteurBufferise` qui encapsule un socket et
fournit `lire_ligne(delim)` en lisant par blocs de 4096 octets dans
un buffer interne. Comparer avec la version naïve en mesurant le
temps de lecture de 1000 lignes courtes.

**Indices**
- L'attribut `_buffer: bytes` accumule ce qui n'a pas encore été
  consommé.
- `lire_ligne` : chercher le délimiteur dans `_buffer` ; s'il n'y
  est pas, faire un `recv(4096)` et concaténer ; recommencer.
- `time.perf_counter()` autour des deux boucles de 1000 itérations.

---

## Atelier 6 — Adapter le client du dossier 01  ★★
*Fichier de référence : 01_Sockets_bas_niveau/02_tcpclt.py*

Reprendre `02_tcpclt.py` du dossier 01 et lui ajouter un **framing
explicite par délimiteur**. Vérifier qu'il interopère correctement
avec `01_delimiteur_srv.py` du dossier courant.

**Indices**
- Ajouter `b"\n"` après chaque `sendall`.
- Remplacer `recv(BUFFER_SIZE)` par `recv_ligne(client)`.
- Vérifier que le `stop` final déclenche encore l'arrêt du serveur.

---

## Atelier 7 — Mesure de débit  ★★
*Fichier de référence : une des trois paires de ce dossier*

Choisir **une** stratégie de framing et écrire un script qui mesure
le débit en messages par seconde sur 1000 échanges client-serveur
courts (message = 10 octets). Comparer mentalement avec ce qu'on
imagine pour les autres stratégies.

**Indices**
- `time.perf_counter()` autour de la boucle.
- Mêmes machine et message pour la comparaison.
- Question à poser : qu'est-ce qui domine, le CPU ou le réseau ?

---

## Atelier 8 — Calculatrice binaire  ★★★
*À écrire de zéro à partir de 03_prefixe_srv.py + 04_prefixe_clt.py*

Définir un protocole **binaire fixe** (sans délimiteur, sans préfixe
de longueur, juste une trame de taille constante) :

- requête : `[opcode u8][a i32][b i32]` (9 octets)
- réponse : `[succès u8][résultat i64]` (9 octets)

Opcodes : `0 = add`, `1 = sub`, `2 = mul`, `3 = div` (entière). En
cas de division par zéro : `succès = 0`, `résultat = 0`.

Implémenter client et serveur.

**Indices**
- `struct.pack("!Bii", opcode, a, b)` côté client.
- `struct.unpack("!Bii", ...)` côté serveur.
- `recv_exactement(sock, 9)` pour lire la trame.

---

## Pour aller plus loin

Une fois ces ateliers terminés, le dossier suivant — **`03_Socketserver/`**
— montre comment Python encapsule tout cela dans un framework de plus
haut niveau (`socketserver.StreamRequestHandler`).
