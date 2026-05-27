# 03 — Flux standards et code retour

## 3.1 Trois tuyaux par programme

Quand le système lance un programme, il lui branche automatiquement
**trois tuyaux** (les *flux standards*) :

| Nom    | Numéro | Sens    | Rôle                           |
|--------|--------|---------|--------------------------------|
| stdin  | 0      | entrée  | Données fournies au programme  |
| stdout | 1      | sortie  | Résultat normal du programme   |
| stderr | 2      | sortie  | Messages d'erreur et journaux  |

Par défaut, stdin est branché sur le clavier, stdout et stderr sur
l'écran. Mais le shell peut **rediriger** chacun de ces tuyaux vers un
fichier ou vers un autre programme — c'est tout l'intérêt de les avoir
séparés.

## 3.2 Les trois tuyaux en Python

Le module `sys` les expose comme des objets fichier ouverts en
permanence :

```python
import sys

sys.stdout.write("Résultat normal\n")
sys.stderr.write("Avertissement\n")
ligne = sys.stdin.readline()    # bloque jusqu'à une entrée
```

`print(...)` écrit par défaut sur `sys.stdout`. Pour écrire sur
`stderr`, on précise l'argument `file` :

```python
print("Erreur fatale", file=sys.stderr)
```

## 3.3 Redirections shell

Le shell offre une notation compacte pour rebrancher les tuyaux :

| Notation         | Effet                                           |
|------------------|-------------------------------------------------|
| `cmd > out.txt`  | Redirige stdout vers `out.txt` (écrase)         |
| `cmd >> out.txt` | Redirige stdout vers `out.txt` (ajoute à la fin)|
| `cmd 2> err.txt` | Redirige stderr vers `err.txt`                  |
| `cmd < in.txt`   | Lit stdin depuis `in.txt`                       |
| `cmd1 \| cmd2`   | Branche stdout de `cmd1` sur stdin de `cmd2`    |

Exemple en pratique :

```
$ python3 mon_script.py > sortie.txt 2> erreurs.txt
```

Le résultat normal va dans `sortie.txt`, les messages d'erreur dans
`erreurs.txt`, et rien ne s'affiche à l'écran.

Et le grand classique du *pipe* :

```
$ python3 producteur.py | python3 consommateur.py
```

Le consommateur lit sur son stdin ce que le producteur écrit sur son
stdout. Aucun fichier temporaire ; tout passe par un tube en mémoire.

## 3.4 Le code retour

Lorsqu'un programme termine, il rend au système un **entier** appelé
*code retour* (ou *exit status*). La convention est universelle :

| Code retour | Signification           |
|-------------|-------------------------|
| `0`         | Succès                  |
| Différent de `0` | Erreur ou échec    |

Le shell récupère ce code dans la variable `$?` :

```
$ python3 mon_script.py
$ echo $?
0
```

En Python, on contrôle le code retour avec `sys.exit(code)` :

```python
import sys

if len(sys.argv) < 2:
    print("Usage: script.py <fichier>", file=sys.stderr)
    sys.exit(1)        # erreur : argument manquant
```

Quelques règles utiles :

- `sys.exit(0)` ou `sys.exit()` : succès.
- `sys.exit(N)` avec `N` entre 1 et 255 : erreur.
- Si une exception non rattrapée remonte jusqu'au sommet, Python
  affiche la trace et sort avec un code différent de zéro.

## 3.5 Pourquoi séparer stdout et stderr ?

Imaginons un script qui produit des données utiles et affiche aussi des
informations de progression. Si tout sort sur stdout, impossible de
sauvegarder les données sans les messages :

```
$ python3 script.py > resultat.txt    # le résultat est pollué !
```

En envoyant la progression sur stderr, on garde stdout « propre » :

```
$ python3 script.py > resultat.txt    # stderr s'affiche toujours
Progression : 10%
Progression : 50%
Progression : 100%
$ cat resultat.txt
(données utiles uniquement)
```

C'est la raison d'être de la séparation : permettre à l'utilisateur de
**filtrer**, **rediriger** ou **canaliser** chaque flux indépendamment.

## À retenir

- Tout programme a trois flux : stdin (0), stdout (1), stderr (2).
- `print` écrit sur stdout ; ajouter `file=sys.stderr` pour stderr.
- Le shell redirige chaque flux avec `>`, `>>`, `2>`, `<`, `|`.
- Le code retour vaut `0` en cas de succès, autre chose en cas d'erreur.
- `sys.exit(code)` permet de choisir explicitement ce code.

## Démo

Exécuter `03_demo_flux.py`, puis essayer les redirections proposées
en commentaire à la fin du script.
