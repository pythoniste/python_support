# Exercices pratiques — dossier 07_Compression

Une fois les trois fiches lues et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** la compression et
l'archivage avec la bibliothèque standard.

Chaque atelier indique :

- la fiche concernée ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier. Les corrigés créent toutes leurs données
d'entrée dans un `tempfile.TemporaryDirectory()` : aucun fichier
n'est laissé sur le disque.

---

## Atelier 1 — Ratio de compression  ★
*Fiche 01 — compression d'un fichier seul*

Écrire `atelier_01.py` qui :

- crée un fichier texte de taille connue (par exemple `"abc\n" * 10_000`) ;
- le compresse en `.gz` avec `gzip` ;
- affiche la taille avant, la taille après et le **ratio**
  (taille compressée / taille originale, en pourcentage).

**Indices**

- `tempfile.TemporaryDirectory()` pour isoler le travail.
- `gzip.open(chemin, "wb")` pour écrire compressé.
- `Path.stat().st_size` donne la taille en octets.

**Exemple de sortie attendue**

```
Original : 40000 octets
Compressé :  126 octets
Ratio    :  0.3 %
```

---

## Atelier 2 — Archiver un dossier en ZIP  ★★
*Fiche 02 — ZIP*

Écrire `atelier_02.py` qui prend en argument un chemin de dossier et
produit un fichier `<nom_dossier>.zip` à côté, contenant
**récursivement** tous les fichiers du dossier — en préservant
l'arborescence relative.

**Indices**

- `Path.rglob("*")` parcourt récursivement.
- Filtrer avec `chemin.is_file()` pour ignorer les dossiers eux-mêmes.
- `arcname = chemin.relative_to(dossier_source)` pour éviter les
  chemins absolus dans l'archive.
- Activer `compression=zipfile.ZIP_DEFLATED`.

Pour l'atelier (et son corrigé), le dossier source est généré dans un
`tempfile.TemporaryDirectory()`.

---

## Atelier 3 — Extraire un .tar.gz en sécurité  ★★
*Fiche 03 — TAR*

Écrire `atelier_03.py` qui :

1. crée un `.tar.gz` factice dans un dossier temporaire (3 fichiers
   minimum) ;
2. extrait l'archive dans un dossier `cible/` ;
3. liste les fichiers extraits.

L'extraction doit utiliser `filter="data"` pour rester sûre.

**Indices**

- `tarfile.open(archive, "w:gz")` pour créer.
- `tar.extractall(cible, filter="data")` pour extraire.
- `Path.rglob("*")` pour lister le résultat.

---

## Atelier 4 — Lister une archive sans extraire  ★★
*Fiches 02 + 03 — dispatch sur extension*

Écrire `atelier_04.py archive` qui :

- détecte le format à partir de l'extension (`.zip` -> `zipfile`,
  `.tar`, `.tar.gz`, `.tgz`, `.tar.bz2`, `.tar.xz` -> `tarfile`) ;
- affiche la liste des fichiers internes **sans rien extraire** ;
- pour chaque entrée, affiche son nom et sa taille (compressée pour
  ZIP, brute pour TAR).

**Indices**

- `ZipFile.infolist()` renvoie des `ZipInfo` avec `.filename` et
  `.compress_size`.
- `TarFile.getmembers()` renvoie des `TarInfo` avec `.name` et
  `.size`.
- `tarfile.open(path, "r")` détecte la compression automatiquement.

Le corrigé crée d'abord à la fois un `.zip` et un `.tar.gz` dans un
dossier temporaire et appelle la fonction de listage sur chacun.

---

## Atelier 5 — Compresseur universel  ★★★
*Fiches 01 + 02 + 03 — choix de format*

Écrire `atelier_05.py` qui accepte un fichier **ou** un dossier en
argument, plus un format (`gz`, `bz2`, `xz`, `zip`, `tar.gz`) et
produit l'archive correspondante :

- formats `gz`, `bz2`, `xz` : refusent les dossiers (un seul fichier
  uniquement) ;
- format `zip` : accepte fichier ou dossier ;
- format `tar.gz` : accepte fichier ou dossier.

Le programme affiche un message clair en cas de combinaison invalide
et sort avec le code retour `1`.

**Indices**

- `argparse.ArgumentParser` avec `choices=[...]` pour le format.
- `Path.is_file()` / `Path.is_dir()` pour décider.
- Pour `gz`/`bz2`/`xz` sur un fichier, voir le motif `read()` /
  `write()` de la fiche 01.

Pour le corrigé, créer les entrées dans un
`tempfile.TemporaryDirectory()` et démontrer chaque cas (fichier en
`.gz`, dossier en `.zip`, dossier en `.tar.gz`).

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait :

- compresser un fichier seul dans les trois formats Unix courants ;
- empaqueter un dossier en `.zip` ou en `.tar.gz` ;
- extraire sans danger ;
- dispatcher proprement selon l'extension.

C'est tout ce qu'il faut pour écrire un outil de sauvegarde correct,
ou pour intégrer la compression à un pipeline plus large (par exemple
des logs envoyés sur le réseau au chapitre suivant).
