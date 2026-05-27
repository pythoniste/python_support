# Exercices pratiques — dossier 09_Environnement

Une fois les trois modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** la lecture de
configuration. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard, sur Python 3.11 ou plus récent.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Explorer son environnement  ★
*Module 01 — `os.environ`*

Écrire un script `atelier_01.py` qui affiche :

- la valeur de `HOME` ;
- la valeur de `USER` ;
- la valeur de `PATH` ;
- le **nombre d'entrées** que contient `PATH` (séparées par `os.pathsep`,
  généralement `:` sous Unix et `;` sous Windows).

**Indices**

- `os.environ.get("HOME", "<absente>")` évite la `KeyError`.
- `os.pathsep` est le séparateur correct selon la plateforme.
- `PATH.split(os.pathsep)` renvoie une liste.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py
HOME : /home/ada
USER : ada
PATH : /usr/local/bin:/usr/bin:/bin
PATH contient 3 entrée(s).
```

---

## Atelier 2 — Lire un INI à deux sections  ★★
*Module 02 — `configparser`*

Écrire un script `atelier_02.py` qui :

1. crée dans un `tempfile.TemporaryDirectory()` un fichier `app.ini`
   contenant **deux sections** `[database]` et `[server]` avec au
   minimum les clés suivantes :
   - `[database]` : `host` (str), `port` (int), `ssl` (bool) ;
   - `[server]`   : `bind` (str), `workers` (int).
2. lit ce fichier avec `configparser` ;
3. affiche chaque section sous la forme suivante :

```
[database]
  host = localhost
  port = 5432 (int)
  ssl = True (bool)
[server]
  bind = 0.0.0.0
  workers = 4 (int)
```

**Indices**

- `tempfile.TemporaryDirectory()` s'utilise dans un `with`.
- `pathlib.Path(...).write_text(...)` écrit le fichier d'un coup.
- `getint`, `getboolean` renvoient des types natifs.

---

## Atelier 3 — Extraire un nom depuis pyproject.toml  ★★
*Module 03 — `tomllib`*

Écrire un script `atelier_03.py` qui :

1. crée dans un dossier temporaire un fichier `pyproject.toml`
   **minimal** contenant au moins :

   ```toml
   [project]
   name = "demo-paquet"
   version = "0.1.0"
   ```

2. ouvre ce fichier en **mode binaire** ;
3. lit avec `tomllib.load(f)` ;
4. affiche le nom et la version du projet.

**Indices**

- `open(chemin, "rb")` est **obligatoire** pour `tomllib.load`.
- Le résultat est un `dict` ordinaire : `data["project"]["name"]`.
- Vérifier au début que `sys.version_info >= (3, 11)`.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
Nom     : demo-paquet
Version : 0.1.0
```

---

## Atelier 4 — Résolution selon CLI > env > défaut  ★★★
*Module 03 — ordre des sources de configuration*

Écrire un script `atelier_04.py` qui détermine un numéro de **port**
en respectant l'ordre de priorité **CLI > env > défaut** :

1. valeur par défaut : `8080` ;
2. si la variable d'environnement `APP_PORT` est définie, elle
   l'emporte sur le défaut ;
3. si la ligne de commande contient `--port N`, elle l'emporte sur
   tout le reste.

Le script doit afficher la valeur finale **et** la source d'où elle
provient (`défaut`, `env` ou `cli`).

**Indices**

- `argparse.ArgumentParser` avec `add_argument("--port", type=int)`.
- `os.environ.get("APP_PORT")` renvoie `None` si la variable manque.
- Toujours convertir en `int` à l'arrivée.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py
Port : 8080 (source : défaut)

$ APP_PORT=9000 python3 atelier_04.py
Port : 9000 (source : env)

$ APP_PORT=9000 python3 atelier_04.py --port 7777
Port : 7777 (source : cli)
```

---

## Atelier 5 — Convertir un INI en JSON  ★★
*Modules 02 + 03 — `configparser` et `json`*

Écrire un script `atelier_05.py` qui :

1. crée dans un dossier temporaire un fichier `app.ini` avec au moins
   deux sections ;
2. lit ce fichier avec `configparser` ;
3. construit un dictionnaire Python `{ section: { clé: valeur, ... }, ... }` ;
4. l'**affiche** au format JSON indenté sur stdout.

**Indices**

- `json.dumps(d, indent=2)` produit une chaîne lisible.
- Les valeurs sont des **chaînes** : on ne convertit pas pour cet atelier
  (l'objectif est la structure, pas les types).
- `config.sections()` et `config[sec].items()` suffisent.

**Exemple de sortie attendue**

```
{
  "database": {
    "host": "localhost",
    "port": "5432"
  },
  "server": {
    "bind": "0.0.0.0",
    "workers": "4"
  }
}
```

**Bonus** : préciser dans la sortie le type natif quand la clé porte
un nom évocateur (`port` → `int`, `ssl` → `bool`). Attention à la
sémantique : un INI ne déclare pas ses types, on les devine.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on est capable d'écrire un script qui
lit sa configuration depuis plusieurs sources, dans le bon ordre, sans
dépendance externe. Étape suivante : produire des **journaux** propres
pour observer ces choix au runtime — voir le dossier `10_Logging`.
