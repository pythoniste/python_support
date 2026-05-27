# 02 — Les f-strings

## 2.1 Interpoler, c'est insérer dans une chaîne

Une **f-string** (chaîne formatée) est une chaîne préfixée par `f` dans
laquelle on peut placer des **expressions Python** entre accolades.
À l'exécution, chaque expression est évaluée et son résultat remplace
les accolades :

```python
nom = "Ada"
age = 36
print(f"{nom} a {age} ans")        # Ada a 36 ans
```

C'est l'équivalent moderne et concis de :

```python
print(nom + " a " + str(age) + " ans")       # concaténation pénible
print("%s a %d ans" % (nom, age))             # vieux style printf
print("{} a {} ans".format(nom, age))         # str.format()
```

En Python 3.6+, on utilise **toujours** les f-strings pour les chaînes
formatées qu'on construit nous-mêmes.

## 2.2 N'importe quelle expression entre `{}`

Le contenu des accolades n'est pas limité à un nom de variable. C'est
n'importe quelle expression Python valide :

```python
x = 7
print(f"Carré : {x * x}")                       # Carré : 49
print(f"Longueur : {len('bonjour')}")           # Longueur : 7
print(f"Majuscule : {nom.upper()}")             # Majuscule : ADA
print(f"Inverse : {1 / x:.4f}")                 # Inverse : 0.1429
print(f"{'positif' if x > 0 else 'négatif'}")   # positif
```

On peut même appeler des fonctions :

```python
from math import sqrt
print(f"sqrt(2) = {sqrt(2)}")                   # sqrt(2) = 1.4142135623730951
```

## 2.3 Format spec : la syntaxe `:` après l'expression

Après l'expression, on peut ajouter `:` suivi d'une **spécification de
format**. Sa structure générale est :

```
{expression:[remplissage][alignement][signe][largeur][,][.précision][type]}
```

Pas besoin de tout retenir : voici les éléments les plus utiles.

### Largeur et alignement

| Code  | Effet                                     |
|-------|-------------------------------------------|
| `<`   | Aligner à **gauche**                      |
| `>`   | Aligner à **droite** (défaut pour nombres)|
| `^`   | **Centrer**                               |

```python
print(f"[{'a':<5}]")     # [a    ]
print(f"[{'a':>5}]")     # [    a]
print(f"[{'a':^5}]")     # [  a  ]
print(f"[{'a':*^5}]")    # [**a**]  remplissage par '*'
```

Le `5` est la **largeur minimale** en caractères. Si le contenu est plus
long, il n'est pas tronqué — la largeur n'est qu'un minimum.

### Précision et type pour les nombres

| Code   | Effet                                         |
|--------|-----------------------------------------------|
| `.2f`  | Flottant avec exactement 2 décimales          |
| `.3e`  | Notation scientifique, 3 chiffres après le `.`|
| `.0f`  | Flottant entier (pas de décimales)            |
| `d`    | Entier décimal                                |
| `b`    | Binaire (`0b1010` sans le préfixe)            |
| `x`    | Hexadécimal minuscule                         |
| `%`    | Pourcentage (multiplie par 100, ajoute `%`)   |

```python
pi = 3.14159265
print(f"{pi:.2f}")           # 3.14
print(f"{pi:.4f}")           # 3.1416
print(f"{pi:10.2f}")         # '      3.14'   largeur 10, 2 décimales
print(f"{0.05:.1%}")         # 5.0%
print(f"{255:b}")            # 11111111
print(f"{255:x}")            # ff
```

### Séparateur de milliers

Une virgule dans la format spec insère le **séparateur anglo-saxon** des
milliers ; un blanc souligné fait pareil avec `_` :

```python
n = 1234567
print(f"{n:,}")              # 1,234,567
print(f"{n:_}")              # 1_234_567
print(f"{n:,.2f}")           # 1,234,567.00
```

(Le séparateur français « espace » n'est pas fourni nativement ; on le
fabrique avec `f"{n:,}".replace(",", " ")`.)

## 2.4 Combiner largeur, précision et alignement

Tout se cumule dans la même format spec :

```python
for nom, prix in [("café", 1.5), ("croissant", 1.2), ("éclair", 3.45)]:
    print(f"{nom:<12} {prix:>6.2f} €")
```

Sortie :

```
café           1.50 €
croissant      1.20 €
éclair         3.45 €
```

Premier champ : aligné à **gauche** sur 12 caractères. Second : aligné
à **droite** sur 6, avec 2 décimales.

## 2.5 Le format de débogage `{x=}`

Depuis Python 3.8, ajouter `=` à l'intérieur des accolades affiche
**à la fois** l'expression et sa valeur. C'est la manière la plus rapide
de débugger sans écrire deux fois la variable :

```python
x = 42
print(f"{x=}")                  # x=42
print(f"{x * 2=}")              # x * 2=84
print(f"{len('bonjour')=}")     # len('bonjour')=7
```

On peut combiner avec une format spec :

```python
import math
print(f"{math.pi=:.3f}")        # math.pi=3.142
```

C'est un raccourci très utilisé pour tracer rapidement l'état d'un
programme sans alourdir les messages.

## À retenir

- Une f-string interpole **n'importe quelle expression** entre `{}`.
- Après `:`, on contrôle alignement (`<>^`), largeur, précision (`.2f`)
  et séparateur de milliers (`,`).
- Le format `{x=}` affiche le nom **et** la valeur — idéal pour débugger.
- Les autres formes (`%`, `.format()`) restent valides mais on préfère
  les f-strings depuis Python 3.6.

## Démo

Exécuter `02_demo_fstrings.py`.
