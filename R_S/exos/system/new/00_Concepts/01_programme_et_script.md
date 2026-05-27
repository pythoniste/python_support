# 01 — Programme, script, REPL

## 1.1 Qu'est-ce qu'un programme Python ?

Un **programme** Python est une suite d'instructions interprétées par
l'exécutable `python3`. Le code source est du texte brut. L'interpréteur
le lit, le transforme en *bytecode*, puis exécute ce bytecode dans une
machine virtuelle interne. On n'a donc **pas** à compiler à la main
comme en C : `python3` s'en occupe à chaque lancement.

Trois façons courantes de lui faire avaler du code :

| Mode               | Quand l'utiliser                        |
|--------------------|-----------------------------------------|
| REPL               | Tester une idée, explorer une API       |
| Script `.py`       | Code réutilisable, à lancer plusieurs fois |
| Module importé     | Code partagé entre plusieurs scripts    |

## 1.2 Le REPL

REPL signifie *Read-Eval-Print-Loop* : « lire, évaluer, afficher,
recommencer ». On le démarre en tapant simplement :

```
$ python3
Python 3.11.x (...) [...]
>>> 1 + 1
2
>>> nom = "Ada"
>>> print(f"Bonjour {nom}")
Bonjour Ada
>>> exit()
```

Le REPL est interactif : chaque ligne tapée est immédiatement évaluée.
C'est l'outil idéal pour expérimenter, mais le code saisi disparaît à
la sortie. Pour conserver le travail, on l'écrit dans un **script**.

## 1.3 Le script `.py`

Un script est un fichier texte d'extension `.py` contenant du code
Python. On le lance avec :

```
$ python3 mon_script.py
```

Le fichier est lu de haut en bas. Quand la dernière ligne est exécutée,
l'interpréteur s'arrête.

## 1.4 Rendre un script directement exécutable (Unix)

Sur Linux et macOS, on peut rendre un script `.py` exécutable comme une
commande, sans préfixer `python3`. Pour cela, deux ingrédients :

1. Une **ligne shebang** en toute première ligne du fichier :

```python
#!/usr/bin/env python3
print("Salut depuis un script exécutable.")
```

2. Le droit d'exécution sur le fichier :

```
$ chmod +x mon_script.py
$ ./mon_script.py
Salut depuis un script exécutable.
```

Le shebang `#!/usr/bin/env python3` demande au système de localiser
`python3` dans le `PATH` de l'utilisateur, ce qui est plus portable
qu'un chemin codé en dur comme `#!/usr/bin/python3`.

| Forme                       | Effet                                      |
|-----------------------------|--------------------------------------------|
| `python3 script.py`         | Marche partout, même sans shebang          |
| `./script.py` (après chmod) | Marche sous Unix, **shebang requis**       |

## 1.5 Le garde `if __name__ == "__main__":`

Quand on lance un fichier directement, Python lui attribue le nom
spécial `"__main__"`. Quand il est *importé* par un autre, son nom
devient celui du module. Le bloc suivant permet de séparer le code de
bibliothèque du code exécuté seulement en tant que script :

```python
def saluer(nom):
    return f"Bonjour {nom}"

if __name__ == "__main__":
    print(saluer("monde"))
```

On reverra ce motif tout au long du cours.

## À retenir

- Un programme Python est du texte interprété par `python3`.
- Le REPL sert à expérimenter, un script `.py` à conserver.
- `python3 fichier.py` marche partout ; `./fichier.py` exige un
  shebang et `chmod +x`.
- `#!/usr/bin/env python3` est le shebang portable recommandé.
- `if __name__ == "__main__":` distingue exécution directe et import.

## Démo

Exécuter `01_demo_programme.py`.
