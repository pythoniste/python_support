# Exercices pratiques — dossier 00_Concepts

Une fois les trois modules lus et leurs démos exécutées, ces quatre
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Du REPL au script  ★
*Module 01 — programme, script, REPL*

1. Ouvrir le REPL avec `python3`, puis afficher `Bonjour, monde !` via
   `print(...)`. Sortir avec `exit()`.
2. Créer un fichier `atelier_01.py` qui produit exactement la même
   sortie. Le lancer avec `python3 atelier_01.py`.
3. Inclure un garde `if __name__ == "__main__":` dans le script.

**Indices**

- Le REPL répond directement à chaque ligne tapée.
- Le script lui doit être lancé par l'interpréteur.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py
Bonjour, monde !
```

---

## Atelier 2 — Shebang et exécution directe  ★
*Module 01 — exécution directe sous Unix*

Écrire un script `atelier_02.py` qui :

- contient une ligne shebang en première position ;
- affiche le chemin de l'interpréteur (`sys.executable`) ;
- est rendu exécutable avec `chmod +x` ;
- se lance ensuite via `./atelier_02.py` (sans préfixer `python3`).

**Indices**

- Le shebang portable est `#!/usr/bin/env python3`.
- `chmod +x atelier_02.py` ajoute le droit d'exécution.
- `sys.executable` est dans le module `sys`.

**Exemple de sortie attendue**

```
$ ./atelier_02.py
Interpréteur : /usr/bin/python3
```

(Le chemin exact dépend du système.)

---

## Atelier 3 — stdout et stderr séparés  ★★
*Module 03 — flux standards*

Écrire un script `atelier_03.py` qui :

- affiche trois lignes de résultat sur **stdout** ;
- affiche deux lignes d'information sur **stderr**.

Vérifier ensuite, depuis le shell, que la redirection
`./atelier_03.py > sortie.txt 2> erreurs.txt` range bien chaque flux
dans le fichier correspondant.

**Indices**

- `print(..., file=sys.stderr)` envoie sur stderr.
- Le shell `bash` ou `zsh` interprète `>` et `2>`.
- `cat sortie.txt` et `cat erreurs.txt` montrent le contenu.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py > sortie.txt 2> erreurs.txt
$ cat sortie.txt
Resultat 1
Resultat 2
Resultat 3
$ cat erreurs.txt
Info : début
Info : fin
```

---

## Atelier 4 — Code retour explicite  ★★
*Module 03 — code retour et sys.exit*

Écrire un script `atelier_04.py` qui prend **un seul argument** sur la
ligne de commande, et qui :

- si l'argument manque, écrit `Usage: atelier_04.py <nom>` sur stderr
  et sort avec le code `1` ;
- sinon, écrit `Bonjour, <nom>` sur stdout et sort avec le code `0`.

Vérifier `$?` dans les deux cas.

**Indices**

- `sys.argv` contient les arguments (`sys.argv[0]` est le script).
- `sys.exit(1)` sort avec le code 1.
- Dans le shell, `echo $?` affiche le code retour précédent.

**Exemple de sortie attendue**

```
$ python3 atelier_04.py
Usage: atelier_04.py <nom>
$ echo $?
1
$ python3 atelier_04.py Ada
Bonjour, Ada
$ echo $?
0
```

**Bonus** : ajouter un mode `--silencieux` qui supprime la sortie
stdout mais conserve le code retour.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on maîtrise le strict minimum pour
attaquer les chapitres suivants : on sait écrire un script, contrôler
ses entrées/sorties et signaler un échec au shell qui l'a lancé.
