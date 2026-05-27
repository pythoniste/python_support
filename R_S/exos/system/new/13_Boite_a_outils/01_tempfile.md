# 01 — `tempfile` : fichiers et dossiers temporaires

## 1.1 Pourquoi des fichiers temporaires

Un **fichier temporaire** est un fichier qu'on crée volontairement avec
l'intention de le supprimer avant la fin du programme. Trois cas
classiques :

- **Tests** : on a besoin d'un fichier d'entrée à lire, mais on ne veut
  pas polluer le dossier du projet ni dépendre d'un fichier livré dans
  le dépôt.
- **Traitement intermédiaire** : on télécharge un gros blob, on le
  manipule, puis on le rejette. Il n'a aucune raison de survivre.
- **Sortie partielle** : on construit un résultat dans un fichier
  temporaire et on ne le déplace dans son emplacement définitif que si
  tout s'est bien passé (écriture atomique).

La règle de bonne tenue est simple : **on n'écrit jamais des fichiers
de travail dans le dossier de l'utilisateur**. Le module `tempfile` de
la bibliothèque standard sait où le système range ces fichiers et
s'occupe du nettoyage à notre place.

## 1.2 Où le système range-t-il les fichiers temporaires ?

`tempfile.gettempdir()` répond à la question :

```python
import tempfile
print(tempfile.gettempdir())
```

| OS               | Dossier renvoyé typiquement                |
|------------------|--------------------------------------------|
| Linux / macOS    | `/tmp`                                     |
| Windows          | `C:\Users\<nom>\AppData\Local\Temp`        |
| Surcharge        | Variables d'environnement `TMPDIR`, `TEMP` |

Le système peut purger ce dossier au redémarrage, voire plus tôt. C'est
le bon endroit pour des données **éphémères** ; **jamais** pour des
données qu'on tient à garder.

## 1.3 Un dossier temporaire (le cas le plus utile)

`tempfile.TemporaryDirectory()` crée un dossier tout neuf et le supprime
automatiquement à la sortie du bloc `with` :

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    (base / "essai.txt").write_text("hello", encoding="utf-8")
    # ... on travaille librement dans `base`
# Ici, le dossier et tout son contenu ont disparu.
```

C'est la forme à privilégier pour les tests et les scripts qui
manipulent plusieurs fichiers. Aucun nettoyage manuel à écrire.

## 1.4 Un fichier temporaire nommé

`tempfile.NamedTemporaryFile()` crée un fichier déjà ouvert, avec un
**chemin** accessible via `.name`. C'est utile quand on doit passer le
chemin à un autre outil (parseur, sous-processus…) :

```python
import tempfile

with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                 suffix=".txt", delete=True) as f:
    f.write("ligne 1\n")
    f.flush()
    print("Chemin :", f.name)
# Le fichier a été supprimé à la sortie du with.
```

Deux arguments à connaître :

| Argument         | Effet                                                |
|------------------|------------------------------------------------------|
| `mode="w"`/`"wb"`| Texte ou binaire, comme `open()`                     |
| `suffix=".txt"`  | Extension du fichier généré                          |
| `delete=True`    | Supprime à la fermeture (défaut)                     |
| `delete=False`   | Conserve : à nous de supprimer, sinon ça s'accumule  |

Sous Windows, `delete=True` empêche un autre processus d'ouvrir le
fichier tant qu'il n'est pas fermé. Si on veut le faire lire par un
sous-processus, passer `delete=False` et supprimer à la main.

## 1.5 `mkdtemp()` — DANGER : pas de nettoyage automatique

`tempfile.mkdtemp()` crée un dossier temporaire et renvoie son chemin,
**mais ne le supprime pas tout seul**. Aucun context manager n'est
fourni. Si on l'utilise sans précaution, le dossier reste, et on
**pollue** progressivement `/tmp` à chaque exécution.

```python
import tempfile

chemin = tempfile.mkdtemp()
print(chemin)
# ... ce dossier existe encore après la fin du script !
```

À n'utiliser que dans des cas rares où la portée du dossier dépasse un
seul bloc `with`. Dans 99 % des cas, **préférer `TemporaryDirectory()`**.

## 1.6 Le motif d'écriture atomique

Pour ne pas laisser un fichier à moitié écrit en cas de crash, on écrit
dans un fichier temporaire **du même dossier** que la destination, puis
on **renomme** en bloc :

```python
import os, tempfile
from pathlib import Path

destination = Path("rapport.txt")
with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8",
                                 dir=destination.parent,
                                 delete=False) as f:
    f.write("contenu final\n")
    nom_tmp = f.name
os.replace(nom_tmp, destination)
```

`os.replace` est **atomique** sur le même système de fichiers : soit la
destination existe avec le contenu final, soit elle n'a pas bougé.
Jamais d'état intermédiaire visible.

## À retenir

- Les fichiers de travail vont dans le dossier temporaire du système,
  pas chez l'utilisateur.
- `tempfile.TemporaryDirectory()` est l'outil par défaut : context
  manager, nettoyage automatique.
- `tempfile.NamedTemporaryFile()` quand on a besoin du **chemin**
  (`.name`) pour le passer à un autre outil.
- `tempfile.mkdtemp()` **ne nettoie rien** : à éviter sauf nécessité.
- `tempfile.gettempdir()` renseigne sur l'emplacement utilisé par l'OS.
- L'écriture atomique combine `NamedTemporaryFile(dir=...)` et
  `os.replace`.

## Démo

Exécuter `01_demo_tempfile.py`.
