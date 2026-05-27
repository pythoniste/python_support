# 03 — Pipes et `Popen` (survol)

Cette fiche est un **survol**. Dans 95 % des cas, `subprocess.run`
suffit : on lance une commande, on attend la fin, on lit la sortie.
Mais quand il faut **chaîner deux commandes** par un pipe (à la
manière de `cmd1 | cmd2` dans le shell), `run` seul ne suffit plus —
on descend d'un cran avec la classe `subprocess.Popen`.

## 3.1 Passer du contenu sur stdin — la version simple

Pour fournir du texte sur l'entrée standard d'**une seule** commande,
`run` suffit largement, via l'argument `input` :

```python
result = subprocess.run(
    ["wc", "-w"],
    input="un deux trois quatre\n",
    capture_output=True,
    text=True,
)
print(result.stdout.strip())   # 4
```

C'est l'équivalent en Python de :

```
$ echo "un deux trois quatre" | wc -w
4
```

Le sous-processus voit le texte d'`input` arriver sur son stdin
exactement comme s'il provenait d'un pipe shell.

## 3.2 Pourquoi `Popen` ?

`subprocess.run` est une façade pratique au-dessus de la classe
`subprocess.Popen`. `run` bloque jusqu'à la fin du sous-processus et
fait tout le travail à notre place. `Popen`, lui, **lance le
sous-processus et rend la main immédiatement**. On a alors la main sur
ses tubes (stdin/stdout/stderr) tant qu'il tourne.

C'est cette différence qui permet de **chaîner** deux processus :
faire vivre les deux en parallèle, et brancher la sortie de l'un sur
l'entrée de l'autre.

## 3.3 Chaîner deux commandes via un pipe

Reproduisons `echo "un deux trois" | wc -w` en pur Python, sans
`shell=True` :

```python
import subprocess

p1 = subprocess.Popen(
    ["echo", "un deux trois"],
    stdout=subprocess.PIPE,        # on veut récupérer son stdout
    text=True,
)

p2 = subprocess.Popen(
    ["wc", "-w"],
    stdin=p1.stdout,               # on branche le stdout de p1 ici
    stdout=subprocess.PIPE,
    text=True,
)

p1.stdout.close()                  # cf. note ci-dessous
sortie, _ = p2.communicate()
print(sortie.strip())              # 3
```

Trois points à noter :

1. **`stdout=subprocess.PIPE`** sur p1 lui dit : « ne déverse pas ta
   sortie sur le terminal, garde-la dans un tube ».
2. **`stdin=p1.stdout`** sur p2 branche directement le tube de sortie
   de p1 sur l'entrée de p2. Les deux processus s'exécutent en
   parallèle.
3. **`p1.stdout.close()`** côté parent : sinon, si p2 se termine,
   p1 ne reçoit jamais d'EOF et risque de bloquer. C'est une subtilité
   classique des pipes Unix.

## 3.4 `communicate()` : l'attente propre

`p.communicate(input=None, timeout=None)` :

- envoie `input` sur stdin (s'il y en a) ;
- lit complètement stdout et stderr ;
- attend la fin du sous-processus ;
- renvoie le couple `(stdout, stderr)`.

C'est la manière sûre d'attendre un `Popen` quand on a redirigé un
flux : sans `communicate()`, on risque le **blocage** parce que les
tubes ont une capacité limitée et que les deux processus peuvent
s'attendre mutuellement.

Après `communicate()`, le code retour est dans `p.returncode`.

## 3.5 Quand s'en passer

On le redit : pour **une** commande, `run` suffit. Pour **deux**
commandes chaînées, on peut souvent éviter `Popen` :

- soit en faisant deux `run` successifs avec une variable Python entre
  les deux (la sortie de l'un devient l'`input` de l'autre) ;
- soit en faisant le filtrage côté Python (par exemple, `wc -w` se
  remplace par `len(texte.split())`).

`Popen` n'est strictement nécessaire que lorsqu'on veut **du vrai
parallélisme** entre les deux commandes, par exemple pour traiter un
flux énorme sans charger l'intermédiaire en mémoire.

## 3.6 Sécurité, encore

Tout ce qui a été dit dans la fiche 01 reste valable : pas de
`shell=True`, commande passée comme liste. Le pipe ici n'est **pas**
un pipe shell — c'est un véritable tube système géré par Python. Il
ne fait pas appel au shell et il n'y a donc pas d'injection
possible via la syntaxe `|`, `;`, `&&` ou autre.

## À retenir

- Pour passer du texte à **une** commande : `run(..., input="...")`.
- Pour chaîner **deux** commandes : `Popen` + `stdout=PIPE` + brancher
  `stdin=p1.stdout` sur le second.
- Toujours appeler `communicate()` à la fin pour éviter les blocages.
- Pour 95 % des cas, `run` suffit largement. `Popen` ne sert que pour
  le parallélisme entre processus.

## Démo

Exécuter `03_demo_pipes.py`.
