# 01 — Variables d'environnement avec `os.environ`

## 1.1 Qu'est-ce qu'une variable d'environnement ?

Une **variable d'environnement** est une paire `NOM=valeur` que le
système d'exploitation passe à chaque processus au moment de son
lancement. Le shell expose les siennes via `$NOM` (Bash, Zsh) ou
`%NOM%` (cmd Windows). Quelques exemples universels :

| Nom    | Contenu typique                                          |
|--------|----------------------------------------------------------|
| `HOME` | Répertoire personnel de l'utilisateur (`/home/ada`)      |
| `PATH` | Liste de dossiers où chercher les exécutables            |
| `USER` | Nom de l'utilisateur courant                             |
| `LANG` | Locale et encodage (`fr_FR.UTF-8`)                       |

L'intérêt : **séparer la configuration du code**. Le même programme
peut tourner sur deux machines différentes et lire `$HOME` au lieu
d'avoir un chemin codé en dur.

## 1.2 `os.environ` en Python

Python expose les variables d'environnement via l'objet
`os.environ`, qui se comporte comme un **dictionnaire** :

```python
import os

print(os.environ["HOME"])   # lève KeyError si la variable n'existe pas
```

Pour éviter la `KeyError`, on utilise `.get()` avec une valeur par
défaut :

```python
print(os.environ.get("HOME", "/tmp"))   # "/tmp" si HOME est absente
```

Une autre forme utile, `setdefault`, **lit** la variable si elle existe
et **la crée** sinon :

```python
os.environ.setdefault("LANG", "C")
```

Convention : les noms de variables d'environnement sont **en
majuscules**, avec des soulignés comme séparateurs (`API_KEY`,
`HTTP_PROXY`).

## 1.3 Écriture : portée limitée

On peut affecter `os.environ["FOO"] = "bar"` pour **modifier** ou
**ajouter** une variable. Mais attention :

> La modification n'est visible que pour le **processus Python**
> en cours et pour les **sous-processus** qu'il lance ensuite. Elle
> ne remonte **jamais** au shell parent.

Autrement dit, `os.environ["FOO"] = "bar"` ne suffit pas à exporter
`FOO` dans le terminal qui a démarré le script. C'est une limite
fondamentale d'Unix : un processus enfant ne peut pas modifier
l'environnement de son parent.

Pour propager une variable à un sous-processus, c'est en revanche
direct :

```python
import os, subprocess

os.environ["MON_REGLAGE"] = "42"
# Le sous-processus voit bien MON_REGLAGE=42 dans son environnement.
subprocess.run(["printenv", "MON_REGLAGE"])
```

## 1.4 Les fichiers `.env`

Dans beaucoup de projets, on regroupe les variables d'environnement
dans un fichier texte appelé `.env`, au format simple :

```
DATABASE_URL=postgres://localhost/app
DEBUG=1
```

**Attention** : ce format n'est **pas natif** en Python. La
bibliothèque standard ne lit pas `.env` automatiquement. L'outil le
plus connu pour le faire est `python-dotenv`, qui est **externe** —
donc hors du périmètre de ce cours. On peut néanmoins parser un `.env`
soi-même en deux ou trois lignes (lecture du fichier, `split("=", 1)`,
remplissage de `os.environ`).

## À retenir

- `os.environ` se comporte comme un dictionnaire de chaînes.
- `os.environ["X"]` lève `KeyError` si `X` n'existe pas ;
  `os.environ.get("X", défaut)` est plus sûr.
- `os.environ.setdefault("X", "val")` initialise `X` si elle est absente.
- L'écriture ne remonte **pas** au shell parent, seulement aux
  sous-processus.
- Convention : noms en MAJUSCULES.
- Les fichiers `.env` ne sont pas natifs — `python-dotenv` (externe) ou
  parsing manuel.

## Démo

Exécuter `01_demo_environ.py`.
