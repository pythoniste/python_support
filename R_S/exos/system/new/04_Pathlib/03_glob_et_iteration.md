# 03 — Parcourir et filtrer

Trois méthodes suffisent pour parcourir un système de fichiers depuis
un `Path` : `iterdir`, `glob` et `rglob`. Elles renvoient toutes des
**itérateurs** d'objets `Path`, donc paresseuses : aucun coût mémoire
même sur des arborescences gigantesques.

## 3.1 Lister un dossier : `.iterdir()`

`.iterdir()` énumère les entrées **directes** d'un dossier (un seul
niveau, sans descendre dans les sous-dossiers) :

```python
dossier = Path("/tmp")

for entree in dossier.iterdir():
    print(entree)
```

Chaque `entree` est déjà un `Path` complet, prêt à être interrogé
(`.is_file()`, `.is_dir()`, `.stat()`, etc.). L'ordre n'est **pas**
garanti — c'est celui du système de fichiers. Pour un ordre stable,
on convertit en liste et on trie :

```python
for entree in sorted(dossier.iterdir()):
    print(entree)
```

`.iterdir()` lève `FileNotFoundError` si le chemin n'existe pas, et
`NotADirectoryError` si c'est un fichier.

## 3.2 Filtrer par motif : `.glob(...)`

`.glob(motif)` renvoie les entrées du dossier dont le nom **correspond
au motif**. Toujours sur un seul niveau (sauf indication contraire).

```python
dossier = Path(".")

for p in dossier.glob("*.py"):
    print(p)
```

Le terme *glob* vient d'Unix ; ce sont des motifs simples, **pas**
des expressions régulières.

### Les caractères jokers

| Motif       | Correspond à                                |
|-------------|---------------------------------------------|
| `*`         | n'importe quelle suite de caractères (sauf `/`) |
| `?`         | exactement un caractère                     |
| `[abc]`     | un seul caractère parmi `a`, `b` ou `c`     |
| `[a-z]`     | un seul caractère dans la plage `a` à `z`   |
| `[!abc]`    | un seul caractère **différent** de `a`, `b`, `c` |

Quelques exemples concrets :

```python
Path(".").glob("*.py")        # tous les .py du dossier courant
Path(".").glob("test_*.py")   # uniquement ceux qui commencent par test_
Path(".").glob("img_???.jpg") # img_001.jpg, img_abc.jpg, etc.
Path(".").glob("[A-Z]*.md")   # markdown dont le nom commence par une majuscule
```

À retenir : `*` ne traverse **pas** les `/`. `*.py` ne descendra
jamais dans un sous-dossier.

## 3.3 Parcours récursif : `.rglob(...)`

Pour descendre dans toute l'arborescence, deux options équivalentes :

```python
Path(".").rglob("*.py")         # forme courte
Path(".").glob("**/*.py")       # forme longue, avec le motif spécial **
```

Le motif `**` signifie « n'importe quel nombre de dossiers
intermédiaires, y compris zéro ». `rglob(motif)` est strictement
équivalent à `glob("**/" + motif)`.

Exemple : compter tous les fichiers Python d'un projet :

```python
total = sum(1 for _ in Path(".").rglob("*.py"))
print(total, "fichiers Python")
```

Attention : sur de gros dossiers (`/`, `~`, etc.), un `rglob` peut
prendre **beaucoup** de temps et générer des millions d'entrées.
Toujours partir d'un point précis.

## 3.4 Filtrer plus finement

Le motif glob est simple par construction. Pour des critères plus
riches (taille, date, contenu), on combine `rglob` et une
condition Python :

```python
# Tous les .py de plus de 10 ko
gros = [
    p for p in Path(".").rglob("*.py")
    if p.is_file() and p.stat().st_size > 10_000
]
```

Le `p.is_file()` est utile car `rglob("*.py")` peut, en théorie,
remonter aussi des **liens** ou des **dossiers** dont le nom finit
par `.py`.

## 3.5 Itérateur, pas liste

Toutes ces méthodes renvoient des **itérateurs**. Conséquences :

- On peut passer dessus une seule fois ; pour les réutiliser, on
  les convertit en liste : `list(dossier.glob("*.py"))`.
- Aucune mémoire n'est consommée à l'avance.
- Une boucle peut s'arrêter dès qu'un élément suffit (`break`,
  `next(...)`).

```python
# Le premier .py rencontré, sans tout charger
premier = next(Path(".").rglob("*.py"), None)
```

## À retenir

- `.iterdir()` : un seul niveau, sans filtre.
- `.glob(motif)` : un seul niveau, avec motif glob.
- `.rglob(motif)` : récursif, avec motif glob.
- Les motifs `*`, `?`, `[abc]` sont **glob**, pas regex.
- Toutes ces méthodes renvoient des **itérateurs** d'objets `Path`.

## Démo

Exécuter `03_demo_glob.py`.
