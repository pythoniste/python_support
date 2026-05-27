# 03 — Redirections shell et coopération avec Python

Les flux standards prennent tout leur sens grâce aux **redirections**
du shell. Le shell est capable, **avant** de lancer le programme, de
rebrancher chacun des trois tuyaux ailleurs : vers un fichier, vers un
autre programme, ou même vers `/dev/null`. Le programme, lui, ne s'en
aperçoit pas : il lit et écrit comme d'habitude.

## 3.1 La table des redirections

| Notation             | Effet                                              |
|----------------------|----------------------------------------------------|
| `cmd > fichier`      | Redirige stdout vers `fichier` (écrase)            |
| `cmd >> fichier`     | Redirige stdout vers `fichier` (ajoute à la fin)   |
| `cmd 2> fichier`     | Redirige stderr vers `fichier` (écrase)            |
| `cmd 2>> fichier`    | Redirige stderr vers `fichier` (ajoute)            |
| `cmd < fichier`      | Lit stdin depuis `fichier`                         |
| `cmd 2>&1`           | Fusionne stderr dans stdout                        |
| `cmd1 \| cmd2`       | Branche stdout de `cmd1` sur stdin de `cmd2`       |

Les numéros viennent des descripteurs OS : `0` = stdin, `1` = stdout,
`2` = stderr. La syntaxe `2>&1` se lit littéralement « redirige le
descripteur 2 vers une copie du descripteur 1 ».

## 3.2 Écraser ou ajouter : `>` contre `>>`

```
$ python3 script.py > sortie.txt     # crée ou écrase sortie.txt
$ python3 script.py >> sortie.txt    # ajoute à la fin de sortie.txt
```

`>` est destructif : tout contenu précédent de `sortie.txt` est perdu.
`>>` préserve l'existant et concatène. Utile pour accumuler les sorties
de plusieurs exécutions dans un même fichier journal.

## 3.3 Séparer stdout et stderr

Reprenons l'exemple central : un script qui produit des données et
écrit aussi des messages de progression sur stderr.

```
$ python3 script.py > donnees.txt
Progression : 10%
Progression : 50%
Progression : 100%
```

Que voit-on ?

- `donnees.txt` ne contient **que** stdout (les données utiles).
- Les lignes de progression, écrites sur stderr, **continuent**
  d'apparaître à l'écran (stderr n'est pas redirigé).

Pour ranger les deux flux dans deux fichiers distincts :

```
$ python3 script.py > donnees.txt 2> progression.log
```

Plus rien à l'écran. Chaque flux atterrit dans son propre fichier.

## 3.4 Fusionner stderr dans stdout : `2>&1`

Parfois, on veut **tout** capturer dans un seul fichier, sans
distinction :

```
$ python3 script.py > tout.txt 2>&1
```

Ordre important : `> tout.txt` rebranche d'abord stdout sur le fichier,
**puis** `2>&1` rebranche stderr sur ce que stdout pointe désormais
(donc `tout.txt`). Inverser l'ordre ne donne pas le même résultat.

Variante très courante pour **jeter** toutes les sorties :

```
$ python3 script.py > /dev/null 2>&1
```

`/dev/null` est le « trou noir » du système : tout ce qu'on y écrit
disparaît. Utile pour les scripts dont on ne veut conserver que le
**code retour**.

## 3.5 Le pipe `|`

Le pipe `|` connecte la **sortie** d'un programme à l'**entrée** du
suivant, **sans** passer par un fichier temporaire :

```
$ python3 producteur.py | python3 consommateur.py
```

Pour le `producteur`, `sys.stdout` n'est plus l'écran : c'est l'entrée
du `consommateur`. Pour le `consommateur`, `sys.stdin` n'est plus le
clavier : c'est ce que le `producteur` écrit.

Important : **stderr n'est pas concerné** par `|`. Les messages
d'erreur du producteur s'affichent toujours à l'écran. Pour les
inclure dans le pipe, on combine avec `2>&1` :

```
$ python3 producteur.py 2>&1 | python3 consommateur.py
```

## 3.6 Lire stdin depuis un fichier : `<`

L'inverse de `>` : alimenter le programme à partir d'un fichier.

```
$ python3 mon_filtre.py < entree.txt
```

Du point de vue du script, c'est strictement identique à un pipe
amont : `sys.stdin` est branché sur `entree.txt`, et `for ligne in
sys.stdin:` itère sur les lignes du fichier.

## 3.7 Ce que ça change pour le script Python

Bonne nouvelle : **rien**. Un script bien écrit fait :

```python
import sys

for ligne in sys.stdin:
    print(traiter(ligne), file=sys.stdout)
```

et il coopère automatiquement avec **toutes** les redirections vues
plus haut. Le shell s'occupe de rebrancher les tuyaux ; Python lit et
écrit comme si de rien n'était.

C'est la philosophie Unix : des petits outils qui lisent stdin et
écrivent stdout, qu'on combine avec des pipes pour construire des
traitements plus gros.

## 3.8 Code retour et redirections

Les redirections **ne changent pas** le code retour. `$?` vaut toujours
ce que le programme a renvoyé via `sys.exit(...)` ou via la fin
naturelle de son exécution :

```
$ python3 mon_script.py > /dev/null 2>&1
$ echo $?
0
```

C'est pratique pour scripter : on jette les sorties et on teste
seulement la réussite.

## À retenir

- `>` écrase, `>>` ajoute, `2>` cible stderr, `<` alimente stdin.
- `2>&1` fusionne stderr dans la destination courante de stdout.
- `|` chaîne deux programmes ; stderr n'est **pas** concerné.
- Un script Python qui utilise `sys.stdin`, `sys.stdout`, `sys.stderr`
  coopère sans aucune ligne supplémentaire avec ces redirections.
- Le code retour est indépendant des redirections.

## Démo

Exécuter `03_demo_redirections.py` avec plusieurs scénarios proposés
en commentaire à la fin du script.
