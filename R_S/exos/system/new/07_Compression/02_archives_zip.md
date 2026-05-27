# 02 — Archives ZIP

## 2.1 Une archive, c'est quoi ?

Une **archive** est un fichier unique qui contient plusieurs fichiers,
avec leur nom et leur arborescence. Le format ZIP est très répandu
parce qu'il fonctionne partout (Windows, macOS, Linux) et qu'il
intègre la compression — chaque fichier interne est compressé
individuellement.

```
docs/
  rapport.txt              ->  docs.zip
  images/logo.png              (contient les 2 fichiers + leurs chemins)
```

Python expose le format ZIP via le module `zipfile`, et plus
précisément la classe `ZipFile`.

## 2.2 Ouvrir une archive — les modes

`ZipFile` s'ouvre avec un mode, comme un fichier :

| Mode  | Sens                                                       |
|-------|------------------------------------------------------------|
| `"r"` | Lecture seule (l'archive doit exister)                     |
| `"w"` | Écriture (crée ou **écrase** l'archive)                    |
| `"a"` | Ajout (crée si absente, ajoute des entrées sinon)          |
| `"x"` | Création exclusive (échoue si l'archive existe déjà)       |

Comme toujours, on l'utilise dans un bloc `with` pour garantir la
fermeture :

```python
import zipfile

with zipfile.ZipFile("documents.zip", "w") as archive:
    archive.write("rapport.txt")
```

## 2.3 Ajouter des fichiers

Deux méthodes principales :

### `.write(path, arcname=None)` — depuis un fichier sur disque

```python
from pathlib import Path
import zipfile

with zipfile.ZipFile("documents.zip", "w",
                     compression=zipfile.ZIP_DEFLATED) as zf:
    zf.write("rapport.txt")                   # rangé à la racine
    zf.write("images/logo.png",
             arcname="medias/logo.png")        # renommé à l'intérieur
```

L'argument `arcname` contrôle **le nom utilisé dans l'archive**. Sans
lui, c'est le chemin tel qu'il a été passé qui est conservé — on peut
donc se retrouver avec des chemins absolus, ce qui n'est pas souhaité.

Le paramètre `compression=zipfile.ZIP_DEFLATED` active la compression
gzip-compatible. Sans lui, les fichiers sont **stockés** dans
l'archive **sans compression** (utile pour des données déjà
compressées, comme des PNG ou des JPEG).

### `.writestr(arcname, donnees)` — depuis la mémoire

Pratique quand on n'a pas (et qu'on ne veut pas créer) de fichier
temporaire sur disque :

```python
with zipfile.ZipFile("documents.zip", "a") as zf:
    zf.writestr("note.txt", "Contenu généré en mémoire\n")
    zf.writestr("data.bin", b"\x00\x01\x02")
```

## 2.4 Lire une archive

```python
with zipfile.ZipFile("documents.zip", "r") as zf:
    # Liste des noms internes :
    for nom in zf.namelist():
        print(nom)

    # Lire un fichier précis (renvoie des octets) :
    octets = zf.read("rapport.txt")
```

Pour lire un fichier interne comme un flux (sans tout charger en
mémoire) :

```python
with zipfile.ZipFile("documents.zip", "r") as zf:
    with zf.open("rapport.txt", "r") as f:
        for ligne in f:
            print(ligne.decode("utf-8"), end="")
```

`zf.open` renvoie un flux **binaire** ; à nous de décoder.

## 2.5 Extraire

`.extractall(path)` extrait tout dans un dossier cible :

```python
with zipfile.ZipFile("documents.zip", "r") as zf:
    zf.extractall("sortie/")
```

`.extract(nom, path)` extrait un seul fichier.

## 2.6 Attention : `zip-slip`

Un fichier ZIP malveillant peut contenir des chemins comme
`../../etc/passwd`. Si on appelle `extractall("sortie/")` sans
vérification, le fichier peut se retrouver **en dehors** de `sortie/`
— c'est la faille dite *zip-slip*.

Depuis Python 3.12, `extractall` filtre par défaut les chemins
dangereux. Mais sur les versions antérieures, ou pour rester
défensif, on vérifie soi-même :

```python
from pathlib import Path
import zipfile

def extraire_sur(archive: Path, cible: Path) -> None:
    cible = cible.resolve()
    with zipfile.ZipFile(archive, "r") as zf:
        for nom in zf.namelist():
            destination = (cible / nom).resolve()
            # On refuse tout chemin qui sort de `cible`.
            if not destination.is_relative_to(cible):
                raise ValueError(f"Chemin suspect : {nom}")
        zf.extractall(cible)
```

`Path.is_relative_to` (Python 3.9+) renvoie `True` si le chemin
résolu reste bien à l'intérieur du dossier cible.

## 2.7 Récapitulatif des méthodes utiles

| Méthode               | Rôle                                              |
|-----------------------|---------------------------------------------------|
| `ZipFile(path, mode)` | Ouvre une archive (avec `with`)                   |
| `.write(p, arcname)`  | Ajoute un fichier du disque                       |
| `.writestr(name, d)`  | Ajoute du contenu en mémoire                      |
| `.read(name)`         | Lit un fichier interne (renvoie `bytes`)          |
| `.open(name)`         | Ouvre un fichier interne comme un flux            |
| `.namelist()`         | Liste les noms internes                           |
| `.extractall(path)`   | Extrait tous les fichiers dans un dossier         |
| `.extract(name, p)`   | Extrait un seul fichier                           |

## À retenir

- `zipfile.ZipFile(path, "w")` crée une archive ; `"r"` la lit, `"a"`
  l'enrichit.
- Toujours penser à passer `compression=zipfile.ZIP_DEFLATED` si on
  veut effectivement **compresser** (sinon les fichiers sont
  seulement stockés).
- `arcname=` contrôle le nom interne ; sans lui, on risque de
  conserver des chemins absolus.
- Avant `extractall`, vérifier que les chemins ne sortent pas du
  dossier cible (zip-slip).

## Démo

Exécuter `02_demo_zip.py`.
