# 02 — Les flux standards vus depuis Python

Le chapitre `00_Concepts` a posé le décor : tout programme dispose de
trois tuyaux (stdin, stdout, stderr) que le système branche
automatiquement. Cette fiche montre **comment Python expose ces tuyaux**
et comment on les utilise dans un script.

## 2.1 Trois objets fichier déjà ouverts

Le module `sys` expose trois objets fichier prêts à l'emploi :

| Attribut       | Numéro OS | Sens    | Usage typique en Python      |
|----------------|-----------|---------|------------------------------|
| `sys.stdin`    | 0         | lecture | `for ligne in sys.stdin:`    |
| `sys.stdout`   | 1         | écriture| `print(...)` y va par défaut |
| `sys.stderr`   | 2         | écriture| `print(..., file=sys.stderr)`|

Ils sont **déjà ouverts** quand le script démarre et **se ferment
tout seuls** quand il s'arrête. On n'ouvre ni ne ferme ces flux
manuellement.

## 2.2 Écrire sur stdout et stderr

`print` écrit sur `sys.stdout` sauf indication contraire :

```python
import sys

print("Résultat normal")                     # va sur stdout
print("Avertissement", file=sys.stderr)      # va sur stderr
```

On peut aussi écrire directement via la méthode `write`, qui n'ajoute
**pas** de saut de ligne :

```python
sys.stdout.write("ligne 1\n")
sys.stderr.write("erreur 1\n")
```

`print` ajoute `\n` automatiquement ; `write` ne le fait pas. Choisir
en conséquence.

## 2.3 Lire depuis stdin

Deux formes très utilisées.

### Ligne par ligne, façon Unix

```python
import sys

for ligne in sys.stdin:
    # ligne se termine par "\n" (sauf éventuellement la dernière)
    ligne = ligne.rstrip("\n")
    print("Reçu :", ligne)
```

C'est la forme idéale pour traiter une entrée potentiellement très
longue : Python lit au fur et à mesure, sans tout charger en mémoire.

### Tout en une fois

```python
import sys

contenu = sys.stdin.read()    # tout, jusqu'à la fin du flux
print("Lu", len(contenu), "caractères")
```

À réserver aux entrées dont on sait qu'elles tiennent en mémoire.

### Quand la lecture s'arrête-t-elle ?

- Si stdin vient d'un **fichier** ou d'un **pipe**, la lecture se
  termine quand la source est épuisée (fin de fichier, ou amont qui se
  termine).
- Si stdin vient du **clavier**, on signale la fin avec `Ctrl+D` sous
  Unix (`Ctrl+Z` puis `Entrée` sous Windows).

## 2.4 Terminal ou pipe ? `isatty()`

Un script peut détecter s'il est branché sur un **terminal interactif**
ou sur **autre chose** (fichier, pipe) :

```python
import sys

if sys.stdin.isatty():
    print("On est branché sur un terminal interactif.")
else:
    print("stdin vient d'un fichier ou d'un pipe.")
```

Cette détection est utile pour :

- afficher une invite uniquement quand un humain regarde ;
- adapter le format de sortie (couleurs en interactif, sortie brute en
  pipe) ;
- refuser de lire `stdin` quand aucune entrée n'a été branchée et que
  l'utilisateur l'a oublié.

`isatty()` existe symétriquement sur `sys.stdout` (utile pour décider
de coloriser ou non) et `sys.stderr`.

## 2.5 stdout vs stderr : la règle d'or

| Sur quel flux ?      | Quoi y écrire                                      |
|----------------------|----------------------------------------------------|
| `sys.stdout`         | Le **résultat** du programme (données utiles)      |
| `sys.stderr`         | Journaux, progression, avertissements, erreurs     |

La raison pratique : on veut pouvoir faire

```
$ python3 mon_script.py > donnees.txt
```

sans que les messages de progression viennent polluer `donnees.txt`.
C'est exactement ce que permet la séparation des deux flux.

Si on n'arrive pas à décider, se poser la question : **« quelqu'un va-t-il
vouloir capturer cette ligne dans un fichier et la traiter ensuite ? »**.
Si oui : stdout. Si c'est juste pour informer un humain : stderr.

## 2.6 Mode texte par défaut

Les trois flux exposés par `sys` sont en **mode texte** (`str`), avec
un encodage qui dépend de l'environnement (presque toujours UTF-8 sur
les systèmes modernes). On y écrit des chaînes, pas des octets.

Pour échanger des **octets** (`bytes`) — par exemple pour un protocole
binaire — on passe par l'attribut `.buffer` :

```python
import sys

sys.stdout.buffer.write(b"\x00\x01\x02")     # octets bruts
donnees = sys.stdin.buffer.read()            # bytes, pas str
```

C'est un détail à connaître ; en pratique, dans ce chapitre, on reste
en mode texte.

## À retenir

- `sys.stdin`, `sys.stdout`, `sys.stderr` sont trois fichiers déjà
  ouverts par le système.
- `print` écrit sur stdout ; `print(..., file=sys.stderr)` sur stderr.
- `for ligne in sys.stdin:` itère ligne à ligne, sans tout charger.
- `sys.stdin.read()` lit jusqu'à la fin du flux.
- `sys.stdin.isatty()` distingue un terminal d'un pipe ou d'un fichier.
- stdout = résultat, stderr = messages : ne pas mélanger.

## Démo

Exécuter `02_demo_flux.py` de plusieurs manières :

```
$ python3 02_demo_flux.py
$ echo "bonjour\nle monde" | python3 02_demo_flux.py
$ python3 02_demo_flux.py < /etc/hostname
```
