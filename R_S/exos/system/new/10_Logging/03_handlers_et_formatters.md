# 03 — Loggers nommés, handlers et formatters

## 3.1 Trois objets, trois rôles

`basicConfig` suffit pour les scripts courts. Dès qu'une application
grossit, on bascule sur l'API « complète » qui distingue trois objets :

| Objet       | Rôle                                                          |
|-------------|---------------------------------------------------------------|
| `Logger`    | Point d'entrée : on lui demande de logger un message          |
| `Handler`   | Où va le message (console, fichier, syslog, ...)              |
| `Formatter` | Comment le message est rendu (date, niveau, message, ...)     |

Un `Logger` peut avoir **plusieurs** handlers. Chaque handler peut avoir
son propre formatter et son propre seuil.

## 3.2 Un logger nommé par module

La convention universelle est de créer un logger par module, nommé
d'après le module :

```python
import logging

logger = logging.getLogger(__name__)
```

`__name__` vaut `"mon_paquet.mon_module"` lorsque le fichier est importé,
ou `"__main__"` lorsqu'il est exécuté directement. L'avantage : la
colonne `%(name)s` indique immédiatement de quel module vient chaque
ligne, et on peut régler des seuils différents par module
(`logging.getLogger("auth").setLevel(logging.DEBUG)` par exemple).

`getLogger(nom)` renvoie toujours **le même objet** pour le même nom.
Pas besoin de le stocker globalement de façon spéciale.

## 3.3 Ajouter un handler à la main

On crée un handler, on lui colle un formatter, on l'attache au logger :

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)   # le logger laisse tout passer

console = logging.StreamHandler()                 # par défaut : stderr
console.setLevel(logging.WARNING)                 # console = WARNING+
console.setFormatter(logging.Formatter(
    "%(levelname)-8s %(name)s : %(message)s"
))
logger.addHandler(console)
```

`StreamHandler()` envoie sur `stderr` par défaut ; passer
`StreamHandler(sys.stdout)` pour rediriger sur stdout.

## 3.4 Deux destinations en parallèle

L'exemple type : tout le détail dans un fichier (pour l'analyse
*a posteriori*), et seulement les ennuis sur la console (pour ne pas
inonder l'utilisateur).

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Fichier : tout, en DEBUG.
fichier = logging.FileHandler("app.log", mode="a", encoding="utf-8")
fichier.setLevel(logging.DEBUG)
fichier.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)-8s %(name)s : %(message)s"
))
logger.addHandler(fichier)

# Console : seulement WARNING et au-dessus, format plus court.
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(logging.Formatter(
    "%(levelname)-8s : %(message)s"
))
logger.addHandler(console)
```

À partir de là, un `logger.debug("...")` finit **uniquement** dans
`app.log` ; un `logger.error("...")` apparaît **sur la console** *et*
dans le fichier.

## 3.5 Comment le filtrage fonctionne

Quand on appelle `logger.info("..."`, voici l'ordre des décisions :

1. Le **logger** compare son seuil au niveau du message. Trop bas ?
   On ignore tout de suite.
2. Sinon, le message est envoyé à **chaque handler** attaché.
3. Chaque **handler** compare *son* seuil au niveau du message. Trop
   bas ? Il ignore. Sinon, il met en forme et écrit.

Conséquence pratique : le seuil du logger sert de filtre **global** ;
le seuil de chaque handler permet d'**affiner** par destination.

## 3.6 Les handlers les plus courants

| Classe           | Destination                            |
|------------------|----------------------------------------|
| `StreamHandler`  | Flux texte (stderr par défaut, stdout) |
| `FileHandler`    | Fichier sur disque                     |
| `NullHandler`    | Rien — utile dans une bibliothèque     |

Il en existe d'autres dans `logging.handlers` (rotation par taille,
rotation quotidienne, syslog, mail, ...) mais ces trois-là couvrent
l'écrasante majorité des besoins.

## À retenir

- Trois objets : `Logger`, `Handler`, `Formatter`.
- `getLogger(__name__)` : un logger par module, nommé proprement.
- Un logger peut avoir plusieurs handlers, chacun avec son propre seuil.
- Filtrage en deux étapes : seuil du logger, puis seuil du handler.
- `FileHandler` pour archiver, `StreamHandler` pour la console.

## Démo

Exécuter `03_demo_handlers.py` : un même logger envoie en `DEBUG` vers
un fichier temporaire et en `WARNING` sur la console. Comparer les
deux sorties.
