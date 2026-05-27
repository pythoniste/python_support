# 02 — Types et validation

## 2.1 Tout arrive en `str`

Quand le shell lance un programme, **tous** les arguments transmis sont
des chaînes. Même `python3 outil.py 42` : `args.nombre` vaut la chaîne
`"42"`, pas l'entier `42`. À nous de convertir — ou plutôt, à
`argparse` de le faire.

## 2.2 `type=...` : convertir et valider

Le paramètre `type` accepte **n'importe quel appelable** prenant une
chaîne et renvoyant la valeur convertie. Les classes natives marchent
telles quelles :

```python
parser.add_argument("n", type=int)         # convertit en entier
parser.add_argument("--seuil", type=float) # convertit en flottant
```

Si la conversion échoue (`int("abc")` lève une exception), `argparse`
attrape l'erreur, l'affiche proprement et sort avec le code `2`. Aucun
`try/except` à écrire.

On peut aussi passer une fonction maison :

```python
def chemin_existant(s: str) -> str:
    import os
    if not os.path.exists(s):
        raise argparse.ArgumentTypeError(f"{s!r} n'existe pas")
    return s

parser.add_argument("fichier", type=chemin_existant)
```

La règle est simple : si la fonction lève une exception (idéalement
`argparse.ArgumentTypeError`), `argparse` la convertit en message
d'erreur lisible.

## 2.3 `choices=[...]` : restreindre les valeurs acceptables

Quand on veut un argument parmi une liste fermée :

```python
parser.add_argument("--couleur", choices=["rouge", "vert", "bleu"])
```

Toute valeur en dehors est rejetée :

```
$ python3 outil.py --couleur jaune
usage: ...
outil.py: error: argument --couleur: invalid choice: 'jaune'
(choose from 'rouge', 'vert', 'bleu')
```

`choices` se combine avec `type` :

```python
parser.add_argument("--niveau", type=int, choices=[1, 2, 3])
```

## 2.4 `default=...` : valeur si l'argument est omis

Pour les optionnels, `default` fixe la valeur retournée quand
l'utilisateur ne passe rien :

```python
parser.add_argument("--port", type=int, default=8080)
```

Sans `default`, un optionnel absent vaut `None`. Préciser un `default`
explicite rend le code appelant plus simple : pas besoin de tester
`if args.port is None`.

## 2.5 `required=True` : rendre un optionnel obligatoire

Par nature, un argument commençant par `--` est **facultatif**.
Parfois, on veut quand même qu'il soit obligatoire, sans lui retirer
son nom de drapeau (plus lisible que la position) :

```python
parser.add_argument("--entree", required=True)
```

Si l'utilisateur l'oublie, `argparse` proteste et sort avec le code
`2`. À utiliser avec modération : un argument vraiment obligatoire
gagne souvent à être positionnel.

## 2.6 `nargs=...` : zéro, un, plusieurs valeurs

Par défaut, un argument prend **une seule** valeur. Le paramètre
`nargs` change la donne.

| Valeur de `nargs` | Sémantique                                       |
|-------------------|--------------------------------------------------|
| `"?"`             | Zéro ou une valeur (utilise `default` sinon).    |
| `"*"`             | Zéro ou plusieurs valeurs (liste, vide possible).|
| `"+"`             | Une ou plusieurs valeurs (liste, jamais vide).   |
| Entier `N`        | Exactement `N` valeurs (liste de longueur fixe). |

Exemples :

```python
# Zéro ou un fichier ; valeur "stdin" par défaut.
parser.add_argument("fichier", nargs="?", default="stdin")

# Un ou plusieurs fichiers (au moins un).
parser.add_argument("fichiers", nargs="+")

# Exactement trois coordonnées.
parser.add_argument("point", nargs=3, type=float)
```

Quand `nargs` est différent de `1`, **la valeur récupérée est toujours
une liste**, même si elle ne contient qu'un élément :

```
$ python3 outil.py a b c
args.fichiers == ["a", "b", "c"]
```

## 2.7 `metavar` : changer l'étiquette dans l'aide

Par défaut, l'aide affiche le nom de l'argument en majuscules :

```
--port PORT
```

`metavar` permet de remplacer cette étiquette par quelque chose de
plus parlant :

```python
parser.add_argument("--port", type=int, metavar="NUMERO")
```

```
--port NUMERO
```

C'est purement cosmétique, mais cela améliore beaucoup la lisibilité
de `--help`.

## À retenir

- Sans `type`, toutes les valeurs sont des **chaînes**.
- `type=int`, `type=float` ou une fonction maison convertissent et
  valident en une ligne.
- `choices=[...]` limite l'ensemble des valeurs autorisées.
- `default=...` fixe la valeur retenue si l'argument est absent.
- `required=True` rend un optionnel obligatoire.
- `nargs` accepte `"?"`, `"*"`, `"+"` ou un entier ; renvoie une liste
  dès qu'il y a plus d'une valeur.
- `metavar` change l'étiquette affichée dans `--help`.

## Démo

Exécuter `02_demo_types.py` avec différentes valeurs (valides, invalides,
au-delà des `choices`, sans arguments), puis avec `--help`.
