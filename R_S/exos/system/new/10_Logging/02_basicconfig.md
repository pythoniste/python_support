# 02 — Configuration minimale avec `basicConfig`

## 2.1 Une seule ligne pour démarrer

Pour utiliser `logging` sérieusement, il faut au moins fixer le seuil et
le format. C'est le rôle de `logging.basicConfig(...)` :

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

Tout `logging.info(...)`, `logging.warning(...)`, etc. appelé **après**
cet appel suivra ces réglages.

## 2.2 Les paramètres utiles

`basicConfig` accepte de nombreux paramètres. On retient cinq en
priorité :

| Paramètre   | Rôle                                                   |
|-------------|--------------------------------------------------------|
| `level`     | Seuil global (`DEBUG`, `INFO`, `WARNING`, ...)         |
| `format`    | Gabarit appliqué à chaque ligne                        |
| `datefmt`   | Format de la date dans `%(asctime)s`                   |
| `filename`  | Fichier où écrire (au lieu de stderr)                  |
| `filemode`  | Mode d'ouverture du fichier : `"a"` (par défaut) ou `"w"` |

Exemple avec un fichier journal :

```python
logging.basicConfig(
    level=logging.DEBUG,
    filename="app.log",
    filemode="a",                # "a" = append, "w" = écrase
    format="%(asctime)s %(levelname)-8s %(name)s : %(message)s",
)
```

## 2.3 Le format recommandé

Le gabarit conseillé pour commencer est :

```
"%(asctime)s %(levelname)-8s %(name)s : %(message)s"
```

Chaque champ entre `%(...)s` est un **attribut** que `logging` remplace
automatiquement :

| Champ           | Contenu                                              |
|-----------------|------------------------------------------------------|
| `%(asctime)s`   | Date et heure de l'événement                         |
| `%(levelname)s` | Nom du niveau (`INFO`, `WARNING`, ...)               |
| `%(name)s`      | Nom du logger (souvent celui du module)              |
| `%(message)s`   | Le message lui-même                                  |

Le `-8` dans `%(levelname)-8s` aligne le nom du niveau sur 8 caractères
à gauche — `INFO    ` au lieu de `INFO`. Cela rend le journal facile à
lire en colonnes.

Exemple de sortie :

```
2026-05-27 09:12:03 INFO     __main__ : démarrage du service
2026-05-27 09:12:05 WARNING  __main__ : disque à 92 %
2026-05-27 09:12:07 ERROR    __main__ : impossible d'ouvrir fichier.txt
```

## 2.4 Une seule fois, en début de programme

`basicConfig` doit être appelé **une fois**, au tout début du
programme, **avant** le premier `logging.info(...)`. La bonne place est
en haut de la fonction `main()` ou tout juste sous les imports.

```python
import logging


def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(name)s : %(message)s")
    logging.info("Programme démarré")
    ...


if __name__ == "__main__":
    main()
```

## 2.5 Piège : appels multiples ignorés

Voici un piège fréquent. Par défaut, `basicConfig` **ne fait rien** si
le système de journalisation est déjà configuré (par un précédent appel,
ou parce qu'un module importé l'a déjà appelé). Code surprenant :

```python
import logging

logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.DEBUG)   # IGNORÉ silencieusement
logging.debug("ce message n'apparaîtra pas")
```

Deux solutions :

1. **Une seule** appel de `basicConfig` dans toute l'application
   (recommandé).
2. Si on doit réellement reconfigurer, passer `force=True` (Python 3.8+) :

   ```python
   logging.basicConfig(level=logging.DEBUG, force=True)
   ```

`force=True` supprime les handlers déjà installés sur le logger racine
avant d'en poser de nouveaux. À utiliser avec précaution.

## À retenir

- `basicConfig` configure le module en une ligne : seuil + format.
- Cinq paramètres clés : `level`, `format`, `datefmt`, `filename`,
  `filemode`.
- Format conseillé : `"%(asctime)s %(levelname)-8s %(name)s : %(message)s"`.
- Appel **unique** en début de programme.
- Un second appel est ignoré, sauf avec `force=True`.

## Démo

Exécuter `02_demo_basicconfig.py` et inspecter le fichier journal créé
dans un répertoire temporaire.
