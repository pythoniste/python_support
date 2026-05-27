# 03 — Renommer, supprimer, ajuster les droits

Cette fiche regroupe les opérations atomiques sur **une** entrée du
système de fichiers : la renommer, la supprimer, en créer une, ou
modifier ses droits Unix.

## 3.1 Renommer

### `os.rename`

```python
import os

os.rename("ancien.txt", "nouveau.txt")
os.rename("/tmp/a", "/tmp/b")
```

Renomme ou déplace un fichier ou un dossier. C'est une opération
**atomique** tant que source et destination sont sur le **même
système de fichiers**.

Attention : si la destination existe déjà, le comportement dépend du
système (sur Linux, le fichier cible est **silencieusement écrasé**
pour un fichier — pas pour un dossier non vide).

### `Path.rename`

L'équivalent `pathlib`, qui renvoie le nouveau `Path` :

```python
from pathlib import Path

ancien = Path("ancien.txt")
nouveau = ancien.rename("nouveau.txt")
print(nouveau)  # nouveau.txt
```

Pour un renommage qui **refuse** d'écraser, utiliser `Path.replace()`
n'aide pas (il écrase aussi). La protection se fait à la main :

```python
cible = Path("nouveau.txt")
if cible.exists():
    raise FileExistsError(cible)
ancien.rename(cible)
```

## 3.2 Supprimer un fichier

### `os.remove` et `os.unlink`

```python
import os

os.remove("a_jeter.txt")
os.unlink("a_jeter.txt")     # synonyme exact
```

Les deux fonctions sont **strictement identiques**. `remove` est plus
lisible côté Python, `unlink` reflète l'appel système Unix sous-jacent.

### `Path.unlink`

```python
from pathlib import Path

Path("a_jeter.txt").unlink()
Path("peut_etre_la.txt").unlink(missing_ok=True)
```

L'argument `missing_ok=True` (Python 3.8+) évite l'exception
`FileNotFoundError` si le fichier n'existe pas — utile pour les
opérations idempotentes.

**Avertissement.** `unlink` / `remove` est **immédiat** et
**irréversible** :

- Pas de corbeille système (Linux/macOS).
- Pas de confirmation.
- Le fichier est dé-référencé, et son contenu sera réutilisé par le
  système au prochain besoin.

Pour un dossier (vide), utiliser `Path.rmdir()` ou `os.rmdir()`. Pour
un dossier non vide, voir `shutil.rmtree` (fiche 02 — encore plus
dangereux).

## 3.3 Créer un dossier

### `Path.mkdir`

```python
from pathlib import Path

Path("nouveau").mkdir()
```

Par défaut, `mkdir` échoue si le dossier **existe déjà**
(`FileExistsError`), et il échoue aussi si le parent n'existe pas
(`FileNotFoundError`). Deux arguments très utiles :

```python
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

- `parents=True` : crée toute la chaîne de parents manquants
  (équivalent de `mkdir -p` en shell).
- `exist_ok=True` : ne lève pas d'exception si le dossier existe déjà.

Combinés, ces deux drapeaux rendent l'opération **idempotente** : on
peut la rejouer sans craindre d'erreur. C'est la forme à privilégier
dans la majorité des scripts.

### `os.mkdir` et `os.makedirs`

Équivalents bas niveau :

- `os.mkdir(chemin)` : un seul dossier, parents requis.
- `os.makedirs(chemin, exist_ok=True)` : crée la chaîne complète.

## 3.4 Ajuster les droits Unix (`chmod`)

Sous Unix, chaque fichier porte un trio de droits :

| Cible            | Droits   |
|------------------|----------|
| Propriétaire (u) | r w x    |
| Groupe (g)       | r w x    |
| Autres (o)       | r w x    |

Encodés sous forme **octale** :

| Notation octale | Droits                                           |
|-----------------|--------------------------------------------------|
| `0o644`         | `rw- r-- r--` (fichier lisible par tous)         |
| `0o600`         | `rw- --- ---` (privé)                            |
| `0o755`         | `rwx r-x r-x` (script exécutable par tous)       |
| `0o700`         | `rwx --- ---` (dossier personnel privé)          |

En Python, le préfixe `0o` indique un littéral octal. **Ne pas oublier
le `0o`** : `chmod(755)` (sans préfixe) demande des droits totalement
différents, et probablement aberrants.

### `os.chmod` et `Path.chmod`

```python
import os
from pathlib import Path

os.chmod("script.py", 0o755)
Path("script.py").chmod(0o755)
```

Les deux fonctions sont équivalentes ; `Path.chmod` est juste plus
lisible quand on manipule déjà un `Path`.

Pour rendre un script Python directement exécutable depuis le shell,
le minimum est :

```python
Path("mon_script.py").chmod(0o755)
```

Combiné avec une ligne shebang `#!/usr/bin/env python3` (voir
chapitre 00), on peut alors lancer `./mon_script.py`.

## 3.5 Récapitulatif

| Action                | `os`                      | `pathlib`                       |
|-----------------------|---------------------------|---------------------------------|
| Renommer              | `os.rename(a, b)`         | `Path(a).rename(b)`             |
| Supprimer un fichier  | `os.remove(p)`            | `Path(p).unlink()`              |
| Supprimer un dossier vide | `os.rmdir(p)`         | `Path(p).rmdir()`               |
| Créer un dossier      | `os.makedirs(p, exist_ok=True)` | `Path(p).mkdir(parents=True, exist_ok=True)` |
| Changer les droits    | `os.chmod(p, 0o755)`      | `Path(p).chmod(0o755)`          |

## À retenir

- `os.remove` et `Path.unlink` suppriment **immédiatement** et
  **sans corbeille**. Toujours vérifier le chemin avant.
- `Path.mkdir(parents=True, exist_ok=True)` est la forme idempotente
  à connaître par cœur.
- `chmod` attend un littéral octal : **toujours** préfixer `0o`.
- Renommer sur le même système de fichiers est atomique ; sinon c'est
  une copie+suppression — préférer alors `shutil.move`.

## Démo

Exécuter `03_demo_renommer.py`.
