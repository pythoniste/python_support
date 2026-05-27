# 01 — Ouvrir et lire un fichier texte

## 1.1 La fonction `open()`

En Python, on ouvre un fichier avec la fonction intégrée `open()` :

```python
f = open(chemin, mode, encoding="utf-8")
```

Trois arguments comptent pour débuter :

- **`chemin`** : une chaîne ou un objet `Path` (chapitre 04) qui
  désigne le fichier.
- **`mode`** : pour quoi faire — lire, écrire, ajouter…
- **`encoding`** : la règle qui convertit les octets du disque en
  caractères Python. **À toujours préciser** en mode texte.

Le résultat est un **objet fichier** : une ressource du système
d'exploitation, qu'il faut refermer une fois le travail terminé.

## 1.2 Toujours utiliser `with`

Comme pour les sockets (vu en réseau), un fichier ouvert est une
ressource OS limitée. S'il n'est pas refermé, il fuit. La forme
canonique est donc :

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
# Ici, f est déjà fermé automatiquement, même si une exception
# a été levée à l'intérieur du bloc.
```

À **éviter** :

```python
f = open("notes.txt", "r")
contenu = f.read()
f.close()   # oublié si une exception se déclenche entre les deux
```

Dans tout le cours, on utilisera **systématiquement** la forme `with`.

## 1.3 Tableau des modes les plus utiles

| Mode  | Effet                                                  |
|-------|--------------------------------------------------------|
| `"r"` | Lecture seule, texte (défaut)                          |
| `"rb"`| Lecture seule, **binaire** (octets bruts)              |
| `"w"` | Écriture, écrase le fichier existant                   |
| `"a"` | Écriture, **ajoute** à la fin                          |
| `"x"` | Création exclusive : échoue si le fichier existe       |
| `"+"` | Combiné aux précédents : lecture **et** écriture       |

Le module 02 reviendra sur les modes d'écriture. Le module 03 expliquera
quand passer en `"b"` (binaire).

## 1.4 Quatre façons de lire

Une fois le fichier ouvert en mode texte, plusieurs méthodes existent.
Soit le fichier `poeme.txt` qui contient trois lignes :

```
roses are red
violets are blue
sugar is sweet
```

### 1.4.1 `f.read()` — tout d'un coup

```python
with open("poeme.txt", "r", encoding="utf-8") as f:
    tout = f.read()
print(tout)     # une seule chaîne avec les '\n' inclus
```

Pratique pour les **petits** fichiers. À éviter sur un fichier de
plusieurs gigaoctets : tout est chargé en mémoire d'un coup.

### 1.4.2 `f.readline()` — ligne par ligne, à la demande

```python
with open("poeme.txt", "r", encoding="utf-8") as f:
    premiere = f.readline()
    deuxieme = f.readline()
```

Renvoie une chaîne **avec** le `\n` final (sauf à la toute dernière
ligne si le fichier ne se termine pas par un retour à la ligne). Quand
la fin du fichier est atteinte, renvoie une chaîne vide `""`.

### 1.4.3 `f.readlines()` — la liste de toutes les lignes

```python
with open("poeme.txt", "r", encoding="utf-8") as f:
    lignes = f.readlines()
# lignes == ['roses are red\n', 'violets are blue\n', 'sugar is sweet\n']
```

Pratique mais charge **tout** en mémoire, comme `read()`.

### 1.4.4 Itérer directement sur `f` — la forme à privilégier

```python
with open("poeme.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        print(ligne.rstrip("\n"))
```

C'est la forme **recommandée** : elle ne charge qu'une ligne à la fois
en mémoire, fonctionne aussi bien sur 10 lignes que sur 10 millions, et
se lit très naturellement.

## 1.5 Le `\n` traînant

Toutes les méthodes qui renvoient des lignes les renvoient avec le
**`\n`** terminal inclus. Pour le retirer, on utilise `.rstrip("\n")`
(seulement le retour à la ligne) ou `.strip()` (les espaces
environnants aussi) :

```python
for ligne in f:
    ligne = ligne.rstrip("\n")   # garde les espaces internes
    ...
```

Oublier ce strip est l'erreur la plus fréquente : un `print(ligne)`
produira alors une ligne vide entre chaque affichage (le `\n` du fichier
plus celui ajouté par `print`).

## 1.6 Encodage : toujours le préciser

```python
with open(chemin, "r", encoding="utf-8") as f:
    ...
```

Si on omet `encoding=`, Python utilise le **réglage du système**, qui
varie selon l'OS et la langue. Un code qui marche sous Linux peut
échouer sous Windows. La règle est simple : **toujours préciser
`encoding="utf-8"`** en mode texte, sauf raison contraire.

Le module 03 reviendra sur les encodages exotiques et la gestion des
erreurs (`errors="replace"`).

## À retenir

- `open(chemin, mode, encoding="utf-8")` ouvre un fichier.
- Toujours dans un bloc **`with`**, jamais à la main.
- Quatre méthodes de lecture : `read()`, `readline()`, `readlines()`,
  itération `for ligne in f:`.
- L'itération est la forme à privilégier (mémoire constante).
- Toutes les lignes lues incluent le `\n` final : `.rstrip("\n")` pour
  le retirer.
- Toujours préciser `encoding="utf-8"` en mode texte.

## Démo

Exécuter `01_demo_lire.py`.
