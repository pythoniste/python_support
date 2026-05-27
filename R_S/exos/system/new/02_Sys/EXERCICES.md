# Exercices pratiques — dossier 02_Sys

Une fois les trois modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** les notions
d'arguments, de flux standards et de redirections. Stdlib uniquement.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Saluer chaque argument  ★
*Module 01 — sys.argv*

Écrire un script `atelier_01.py` qui saluera **chaque** argument
fourni sur la ligne de commande, un par un, sur une ligne séparée. Si
aucun argument n'est fourni, le script ne doit **rien** afficher et
sortir normalement (code 0).

**Indices**

- `sys.argv[1:]` saute le nom du script.
- Une simple boucle `for` suffit.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py Ada Linus Grace
Bonjour, Ada
Bonjour, Linus
Bonjour, Grace
$ echo $?
0
$ python3 atelier_01.py
$ echo $?
0
```

---

## Atelier 2 — Mini `wc -l`  ★★
*Module 02 — lire stdin*

Écrire un script `atelier_02.py` qui lit son entrée standard ligne par
ligne et imprime, à la fin, le **nombre total de lignes** lues.
Imiter le comportement de `wc -l` (en plus minimaliste).

Tester avec un pipe **et** avec une redirection depuis un fichier.

**Indices**

- `for ligne in sys.stdin:` itère ligne à ligne sans tout charger.
- Un compteur entier suffit.
- La sortie finale va sur stdout (c'est le résultat).

**Exemple de sortie attendue**

```
$ printf "alpha\nbeta\ngamma\n" | python3 atelier_02.py
3

$ python3 atelier_02.py < /etc/hostname
1
```

---

## Atelier 3 — Argument obligatoire ou code 1  ★★
*Module 01 — sys.argv et sys.exit*

Écrire un script `atelier_03.py` qui :

- exige **exactement un** argument sur la ligne de commande ;
- s'il en manque (ou s'il y en a trop), écrit
  `Usage: atelier_03.py <nom>` sur **stderr** et sort avec le code
  retour `1` (utiliser `sys.exit("...")` pour faire les deux en une
  ligne) ;
- s'il y en a un, écrit `Bonjour, <nom>` sur stdout et sort en `0`.

Vérifier `$?` dans chaque cas.

**Indices**

- `sys.exit("message")` écrit sur stderr et sort en 1.
- `len(sys.argv) == 2` correspond à exactement un argument utilisateur.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
Usage: atelier_03.py <nom>
$ echo $?
1
$ python3 atelier_03.py Ada
Bonjour, Ada
$ echo $?
0
$ python3 atelier_03.py Ada Linus
Usage: atelier_03.py <nom>
$ echo $?
1
```

---

## Atelier 4 — Nombres sur stdout, erreurs sur stderr  ★★
*Module 02 — séparation stdout / stderr*

Écrire un script `atelier_04.py` qui reçoit une liste de chaînes en
arguments. Pour chacune :

- s'il s'agit d'un entier valide, écrire `<n> * 2 = <2n>` sur
  **stdout** ;
- sinon, écrire `ignoré : <valeur>` sur **stderr** et continuer (on
  ne s'arrête pas au premier mauvais argument).

Le code retour vaut `0` si tous les arguments étaient valides, `1` si
au moins un a été ignoré.

Vérifier ensuite, depuis le shell, qu'en faisant
`python3 atelier_04.py 1 deux 3 > nombres.txt 2> rejets.txt`, on
range bien les bons résultats d'un côté et les rejets de l'autre.

**Indices**

- `int("deux")` lève `ValueError` ; un `try / except` simple suffit.
- Tenir un drapeau `eu_erreur` pour choisir le code retour final.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py 1 deux 3
1 * 2 = 2
ignoré : deux
3 * 2 = 6
$ echo $?
1

$ python3 atelier_04.py 1 2 3 > nombres.txt 2> rejets.txt
$ cat nombres.txt
1 * 2 = 2
2 * 2 = 4
3 * 2 = 6
$ cat rejets.txt
$ echo $?
0
```

---

## Atelier 5 — Filtre `grep` minimaliste  ★★★
*Modules 01 + 02 — argv et stdin*

Écrire un script `atelier_05.py` qui prend **un** argument (un motif),
lit son entrée standard ligne par ligne, et n'imprime sur stdout que
les lignes **contenant** ce motif. Si l'argument est absent, écrire
l'usage sur stderr et sortir en `2` (convention « erreur d'usage »).

Le script doit pouvoir s'utiliser dans un pipe :

```
$ printf "alpha\nbeta\ngamma\n" | python3 atelier_05.py a
alpha
gamma
```

**Indices**

- `motif in ligne` teste l'inclusion d'une sous-chaîne.
- Penser à retirer le `\n` final avec `rstrip("\n")` avant
  l'affichage (sinon `print` en ajoutera un second).
- Sortir en `2` se fait avec `sys.exit(2)` ; un message d'erreur
  préalable sur stderr est de bon goût.

**Bonus**

- Ajouter une option `-v` (à passer **avant** le motif) qui inverse
  le sens : afficher les lignes qui **ne** contiennent **pas** le
  motif.
- Ajouter, en fin de traitement et sur **stderr** uniquement, un
  résumé `N ligne(s) sur M correspondent.`

**Exemple de sortie attendue**

```
$ printf "alpha\nbeta\ngamma\n" | python3 atelier_05.py a
alpha
gamma
$ echo $?
0

$ python3 atelier_05.py
Usage: atelier_05.py <motif>
$ echo $?
2
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait écrire un petit outil en ligne
de commande qui se branche naturellement sur des pipes Unix. Les
chapitres suivants s'appuieront là-dessus pour manipuler des fichiers,
des processus et des sockets sans réexpliquer ce qu'est stdin.
