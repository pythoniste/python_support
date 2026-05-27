# 01 — `Path` de base

## 1.1 Pourquoi `pathlib` ?

Pendant longtemps, manipuler des chemins en Python passait par des
fonctions de `os.path` qui prenaient et rendaient des **chaînes de
caractères**. C'était verbeux et fragile (séparateur `/` ou `\`,
oublis de jointure, opérations dispersées dans plusieurs modules).

Depuis Python 3.4, le module `pathlib` propose une classe `Path` qui
regroupe **tout** ce dont on a besoin sur un objet unique.

```python
from pathlib import Path
```

Une seule importation, et on dispose des opérations de construction,
d'inspection, de parcours et de lecture/écriture sur le même objet.

## 1.2 Construire un chemin

On instancie `Path` avec une chaîne de caractères :

```python
p = Path("/tmp/exemple.txt")
print(p)         # /tmp/exemple.txt
print(type(p))   # <class 'pathlib.PosixPath'>
```

Le type renvoyé dépend du système : `PosixPath` sous Linux/macOS,
`WindowsPath` sous Windows. C'est transparent pour l'utilisateur.

Quelques chemins particuliers, qui n'exigent pas de littéral :

```python
Path.cwd()    # le dossier courant
Path.home()   # le dossier personnel de l'utilisateur
Path()        # équivalent à Path(".")
```

## 1.3 Assembler avec l'opérateur `/`

Le grand confort de `pathlib`, c'est de surcharger l'opérateur `/`
pour assembler les morceaux d'un chemin :

```python
racine = Path("/tmp")
fichier = racine / "donnees" / "rapport.csv"
print(fichier)   # /tmp/donnees/rapport.csv
```

L'opérateur fonctionne aussi entre `Path` et `str`, dans les deux sens :

```python
Path("/tmp") / "x"           # /tmp/x
"/tmp" / Path("x")           # /tmp/x
```

Aucun risque d'oublier ou de doubler un séparateur : `pathlib` s'en
occupe.

### Comparaison avec l'ancienne approche

| Tâche                          | Ancien (`os.path`)                        | Nouveau (`pathlib`)             |
|--------------------------------|-------------------------------------------|---------------------------------|
| Assembler                      | `os.path.join("/tmp", "x", "y")`          | `Path("/tmp") / "x" / "y"`      |
| Nom de fichier                 | `os.path.basename(p)`                     | `p.name`                        |
| Dossier parent                 | `os.path.dirname(p)`                      | `p.parent`                      |
| Extension                      | `os.path.splitext(p)[1]`                  | `p.suffix`                      |
| Existence                      | `os.path.exists(p)`                       | `p.exists()`                    |
| Chemin absolu                  | `os.path.abspath(p)`                      | `p.resolve()`                   |
| Dossier courant                | `os.getcwd()`                             | `Path.cwd()`                    |

Le nouveau code tient sur **une ligne** et se lit comme du français.

## 1.4 Les attributs d'un chemin

Une fois un `Path` construit, on accède à ses morceaux sans aucun
calcul :

```python
p = Path("/home/ada/projets/notes.txt")

p.name        # 'notes.txt'         le dernier composant
p.stem        # 'notes'             le nom sans la dernière extension
p.suffix      # '.txt'              la dernière extension
p.suffixes    # ['.txt']            toutes les extensions
p.parent      # PosixPath('/home/ada/projets')   le dossier
p.parts       # ('/', 'home', 'ada', 'projets', 'notes.txt')
```

Le pluriel `parents` est un peu différent : il renvoie **tous** les
dossiers parents, du plus proche au plus lointain :

```python
list(p.parents)
# [PosixPath('/home/ada/projets'),
#  PosixPath('/home/ada'),
#  PosixPath('/home'),
#  PosixPath('/')]
```

### Cas particulier : plusieurs extensions

Pour un fichier comme `archive.tar.gz`, `suffix` et `suffixes`
divergent :

```python
p = Path("archive.tar.gz")
p.suffix      # '.gz'           juste la dernière
p.suffixes    # ['.tar', '.gz'] toutes
p.stem        # 'archive.tar'   tout sauf la dernière
```

Pour récupérer le nom « brut » sans aucune extension, on retire
toutes les `suffixes` une par une — un cas où l'on revient sur du
travail manuel.

## 1.5 Changer un morceau

`Path` est **immuable** : aucune méthode ne modifie l'objet
existant. On reconstruit toujours un nouveau chemin :

```python
p = Path("/tmp/notes.txt")
p.with_suffix(".md")      # PosixPath('/tmp/notes.md')
p.with_name("autre.txt")  # PosixPath('/tmp/autre.txt')
p.with_stem("autre")      # PosixPath('/tmp/autre.txt')   (Python 3.9+)
```

L'objet `p` d'origine est inchangé. C'est exactement comme pour les
chaînes de caractères : `"abc".upper()` renvoie une nouvelle chaîne.

## À retenir

- `from pathlib import Path` suffit pour démarrer.
- L'opérateur `/` assemble proprement les morceaux, sans souci de
  séparateur.
- Les attributs (`name`, `stem`, `suffix`, `parent`, `parts`) renvoient
  des morceaux **sans rien calculer** soi-même.
- `Path` est immuable : `with_suffix`, `with_name`, `with_stem`
  renvoient un **nouvel** objet.
- `pathlib` remplace `os.path` ligne pour ligne, en plus lisible.

## Démo

Exécuter `01_demo_path.py`.
