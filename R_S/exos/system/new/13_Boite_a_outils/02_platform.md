# 02 — `platform` : connaître la machine

## 2.1 À quoi ça sert

Le module `platform` permet d'interroger Python sur **la machine qui
l'exécute** : système d'exploitation, version, architecture, nom de
machine, version de Python. C'est utile pour :

- adapter du code à l'OS (un chemin par défaut diffère sous Linux et
  Windows) ;
- afficher un message d'accueil personnalisé dans un script
  d'installation ;
- coller dans un rapport de bug une description fiable de
  l'environnement.

Aucune dépendance, aucune connexion réseau : tout est lu localement.

## 2.2 Les six fonctions à connaître

```python
import platform

print(platform.system())          # nom de l'OS
print(platform.release())         # version courte du noyau
print(platform.version())         # version détaillée du noyau
print(platform.machine())         # architecture CPU
print(platform.node())            # nom réseau de la machine
print(platform.python_version())  # version de Python qui exécute
```

| Fonction                  | Renvoie (exemple)                      |
|---------------------------|----------------------------------------|
| `platform.system()`       | `"Linux"`, `"Darwin"` (macOS), `"Windows"` |
| `platform.release()`      | `"6.1.0-48-amd64"`, `"23.0.0"`, `"10"` |
| `platform.version()`      | Une chaîne longue propre à l'OS        |
| `platform.machine()`      | `"x86_64"`, `"arm64"`, `"aarch64"`     |
| `platform.node()`         | Nom d'hôte, p. ex. `"laptop-ada"`      |
| `platform.python_version()` | `"3.12.3"`                           |

À noter : `platform.system()` renvoie `"Darwin"` sur macOS (le nom
historique du noyau), **pas** `"macOS"`. Piège classique quand on
écrit un test `if system == "macOS"` qui ne se déclenche jamais.

## 2.3 Adapter un code selon l'OS

Le motif typique :

```python
import platform

systeme = platform.system()
if systeme == "Linux":
    config = "/etc/monapp/config.ini"
elif systeme == "Darwin":
    config = "/Library/Application Support/monapp/config.ini"
elif systeme == "Windows":
    config = r"C:\ProgramData\monapp\config.ini"
else:
    raise RuntimeError(f"OS non supporte : {systeme}")
```

Pour les chemins de configuration utilisateur, il existe mieux
(`pathlib.Path.home()`, ou la bibliothèque `platformdirs` hors stdlib).
Mais pour un branchement métier simple, `platform.system()` suffit.

## 2.4 Distinguer 32 / 64 bits

`platform.machine()` donne l'architecture du processeur. Pour
distinguer 32 et 64 bits côté **Python**, le plus simple reste :

```python
import sys
print(sys.maxsize > 2**32)   # True sur un Python 64 bits
```

`platform.architecture()` existe aussi mais renvoie un résultat moins
fiable sous macOS et Windows ; à éviter en première intention.

## 2.5 Un en-tête de rapport de bug

Quand on demande à un utilisateur de copier-coller son environnement,
ces quelques lignes font le travail :

```python
import platform, sys

print("OS     :", platform.system(), platform.release())
print("Arch   :", platform.machine())
print("Machine:", platform.node())
print("Python :", platform.python_version(), "(", sys.executable, ")")
```

Sortie typique sous Linux :

```
OS     : Linux 6.1.0-48-amd64
Arch   : x86_64
Machine: laptop-ada
Python : 3.12.3 ( /usr/bin/python3 )
```

## À retenir

- `platform.system()` renvoie `"Linux"`, `"Darwin"` (macOS),
  `"Windows"` — **pas** `"macOS"`.
- `platform.machine()` donne l'architecture (`x86_64`, `arm64`…).
- `platform.node()` donne le nom de la machine, `platform.python_version()`
  la version de Python en cours.
- Pour brancher selon l'OS, comparer `platform.system()` à une chaîne
  fixe.
- Pour 64 bits, préférer `sys.maxsize > 2**32` à
  `platform.architecture()`.

## Démo

Exécuter `02_demo_platform.py`.
