# 01 — La fonction `print()`

## 1.1 La signature complète

On utilise `print(...)` depuis le premier jour, en général sans soupçonner
qu'elle prend **cinq paramètres**, pas un seul :

```python
print(*args, sep=' ', end='\n', file=sys.stdout, flush=False)
```

| Paramètre | Rôle                                                       | Valeur par défaut |
|-----------|------------------------------------------------------------|-------------------|
| `*args`   | Les valeurs à afficher (zéro, une, ou plusieurs)           | —                 |
| `sep`     | Chaîne insérée **entre** les valeurs                       | `' '` (espace)    |
| `end`     | Chaîne ajoutée **après** la dernière valeur                | `'\n'` (saut)     |
| `file`    | Objet fichier dans lequel écrire                           | `sys.stdout`      |
| `flush`   | Forcer l'envoi immédiat du tampon (`True`/`False`)         | `False`           |

Tous les paramètres autres que `*args` sont **nommés** : on les passe
sous la forme `nom=valeur`.

## 1.2 `*args` : zéro, une, ou plusieurs valeurs

```python
print()                    # ligne vide
print("Bonjour")           # une valeur
print("Bonjour", "Ada")    # deux valeurs, séparées par un espace
```

Chaque valeur est convertie en chaîne par `str(...)` avant l'affichage,
donc on peut mélanger les types librement :

```python
print("Année :", 2026, True)   # Année : 2026 True
```

## 1.3 `sep` : changer le séparateur

Par défaut, les valeurs sont collées avec un **espace** :

```python
print("a", "b", "c")             # a b c
print("a", "b", "c", sep="-")    # a-b-c
print("a", "b", "c", sep="")     # abc
print("a", "b", "c", sep="\n")   # une valeur par ligne
```

## 1.4 `end` : changer la fin

Par défaut, `print` termine par un **saut de ligne**. On peut le remplacer :

```python
print("Chargement", end="")
print("...", end="")
print(" OK")                     # Chargement... OK
```

C'est pratique pour construire une ligne morceau par morceau, ou pour
afficher une **barre de progression** qui se met à jour sans descendre.

## 1.5 `file` : choisir la destination

Par défaut, `print` écrit sur `sys.stdout` (la sortie standard). On peut
viser **stderr** (la sortie d'erreur) ou n'importe quel fichier ouvert :

```python
import sys

print("Résultat utile")                       # va sur stdout
print("Avertissement", file=sys.stderr)       # va sur stderr

with open("journal.txt", "w", encoding="utf-8") as f:
    print("Ligne écrite dans le fichier", file=f)
```

Distinction utile : depuis le shell, on redirige stdout avec `>` et
stderr avec `2>`. Voir le module `00_Concepts/03_flux_standards.md`.

## 1.6 `flush` : forcer l'envoi

Pour des raisons de performance, Python **bufferise** la sortie :
ce qu'on écrit avec `print` ne part pas immédiatement vers le terminal,
mais s'accumule dans un tampon (en mémoire) qui n'est vidé qu'à
intervalles réguliers (typiquement à chaque saut de ligne en mode
interactif, ou à la fermeture du programme).

Tant qu'il est dans le tampon, le texte **n'est pas encore visible**.
On force la vidange avec `flush=True` :

```python
import time

print("Traitement", end="", flush=True)   # apparaît tout de suite
for _ in range(3):
    time.sleep(1)
    print(".", end="", flush=True)        # un point par seconde
print(" terminé.")
```

Sans `flush=True`, on aurait vu apparaître `Traitement... terminé.` d'un
seul coup à la fin, parce que rien n'a forcé le tampon à se vider entre
les `print`.

Règle pratique : on a besoin de `flush=True` chaque fois qu'on veut
voir un message **avant** un saut de ligne ou avant la fin du programme
(animation, progression, attente d'une entrée).

## À retenir

- `print` accepte plusieurs valeurs séparées par `sep`, et termine par `end`.
- `file=sys.stderr` envoie le message sur la sortie d'erreur.
- `flush=True` force l'affichage immédiat (utile pour les animations).
- Toutes les valeurs sont converties en chaîne par `str()` au passage.

## Démo

Exécuter `01_demo_print.py`.
