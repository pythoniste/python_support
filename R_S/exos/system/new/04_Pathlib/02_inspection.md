# 02 — Inspecter un chemin

Construire un `Path` ne touche **pas** au disque. C'est juste un objet
qui contient une suite de morceaux. Tant qu'on n'appelle pas une
méthode d'inspection, rien n'est vérifié — le chemin peut très bien
ne désigner aucun fichier réel.

## 2.1 Existence et type

Quatre méthodes de base, toutes booléennes :

```python
p = Path("/etc/hosts")

p.exists()       # True si quelque chose existe à ce chemin
p.is_file()      # True si c'est un fichier régulier
p.is_dir()       # True si c'est un dossier
p.is_symlink()   # True si c'est un lien symbolique
```

À noter : `exists()` suit les liens symboliques par défaut. Si le
chemin est un lien vers un fichier supprimé, `exists()` renvoie
`False`, mais `is_symlink()` renvoie quand même `True`. Le lien
existe ; sa cible non.

`is_file()` et `is_dir()` renvoient `False` si le chemin n'existe pas
du tout, **sans** lever d'exception. C'est très pratique : on peut
toujours interroger un `Path`, même incertain.

## 2.2 Métadonnées avec `.stat()`

Pour obtenir taille, dates de modification, propriétaire, etc., on
appelle `.stat()`. La méthode renvoie un objet `os.stat_result` :

```python
p = Path("/etc/hosts")
infos = p.stat()

infos.st_size      # taille en octets
infos.st_mtime     # date de modification (timestamp Unix, float)
infos.st_mode      # type et permissions (octal)
infos.st_uid       # identifiant du propriétaire
```

Le timestamp `st_mtime` se convertit en date lisible avec `datetime` :

```python
from datetime import datetime

mtime = datetime.fromtimestamp(p.stat().st_mtime)
print(mtime)   # 2026-05-27 10:42:13.123456
```

Contrairement aux méthodes booléennes, `.stat()` **lève** une
exception (`FileNotFoundError`) si le chemin n'existe pas. Toujours
vérifier `.exists()` avant, ou attraper l'exception.

## 2.3 Dossier courant, dossier personnel

Deux raccourcis fréquemment utilisés :

```python
Path.cwd()     # le dossier courant (Current Working Directory)
Path.home()    # le dossier personnel de l'utilisateur
```

`Path.cwd()` reflète **où** le script a été lancé, pas où il est
stocké. Si on lance `python3 /opt/script.py` depuis `/tmp`, alors
`Path.cwd()` vaut `/tmp` et non `/opt`.

Pour obtenir le dossier **du script lui-même** :

```python
Path(__file__).parent
```

## 2.4 Rendre un chemin absolu : `absolute` vs `resolve`

Un chemin peut être **relatif** (`"./notes.txt"`,  `"../data/x"`) ou
**absolu** (`"/home/ada/notes.txt"`). Deux méthodes le rendent absolu,
mais elles diffèrent sur deux points clés.

### `.absolute()`

Renvoie le chemin préfixé par `Path.cwd()`, **sans** toucher au
disque, **sans** résoudre les `.`, `..` ou les liens symboliques :

```python
Path("notes.txt").absolute()
# /tmp/notes.txt    (si cwd = /tmp)

Path("../notes.txt").absolute()
# /tmp/../notes.txt   les '..' sont conservés
```

C'est rapide et fonctionne même si le fichier n'existe pas — mais le
résultat peut contenir des composants redondants.

### `.resolve()`

Renvoie le chemin **canonique** : absolu, sans `.` ni `..`, avec les
liens symboliques **résolus** :

```python
Path("../notes.txt").resolve()
# /home/ada/notes.txt    forme finale, propre

Path("/var/log").resolve()
# /var/log               (ou la vraie cible si /var est un lien)
```

`.resolve()` interroge le système de fichiers. Sous Python 3.6+, elle
fonctionne même si le fichier n'existe pas (les composants non
résolvables sont laissés tels quels). Avec l'argument `strict=True`,
elle lève `FileNotFoundError` si le chemin est invalide.

### Résumé pratique

| Méthode      | Préfixe `cwd` | Résout `..` | Suit les liens | Touche au disque |
|--------------|---------------|-------------|----------------|------------------|
| `.absolute()` | oui          | non         | non            | non              |
| `.resolve()`  | oui          | oui         | oui            | oui              |

Règle simple : **utiliser `resolve()` par défaut**, sauf si on veut
exprès garder le chemin tel qu'il a été tapé.

## À retenir

- Construire un `Path` ne lit jamais le disque ; il faut une méthode
  d'inspection pour ça.
- `.exists()`, `.is_file()`, `.is_dir()`, `.is_symlink()` sont sûres :
  elles renvoient `False` plutôt que de lever sur un chemin absent.
- `.stat()` donne taille, mtime, etc., mais **lève** si le chemin
  n'existe pas.
- `Path.cwd()` change selon l'endroit d'où on lance le script ;
  `Path(__file__).parent` donne le dossier du script.
- `.absolute()` est syntaxique ; `.resolve()` est canonique. En cas de
  doute, on choisit `.resolve()`.

## Démo

Exécuter `02_demo_inspection.py`.
