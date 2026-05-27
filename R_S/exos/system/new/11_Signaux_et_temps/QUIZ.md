# Quiz de validation — dossier 11_Signaux_et_temps

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer au chapitre suivant. Les réponses se trouvent en fin de document
— tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Pour chronométrer la durée d'une opération, on hésite entre
`datetime.now()` et `time.monotonic()`. Lequel choisir, et pourquoi
l'autre est-il un mauvais choix ?

**Q2.** Quelle est la signature obligatoire d'un handler de signal en
Python ? Que représente chaque paramètre ?

**Q3.** Un script installe un handler pour `SIGINT`. Un utilisateur
veut malgré tout l'arrêter coûte que coûte. Quelle commande peut-il
employer, et pourquoi est-elle imparable ?

**Q4.** Trois fonctions sont enregistrées dans cet ordre :

```python
atexit.register(a)
atexit.register(b)
atexit.register(c)
```

Dans quel ordre s'exécutent-elles à la sortie du programme ?

**Q5.** Citer **deux** cas où une fonction enregistrée avec
`atexit.register` ne sera **pas** appelée.

**Q6.** Que renvoie l'expression suivante, et de quel type ?

```python
from datetime import datetime
datetime(2026, 5, 27, 14, 32, 0) - datetime(2026, 5, 27, 14, 30, 0)
```

---

## Réponses

**R1.** On choisit `time.monotonic()`. Cette horloge est garantie de
**ne jamais reculer**, ce qui est exactement ce qu'on veut pour une
durée. `datetime.now()` reflète l'heure murale, qui peut sauter en
arrière (passage à l'heure d'hiver, synchronisation NTP, action de
l'administrateur), ce qui peut produire des durées négatives ou
fantaisistes.

**R2.** `def handler(signum, frame): ...`. `signum` est le numéro
entier du signal reçu ; `frame` est la frame d'exécution Python
interrompue par l'arrivée du signal. En pratique, on utilise rarement
`frame`, mais elle doit figurer dans la signature.

**R3.** `kill -9 <pid>`, qui envoie `SIGKILL`. Ce signal **ne peut
pas être intercepté**, ignoré, ralenti ni ralenti par le programme :
le système tue le processus immédiatement. C'est précisément pour
cette raison qu'on garde toujours une porte de sortie « ultime ».
`SIGSTOP` (suspension forcée) partage la même propriété.

**R4.** Ordre **inverse** : `c`, puis `b`, puis `a`. `atexit` suit le
modèle LIFO (Last In, First Out) — la dernière fonction enregistrée
est la première exécutée.

**R5.** Quelques exemples valables :

- appel à `os._exit(code)` (sortie immédiate, sans nettoyage Python) ;
- réception d'un signal fatal non intercepté, en particulier `SIGKILL`
  (`kill -9`) ;
- crash de l'interpréteur (segfault, panne).

Citer deux de ces cas suffit.

**R6.** Un objet `datetime.timedelta` représentant une durée de 2
minutes (`0:02:00`). On peut en extraire les secondes totales avec
`.total_seconds()`, qui vaudrait alors `120.0`. La soustraction de
deux `datetime` ne donne **jamais** un nombre brut.
