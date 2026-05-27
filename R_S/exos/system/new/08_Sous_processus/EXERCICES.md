# Exercices pratiques — dossier 08_Sous_processus

Une fois les trois modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard et des utilitaires Unix de base (`ls`, `echo`,
`date`, `wc`, `git`).

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Compter les entrées d'un répertoire  ★
*Module 01 — subprocess.run*

Écrire un script `atelier_01.py` qui lance `ls` sur le répertoire
courant via `subprocess.run`, capture sa sortie, et affiche :

- la sortie brute de `ls` ;
- le **nombre d'entrées** trouvées (= nombre de lignes non vides de
  la sortie).

**Indices**

- `subprocess.run(["ls"], capture_output=True, text=True)`.
- `result.stdout.splitlines()` découpe la sortie en liste de lignes.
- Filtrer les lignes vides avant de compter.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py
Sortie de ls :
README.md
atelier_01.py
...
Nombre d'entrées : 7
```

---

## Atelier 2 — Parser la sortie de `date` reformatée  ★
*Module 01 — subprocess.run avec arguments*

Écrire un script `atelier_02.py` qui :

- lance `date "+%Y-%m-%d %H:%M:%S"` via `subprocess.run` ;
- récupère la sortie, la nettoie (`strip()`) ;
- découpe la chaîne en deux morceaux (date et heure) et les affiche
  sur deux lignes distinctes.

**Indices**

- Bien penser à passer le format **dans une case de la liste** :
  `["date", "+%Y-%m-%d %H:%M:%S"]`. Pas d'espace entre `+` et le format.
- `chaine.split(" ", 1)` découpe au premier espace.

**Exemple de sortie attendue**

```
$ python3 atelier_02.py
Date : 2026-05-27
Heure : 14:32:08
```

---

## Atelier 3 — Mesurer la durée d'un `git status`  ★★
*Module 02 — code retour et exceptions*

Écrire un script `atelier_03.py` qui :

- mesure avec `time.perf_counter()` la durée d'un appel
  `subprocess.run(["git", "status"], ...)` ;
- affiche la durée en millisecondes ;
- affiche le code retour ;
- gère **proprement** le cas où `git` n'est pas installé
  (`FileNotFoundError`) et le cas où on n'est pas dans un dépôt
  (`CalledProcessError` si on a passé `check=True`).

**Indices**

- `t0 = time.perf_counter()` avant, `t1 = time.perf_counter()` après ;
  durée en secondes = `t1 - t0`. Multiplier par 1000 pour les ms.
- `capture_output=True` pour ne pas polluer le terminal avec la
  sortie de `git status`.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
git status terminé en 18.4 ms (code retour 0)
```

---

## Atelier 4 — Chaîner `echo` puis `wc -w` via un pipe  ★★
*Module 03 — Popen et pipes*

Écrire un script `atelier_04.py` qui reproduit en pur Python le pipe
shell :

```
echo "le réseau et le système, c'est pareil" | wc -w
```

en utilisant **deux `Popen`** chaînés (donc sans `shell=True` ni
`run(..., input=...)`). Afficher le nombre de mots renvoyé.

**Indices**

- `p1 = Popen(["echo", "..."], stdout=PIPE, text=True)`.
- `p2 = Popen(["wc", "-w"], stdin=p1.stdout, stdout=PIPE, text=True)`.
- `p1.stdout.close()` puis `p2.communicate()`.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py
Nombre de mots : 8
```

**Bonus** : refaire le même exercice avec `subprocess.run` + `input=`,
et comparer les deux approches en quelques lignes de commentaires.

---

## Atelier 5 — Mini `which`  ★★★
*Modules 01 + 02 — synthèse*

Écrire un script `atelier_05.py` qui prend en argument le nom d'un
programme (par exemple `python3`, `ls`, `nimportequoi`) et qui :

- utilise `subprocess.run(["which", nom], ...)` pour le localiser ;
- imprime le chemin trouvé si le code retour est `0` ;
- imprime `<nom> : introuvable` et sort avec `sys.exit(1)` sinon ;
- gère **également** le cas où `which` lui-même n'est pas dans le
  `PATH` (`FileNotFoundError`).

**Indices**

- `sys.argv[1]` pour récupérer le nom.
- Si `sys.argv` est trop court, afficher un message d'usage sur
  stderr et `sys.exit(2)`.
- `which` rend `0` si trouvé, `1` sinon.

**Exemple de sortie attendue**

```
$ python3 atelier_05.py python3
python3 : /usr/bin/python3
$ python3 atelier_05.py nimportequoi
nimportequoi : introuvable
$ echo $?
1
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait appeler proprement un
programme externe, récupérer sa sortie, gérer ses erreurs et chaîner
deux commandes. Suite logique : `09_Environnement/` pour apprendre à
passer des variables au sous-processus.
