# 01 — Parcourir une arborescence

## 1.1 Quatre outils pour quatre besoins

La bibliothèque standard offre **quatre** manières de lister le
contenu d'un dossier. Toutes utilisent en interne le même appel
système (`opendir`/`readdir` sous Unix), mais elles diffèrent par leur
ergonomie et leur récursivité.

| Fonction              | Récursif ? | Type retourné        |
|-----------------------|------------|----------------------|
| `os.listdir(chemin)`  | Non        | `list[str]`          |
| `Path.iterdir()`      | Non        | itérateur de `Path`  |
| `os.walk(racine)`     | Oui        | itérateur de triplets|
| `Path.rglob(motif)`   | Oui        | itérateur de `Path`  |

## 1.2 Lister un seul dossier

### `os.listdir`

```python
import os

for nom in os.listdir("."):
    print(nom)
```

`os.listdir` renvoie **uniquement les noms** (sans le dossier
parent), et **ne descend pas** dans les sous-dossiers. Le résultat
n'est pas trié.

### `Path.iterdir`

```python
from pathlib import Path

for chemin in Path(".").iterdir():
    print(chemin)
```

`iterdir` renvoie des **objets `Path` complets** (préfixés par le
dossier parent). Comme `os.listdir`, il ne descend pas dans les
sous-dossiers.

À retenir : `iterdir` est presque toujours préférable à `os.listdir`
en code moderne, car on obtient directement des `Path` qu'on peut
chaîner (`chemin.is_dir()`, `chemin.suffix`, etc.).

## 1.3 Parcourir récursivement

### `os.walk`

`os.walk` est l'outil **historique** pour parcourir une arborescence
complète. Il *yielde* un **triplet** par dossier visité :

```python
for dirpath, dirnames, filenames in os.walk("/tmp"):
    print(dirpath)
    for d in dirnames:
        print("  sous-dossier :", d)
    for f in filenames:
        print("  fichier      :", f)
```

- `dirpath` : chemin du dossier en cours de visite (chaîne).
- `dirnames` : liste des noms de sous-dossiers présents dans `dirpath`.
- `filenames` : liste des noms de fichiers présents dans `dirpath`.

Détail utile : `dirnames` est une **liste mutable**. Si on la modifie
sur place (par exemple `dirnames.remove(".git")`), `os.walk` ne
descendra **pas** dans les dossiers retirés. C'est la manière
canonique d'élaguer le parcours.

### `Path.rglob`

`rglob` (récursif glob) est l'équivalent moderne, fondé sur les
*patterns* style shell :

```python
from pathlib import Path

for chemin in Path("/tmp").rglob("*"):
    print(chemin)

for fichier_py in Path(".").rglob("*.py"):
    print(fichier_py)
```

`rglob("*")` correspond à tous les fichiers et dossiers, à toute
profondeur. `rglob("*.txt")` filtre directement par extension.

## 1.4 `os.walk` vs `rglob` — quand utiliser quoi ?

| Critère                   | `os.walk`                          | `Path.rglob`                  |
|---------------------------|------------------------------------|-------------------------------|
| Type retourné             | triplets `(str, list, list)`       | `Path`                        |
| Distinction fichier/dossier | implicite (deux listes séparées) | il faut tester (`is_dir()`)   |
| Élagage (skip d'un dossier) | facile (`dirnames.remove(...)`)  | non direct                    |
| Filtrage par motif        | manuel (`if f.endswith(...)`)      | natif (`rglob("*.py")`)       |
| Lisibilité moderne        | moyenne                            | très bonne                    |
| Cas idéal                 | élagage, traitement par dossier    | « tous les `.ext` sous X »    |

Règle de pouce :

- Besoin de **filtrer par extension** ou « tout sous X » :
  `Path.rglob("*.ext")`.
- Besoin de **traiter dossier par dossier**, ou d'**ignorer**
  certains sous-dossiers (`.git`, `__pycache__`, etc.) :
  `os.walk`.

## 1.5 Performance et gros volumes

Pour des arborescences **très** profondes ou très peuplées,
`os.scandir()` est plus rapide que `os.listdir` car il évite un appel
système supplémentaire pour chaque entrée. En pratique, on l'utilise
rarement directement : `os.walk` l'utilise déjà en interne depuis
Python 3.5.

## À retenir

- `os.listdir` et `Path.iterdir` : un seul niveau, sans récursion.
- `os.walk` : récursif, *yielde* `(dirpath, dirnames, filenames)`,
  permet l'élagage en modifiant `dirnames` sur place.
- `Path.rglob(motif)` : récursif, filtrage par motif intégré.
- Préférer `pathlib` (`iterdir`, `rglob`) en code moderne, sauf
  besoin d'élagage qui reste plus simple avec `os.walk`.

## Démo

Exécuter `01_demo_parcourir.py`.
