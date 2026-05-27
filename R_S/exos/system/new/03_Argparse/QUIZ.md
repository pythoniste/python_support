# Quiz de validation — dossier 03_Argparse

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la différence entre un argument **positionnel** et
un argument **optionnel** dans `argparse` ? Comment `argparse` les
distingue-t-il à la déclaration ?

**Q2.** Que renvoie l'expression suivante quand l'utilisateur tape
`python3 outil.py 42` ? Et avec `type=int` ?

```python
parser.add_argument("n")            # cas A
parser.add_argument("n", type=int)  # cas B
```

**Q3.** À quoi servent respectivement `nargs="?"`, `nargs="*"`,
`nargs="+"` et `nargs=3` ? Lequel **garantit** une liste non vide ?

**Q4.** Quelle est la différence entre `action="store_true"` et
`action="count"` ? Donner un cas d'usage typique pour chacun.

**Q5.** En une CLI à sous-commandes, comment dispatcher proprement
vers la bonne fonction selon la sous-commande choisie ? Citer le
patron en deux lignes maximum.

**Q6.** Pourquoi écrit-on `parser.add_argument("--from", dest="depuis")`
plutôt que simplement `parser.add_argument("--from")` ?

---

## Réponses

**R1.** Un argument **positionnel** est **obligatoire** et identifié
par sa **position** dans la ligne de commande ; son nom de déclaration
ne commence pas par `-`. Un argument **optionnel** est **facultatif**
et identifié par un **drapeau** (`--option` ou `-o`) ; son nom de
déclaration commence par `-` ou `--`. C'est cette première lettre qui
sert de signal à `argparse`.

**R2.** Cas A : `args.n` vaut la **chaîne** `"42"` — tous les
arguments arrivent en `str` par défaut. Cas B : `args.n` vaut
l'**entier** `42`, et si l'utilisateur passe `"abc"`, `argparse`
affiche un message d'erreur lisible et sort avec le code `2`, sans
qu'on ait besoin d'écrire un `try/except`.

**R3.** `nargs="?"` : zéro ou une valeur (utilise `default` si
absent). `nargs="*"` : zéro ou plusieurs valeurs, liste vide possible.
`nargs="+"` : une ou plusieurs valeurs, **liste jamais vide** — c'est
celui qui garantit le non-vide. `nargs=3` : exactement trois valeurs,
liste de longueur fixe. Dès que `nargs` n'est pas `1` ou non précisé,
la valeur récupérée est une **liste**.

**R4.** `store_true` est un drapeau **booléen** : présent il vaut
`True`, absent il vaut `False`. Aucune valeur n'est consommée après
lui. Typique pour `--verbeux`, `--brouillon`. `count` **compte** les
occurrences du même drapeau : `-v` vaut 1, `-vv` vaut 2, `-vvv` vaut
3. Typique pour graduer la verbosité d'un outil.

**R5.** Le patron classique est d'attacher une fonction à chaque
sous-parser avec `set_defaults(func=cmd_xxx)`, puis dans le main :

```python
args = parser.parse_args()
args.func(args)
```

C'est `args.func` qui dispatche, sans `if/elif` à rallonge.

**R6.** Parce que `from` est un **mot-clé réservé** de Python. On ne
peut pas écrire `args.from`. Le paramètre `dest="depuis"` indique à
`argparse` de ranger la valeur dans `args.depuis`, ce qui rend le code
appelant légal. Le drapeau exposé à l'utilisateur reste `--from`.
