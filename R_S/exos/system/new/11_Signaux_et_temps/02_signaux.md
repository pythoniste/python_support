# 02 — Signaux

## 2.1 Qu'est-ce qu'un signal ?

Un **signal** est un événement **asynchrone** envoyé à un processus par
le système d'exploitation (ou par un autre processus). « Asynchrone »
veut dire qu'il **peut arriver à n'importe quel moment**, sans crier
gare, au milieu de n'importe quelle ligne de code.

Le cas le plus quotidien : on tape **Ctrl+C** dans un terminal pendant
qu'un script tourne. Le shell envoie alors le signal `SIGINT` au
processus, et Python lève par défaut une exception
`KeyboardInterrupt`. C'est *déjà* un comportement par défaut basé sur
les signaux.

## 2.2 Les signaux à connaître

On retient surtout trois noms :

| Signal     | Provenance typique            | Trappable ? |
|------------|-------------------------------|-------------|
| `SIGINT`   | Ctrl+C dans le terminal       | Oui         |
| `SIGTERM`  | `kill <pid>` (arrêt poli)     | Oui         |
| `SIGKILL`  | `kill -9 <pid>` (arrêt brutal)| **Non**     |

**Insistons.** `SIGKILL` ne peut **jamais** être intercepté, ignoré ou
ralenti par le programme. Le système tue le processus immédiatement.
Aucun handler Python ne s'exécute, aucun bloc `finally` ne tourne,
aucune fonction `atexit` n'est appelée. C'est la mort instantanée.

Même chose pour `SIGSTOP` (le frère jumeau, qui suspend le processus
au lieu de le tuer) : non trappable.

Conséquence pratique : on peut écrire un script qui s'arrête
proprement sur Ctrl+C ou sur `kill <pid>`, mais aucun code ne peut se
prémunir contre `kill -9`. C'est *voulu*, pour pouvoir tuer un
processus bloqué quoi qu'il arrive.

## 2.3 Installer un handler

Le module `signal` permet d'associer une fonction à un signal :

```python
import signal

def handler(signum, frame):
    print(f"Signal {signum} reçu, arrêt propre.")
    raise SystemExit(0)

signal.signal(signal.SIGINT, handler)
```

La signature d'un handler est **toujours** `(signum, frame)`, même
si on n'utilise pas `frame` :

- `signum` : le numéro du signal reçu (entier).
- `frame` : la frame d'exécution Python interrompue (rarement utile).

Une fois `signal.signal(...)` appelée, la fonction `handler` est
exécutée à la place du comportement par défaut chaque fois que ce
signal arrive.

## 2.4 Exemple : boucle qui s'arrête proprement

```python
import signal
import time

stop = False

def handler(signum, frame):
    global stop
    print("Arrêt demandé.")
    stop = True

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

while not stop:
    print("Travail en cours...")
    time.sleep(1)

print("Sortie propre.")
```

On peut tester ce script en tapant Ctrl+C, ou bien en envoyant
`SIGTERM` depuis un autre terminal :

```
$ kill <pid>
```

Le handler met `stop` à `True`, la boucle s'arrête après l'itération
en cours, et le programme sort avec le code retour `0`.

## 2.5 Cas Windows

Sous Windows, **très peu de signaux existent**. En pratique, on peut
compter sur `SIGINT` (Ctrl+C) et c'est à peu près tout. `SIGTERM`
existe mais son comportement diffère, et la plupart des autres
constantes ne sont pas disponibles. Si on cible Windows, on s'en tient
à `SIGINT` ou on protège l'installation du handler :

```python
import signal

if hasattr(signal, "SIGTERM"):
    signal.signal(signal.SIGTERM, handler)
```

## 2.6 Restaurer le comportement par défaut

Deux constantes spéciales permettent de réinitialiser ou d'ignorer
un signal :

```python
signal.signal(signal.SIGINT, signal.SIG_DFL)   # comportement par défaut
signal.signal(signal.SIGINT, signal.SIG_IGN)   # ignorer le signal
```

`SIG_IGN` rend le signal silencieux ; à utiliser avec parcimonie, car
on peut rendre un programme **impossible à arrêter avec Ctrl+C**, ce
qui frustre l'utilisateur. Dans ce cas, `kill -9` reste l'ultime
recours, justement parce qu'il est non trappable.

## À retenir

- Un signal est un événement asynchrone envoyé au processus.
- `signal.signal(signal.SIGINT, handler)` installe une fonction
  pour `SIGINT` ; la signature est `(signum, frame)`.
- `SIGINT` = Ctrl+C, `SIGTERM` = `kill <pid>`.
- `SIGKILL` (`kill -9`) et `SIGSTOP` ne peuvent **jamais** être
  interceptés.
- Sous Windows, l'éventail de signaux est très limité ; rester sur
  `SIGINT` est le plus sûr.

## Démo

Exécuter `02_demo_signaux.py`, puis taper Ctrl+C pour voir le
handler s'exécuter.
