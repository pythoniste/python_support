# Exercices pratiques — dossier 01_Print_et_Input

Une fois les trois modules lus et leurs démos exécutées, ces six
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- s'il est **interactif** (l'utilisateur doit taper au clavier) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après** avoir
tenté chaque atelier.

---

## Atelier 1 — Tableau aligné nom / âge  ★
*Module 02 — f-strings (alignement et largeur)*

Écrire un script `atelier_01.py` **non interactif** qui contient une
liste de couples `(nom, age)` codée en dur :

```python
PERSONNES = [
    ("Ada", 36),
    ("Linus", 54),
    ("Grace", 85),
    ("Donald", 87),
]
```

Afficher un tableau aligné : la colonne « Nom » alignée à gauche sur 10
caractères, la colonne « Âge » alignée à droite sur 4 caractères, avec
une ligne d'en-tête.

**Indices**

- `f"{nom:<10}"` pour aligner à gauche sur 10 caractères.
- `f"{age:>4}"` pour aligner à droite sur 4.
- Une ligne d'en-tête se construit comme une ligne de données.

**Exemple de sortie attendue**

```
Nom         Âge
Ada          36
Linus        54
Grace        85
Donald       87
```

---

## Atelier 2 — Phrase formatée à partir d'une saisie  ★
*Module 03 — input + Module 02 — f-strings*  (**interactif**)

Écrire un script `atelier_02.py` qui demande à l'utilisateur son prénom
puis son âge, et affiche :

```
Bonjour, <prénom>, tu as <âge> ans, donc tu es né(e) vers <année>.
```

L'année est calculée à partir de l'année courante (`datetime.date.today().year`).

**Indices**

- Deux appels à `input(...)`.
- `int(...)` pour convertir l'âge.
- `from datetime import date` puis `date.today().year`.

**Exemple de sortie attendue**

```
$ python3 atelier_02.py
Ton prénom : Ada
Ton âge : 36
Bonjour, Ada, tu as 36 ans, donc tu es né(e) vers 1990.
```

---

## Atelier 3 — Mot de passe avec confirmation  ★★
*Module 03 — getpass*  (**interactif**)

Écrire un script `atelier_03.py` qui demande deux fois un mot de passe
via `getpass.getpass`, et :

- redemande **les deux saisies** tant qu'elles diffèrent ;
- une fois identiques, affiche `Mot de passe enregistré.` et indique sa
  longueur (mais **jamais** son contenu).

**Indices**

- `import getpass`.
- `while True: ... if a == b: break`.
- Ne **jamais** afficher `mdp` directement, même pour débugger.

**Exemple de session attendue**

```
$ python3 atelier_03.py
Nouveau mot de passe :
Confirmation :
Les deux saisies diffèrent, réessaye.
Nouveau mot de passe :
Confirmation :
Mot de passe enregistré. (8 caractères)
```

---

## Atelier 4 — Entier dans [1, 100] avec relance  ★★
*Module 03 — boucle de validation*  (**interactif**)

Écrire un script `atelier_04.py` qui demande un entier entre 1 et 100,
et redemande tant que :

- la saisie n'est pas un entier (`ValueError`) ;
- ou que la valeur est hors de l'intervalle `[1, 100]`.

Une fois la valeur acceptée, afficher `Merci, j'ai bien <n>.`.

**Indices**

- `while True:` + `try/except ValueError:` + `continue`.
- Comparer `1 <= n <= 100`.

**Exemple de session attendue**

```
$ python3 atelier_04.py
Entre un entier entre 1 et 100 : abc
Ce n'est pas un entier, réessaye.
Entre un entier entre 1 et 100 : 200
Hors plage, réessaye.
Entre un entier entre 1 et 100 : 42
Merci, j'ai bien 42.
```

---

## Atelier 5 — Moyenne de N notes  ★★
*Modules 02 et 03*  (**interactif**)

Écrire un script `atelier_05.py` qui :

1. demande combien de notes saisir (entier `n`, avec validation) ;
2. lit ensuite `n` notes flottantes (avec validation) ;
3. affiche la moyenne avec **2 décimales** et le séparateur de milliers
   (la valeur sera petite, mais la spec est demandée pour entraîner) ;
4. affiche aussi le minimum et le maximum, alignés sur 6 caractères.

**Indices**

- Une fonction utilitaire `lire_flottant(invite)`.
- `sum(notes) / len(notes)` pour la moyenne.
- `min(notes)`, `max(notes)`.
- `f"{x:>6.2f}"` pour aligner à droite avec 2 décimales.

**Exemple de session attendue**

```
$ python3 atelier_05.py
Combien de notes ? 3
Note 1 : 12
Note 2 : 15.5
Note 3 : 8
Moyenne :  11.83
Min     :   8.00
Max     :  15.50
```

---

## Atelier 6 — Mini-quiz 3 questions avec score  ★★★
*Modules 01, 02, 03 — synthèse*  (**interactif**)

Écrire un script `atelier_06.py` qui pose trois questions à choix unique
en dur dans le code (par exemple : capitale de la France, résultat de
`2 + 2`, langue de Python — comme un quiz culturel court).

- Pour chaque question, lire la réponse via `input`.
- Comparer en mode tolérant : `reponse.strip().lower() == bonne_reponse`.
- Afficher à la fin le score sous la forme `Score : N / 3 (pourcentage)`.
- Si toutes les réponses sont justes, écrire un message sur `stdout` ;
  sinon un message sur `stderr` (pour entraîner la séparation des flux).

**Indices**

- Une liste de tuples `(question, bonne_reponse)`.
- Une variable `score` incrémentée à chaque bonne réponse.
- `f"{score} / {total} ({score / total:.0%})"` pour le pourcentage.
- `print(..., file=sys.stderr)` pour le message d'échec.

**Exemple de session attendue**

```
$ python3 atelier_06.py
Capitale de la France ? Paris
Combien font 2 + 2 ? 4
Quelle langue programmons-nous ? python
Score : 3 / 3 (100%)
Bravo, tout juste !
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait dialoguer proprement avec
l'utilisateur en ligne de commande : afficher, formater, lire, valider.
C'est le strict minimum pour aborder les chapitres suivants, qui
manipulent fichiers, dates et processus.
