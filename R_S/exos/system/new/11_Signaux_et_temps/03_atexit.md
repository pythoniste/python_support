# 03 — `atexit` : code à la sortie

## 3.1 Le besoin

Beaucoup de scripts doivent **libérer une ressource** ou **sauvegarder
un état** avant de quitter : fermer un fichier journal, écrire un
fichier de configuration, supprimer un fichier temporaire, déconnecter
un socket. On pourrait mettre ce code à la fin du `main()`, mais que
se passe-t-il si une exception remonte avant ?

Le module `atexit` permet d'enregistrer **dès le début du programme**
une fonction qui sera appelée **à la sortie**, normale ou par
exception non rattrapée.

## 3.2 L'API

```python
import atexit

def au_revoir():
    print("Programme terminé, on range.")

atexit.register(au_revoir)
```

Plus tard, à la sortie du programme, Python appelle `au_revoir()`.
On peut aussi passer des arguments à enregistrer :

```python
atexit.register(sauver_fichier, "etat.json", {"compteur": 42})
```

Au moment de la sortie, Python appellera
`sauver_fichier("etat.json", {"compteur": 42})`.

## 3.3 Ordre d'exécution : LIFO

Si plusieurs fonctions sont enregistrées, elles sont exécutées dans
l'ordre **inverse de l'enregistrement** (LIFO, *Last In First Out*) :

```python
atexit.register(lambda: print("A"))
atexit.register(lambda: print("B"))
atexit.register(lambda: print("C"))
# À la sortie : C, B, A
```

Cet ordre est logique : la dernière chose initialisée est souvent
la première à libérer (un fichier ouvert *après* un socket doit être
fermé *avant* lui).

## 3.4 Ce qui déclenche `atexit`

`atexit` est exécuté :

- à la fin normale du programme (le `main()` rend la main) ;
- sur `sys.exit(code)` (qui lève `SystemExit`) ;
- sur une exception non rattrapée qui remonte jusqu'au sommet.

## 3.5 Ce qui ne le déclenche **pas**

Trois cas où les fonctions enregistrées **ne tournent pas** :

- **`os._exit(code)`** : sortie immédiate, sans nettoyage Python.
  À éviter sauf cas très particuliers (processus fils après `fork`,
  par exemple).
- **Signaux fatals non interceptés** : `SIGKILL`, et tout autre
  signal qui termine le processus sans qu'un handler ne lève une
  exception côté Python.
- **Crash du processus** (segfault de l'interpréteur, panne matérielle).

Conséquence importante : `atexit` est un mécanisme **best-effort**
pour la sortie normale. Ce n'est **pas** une garantie absolue. Pour les
données vraiment critiques, on écrit au fil de l'eau plutôt que
d'attendre la fin.

## 3.6 Combiner `atexit` et signaux

Un patron utile : on installe un handler de signal qui appelle
`sys.exit(0)`, et on met le nettoyage dans `atexit`. Ainsi, Ctrl+C
provoque bien le nettoyage.

```python
import atexit
import signal

def nettoyer():
    print("Nettoyage final.")

atexit.register(nettoyer)

def handler(signum, frame):
    raise SystemExit(0)   # déclenche atexit

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
```

Sans le handler, `SIGTERM` brut tue le processus *sans* passer par
`atexit`. Avec le handler qui lève `SystemExit`, on bascule sur une
sortie normale et `atexit` est appelé.

## À retenir

- `atexit.register(fonction, *args)` programme un appel à la sortie.
- L'ordre d'exécution est **LIFO** (dernier enregistré, premier exécuté).
- `atexit` tourne pour la sortie normale, `sys.exit`, et les exceptions
  non rattrapées.
- `atexit` ne tourne **pas** pour `os._exit`, ni pour les signaux
  fatals non interceptés (`SIGKILL` en particulier).
- Pour garantir que Ctrl+C ou `kill <pid>` déclenche `atexit`,
  installer un handler de signal qui lève `SystemExit`.

## Démo

Exécuter `03_demo_atexit.py` et observer l'ordre LIFO de sortie.
