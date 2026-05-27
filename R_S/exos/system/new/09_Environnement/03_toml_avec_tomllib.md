# 03 — Fichiers TOML avec `tomllib`

## 3.1 Pourquoi TOML ?

**TOML** (*Tom's Obvious, Minimal Language*) est un format de
configuration moderne, conçu pour rester lisible tout en supportant
des **types riches** : entiers, flottants, booléens, dates, listes,
tables imbriquées. Il a été adopté par l'écosystème Python comme
format officiel pour `pyproject.toml`, le fichier qui décrit un
paquet Python.

Exemple typique :

```toml
[project]
name = "mon-paquet"
version = "1.0.0"
requires-python = ">=3.11"

[project.dependencies]
requests = "^2.31"
```

À comparer à INI : on garde les sections `[...]`, mais on peut écrire
`port = 5432` (un vrai entier) ou `tags = ["web", "api"]` (une vraie
liste).

## 3.2 `tomllib` : Python 3.11 et plus

Depuis **Python 3.11**, la bibliothèque standard inclut `tomllib`. Sur
les versions antérieures (3.10 et avant), il faut un paquet externe
(`tomli`). Vérifier sa version avant tout :

```
$ python3 --version
Python 3.11.x
```

## 3.3 Lire un fichier TOML

Une particularité importante : `tomllib.load` exige que le fichier soit
ouvert en **mode binaire** (`"rb"`), pas en texte. La raison : TOML
impose UTF-8 et `tomllib` veut contrôler le décodage lui-même.

```python
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

print(data["project"]["name"])           # "mon-paquet" (str)
print(data["project"]["version"])        # "1.0.0"      (str)
```

Le résultat `data` est un **dictionnaire Python** ordinaire, avec des
types Python natifs aux feuilles (`int`, `float`, `bool`, `str`,
`list`, `dict`, `datetime.datetime`...). Pas besoin de convertisseurs
manuels comme `getint`.

Pour lire depuis une chaîne déjà en mémoire :

```python
contenu = 'port = 8080\nname = "demo"\n'
data = tomllib.loads(contenu)
print(data["port"])   # 8080 (int)
```

## 3.4 Écriture : non couvert par `tomllib`

`tomllib` est **en lecture seule**. Il n'y a pas (encore) de
`tomllib.dump` dans la bibliothèque standard. Pour produire du TOML,
il faut un paquet externe (par exemple `tomli-w` ou `tomlkit`). En
général, ce n'est pas un problème : les fichiers de configuration
sont écrits à la main, pas générés.

## À retenir

- `tomllib` est dans la stdlib **depuis Python 3.11**.
- Ouvrir le fichier en **mode binaire** : `open(path, "rb")`.
- `tomllib.load(f)` renvoie un `dict` aux types Python natifs.
- Le format est utilisé par `pyproject.toml`.
- Lecture uniquement — pour écrire, paquet externe.

## 3.6 Ordre des sources de configuration

Un programme un peu sérieux lit sa configuration depuis **plusieurs
sources** à la fois : un fichier, l'environnement, parfois la ligne de
commande, et toujours des valeurs par défaut intégrées au code. Que
fait-on quand deux sources donnent une valeur différente pour la même
option ?

L'ordre de priorité conventionnel, du **plus prioritaire** au **moins
prioritaire** :

```
CLI  >  variable d'environnement  >  fichier de configuration  >  défaut
```

Pourquoi cet ordre ?

1. **CLI gagne toujours.** L'utilisateur qui tape une option sur la
   ligne de commande exprime une intention immédiate et explicite. Si
   `--port 9000` ne l'emportait pas sur le fichier, l'option serait
   trompeuse.
2. **L'environnement passe avant le fichier.** Une variable
   d'environnement est définie par la session (ou par l'orchestrateur,
   en production : Docker, systemd, CI). Elle reflète le contexte
   d'exécution, qui doit pouvoir surcharger un fichier embarqué.
3. **Le fichier passe avant le défaut.** Un fichier de configuration
   est un choix conscient de l'opérateur ; les défauts sont là pour
   que le programme démarre sans aucune configuration.

En pratique, on lit ces sources dans l'**ordre inverse** (du moins
prioritaire au plus prioritaire) en écrasant à chaque étape :

```python
config = {"port": 8080}                              # défaut
config.update(lire_fichier())                        # fichier
if "PORT" in os.environ:
    config["port"] = int(os.environ["PORT"])         # env
if args.port is not None:
    config["port"] = args.port                       # CLI
```

L'atelier 4 de ce dossier met ce motif en application.

## Démo

Exécuter `03_demo_toml.py`.
