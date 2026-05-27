# 03 — Actions courantes

## 3.1 Qu'est-ce qu'une *action* ?

Par défaut, quand `argparse` rencontre un argument, il **stocke** la
valeur fournie dans le `Namespace` (action `"store"`). Mais ce n'est
pas toujours ce que l'on veut : pour un drapeau booléen, il n'y a
*pas* de valeur à fournir — la présence du drapeau suffit. Pour `-v`
répété, on veut compter les occurrences. Pour `--include`, on veut
accumuler une liste.

Le paramètre `action="..."` de `add_argument` choisit la stratégie à
appliquer. Voici les quatre les plus utiles au quotidien.

## 3.2 `action="store_true"` — drapeau booléen vrai

L'argument ne prend **aucune valeur**. S'il est présent, il vaut
`True` ; absent, il vaut `False`.

```python
parser.add_argument("--verbeux", "-v", action="store_true")
```

```
$ python3 outil.py            # args.verbeux == False
$ python3 outil.py --verbeux  # args.verbeux == True
$ python3 outil.py -v         # args.verbeux == True
```

C'est le mode standard pour un drapeau de type « activer/désactiver ».
À noter : avec `store_true`, le `default` est implicitement `False` —
inutile de le préciser.

## 3.3 `action="store_false"` — drapeau booléen faux

Symétrique du précédent. La présence du drapeau **abaisse** la valeur
à `False`, l'absence la laisse à `True` (default implicite).

```python
parser.add_argument("--couleur", action="store_false")
```

```
$ python3 outil.py            # args.couleur == True (par défaut)
$ python3 outil.py --couleur  # args.couleur == False
```

C'est pratique pour les options du genre `--sans-couleur`, `--no-cache`,
quand le comportement par défaut est *avec*. Pour éviter la
confusion entre nom et signification, on choisit souvent un nom
explicitement négatif :

```python
parser.add_argument(
    "--sans-couleur",
    dest="couleur",            # nom de l'attribut dans le Namespace
    action="store_false",
)
```

L'attribut récupéré est alors `args.couleur` (lisible dans le code),
tandis que le drapeau exposé à l'utilisateur reste `--sans-couleur`.

## 3.4 `action="count"` — compter les occurrences

Très utile pour les niveaux de verbosité, où l'utilisateur peut taper
`-v`, `-vv` ou `-vvv` pour ajuster.

```python
parser.add_argument("-v", "--verbeux", action="count", default=0)
```

```
$ python3 outil.py             # args.verbeux == 0
$ python3 outil.py -v          # args.verbeux == 1
$ python3 outil.py -vv         # args.verbeux == 2
$ python3 outil.py -vvv        # args.verbeux == 3
$ python3 outil.py -v -v -v    # args.verbeux == 3 (équivalent)
```

Toujours **fixer un `default=0`** : sans cela, l'attribut vaut `None`
quand le drapeau est absent, ce qui complique les comparaisons.

## 3.5 `action="append"` — accumuler une liste

Quand on veut autoriser l'utilisateur à passer plusieurs fois le même
drapeau, chaque occurrence ajoutant une valeur à une liste :

```python
parser.add_argument("--inclure", action="append")
```

```
$ python3 outil.py --inclure a --inclure b --inclure c
args.inclure == ["a", "b", "c"]
```

Si le drapeau n'est jamais passé, l'attribut vaut `None` — pas
`[]`. Pour éviter ce piège, fixer un `default=[]` (et attention : ce
default est partagé entre invocations dans un script long, mais en
pratique sans conséquence pour une CLI lancée une seule fois).

Différence avec `nargs="+"` : `nargs="+"` consomme **plusieurs valeurs
sous un seul drapeau** (`--inclure a b c`), tandis que `append`
attend **un drapeau par valeur** (`--inclure a --inclure b --inclure c`).
Les deux ont leur place selon l'usage.

## 3.6 Tableau récapitulatif

| `action`        | Présence du drapeau                | Type final           |
|-----------------|------------------------------------|----------------------|
| `"store"` (def.)| stocke la valeur fournie           | dépend de `type`     |
| `"store_true"`  | passe à `True` (default `False`)   | `bool`               |
| `"store_false"` | passe à `False` (default `True`)   | `bool`               |
| `"count"`       | incrémente un compteur             | `int`                |
| `"append"`      | ajoute la valeur à la liste        | `list`               |

## À retenir

- Une *action* dicte ce que fait `argparse` quand il rencontre un
  argument.
- `store_true` / `store_false` : drapeaux booléens sans valeur.
- `count` : `-v`, `-vv`, `-vvv` pour graduer un comportement.
- `append` : un drapeau répétable qui accumule une liste.
- Toujours fixer `default=0` pour `count` et `default=[]` pour
  `append` afin d'éviter le `None` traître.

## Démo

Exécuter `03_demo_actions.py` plusieurs fois avec `-v`, `-vv`, et
plusieurs `--inclure` pour observer le résultat.
