# 01 — Premier parser

## 1.1 Pourquoi `argparse` plutôt que `sys.argv` ?

Tout programme Python reçoit ses arguments dans la liste `sys.argv` :
`sys.argv[0]` est le nom du script, et `sys.argv[1:]` sont les chaînes
brutes tapées après. À la main, on peut très vite s'en sortir pour un
script jouet :

```python
import sys
nom = sys.argv[1]
print(f"Bonjour, {nom}")
```

Mais dès qu'on veut quelque chose d'un peu sérieux, la liste de tâches
explose :

- vérifier qu'il y a le bon nombre d'arguments ;
- convertir les chaînes en `int` ou en `float` ;
- distinguer les arguments positionnels (obligatoires, dans l'ordre)
  des options (`--verbeux`, `-n 3`, etc.) ;
- gérer les abréviations (`-h` ou `--help`) ;
- afficher un message d'usage propre en cas d'erreur ;
- générer une page d'aide.

`argparse`, fourni dans la **bibliothèque standard**, fait tout cela
pour nous. Aucune dépendance à installer.

## 1.2 Le squelette en quatre étapes

Toute CLI écrite avec `argparse` suit le même plan :

```python
import argparse

# 1. Créer le parser.
parser = argparse.ArgumentParser(
    prog="mon_outil",
    description="Une démo minimale.",
)

# 2. Déclarer les arguments attendus.
parser.add_argument("nom")                       # positionnel
parser.add_argument("--majuscules", "-m")        # optionnel

# 3. Analyser la ligne de commande (sys.argv par défaut).
args = parser.parse_args()

# 4. Utiliser les valeurs récupérées.
print(args.nom, args.majuscules)
```

Les quatre étapes restent **toujours** identiques. Ce qui change, c'est
le détail des `add_argument(...)`.

## 1.3 `ArgumentParser(prog, description)`

Le constructeur du parser accepte deux paramètres très utiles dès le
départ :

| Paramètre     | Effet                                                          |
|---------------|----------------------------------------------------------------|
| `prog`        | Nom du programme affiché dans l'aide (sinon `sys.argv[0]`).    |
| `description` | Phrase affichée en haut de `--help`.                           |

D'autres existent (`epilog`, `formatter_class`...), à découvrir le jour
où on en a besoin.

## 1.4 Positionnel vs optionnel

`add_argument` distingue deux familles d'arguments selon **la première
lettre** du nom déclaré :

### Positionnel — obligatoire, identifié par sa position

```python
parser.add_argument("fichier")
```

Le nom **ne commence pas par `-`**. La valeur est obligatoire ; on
l'appelle dans l'ordre où elle apparaît :

```
$ python3 outil.py rapport.txt
```

On y accède via `args.fichier`.

### Optionnel — facultatif, identifié par un drapeau

```python
parser.add_argument("--sortie", "-s")
```

Le nom **commence par `--`** (forme longue) et peut être doublé d'une
forme courte commençant par `-`. L'utilisateur le passe sous la forme
`--sortie nom.txt` ou `-s nom.txt`. S'il n'est pas fourni, la valeur
vaut `None`.

On y accède via `args.sortie` (le `--` est retiré, les `-` deviennent
des `_`).

## 1.5 `parse_args()`

L'appel `args = parser.parse_args()` lit `sys.argv[1:]` (par défaut),
le valide, et renvoie un objet **`argparse.Namespace`**. C'est un
simple conteneur d'attributs : `args.fichier`, `args.sortie`, etc.

En cas d'erreur (argument manquant, valeur invalide), `argparse` :

- affiche un message sur **stderr** ;
- appelle `sys.exit(2)`.

Autrement dit, on n'a **rien à coder** pour gérer les mauvais usages :
le programme s'arrête tout seul, avec un code retour conventionnel
pour signaler une erreur d'invocation.

## 1.6 `--help` automatique

Toute CLI construite avec `argparse` répond gratuitement à `-h` et à
`--help`. Plus la peine de l'écrire à la main :

```
$ python3 mon_outil.py --help
usage: mon_outil [-h] [--majuscules MAJUSCULES] nom

Une démo minimale.

positional arguments:
  nom

options:
  -h, --help            show this help message and exit
  --majuscules MAJUSCULES, -m MAJUSCULES
```

On peut enrichir cette page en passant `help="..."` à chaque
`add_argument` :

```python
parser.add_argument("nom", help="prénom à saluer")
parser.add_argument("--majuscules", "-m", help="convertir en majuscules")
```

C'est la **première bonne habitude** : un `help` à chaque argument.

## À retenir

- `argparse` est dans la **stdlib** : zéro dépendance.
- Quatre étapes : créer le parser, déclarer les arguments, parser,
  utiliser.
- Positionnel = nom sans `-` (obligatoire) ; optionnel = nom avec
  `--` (facultatif).
- `parse_args()` renvoie un `Namespace` ; les erreurs sortent en
  code 2 sur stderr.
- `--help` et `-h` sont gérés automatiquement.

## Démo

Exécuter `01_demo_parser.py` avec différentes lignes de commande,
puis avec `--help`.
