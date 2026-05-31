# Conventions de rédaction des notebooks

Guide obligatoire pour écrire ou modifier un notebook dans `Bibliotheque_notebooks/`. Ces conventions garantissent la **cohérence pédagogique**, la **progressivité stricte**, et la compatibilité avec les cinq formats de formation (Initiation 5 j/3 j, Intermédiaire 5 j/3 j, Avancé 5 j).

---

## Table des matières

1. [Règle d'or : progressivité stricte](#1-règle-dor--progressivité-stricte)
2. [En-tête de prérequis obligatoire](#2-en-tête-de-prérequis-obligatoire)
3. [Une cellule = un concept](#3-une-cellule--un-concept)
4. [Patterns d'affichage selon le niveau](#4-patterns-daffichage-selon-le-niveau)
5. [Style d'exercices selon le niveau](#5-style-dexercices-selon-le-niveau)
6. [Tags de cellule](#6-tags-de-cellule)
7. [Format des corrections](#7-format-des-corrections)
8. [Utilisation du helper `verifier_et_reveler`](#8-utilisation-du-helper-verifier_et_reveler)
9. [Structure standard d'un notebook](#9-structure-standard-dun-notebook)
10. [Table des notions disponibles par notebook](#10-table-des-notions-disponibles-par-notebook)
11. [Checklist avant commit](#11-checklist-avant-commit)

---

## 1. Règle d'or : progressivité stricte

Un notebook n'utilise **jamais** une notion introduite dans un notebook postérieur. Aucune forward reference n'est tolérée, y compris dans :

- le code des exemples
- le code des exercices (énoncés et corrections)
- les commentaires
- le formatage d'affichage
- les type hints

### Si tu as besoin d'une notion pas encore vue, trois options :

1. **Ne pas l'utiliser** — chercher une alternative avec les outils déjà connus.
2. **Remplacer** par un équivalent disponible (ex. `print("label :", x)` au lieu de `f"{x}"`).
3. **Déplacer la notion plus tôt** dans le plan — à valider avec l'auteur.

### Pourquoi c'est important

Un stagiaire qui voit un `f"{x:.2f}"` au chapitre 1 alors que les f-strings sont présentées au chapitre 3 reçoit un message contradictoire : soit il demande des explications et interrompt le cours, soit il ignore la syntaxe et rate la compréhension. Les deux sont mauvais pour l'apprentissage.

---

## 2. En-tête de prérequis obligatoire

Chaque notebook commence par **deux cellules markdown obligatoires** : objectifs + prérequis.

### Modèle

```markdown
# <Numéro> — <Titre>

## Objectifs pédagogiques

À la fin de ce notebook, vous saurez :
- <compétence 1>
- <compétence 2>
- <compétence 3>

## Prérequis — ce que vous connaissez déjà

À ce stade de la formation, vous savez :
- <notion 1>
- <notion 2>
- <notion 3>

Ce que nous n'avons **pas encore vu** (et que nous n'utiliserons donc pas
dans ce notebook) :
- <notion future 1>
- <notion future 2>
```

La cellule de prérequis sert de **contrat d'écriture** pour l'auteur et de **rappel explicite** pour le stagiaire. Elle est consultée quand il se demande « pourquoi on n'utilise pas `f"{x}"` ici ? ».

---

## 3. Une cellule = un concept

**Un exemple par cellule de code**, pas plusieurs.

### ❌ Mauvais — un gros bloc qui empile les exemples

```python
# Opérations arithmétiques
a = 5
b = 2
print(a + b)  # 7
print(a - b)  # 3
print(a * b)  # 10
print(a / b)  # 2.5
print(a // b) # 2
```

### ✅ Bon — une cellule par opérateur

Cellule 1 : `4 + 2`
Cellule 2 : `4 - 2`
Cellule 3 : `5 * 2`
Cellule 4 : `5 / 2`
…

### Pourquoi

- Le stagiaire **ré-exécute** isolément chaque concept, modifie les valeurs, voit l'effet sans se perdre.
- Chaque cellule a un output distinct dans Jupyter, ce qui facilite la mémorisation visuelle.
- Une cellule fait ~1-3 lignes, se lit en 2 secondes, se modifie en 2 clics.
- La cellule devient une **unité atomique de démonstration**, réutilisable dans d'autres contextes.

---

## 4. Patterns d'affichage selon le niveau

### Avant `03_Chaines.ipynb` — pas de f-strings

Les f-strings sont introduites dans `Initiation/03_Types_de_donnees/03_Chaines.ipynb`. Avant ce notebook, on utilise uniquement :

```python
# Une valeur seule
resultat = 2 + 3
print(resultat)

# Une étiquette et une valeur (la virgule met un espace automatiquement)
print("Résultat :", resultat)

# Plusieurs valeurs côte à côte
print("x =", x, " y =", y)

# Arrondir pour l'affichage
print("Prix :", round(prix, 2))
```

### À partir de `03_Chaines.ipynb`

```python
print(f"Résultat : {resultat}")
print(f"x = {x}, y = {y}")
print(f"Prix : {prix:.2f}")
print(f"{resultat=}")   # debug Python 3.8+
```

**Ne pas mélanger les deux styles dans un même notebook.** Un notebook d'initiation utilise soit l'ancien style (avant `03_Chaines`), soit le nouveau (après). Pas de mélange.

---

## 5. Style d'exercices selon le niveau

### Avant `04_Fonctions.ipynb` — pas de `def`

Les fonctions sont introduites dans `Initiation/04_Fonctions/`. Avant ce notebook, les exercices sont des **scripts impératifs** qui calculent et affichent.

```python
# Exercice : conversion de température
celsius = float(input("Celsius : "))
fahrenheit = celsius * 9 / 5 + 32
print("Fahrenheit :", round(fahrenheit, 2))
```

Pas de `def`, pas de type hints, pas de `return`.

### À partir de `04_Fonctions.ipynb`

Exercices en **fonctions typées**, `mypy --strict` vert.

```python
def celsius_vers_fahrenheit(celsius: float) -> float:
    """Convertit une température de Celsius en Fahrenheit."""
    return celsius * 9 / 5 + 32
```

### Conséquence sur les types composites

Avant `04_Listes`, `05_Tuples`, `06_Dictionnaires` : pas de `list[...]`, `tuple[...]`, `dict[...]` dans les exercices. On utilise les primitives qui acceptent des arguments variadiques :

```python
# ✅ Bon — min avec plusieurs args
min(4, 3, 6, 1, 3, 6, 8)

# ❌ Mauvais — min avec une liste (liste pas encore vue)
valeurs = [4, 3, 6, 1, 3, 6, 8]
min(valeurs)
```

Ou on utilise `range()` qui est vu dès `02_Syntaxe/05_Boucles.ipynb` :

```python
# ✅ Bon — sum avec range
sum(range(1, 11))
```

---

## 6. Tags de cellule

Chaque cellule peut porter un ou plusieurs tags qui déterminent son comportement dans les versions 5 j et 3 j.

| Tag | Sens | 5 j | 3 j |
|---|---|---|---|
| *(aucun)* | Tronc commun | Affiché | Affiché |
| `skip-3j` | Approfondissement 5 j uniquement | Affiché | **Retiré** |
| `exo-facile` | Exercice niveau facile | Affiché | Affiché |
| `exo-moyen` | Exercice niveau intermédiaire | Affiché | Affiché |
| `exo-difficile` | Exercice challenge | Affiché | **Retiré** |
| `deep-dive` | Section fouille approfondie | Affiché | **Retiré** |
| `bonus` | Contenu bonus si temps | Affiché | **Retiré** |
| `correction` | Corrigé d'exercice (deprecated, préférer `<details>`) | Affiché | Affiché |

### Comment taguer une cellule dans un générateur Python

```python
cell.metadata["tags"] = ["deep-dive"]
```

### Comment taguer dans JupyterLab

Via le panneau de droite « Property Inspector » → « Common Tools » → « Cell Tags ».

### Collapse automatique des headings

Pour qu'une section entière (introduite par un `##` ou `###`) soit repliée par défaut en JupyterLab :

```python
cell.metadata["jp-MarkdownHeadingCollapsed"] = True
```

Ce repli n'est **qu'un affichage** ; la cellule reste présente dans le notebook. Pour retirer la section en 3 j, utiliser aussi le tag `deep-dive` ou `skip-3j`.

---

## 7. Format des corrections

Les corrections d'exercices sont des blocs HTML `<details>` natifs dans une cellule markdown dédiée. **Pas de cellule code taguée `correction`**.

### Modèle

````markdown
<details>
<summary>📖 Voir la correction</summary>

```python
celsius = float(input("Celsius : "))
fahrenheit = celsius * 9 / 5 + 32
print("Fahrenheit :", round(fahrenheit, 2))
```

</details>
````

### Avantages

- ✅ **Rendu identique partout** : JupyterLab, VS Code, GitHub, nbviewer, HTML exporté.
- ✅ **Affordance visuelle explicite** : « 📖 Voir la correction » avec un triangle cliquable.
- ✅ **Zéro dépendance**.
- ✅ **N'affecte pas l'état du notebook** (ouvrir ne modifie pas le `.ipynb`).
- ✅ **Non-exécutable** : le stagiaire doit recopier, ce qui force la lecture.

### Ligne vide obligatoire entre `<summary>` et le bloc code

Sans la ligne vide, le bloc code n'est pas rendu comme bloc code par le parseur markdown. **Toujours mettre une ligne vide**.

---

## 8. Utilisation du helper `verifier_et_reveler`

Pour les exercices « clés » (1 ou 2 par notebook maximum), utiliser le helper `verifier_et_reveler` du module `Bibliotheque_notebooks/_common/utils_pedagogie.py`. Il :

- exécute les tests du stagiaire ;
- affiche la correction seulement en cas de succès ;
- envoie l'événement au serveur formateur en best-effort.

### Usage typique

```python
# Cellule du stagiaire : il écrit son code
celsius = float(input("Celsius : "))
fahrenheit = celsius * 9 / 5 + 32
print("Fahrenheit :", round(fahrenheit, 2))
```

```python
# Cellule de vérification : le stagiaire l'exécute quand il pense avoir fini
from utils_pedagogie import verifier_et_reveler

def _tests():
    assert fahrenheit == celsius * 9 / 5 + 32, \
        "Le calcul Fahrenheit ne correspond pas"

verifier_et_reveler(
    notebook="01_Nombres",
    exercice=2,
    tests=_tests,
    correction="""\
celsius = float(input("Celsius : "))
fahrenheit = celsius * 9 / 5 + 32
print("Fahrenheit :", round(fahrenheit, 2))
""",
)
```

### Quand utiliser le helper

- ✅ Pour **1 ou 2 exercices clés** par notebook — ceux où l'auto-gate a vraiment un sens pédagogique.
- ❌ **Pas pour tous les exercices** — ça devient lourd et le stagiaire copie-colle le squelette.
- ✅ Pour **tous les exercices d'évaluation** (élèves ingénieurs), où la notation automatique passe par ce helper.

### Quand utiliser uniquement `<details>`

Pour les exercices simples d'auto-formation, `<details>` seul suffit largement.

---

## 9. Structure standard d'un notebook

```
1. Titre + objectifs pédagogiques       (1 cellule markdown)
2. Prérequis                             (1 cellule markdown obligatoire)
3. Plan                                  (1 cellule markdown, liste des sections)
4. --- séparateur horizontal
5. Section 1
   - Intro markdown
   - Cellules code (une par concept)
   - Sous-sections avec ###
6. Section 2
   ...
N. --- séparateur
N+1. Synthèse / récapitulatif            (tableau + règles à retenir)
N+2. --- séparateur
N+3. Exercices
     - Intro
     - Énoncé 1 + starter + correction <details>
     - Énoncé 2 + starter + correction <details>
     ...
N+4. --- séparateur
N+5. Ressources externes                  (doc officielle, PEPs, lectures)
```

**Longueur cible** : 60-100 cellules pour un notebook d'initiation, 80-140 pour un notebook intermédiaire.

---

## 10. Table des notions disponibles par notebook

Snapshot de ce qu'un stagiaire **connaît** à chaque étape de l'Initiation 5 j. À lire de haut en bas : chaque ligne cumule les connaissances des précédentes.

| Après notebook | Notions disponibles |
|---|---|
| `01_Presentation/*` | Installation, REPL, Jupyter, premier script |
| `02_Syntaxe/01_Variables_et_types_primitifs` | Variables, `int`, `float`, `str`, `bool`, affectation, `type()` |
| `02_Syntaxe/02_Operateurs_et_expressions` | `+ - * / // % **`, comparaisons, `and/or/not` |
| `02_Syntaxe/03_Entrees_sorties_console` | `print(...)`, `input(...)`, conversions `int()`/`float()` |
| `02_Syntaxe/04_Conditions` | `if`/`elif`/`else`, `match`/`case` (intro) |
| `02_Syntaxe/05_Boucles` | `for i in range(...)`, `while`, `break`, `continue` |
| **`03_Types_de_donnees/01_Nombres`** ← premier notebook de types | Tout ce qui précède uniquement |
| `03_Types_de_donnees/02_Booleens` | + truthiness, `all`, `any` |
| `03_Types_de_donnees/03_Chaines` | **+ f-strings**, méthodes de `str` |
| `03_Types_de_donnees/04_Listes` | + `list`, méthodes de liste, itération |
| `03_Types_de_donnees/05_Tuples` | + `tuple`, déballage |
| `03_Types_de_donnees/06_Dictionnaires` | + `dict`, accès, itération |
| `03_Types_de_donnees/07_Ensembles` | + `set`, opérations ensemblistes |
| `03_Types_de_donnees/08_Donnees_temporelles` | + `datetime`, `zoneinfo` |
| `04_Fonctions/01_Signatures` | **+ `def`**, paramètres, retours |
| `04_Fonctions/02_Type_hints_intro` | **+ type hints** `int | None`, `list[T]` |
| `04_Fonctions/03_Portee_et_closures` | + closures, variables globales |
| `05_Programmation_fonctionnelle/01_Comprehensions` | + comprehensions, générateurs |
| `02_Syntaxe/06_Exceptions` | + `try`/`except`, exceptions personnalisées |
| `06_Modules_et_packages/01_Modules_standard` | + `math` déjà vu, `random`, `statistics`, `pathlib` |
| `07_Entrees_sorties/01_Fichiers_et_pathlib` | + lecture/écriture fichiers |
| `07_Entrees_sorties/02_CSV` | + `csv.reader`/`DictReader` |
| `07_Entrees_sorties/03_JSON` | + `json.load`/`dump` |

**Point de repère :** à `01_Nombres` (tout premier notebook de types), le stagiaire ne connaît que variables, primitives, opérateurs, `print`, `input`, conditions, boucles, `range`, et `import`. **Rien d'autre.**

---

## 11. Checklist avant commit

Avant de valider un notebook, vérifier :

- [ ] Cellule **titre + objectifs** présente
- [ ] Cellule **prérequis** présente et à jour
- [ ] Cellule **plan** listant les sections
- [ ] **Un exemple par cellule de code** (pas de bloc empilé)
- [ ] **Pas de forward reference** : toute notion utilisée est dans la liste des notions disponibles à ce stade (voir section 10)
- [ ] **Format d'affichage** cohérent avec le niveau (`print` + `,` ou f-strings selon le notebook)
- [ ] **Exercices** cohérents avec le niveau (scripts ou fonctions typées selon le notebook)
- [ ] **Tags** corrects : `skip-3j`, `deep-dive`, `bonus`, `exo-facile/moyen/difficile`
- [ ] **Corrections en `<details>`** avec ligne vide entre `<summary>` et le code
- [ ] **Synthèse** présente avec tableau + règles à retenir
- [ ] **Exercices gradués** (au moins 3-4 de difficulté croissante)
- [ ] **Ressources externes** en fin de notebook
- [ ] Notebook **exécute sans erreur** avec Python 3.14 (`jupyter nbconvert --execute`)
- [ ] **`ruff check`** vert sur le code extrait
- [ ] Rendu 3 j validé : exécuter `python tools/build_3j.py <notebook>` et vérifier le résultat

---

*Ce guide est en vigueur depuis 2026-04-14. Les notebooks plus anciens qui ne respectent pas ces règles sont en cours de migration.*
