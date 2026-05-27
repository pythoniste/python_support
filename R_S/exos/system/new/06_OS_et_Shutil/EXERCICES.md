# Exercices pratiques — dossier 06_OS_et_Shutil

Une fois les trois fiches lues et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** le parcours, la copie,
le renommage et la suppression. Aucune dépendance tierce : tout se
fait avec la bibliothèque standard.

Chaque atelier indique :

- la fiche concernée ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

**Avertissement.** Plusieurs ateliers manipulent des opérations
**destructives** (`shutil.rmtree`, `Path.unlink`). Les corrigés
travaillent **systématiquement** dans un dossier
`tempfile.TemporaryDirectory()` qu'ils peuplent eux-mêmes. Avant de
viser un vrai dossier de l'utilisateur, ajouter au minimum un
`print(chemin)` et une demande de confirmation (`input(...)`).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Taille totale d'un dossier  ★
*Fiche 01 — parcourir une arborescence*

Écrire un script `atelier_01.py` qui prend un chemin de dossier en
argument et affiche :

- le nombre total de fichiers ;
- la taille cumulée, en octets, de tous les fichiers (récursivement).

**Indices**

- `sys.argv[1]` pour récupérer le chemin.
- `Path(chemin).rglob("*")` parcourt tout récursivement.
- `p.is_file()` filtre les fichiers (un dossier a aussi une taille).
- `p.stat().st_size` donne la taille en octets.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py /tmp
Fichiers : 17
Taille   : 84531 octets
```

---

## Atelier 2 — Backup horodaté  ★★
*Fiche 02 — copier et déplacer*

Écrire un script `atelier_02.py` qui prend en argument le chemin
d'un dossier source, et le copie vers
`backup_YYYYMMDD_HHMMSS/` (créé à côté du source), en préservant les
métadonnées.

**Indices**

- `from datetime import datetime` puis
  `datetime.now().strftime("%Y%m%d_%H%M%S")`.
- `shutil.copytree(src, dst)` copie récursivement en préservant
  les métadonnées (utilise `copy2` en interne).
- La cible doit ne **pas** exister avant l'appel (sinon
  `FileExistsError`).

**Exemple de sortie attendue**

```
$ python3 atelier_02.py /tmp/projet
Backup créé : /tmp/backup_20260527_143012
Fichiers copiés : 12
```

---

## Atelier 3 — Renommer en masse par préfixe  ★★
*Fiche 03 — renommer*

Écrire un script `atelier_03.py` qui prend trois arguments :

- un dossier ;
- un préfixe ancien (par exemple `foo_`) ;
- un préfixe nouveau (par exemple `bar_`).

Le script doit renommer **tous** les fichiers du dossier qui commencent
par l'ancien préfixe, en remplaçant ce préfixe par le nouveau. On ne
descend pas dans les sous-dossiers.

Exemple : `foo_001.txt`, `foo_002.txt` → `bar_001.txt`, `bar_002.txt`.

**Indices**

- `Path(dossier).iterdir()` pour lister un niveau.
- `nom.startswith(ancien_prefix)` pour filtrer.
- `chemin.rename(chemin.with_name(nouveau_nom))` pour renommer.

**Question** : pourquoi serait-il dangereux d'utiliser `rglob` au
lieu d'`iterdir` ici ?

---

## Atelier 4 — Nettoyer les fichiers de plus de 30 jours  ★★★
*Fiches 01 + 03 — parcourir et supprimer (DESTRUCTIF)*

Écrire un script `atelier_04.py` qui prend un dossier en argument et
supprime tous les fichiers (récursivement) **dont la date de
modification est plus ancienne que 30 jours**.

**Contraintes très importantes** :

- **Mode `--dry-run` par défaut** : par défaut, le script
  **n'efface rien**, il se contente d'**afficher** la liste des
  fichiers qui *seraient* supprimés.
- Le drapeau `--apply` doit être fourni explicitement pour effectuer
  la suppression.
- Avant toute suppression réelle, afficher le nombre de fichiers
  concernés et demander une confirmation (`input("Confirmer ? ")`).

**Indices**

- `time.time()` donne l'heure courante en secondes depuis l'epoch.
- `p.stat().st_mtime` donne la date de modif (même unité).
- Différence en secondes ÷ 86400 = jours.
- `Path.unlink()` pour supprimer.

**Question** : pourquoi le mode `--dry-run` doit-il être **le défaut**
plutôt qu'une option à activer ?

---

## Atelier 5 — Aplatir une arborescence  ★★★
*Fiches 01 + 02 — parcourir + copier*

Écrire un script `atelier_05.py` qui prend en argument un dossier
**source** et un dossier **destination**, et copie **tous** les
fichiers du source (récursivement, à toute profondeur) **à plat**
dans le destination — c'est-à-dire sans recréer la hiérarchie.

Problème : deux fichiers profonds peuvent avoir le même nom. Dans ce
cas, ajouter un suffixe numérique : `image.jpg`, `image_1.jpg`,
`image_2.jpg`, etc.

**Indices**

- `Path(source).rglob("*")` pour parcourir.
- `p.is_file()` pour filtrer.
- Construire le nom cible, vérifier `dst.exists()`, incrémenter un
  compteur jusqu'à trouver un nom libre.
- `shutil.copy2(src, dst)` pour copier en préservant les métadonnées.

**Exemple**

```
source/a/foto.jpg
source/b/foto.jpg
source/c/d/foto.jpg
```

doit donner :

```
destination/foto.jpg
destination/foto_1.jpg
destination/foto_2.jpg
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on dispose de toutes les briques pour
écrire un vrai outil de maintenance : sauvegarde, nettoyage,
réorganisation. Le chapitre suivant (`07_Compression`) montrera
comment empaqueter et archiver tout ça.
