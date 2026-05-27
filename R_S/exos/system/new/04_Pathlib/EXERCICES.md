# Exercices pratiques — dossier 04_Pathlib

Une fois les trois fiches lues et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** `pathlib` dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- la fiche concernée ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

Convention : les ateliers qui acceptent un chemin en argument utilisent
**`.` par défaut** (le dossier courant), de manière à être testables
immédiatement sans paramètre.

---

## Atelier 1 — Décomposer un chemin  ★
*Fiche 01 — attributs de Path*

Écrire un script `atelier_01.py` qui prend un chemin de fichier en
argument (par défaut `./README.md`) et affiche, ligne par ligne :

- le dossier parent ;
- le nom sans extension ;
- l'extension ;
- la liste des `parts`.

**Indices**

- `Path(s).parent`, `.stem`, `.suffix`, `.parts`.
- `sys.argv[1] if len(sys.argv) > 1 else "./README.md"`.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py /tmp/donnees/rapport.tar.gz
Parent     : /tmp/donnees
Stem       : rapport.tar
Suffix     : .gz
Parts      : ('/', 'tmp', 'donnees', 'rapport.tar.gz')
```

---

## Atelier 2 — Tous les `.py` du dossier courant  ★
*Fiche 03 — glob simple*

Écrire un script `atelier_02.py` qui affiche, **triés
alphabétiquement**, tous les fichiers `.py` du dossier passé en
argument (par défaut `.`). Un fichier par ligne.

**Indices**

- `Path(dossier).glob("*.py")`.
- `sorted(...)` pour trier la liste.
- Ne pas descendre dans les sous-dossiers : `glob` suffit (pas
  `rglob`).

**Exemple de sortie attendue**

```
$ python3 atelier_02.py
01_demo_path.py
02_demo_inspection.py
03_demo_glob.py
atelier_02.py
```

---

## Atelier 3 — Compter les fichiers par extension  ★★
*Fiche 03 — rglob + agrégation*

Écrire un script `atelier_03.py` qui parcourt **récursivement** le
dossier passé en argument (par défaut `.`) et affiche le nombre de
fichiers regroupés par extension. Trier de la plus fréquente à la
moins fréquente.

Les fichiers sans extension sont comptés sous l'étiquette `(aucune)`.

**Indices**

- `Path(d).rglob("*")` et filtrer avec `.is_file()`.
- `collections.Counter` pour l'agrégation.
- L'extension est `p.suffix` ; vide si aucune.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
.py     4
.md     4
(aucune) 1
```

---

## Atelier 4 — Séparer un chemin en trois  ★
*Fiche 01 — attributs de Path*

Écrire une fonction `decomposer(chemin: str) -> tuple[str, str, str]`
qui renvoie le triplet **(dossier, nom_sans_extension, extension)**.
Pour les fichiers à extension multiple, on garde uniquement la
**dernière** extension.

Le script `atelier_04.py` doit :

- définir la fonction ;
- l'appliquer à au moins trois exemples « en dur » dans le code
  (dont un chemin avec `.tar.gz` et un chemin sans extension) ;
- afficher proprement chaque résultat.

**Indices**

- `Path(c).parent`, `.stem`, `.suffix`.
- Convertir le `Path` du parent en `str` pour le retour.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py
/tmp/a.txt           -> ('/tmp', 'a', '.txt')
/var/log/archive.tar.gz -> ('/var/log', 'archive.tar', '.gz')
/etc/hosts            -> ('/etc', 'hosts', '')
```

---

## Atelier 5 — Fichiers modifiés dans les dernières 24 heures  ★★★
*Fiches 02 + 03 — stat.st_mtime + rglob*

Écrire un script `atelier_05.py` qui parcourt **récursivement** le
dossier passé en argument (par défaut `.`) et affiche les fichiers
modifiés dans les dernières **24 heures**, triés du plus récent au
plus ancien. Pour chaque fichier, indiquer le chemin et l'horodatage
de modification au format `YYYY-MM-DD HH:MM:SS`.

**Indices**

- `time.time()` pour le « maintenant » (en secondes Unix).
- `p.stat().st_mtime` pour l'âge d'un fichier.
- `datetime.fromtimestamp(...)` pour formater la date.
- Filtrer : `now - p.stat().st_mtime < 24 * 3600`.

**Exemple de sortie attendue**

```
$ python3 atelier_05.py
2026-05-27 09:48:11  ./README.md
2026-05-27 09:42:03  ./EXERCICES.md
2026-05-26 23:11:50  ./03_demo_glob.py
```

**Bonus** : accepter un second argument `--heures N` pour changer la
fenêtre (par défaut 24).

---

## Pour aller plus loin

Une fois ces ateliers terminés, on maîtrise `pathlib` à un niveau
suffisant pour aborder la lecture/écriture de fichiers, les archives
et tous les chapitres suivants — où les chemins seront manipulés
**sans** détour par `os.path`.
