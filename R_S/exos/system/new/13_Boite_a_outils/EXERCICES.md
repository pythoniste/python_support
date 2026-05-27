# Exercices pratiques — dossier 13_Boite_a_outils

Une fois les cinq fiches lues et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** chacun des modules dans
des scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après** avoir
tenté chaque atelier. Chaque corrigé crée lui-même son contenu de test
dans un `tempfile.TemporaryDirectory()` : on peut donc tous les exécuter
tels quels, sans rien préparer.

---

## Atelier 1 — Empreinte SHA-256 d'un fichier  ★
*Module 03 — hashlib + tempfile*

Écrire un script `atelier_01.py` qui crée un fichier dans un dossier
temporaire (par exemple 100 Kio de texte généré), calcule son empreinte
**SHA-256** en lisant **par blocs de 4096 octets**, et affiche le
résultat.

**Indices**

- `tempfile.TemporaryDirectory()` pour le dossier de travail.
- Boucle `while True: bloc = f.read(4096); if not bloc: break`.
- `h = hashlib.sha256()` ; `h.update(bloc)` ; `h.hexdigest()`.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py
fichier : echantillon.txt ( 102400 octets )
sha256  : 9b74c9897bac770ffc029102a200c5de...e7f2
```

---

## Atelier 2 — Accueil adapté à l'OS  ★
*Module 02 — platform*

Écrire un script `atelier_02.py` qui détecte le système d'exploitation
via `platform.system()` et affiche un message d'accueil **différent**
selon le cas (Linux, macOS, Windows, autre). Le script doit aussi
indiquer l'architecture (`platform.machine()`) et la version de Python.

**Indices**

- `if / elif / else` sur `platform.system()`.
- Attention : macOS s'appelle `"Darwin"` côté noyau, **pas** `"macOS"`.
- `platform.python_version()` renvoie déjà la version courte.

**Exemple de sortie attendue (sous Linux x86_64)**

```
$ python3 atelier_02.py
Bonjour ! Detecte Linux (x86_64), Python 3.12.3.
On est sur un Unix-like : les chemins de config vont sous /etc.
```

---

## Atelier 3 — Token URL-safe dans un `.env` temporaire  ★★
*Module 04 + 01 — secrets + tempfile*

Écrire un script `atelier_03.py` qui :

1. génère un token URL-safe de **32 octets** avec `secrets.token_urlsafe`,
2. l'écrit dans un fichier `.env` placé dans un dossier temporaire,
   sous la forme `TOKEN=...`,
3. **relit** le fichier, extrait la valeur du token, et vérifie avec
   `secrets.compare_digest` qu'on retrouve bien le token initial.

**Indices**

- `secrets.token_urlsafe(32)` renvoie une `str` ASCII.
- Format `.env` minimaliste : une ligne `CLE=VALEUR` par variable.
- Pour parser : `cle, _, valeur = ligne.partition("=")`.
- Comparer avec `secrets.compare_digest`, **pas** `==`.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
fichier .env : /tmp/.../.env
contenu     : TOKEN=...
lu          : ...
identique   : True
```

---

## Atelier 4 — Signer et vérifier avec HMAC-SHA256  ★★
*Module 04 — hmac*

Écrire un script `atelier_04.py` qui prend **deux arguments** :

- `sys.argv[1]` : la **clé secrète** (chaîne quelconque),
- `sys.argv[2]` : le **message** à signer (chaîne quelconque).

Le script affiche la signature HMAC-SHA256 du message, puis simule un
récepteur qui recalcule la signature et la compare avec
`hmac.compare_digest`. Le script doit également démontrer la
**détection** : si on modifie un caractère du message, la vérification
doit échouer.

**Indices**

- Encoder la clé et le message en `bytes` avec `.encode("utf-8")` avant
  de les passer à `hmac.new`.
- `hmac.new(cle, message, hashlib.sha256).hexdigest()`.
- Pour la falsification : `message + " (modifie)"` suffit.
- Si aucun argument n'est passé, le script doit fonctionner avec des
  valeurs par défaut pour rester exécutable tel quel.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py macle "transfert:100"
message   : transfert:100
signature : 3b7a...c9
verification du meme message      : OK
verification d'un message modifie : KO (detection reussie)
```

---

## Atelier 5 — Aller-retour base64 sur un blob aléatoire  ★★★
*Module 05 + 04 — base64 + secrets*

Écrire un script `atelier_05.py` qui :

1. génère un **blob binaire** de 100 octets aléatoires avec
   `secrets.token_bytes(100)`,
2. l'**encode** en base64 standard et en base64 URL-safe,
3. **décode** les deux versions et vérifie que les deux octets décodés
   sont **strictement identiques** au blob d'origine,
4. produit aussi son **SHA-256** avant encodage et après décodage pour
   un contrôle d'intégrité supplémentaire.

**Indices**

- `base64.b64encode` / `base64.b64decode` pour la version standard.
- `base64.urlsafe_b64encode` / `urlsafe_b64decode` pour la version URL.
- `hashlib.sha256(octets).hexdigest()` calcule l'empreinte d'un blob en
  mémoire (pas besoin de fichier ici).
- Afficher les premiers caractères des encodages pour observer la
  différence visuelle entre standard et URL-safe.

**Exemple de sortie attendue**

```
$ python3 atelier_05.py
blob (100 octets) sha256 : c4d2...
b64 standard (extrait)   : tQq3+Z/aB8...
b64 url-safe (extrait)   : tQq3-Z_aB8...
decodage standard identique : True
decodage urlsafe identique  : True
sha256 apres aller-retour   : c4d2... (identique)
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on peut combiner les briques : un
script qui signe un fichier (HMAC sur son contenu), encode la signature
en base64 et écrit le tout dans un `.env` temporaire — c'est très
proche de ce que font les services qui distribuent des artefacts
signés.
