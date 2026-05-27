# 01 — `subprocess.run` : la fonction recommandée

## 1.1 Le besoin

On veut, depuis un script Python, lancer une **commande externe** —
par exemple `ls -la` — et récupérer ce qu'elle affiche. On a trois
informations à récolter :

- le **texte écrit sur stdout** par la commande ;
- le **texte écrit sur stderr** par la commande ;
- le **code retour** (0 = succès, autre = échec).

La fonction `subprocess.run` fait exactement cela en un seul appel.

## 1.2 Signature minimale

```python
import subprocess

result = subprocess.run(
    args,                # la commande à lancer (voir 1.3)
    capture_output=True, # capturer stdout et stderr dans result
    text=True,           # décoder en str (sinon : bytes)
    check=False,         # lever une exception si code retour != 0
    timeout=None,        # nombre de secondes max, sinon TimeoutExpired
    input=None,          # texte à passer sur stdin du sous-processus
)
```

L'appel **bloque** jusqu'à ce que le sous-processus se termine, puis
renvoie un objet `CompletedProcess` qui expose trois attributs utiles :

| Attribut             | Contenu                                  |
|----------------------|------------------------------------------|
| `result.stdout`      | Tout ce qui a été écrit sur stdout       |
| `result.stderr`      | Tout ce qui a été écrit sur stderr       |
| `result.returncode`  | Le code retour de la commande (entier)   |

## 1.3 Passer la commande comme **liste**

C'est la règle d'or :

```python
subprocess.run(["ls", "-la", "/tmp"])
```

Et **non** :

```python
subprocess.run("ls -la /tmp")        # ne marchera pas (sans shell=True)
subprocess.run("ls -la /tmp", shell=True)   # à éviter (voir 1.6)
```

Pourquoi une liste ? Parce que Python passe alors le tableau
**directement** au système, qui le donne au programme tel quel. Pas
d'analyse, pas de découpage, pas de réinterprétation des espaces, des
guillemets ou des caractères spéciaux. C'est sûr et prévisible.

Le **premier** élément de la liste est le nom du programme. Les
suivants sont ses arguments, un par case :

```python
["echo", "bonjour", "le", "monde"]    # 4 cases : echo + 3 arguments
```

Si un argument contient lui-même un espace, il reste **dans une seule
case** :

```python
["echo", "bonjour le monde"]          # 2 cases : echo + 1 argument
```

## 1.4 Récupérer la sortie

Sans `capture_output=True`, la sortie du sous-processus se déverse
directement sur le terminal du programme appelant. Pour la
**récupérer** dans une variable Python, on demande explicitement la
capture :

```python
result = subprocess.run(
    ["echo", "bonjour"],
    capture_output=True,
    text=True,
)
print(repr(result.stdout))    # 'bonjour\n'
print(repr(result.stderr))    # ''
print(result.returncode)      # 0
```

`text=True` est presque toujours ce qu'on veut : Python décode la
sortie en `str` (UTF-8 par défaut sur les systèmes modernes). Sans cet
argument, on obtient des `bytes`, qu'il faut décoder soi-même.

## 1.5 Passer du texte sur stdin

L'argument `input` envoie une chaîne sur l'entrée standard du
sous-processus. Le sous-processus voit ce texte arriver comme si on
l'avait tapé au clavier :

```python
result = subprocess.run(
    ["wc", "-w"],
    input="un deux trois quatre\n",
    capture_output=True,
    text=True,
)
print(result.stdout.strip())   # 4
```

## 1.6 Pourquoi `shell=False` est la valeur sûre par défaut

`subprocess.run` accepte un argument `shell` qui vaut `False` par
défaut. Tenter de passer `shell=True` semble parfois pratique (« je
veux écrire ma commande comme dans le terminal ») mais c'est une
porte d'entrée à un risque classique : **l'injection de commande**.

Considérer ce code :

```python
nom = input("Nom du fichier ? ")
subprocess.run(f"cat {nom}", shell=True)   # DANGEREUX
```

Si l'utilisateur tape `truc.txt; rm -rf ~`, le shell interprète le
point-virgule et exécute aussi la deuxième commande. Catastrophe.

Avec une liste et `shell=False` (par défaut), le danger disparaît :

```python
nom = input("Nom du fichier ? ")
subprocess.run(["cat", nom])               # sûr
```

`nom` n'est jamais réinterprété par un shell : il est passé **tel
quel** comme argument unique à `cat`. Au pire, `cat` se plaint que le
fichier `truc.txt; rm -rf ~` n'existe pas.

**Règle** : ne jamais utiliser `shell=True` avec une entrée
utilisateur non vérifiée. Et si on n'a pas besoin du shell (variables
d'environnement, glob `*`, pipe `|`...), ne pas l'utiliser du tout.

## À retenir

- `subprocess.run(args, ...)` lance une commande et bloque jusqu'à
  sa fin.
- Toujours passer la commande comme **liste** : `["ls", "-la"]`.
- `capture_output=True` + `text=True` pour récupérer stdout/stderr en
  chaînes Python.
- L'objet renvoyé expose `stdout`, `stderr`, `returncode`.
- `shell=False` (la valeur par défaut) est la valeur sûre. Ne pas
  toucher.

## Démo

Exécuter `01_demo_run.py`.
