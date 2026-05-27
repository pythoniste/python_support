# 01 — Temps et dates

## 1.1 Deux questions, deux outils

Avant d'écrire la moindre ligne, il faut distinguer deux questions
que les débutants confondent souvent :

| Question                              | Outil approprié                |
|---------------------------------------|--------------------------------|
| « Quelle heure est-il **maintenant** ? » | `datetime` (un *instant*)   |
| « Combien de temps a duré ceci ? »    | `time.monotonic` (une *durée*) |

Un *instant* est une date sur le calendrier (le 27 mai 2026 à 14 h 30).
Une *durée* est un intervalle entre deux mesures (3,4 secondes).

Le piège classique : utiliser `datetime.now()` pour mesurer une durée.
Si l'horloge système est ajustée pendant la mesure (changement d'heure
d'été, synchronisation NTP, action de l'administrateur), la durée
mesurée devient fausse — parfois négative ! C'est pour ça qu'il existe
des horloges dites **monotones**.

## 1.2 Mesurer une durée : `time.monotonic` et `time.perf_counter`

Le module `time` expose plusieurs horloges. Les deux qui comptent
pour mesurer un intervalle sont :

```python
import time

debut = time.monotonic()
# ... opération à mesurer ...
duree = time.monotonic() - debut
print(f"Durée : {duree:.3f} s")
```

- `time.monotonic()` : ne **recule jamais**, idéal pour chronométrer.
- `time.perf_counter()` : même garantie, avec la **plus haute
  résolution** disponible sur la machine. Pour des durées très
  courtes (microsecondes), c'est ce qu'on prend.

La valeur absolue renvoyée n'a aucun sens en soi (elle peut valoir
quelques centaines de millions). Seules les **différences** entre deux
mesures sont utilisables.

## 1.3 Faire une pause : `time.sleep`

```python
time.sleep(2.5)   # bloque le programme pendant 2,5 seconde
```

L'argument est en **secondes** (entier ou flottant). Pendant la pause,
le processus est suspendu : il ne consomme pas de CPU. C'est l'outil
de base pour boucler à intervalles réguliers, ralentir une boucle, ou
attendre un événement externe avant de réessayer.

## 1.4 L'heure courante : `datetime.datetime.now`

```python
from datetime import datetime

maintenant = datetime.now()
print(maintenant)            # 2026-05-27 14:30:00.123456
print(maintenant.year)       # 2026
print(maintenant.hour)       # 14
```

Un objet `datetime` contient année, mois, jour, heure, minute, seconde
et microsecondes. On peut accéder à chaque composant par attribut.

## 1.5 Formater et parser : `strftime` et `strptime`

Pour passer d'un `datetime` à une chaîne lisible :

```python
maintenant.strftime("%Y-%m-%d %H:%M:%S")   # "2026-05-27 14:30:00"
```

Pour faire l'inverse — parser une chaîne en `datetime` :

```python
datetime.strptime("2026-05-27 14:30:00", "%Y-%m-%d %H:%M:%S")
```

Les codes de format les plus utiles :

| Code   | Signification           | Exemple |
|--------|-------------------------|---------|
| `%Y`   | Année sur 4 chiffres    | `2026`  |
| `%m`   | Mois sur 2 chiffres     | `05`    |
| `%d`   | Jour sur 2 chiffres     | `27`    |
| `%H`   | Heure (0–23)            | `14`    |
| `%M`   | Minute                  | `30`    |
| `%S`   | Seconde                 | `00`    |

Cas particulier : le format ISO 8601 (`2026-05-27T14:30:00`) est si
courant qu'il y a une méthode dédiée, sans format à fournir :

```python
datetime.fromisoformat("2026-05-27T14:30:00")
```

## 1.6 Calculer avec des dates : `timedelta`

Soustraire deux `datetime` ne donne **pas** un nombre, mais un
`timedelta` (une durée) :

```python
from datetime import datetime, timedelta

a = datetime(2026, 5, 27, 14, 30, 0)
b = datetime(2026, 5, 27, 14, 32, 30)
diff = b - a
print(diff)                 # 0:02:30
print(diff.total_seconds()) # 150.0
```

On peut aussi **ajouter** une durée à une date :

```python
demain = datetime.now() + timedelta(days=1)
dans_5_min = datetime.now() + timedelta(minutes=5)
```

À noter : `timedelta` représente une **durée calendaire**. Pour
chronométrer une opération, on reste avec `time.monotonic` — c'est
plus simple et plus fiable.

## À retenir

- *Instant* → `datetime` ; *durée mesurée* → `time.monotonic`.
- `time.sleep(s)` met le programme en pause pendant `s` secondes.
- `time.perf_counter()` est la plus haute résolution pour les
  durées très courtes.
- `strftime` formate, `strptime` parse, `fromisoformat` parse l'ISO.
- Soustraire deux `datetime` donne un `timedelta`, pas un nombre.

## Démo

Exécuter `01_demo_temps.py`.
