# Exercices pratiques — dossier 03_Argparse

Une fois les quatre fiches lues et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** `argparse` dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- la fiche concernée ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent) ;
- un ou plusieurs exemples d'invocation.

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Mini-calculatrice CLI  ★
*Fiche 01 — premier parser ; fiche 02 — type / choices*

Écrire un script `atelier_01.py` qui prend **trois arguments
positionnels** : deux nombres et un opérateur, puis affiche le
résultat de l'opération.

- Les nombres doivent être des `float`.
- L'opérateur doit appartenir à `{"+", "-", "*", "/"}`.
- En cas de division par zéro, afficher `Erreur : division par zéro`
  sur stderr et sortir avec le code `1`.

**Indices**

- `type=float` et `choices=["+", "-", "*", "/"]` font le gros du travail.
- Penser à `sys.exit(1)` après le message d'erreur.
- Attention : le shell peut interpréter `*` ; on tape `'*'` (entre
  guillemets) pour le passer tel quel.

**Exemple d'invocation**

```
$ python3 atelier_01.py 3 + 4
3.0 + 4.0 = 7.0
$ python3 atelier_01.py 10 / 0
Erreur : division par zéro
$ echo $?
1
$ python3 atelier_01.py 6 '*' 7
6.0 * 7.0 = 42.0
```

---

## Atelier 2 — Mini-grep  ★★
*Fiche 02 — types/validation ; fiche 03 — store_true*

Écrire un script `atelier_02.py` qui imite très grossièrement
`grep` :

- un argument positionnel `motif` ;
- un argument positionnel `fichier` ;
- un drapeau `--ignore-case` (ou `-i`) ;
- un drapeau `--line-number` (ou `-n`) qui affiche le numéro de ligne.

Le programme lit le fichier ligne par ligne et imprime les lignes qui
contiennent `motif`. Si `--ignore-case` est passé, la recherche est
insensible à la casse. Si `--line-number` est passé, chaque ligne
imprimée est préfixée par `N:` où `N` est son numéro (à partir de 1).

**Indices**

- `action="store_true"` pour les deux drapeaux.
- `open(args.fichier)` puis itérer.
- `enumerate(lignes, start=1)` pour numéroter.
- Comparer avec `.lower()` quand `--ignore-case` est actif.

**Exemple d'invocation**

```
$ cat > exemple.txt <<EOF
Python est cool
PYTHON est puissant
Ruby aussi
EOF

$ python3 atelier_02.py Python exemple.txt
Python est cool

$ python3 atelier_02.py -i python exemple.txt
Python est cool
PYTHON est puissant

$ python3 atelier_02.py -in python exemple.txt
1:Python est cool
2:PYTHON est puissant
```

---

## Atelier 3 — Verbosité graduée  ★
*Fiche 03 — action="count"*

Écrire un script `atelier_03.py` qui accepte un drapeau `-v`
répétable (`-v`, `-vv`, `-vvv`...). Selon le nombre de répétitions,
il affiche :

- 0 : rien sur stderr ;
- 1 : `[INFO] ...` ;
- 2 : `[INFO] ...` et `[DEBUG] ...` ;
- 3 ou plus : `[INFO] ...`, `[DEBUG] ...` et `[TRACE] ...`.

Sur stdout, le programme affiche simplement `Travail terminé`.

**Indices**

- `action="count"` et `default=0`.
- Les messages de journal vont sur **stderr** (`file=sys.stderr`).
- Vérifier que `python3 atelier_03.py -vv > /dev/null` n'affiche que
  les journaux (sur stderr).

**Exemple d'invocation**

```
$ python3 atelier_03.py
Travail terminé

$ python3 atelier_03.py -v
[INFO] démarrage
[INFO] fin
Travail terminé

$ python3 atelier_03.py -vvv
[INFO] démarrage
[DEBUG] détails internes
[TRACE] trace très bavarde
[INFO] fin
Travail terminé
```

---

## Atelier 4 — Todo list à sous-commandes  ★★★
*Fiche 04 — add_subparsers + set_defaults*

Écrire un script `atelier_04.py` qui gère une liste de tâches
persistée dans un fichier JSON local `taches.json` (créé dans le
répertoire courant). Trois sous-commandes :

- `ajouter "texte"` : ajoute une tâche, lui attribue un identifiant
  entier croissant, statut `"actif"`. Affiche `Tâche N ajoutée.`.
- `lister` : affiche les tâches actives. Avec `--toutes`, inclut aussi
  les tâches terminées. Format : `N [statut] texte`.
- `finir N` : passe la tâche `N` à `statut = "termine"`. Si l'id
  n'existe pas, erreur sur stderr et code retour 1.

**Indices**

- `import json` ; `json.load`/`json.dump`.
- Si `taches.json` n'existe pas, partir d'une liste vide.
- Une tâche est un dict : `{"id": 1, "texte": "...", "statut": "actif"}`.
- Utiliser le patron `set_defaults(func=...)` pour dispatcher.

**Exemple d'invocation**

```
$ python3 atelier_04.py ajouter "écrire le rapport"
Tâche 1 ajoutée.
$ python3 atelier_04.py ajouter "envoyer le mail"
Tâche 2 ajoutée.
$ python3 atelier_04.py lister
1 [actif] écrire le rapport
2 [actif] envoyer le mail
$ python3 atelier_04.py finir 1
Tâche 1 terminée.
$ python3 atelier_04.py lister
2 [actif] envoyer le mail
$ python3 atelier_04.py lister --toutes
1 [termine] écrire le rapport
2 [actif] envoyer le mail
$ python3 atelier_04.py finir 99
Erreur : tâche 99 introuvable
$ echo $?
1
```

---

## Atelier 5 — Convertisseur de température  ★★
*Fiche 01 + fiche 02 — choices et required*

Écrire un script `atelier_05.py` qui convertit une température entre
trois échelles : Celsius, Fahrenheit, Kelvin.

- Un argument positionnel `valeur` (`float`).
- Un drapeau **obligatoire** `--from` parmi `["celsius", "fahrenheit", "kelvin"]`.
- Un drapeau **obligatoire** `--to` parmi `["celsius", "fahrenheit", "kelvin"]`.
- Un drapeau `--precision` (entier, par défaut 2) qui contrôle le
  nombre de décimales en sortie.

Formules utiles :

```
celsius    -> fahrenheit : C * 9/5 + 32
fahrenheit -> celsius    : (F - 32) * 5/9
celsius    -> kelvin     : C + 273.15
kelvin     -> celsius    : K - 273.15
```

Si `--from` et `--to` sont identiques, la valeur est renvoyée telle
quelle.

**Indices**

- Attention : `--from` est un mot-clé Python ; utiliser
  `dest="depuis"` pour récupérer l'attribut sous un nom valide.
- Pareil pour `--to` : `dest="vers"`.
- Passer par le Celsius comme **étape intermédiaire** simplifie
  beaucoup le code (6 formules au lieu de 9).

**Exemple d'invocation**

```
$ python3 atelier_05.py 100 --from celsius --to fahrenheit
100.00 celsius = 212.00 fahrenheit

$ python3 atelier_05.py 32 --from fahrenheit --to celsius --precision 3
32.000 fahrenheit = 0.000 celsius

$ python3 atelier_05.py 0 --from celsius --to kelvin
0.00 celsius = 273.15 kelvin

$ python3 atelier_05.py 100        # erreur : --from et --to manquent
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait écrire une CLI propre avec
arguments positionnels et optionnels, validation de type, drapeaux
booléens et compteurs, et sous-commandes dispatchées. C'est la base
qui sera réutilisée dans tous les outils des chapitres suivants.
