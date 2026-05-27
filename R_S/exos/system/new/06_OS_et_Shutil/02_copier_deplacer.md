# 02 — Copier et déplacer

Le module `shutil` (« shell utilities ») regroupe les opérations de
**haut niveau** qui auraient nécessité plusieurs lignes en pur `os` :
copier un fichier, dupliquer une arborescence, déplacer un dossier
entre deux systèmes de fichiers, supprimer récursivement.

## 2.1 `shutil.copy` — copier un fichier (contenu seul)

```python
import shutil

shutil.copy("source.txt", "destination.txt")
```

Copie **le contenu** du fichier source vers la destination. Les
**métadonnées** (date de modification, droits exacts) ne sont pas
préservées : la copie reçoit la date du jour et les droits par défaut
du processus.

Si la destination est un **dossier existant**, le fichier est copié
**dans** ce dossier en gardant son nom :

```python
shutil.copy("rapport.pdf", "/tmp/")       # crée /tmp/rapport.pdf
```

## 2.2 `shutil.copy2` — contenu + métadonnées

```python
shutil.copy2("source.txt", "destination.txt")
```

Identique à `copy`, mais **préserve les métadonnées** :

- date de modification (`mtime`) ;
- date d'accès (`atime`) ;
- droits Unix (`mode`).

C'est la fonction à utiliser dès qu'on fait une **sauvegarde** ou un
**archivage** : on veut garder l'historique temporel d'origine.

Règle simple :

- `copy` : copier vite, métadonnées négligeables.
- `copy2` : copier en préservant la « photographie » du fichier.

## 2.3 `shutil.copytree` — copier un dossier entier

```python
shutil.copytree("source_dir", "dest_dir")
```

Copie **récursivement** tout le contenu de `source_dir` dans
`dest_dir`. Par défaut, `dest_dir` **ne doit pas exister** : `copytree`
le crée lui-même. Lever `FileExistsError` autrement.

Pour autoriser la copie dans un dossier déjà existant :

```python
shutil.copytree("source_dir", "dest_dir", dirs_exist_ok=True)
```

`copytree` utilise `copy2` en interne par défaut — donc les
métadonnées sont préservées. On peut changer ce comportement avec
l'argument `copy_function`.

## 2.4 `shutil.move` — déplacer ou renommer

```python
shutil.move("ancien_chemin", "nouveau_chemin")
```

Trois comportements possibles selon le contexte :

1. **Renommage** (source et destination sur le **même** système de
   fichiers) : l'opération est instantanée — c'est juste une mise à
   jour de l'entrée du répertoire (équivalent de `os.rename`).
2. **Déplacement réel** (entre systèmes de fichiers différents,
   ou vers un autre disque) : `shutil.move` recopie puis supprime
   l'original.
3. Si la destination est un **dossier existant**, la source est
   déplacée **à l'intérieur** en gardant son nom.

Attention : `shutil.move` peut **écraser** une destination fichier
existante sans confirmation. Vérifier au préalable avec `Path.exists()`
si on tient à la donnée.

## 2.5 `shutil.rmtree` — supprimer un dossier non vide

```python
shutil.rmtree("dossier_a_jeter")
```

**DANGER.** `rmtree` supprime le dossier indiqué **et tout son
contenu**, récursivement, **sans confirmation** et **sans corbeille**.
Les données sont perdues immédiatement.

Quelques règles à graver :

- **Toujours** vérifier le chemin **avant** : un `print(chemin)`
  préalable peut sauver la mise.
- **Jamais** construire le chemin par concaténation hasardeuse :
  une variable vide donnerait `rmtree("/")` — catastrophique.
- En cas de doute, passer par un dossier `tempfile.TemporaryDirectory()`
  pour tester.
- Pour un dossier **vide**, préférer `os.rmdir()` ou `Path.rmdir()`
  qui échouent si le dossier n'est pas vide — c'est un garde-fou.

Exemple défensif :

```python
from pathlib import Path
import shutil

cible = Path("/tmp/mes_archives_2020")

# Garde-fous minimaux avant un rmtree.
assert cible.is_dir(), f"{cible} n'est pas un dossier"
assert str(cible).startswith("/tmp/"), "Refus de supprimer hors /tmp"

shutil.rmtree(cible)
```

## 2.6 Tableau récapitulatif

| Fonction          | Effet                                            |
|-------------------|--------------------------------------------------|
| `shutil.copy`     | Copie d'un fichier (contenu seul)                |
| `shutil.copy2`    | Copie d'un fichier (contenu + métadonnées)       |
| `shutil.copytree` | Copie récursive d'un dossier                     |
| `shutil.move`     | Déplacement ou renommage (fichier ou dossier)    |
| `shutil.rmtree`   | Suppression récursive d'un dossier (DESTRUCTIF)  |

## À retenir

- `copy` vs `copy2` : ne diffèrent que sur les métadonnées.
- `copytree` est récursif et préserve les métadonnées par défaut.
- `move` peut renommer ou déplacer, et **écrase** sans demander.
- `rmtree` supprime **tout** un dossier sans confirmation. Toujours
  inspecter le chemin avant.

## Démo

Exécuter `02_demo_copier.py`. Le script crée son propre dossier
temporaire, le peuple, copie et déplace en interne, puis nettoie tout
à la sortie : aucun risque pour le système de fichiers de
l'utilisateur.
