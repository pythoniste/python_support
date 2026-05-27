# 02 — Fichiers INI avec `configparser`

## 2.1 Le format INI

Un fichier INI est un fichier texte structuré en **sections**, chacune
contenant des paires **`clé = valeur`**. C'est le format de
configuration le plus ancien encore en usage aujourd'hui :

```ini
[database]
host = localhost
port = 5432
ssl  = true

[server]
bind = 0.0.0.0
workers = 4
```

Il est lisible à l'œil nu, facile à éditer à la main, et compris par
de nombreux outils (`systemd`, `pip`, anciens fichiers Windows).
Limite : pas de listes ni de structures imbriquées — c'est plat,
deux niveaux maximum (section, clé).

## 2.2 Lire un fichier INI

La bibliothèque standard expose le module `configparser` :

```python
import configparser

config = configparser.ConfigParser()
config.read("app.ini")

print(config["database"]["host"])   # "localhost" (toujours une str)
print(config["server"]["bind"])     # "0.0.0.0"
```

`config.read(chemin)` est **silencieux** si le fichier est absent : il
renvoie la liste des fichiers effectivement lus. À tester soi-même
quand un défaut est important.

Toutes les valeurs lues sont des **chaînes de caractères**, même
`port = 5432`. Pour récupérer des types Python natifs, on utilise les
accesseurs typés :

| Méthode                         | Renvoie       |
|---------------------------------|---------------|
| `config.getint("s", "k")`       | `int`         |
| `config.getfloat("s", "k")`     | `float`       |
| `config.getboolean("s", "k")`   | `bool`        |

```python
port    = config.getint("database", "port")     # 5432  (int)
ssl_on  = config.getboolean("database", "ssl")  # True  (bool)
```

`getboolean` reconnaît `yes`/`no`, `true`/`false`, `on`/`off`,
`1`/`0` (insensible à la casse). C'est plus permissif qu'un simple
`bool("true")` qui renverrait toujours `True`.

## 2.3 Parcourir les sections

`config.sections()` renvoie la liste des sections, et chaque section
se comporte comme un dictionnaire :

```python
for nom_section in config.sections():
    print(f"[{nom_section}]")
    for cle, valeur in config[nom_section].items():
        print(f"  {cle} = {valeur}")
```

Une section spéciale `[DEFAULT]` peut être déclarée en tête de fichier :
ses clés servent de **valeurs par défaut** pour toutes les autres
sections.

## 2.4 Écrire un fichier INI

`configparser` peut aussi **produire** du INI. On manipule l'objet
comme un dict imbriqué, puis on l'écrit dans un fichier texte :

```python
config = configparser.ConfigParser()
config["database"] = {"host": "localhost", "port": "5432"}
config["server"]   = {"bind": "0.0.0.0", "workers": "4"}

with open("app.ini", "w", encoding="utf-8") as f:
    config.write(f)
```

Note : on écrit les valeurs sous forme de chaînes (`"5432"`, pas `5432`).
`configparser` exige des `str` à l'écriture.

## À retenir

- Format plat à deux niveaux : `[section]` puis `clé = valeur`.
- `config.read(chemin)` est silencieux si le fichier manque.
- Toutes les valeurs lues sont des chaînes : utiliser `getint`,
  `getfloat`, `getboolean` pour les autres types.
- Une section `[DEFAULT]` propage ses clés à toutes les autres.
- L'écriture se fait via `config.write(fichier_texte)`.

## Démo

Exécuter `02_demo_ini.py`.
