# 01 — Compresser un fichier seul

## 1.1 Compression n'est pas archivage

Les modules `gzip`, `bz2` et `lzma` font **une seule chose** :
prendre un flux d'octets et le rendre plus petit (en moyenne). Ils
ne mémorisent ni nom de fichier, ni date, ni structure de dossiers.

```
fichier.txt   ->   gzip   ->   fichier.txt.gz
```

À l'arrivée, `fichier.txt.gz` ne contient qu'**un seul** contenu :
celui de `fichier.txt`. Pour compresser plusieurs fichiers, il faut
d'abord les regrouper dans une archive (voir fiches 02 et 03).

## 1.2 Une API commune : `open()`

Les trois modules exposent la même fonction `open()`, qui se comporte
exactement comme `builtins.open` — avec les modes habituels :

| Mode   | Sens                       |
|--------|----------------------------|
| `"rb"` | Lecture binaire            |
| `"wb"` | Écriture binaire           |
| `"rt"` | Lecture texte (décodé)     |
| `"wt"` | Écriture texte (encodé)    |

Exemple en binaire :

```python
import gzip

with gzip.open("notes.txt.gz", "wb") as f:
    f.write(b"Ligne 1\n")
    f.write(b"Ligne 2\n")

with gzip.open("notes.txt.gz", "rb") as f:
    donnees = f.read()
```

Exemple en texte (avec décodage automatique, par défaut UTF-8) :

```python
with gzip.open("notes.txt.gz", "wt", encoding="utf-8") as f:
    f.write("Bonjour le monde\n")

with gzip.open("notes.txt.gz", "rt", encoding="utf-8") as f:
    texte = f.read()
```

Pour `bz2` et `lzma`, **le code est identique** — seul le nom du
module change :

```python
import bz2
import lzma

with bz2.open("notes.txt.bz2", "wt", encoding="utf-8") as f:
    f.write("Bonjour\n")

with lzma.open("notes.txt.xz", "wt", encoding="utf-8") as f:
    f.write("Bonjour\n")
```

## 1.3 Compresser un fichier existant

Le motif courant : lire un fichier d'origine en binaire, écrire la
version compressée en binaire.

```python
from pathlib import Path
import gzip

src = Path("rapport.txt")
dst = Path("rapport.txt.gz")

with src.open("rb") as entree, gzip.open(dst, "wb") as sortie:
    sortie.write(entree.read())
```

Pour les très gros fichiers, on évitera de tout charger en mémoire
en lisant par morceaux :

```python
TAILLE = 64 * 1024   # 64 Kio

with src.open("rb") as entree, gzip.open(dst, "wb") as sortie:
    while morceau := entree.read(TAILLE):
        sortie.write(morceau)
```

## 1.4 Tableau comparatif

Les trois algorithmes n'ont pas les mêmes caractéristiques. Les
chiffres ci-dessous sont des ordres de grandeur (très dépendants des
données et de la machine).

| Module  | Extension | Vitesse           | Taux de compression  | Cas typique                  |
|---------|-----------|-------------------|----------------------|------------------------------|
| `gzip`  | `.gz`     | Rapide            | Moyen                | Logs, échanges réseau        |
| `bz2`   | `.bz2`    | Lent              | Bon                  | Sauvegardes ponctuelles      |
| `lzma`  | `.xz`     | Très lent (écrit) | Excellent            | Distribution de logiciels    |

Règle simple : `gzip` quand on veut quelque chose de **rapide** et
omniprésent ; `lzma` quand on veut le **plus petit** fichier possible
et qu'on peut attendre.

## 1.5 Détecter un fichier déjà compressé

Compresser un fichier déjà compressé ne sert à rien (et peut même
augmenter sa taille). On peut détecter le format en regardant les
premiers octets (« magic number ») :

| Format  | Premiers octets     |
|---------|---------------------|
| gzip    | `\x1f\x8b`          |
| bzip2   | `BZh` (`\x42\x5a\x68`) |
| xz      | `\xfd7zXZ\x00`      |

```python
with open("inconnu.bin", "rb") as f:
    tete = f.read(6)
deja_gz = tete.startswith(b"\x1f\x8b")
```

## 1.6 Ce qu'il ne faut **pas** attendre de `gzip`

- Il ne stocke **pas** le nom du fichier original (la commande shell
  `gzip` le fait dans l'en-tête, mais le module Python ne l'expose
  pas par défaut).
- Il ne gère **pas** plusieurs fichiers d'un coup.
- Il ne préserve **pas** la structure de dossiers.

Pour tout ça, il faut une **archive** : c'est l'objet des fiches 02
et 03.

## À retenir

- `gzip`, `bz2`, `lzma` compressent **un seul flux d'octets**.
- Même API pour les trois : `xxx.open(path, mode)` avec `"rb"`,
  `"wb"`, `"rt"`, `"wt"`.
- `gzip` est rapide et standard ; `lzma` (`.xz`) compresse mieux mais
  beaucoup plus lentement.
- Pour plusieurs fichiers, utiliser `zipfile` ou `tarfile`.

## Démo

Exécuter `01_demo_gzip.py`.
