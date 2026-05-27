# 03 — Archives TAR

## 3.1 Tar : archiver d'abord, compresser ensuite

Le format **TAR** (*Tape ARchive*, hérité des bandes magnétiques) est
omniprésent sur les systèmes Unix. Son fonctionnement diffère de ZIP :

- `tar` produit une archive **non compressée** : un simple
  concaténation des fichiers avec leurs métadonnées (permissions,
  propriétaire, horodatage).
- La compression est faite **après**, sur l'archive entière, par
  `gzip`, `bzip2` ou `xz`.

D'où les extensions courantes :

| Extension     | Compression       |
|---------------|-------------------|
| `.tar`        | aucune            |
| `.tar.gz`     | gzip (`.tgz`)     |
| `.tar.bz2`    | bzip2             |
| `.tar.xz`     | xz / lzma         |

Conséquence pratique : un fichier `.tar.gz` ne peut être **lu que
séquentiellement** — pour extraire un seul fichier, on doit décompresser
toute l'archive jusqu'à lui. À l'inverse, un `.zip` permet l'accès
aléatoire à n'importe quel fichier interne.

## 3.2 Ouvrir une archive avec `tarfile.open`

Le module `tarfile` expose la fonction `open(path, mode)` qui choisit
la compression via la deuxième moitié du mode :

| Mode      | Action            | Compression |
|-----------|-------------------|-------------|
| `"r"`     | Lecture (auto)    | détectée    |
| `"w"`     | Écriture          | aucune      |
| `"w:gz"`  | Écriture          | gzip        |
| `"w:bz2"` | Écriture          | bzip2       |
| `"w:xz"`  | Écriture          | xz / lzma   |
| `"a"`     | Ajout             | aucune *    |

\* Le mode ajout n'est pas supporté sur les archives compressées : il
faudrait décompresser, ajouter, puis recompresser.

```python
import tarfile

with tarfile.open("documents.tar.gz", "w:gz") as tar:
    tar.add("rapport.txt")
    tar.add("images", arcname="medias")   # dossier entier, renommé
```

`.add` ajoute un fichier **ou un dossier**, récursivement. C'est plus
direct que `zipfile.write` qui ne traite qu'un fichier à la fois.

## 3.3 Ajouter, lister, extraire

```python
import tarfile

# Lister sans extraire :
with tarfile.open("documents.tar.gz", "r") as tar:
    for nom in tar.getnames():
        print(nom)

# Extraire :
with tarfile.open("documents.tar.gz", "r") as tar:
    tar.extractall("sortie/")
```

Lire un fichier interne sans extraire sur disque :

```python
with tarfile.open("documents.tar.gz", "r") as tar:
    f = tar.extractfile("medias/logo.png")
    if f is not None:                     # None si c'est un dossier
        octets = f.read()
```

## 3.4 Sécurité et `filter=`

Comme ZIP, TAR peut contenir des chemins traversants
(`../../etc/passwd`). Pire encore, il peut contenir des **liens
symboliques** pointant n'importe où.

Depuis Python 3.12, `extractall` exige un paramètre `filter=` pour
expliciter la politique :

```python
with tarfile.open("documents.tar.gz", "r") as tar:
    tar.extractall("sortie/", filter="data")
```

| Valeur de `filter` | Politique                                                  |
|--------------------|------------------------------------------------------------|
| `"fully_trusted"`  | Aucun filtrage (comportement historique, dangereux)        |
| `"tar"`            | Politique stricte TAR (refuse les liens externes, etc.)    |
| `"data"`           | Encore plus stricte : adapté aux fichiers de **données**   |

`"data"` est la valeur recommandée quand on extrait une archive
inconnue. Sans `filter=`, un `DeprecationWarning` apparaît en 3.12 et
le code lèvera une erreur dans une version future.

## 3.5 Récapitulatif des méthodes utiles

| Méthode                   | Rôle                                          |
|---------------------------|-----------------------------------------------|
| `tarfile.open(path, mode)`| Ouvre une archive (avec `with`)               |
| `.add(p, arcname=None)`   | Ajoute un fichier ou un dossier (récursif)    |
| `.getnames()`             | Liste les noms internes                       |
| `.getmembers()`           | Liste les `TarInfo` (métadonnées détaillées)  |
| `.extractall(p, filter=)` | Extrait tout (préciser `filter="data"`)       |
| `.extractfile(name)`      | Lit un membre comme un flux (sans disque)     |

## 3.6 ZIP ou TAR ?

| Critère                          | ZIP             | TAR (`.tar.gz`)         |
|----------------------------------|-----------------|-------------------------|
| Plateforme dominante             | Windows         | Unix / Linux            |
| Compression                      | Par fichier     | Sur l'archive entière   |
| Accès aléatoire à un fichier     | Oui             | Non (séquentiel)        |
| Préserve les permissions Unix    | Limité          | Oui                     |
| Préserve les liens symboliques   | Non             | Oui                     |
| Ajout après création             | Oui (mode `"a"`)| Seulement si non compressée |

En règle générale :

- **ZIP** pour échanger avec Windows ou quand on veut piocher un
  fichier précis sans tout décompresser.
- **TAR** (en `.tar.gz`) pour archiver une arborescence Unix complète,
  ou pour bénéficier d'un meilleur taux de compression global (la
  compression voit l'ensemble de l'archive d'un coup, pas chaque
  fichier isolément).

## À retenir

- `tarfile.open(path, "w:gz")` crée une archive `.tar.gz` ;
  `"w:bz2"` et `"w:xz"` changent la compression.
- `.add(chemin)` ajoute récursivement (fichiers **ou dossiers**).
- À l'extraction, **toujours** passer `filter="data"` pour les
  archives venues de l'extérieur.
- TAR préserve mieux les métadonnées Unix que ZIP, mais ne permet
  pas l'accès aléatoire.

## Démo

Exécuter `03_demo_tar.py`.
