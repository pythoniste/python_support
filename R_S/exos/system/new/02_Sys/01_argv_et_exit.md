# 01 — `sys.argv` et `sys.exit`

## 1.1 Lire les arguments de ligne de commande

Quand on lance un script avec :

```
$ python3 mon_script.py alpha beta gamma
```

le shell transmet à Python la liste des mots tapés après l'interpréteur.
Python l'expose dans `sys.argv`, qui est une **liste de chaînes** :

```python
import sys

print(sys.argv)
# ['mon_script.py', 'alpha', 'beta', 'gamma']
```

Deux choses à retenir :

- `sys.argv[0]` est **toujours présent** : c'est le nom (ou le chemin)
  du script lui-même.
- `sys.argv[1:]` contient les vrais arguments fournis par l'utilisateur.

Si l'utilisateur ne passe rien, la liste ne contient que `argv[0]` :

```
$ python3 mon_script.py
['mon_script.py']
```

## 1.2 Convertir et valider

Tous les éléments de `sys.argv` sont des **chaînes**, même quand
l'utilisateur tape un nombre. C'est au script de convertir et de
contrôler :

```python
import sys

if len(sys.argv) < 2:
    print("Usage: mon_script.py <nombre>", file=sys.stderr)
    sys.exit(1)

n = int(sys.argv[1])   # peut lever ValueError si l'argument n'est pas un entier
print(n * 2)
```

Pour les scripts un peu plus sérieux, on préférera `argparse` (vu dans
un chapitre ultérieur). `sys.argv` reste utile pour les petits scripts
et pour comprendre ce qui se passe en dessous.

## 1.3 Le code retour, rappel express

Quand un programme termine, il rend au système un **entier** appelé
*code retour*. La convention est universelle :

| Code retour       | Signification           |
|-------------------|-------------------------|
| `0`               | Succès                  |
| Différent de `0`  | Erreur ou échec         |

Le shell le récupère dans `$?` :

```
$ python3 mon_script.py
$ echo $?
0
```

## 1.4 `sys.exit` en détail

`sys.exit(code)` arrête le programme **et** transmet le code au shell.
Il accepte plusieurs formes :

```python
import sys

sys.exit()         # équivalent à sys.exit(0) : succès
sys.exit(0)        # succès explicite
sys.exit(1)        # échec générique
sys.exit(2)        # erreur d'usage (convention courante)
```

Cas particulier très utile : si on passe une **chaîne** au lieu d'un
entier, Python l'écrit sur **stderr** et sort avec le code **1** :

```python
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: mon_script.py <fichier>")
    # Écrit le message sur stderr, puis sort en 1.
```

C'est un raccourci pratique pour signaler une erreur d'utilisation en
une seule ligne, sans avoir à enchaîner `print(..., file=sys.stderr)`
puis `sys.exit(1)`.

## 1.5 Implémentation : `sys.exit` lève une exception

`sys.exit` ne fait pas un arrêt « brutal ». Il lève `SystemExit`, une
exception que Python laisse remonter jusqu'au sommet. Conséquences :

- Un `try / except` qui attrape **tout** (par exemple `except:`) peut
  intercepter `SystemExit` par accident et empêcher la sortie. À
  éviter.
- Les blocs `finally` et les contextes `with` sont **bien** exécutés
  avant la sortie effective, ce qui garantit la libération des
  ressources.

## 1.6 Conventions de code retour Unix

La plupart des programmes Unix suivent ces conventions, qu'on peut
réutiliser dans un script Python :

| Code | Signification typique                                      |
|------|------------------------------------------------------------|
| 0    | Succès                                                     |
| 1    | Erreur générique                                           |
| 2    | Erreur d'usage (mauvais argument, option inconnue)         |
| 64+  | Erreurs spécifiques à l'application (rare)                 |

Les codes valides vont de **0 à 255**. Au-delà, le shell tronque.

## À retenir

- `sys.argv` est une liste de chaînes ; `argv[0]` est le nom du script.
- `sys.argv[1:]` contient les arguments réellement fournis.
- Code retour : `0` = succès, autre = erreur, plage 0–255.
- `sys.exit(0)` réussit, `sys.exit(N)` échoue avec le code `N`.
- `sys.exit("message")` écrit sur stderr et sort en `1`.
- `sys.exit` lève `SystemExit` : les blocs `finally` et `with` sont
  exécutés normalement.

## Démo

Exécuter `01_demo_argv.py`, avec et sans arguments :

```
$ python3 01_demo_argv.py
$ python3 01_demo_argv.py alpha beta 42
```
