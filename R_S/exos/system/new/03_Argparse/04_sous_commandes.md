# 04 — Sous-commandes

## 4.1 Pourquoi des sous-commandes ?

Les outils sérieux exposent souvent **plusieurs actions** sous une
même commande racine. Quelques exemples connus :

```
git clone ...
git commit ...
git push ...
```

```
docker build ...
docker run ...
docker ps ...
```

Chaque sous-commande (`clone`, `commit`, `build`, `run`...) a ses
**propres** arguments. Plutôt que de tout mélanger dans un seul
parser, `argparse` permet de construire un parser par sous-commande
et de les coller à un parser racine.

## 4.2 `add_subparsers()` : créer le point de branchement

On part d'un parser principal, puis on lui demande un objet capable
d'accueillir les sous-parsers :

```python
parser = argparse.ArgumentParser(prog="todo")
sous_parsers = parser.add_subparsers(
    dest="commande",     # où stocker le nom choisi
    required=True,       # interdit d'oublier la sous-commande
)
```

| Paramètre   | Effet                                                 |
|-------------|-------------------------------------------------------|
| `dest`      | Nom de l'attribut où sera rangé le nom invoqué.       |
| `required`  | Force l'utilisateur à choisir une sous-commande.      |

Sans `required=True`, l'utilisateur peut taper `python3 outil.py`
tout seul, et `args.commande` vaut `None` — à gérer à la main.

## 4.3 Un parser par sous-commande

Sur l'objet `sous_parsers`, chaque appel `.add_parser(nom)` renvoie
**un nouveau parser** auquel on ajoute ses propres arguments :

```python
# Sous-commande "ajouter"
p_ajouter = sous_parsers.add_parser("ajouter", help="ajouter une tâche")
p_ajouter.add_argument("texte", help="description de la tâche")
p_ajouter.add_argument("--priorite", type=int, default=1)

# Sous-commande "lister"
p_lister = sous_parsers.add_parser("lister", help="afficher les tâches")
p_lister.add_argument("--toutes", action="store_true")

# Sous-commande "finir"
p_finir = sous_parsers.add_parser("finir", help="cocher une tâche")
p_finir.add_argument("id", type=int)
```

Chaque sous-parser hérite du fonctionnement standard :

- ses arguments positionnels et optionnels lui appartiennent ;
- il a sa propre page `--help`.

```
$ python3 outil.py ajouter --help
$ python3 outil.py lister --help
```

## 4.4 `set_defaults(func=...)` : dispatcher proprement

À l'usage, on ne veut pas écrire un gros `if args.commande == "...":`
en bas du script. La technique propre consiste à **attacher une
fonction par défaut** à chaque sous-parser :

```python
def cmd_ajouter(args):
    print(f"Ajout : {args.texte} (priorité {args.priorite})")

def cmd_lister(args):
    print("Affichage des tâches (toutes :", args.toutes, ")")

def cmd_finir(args):
    print(f"Tâche {args.id} marquée comme terminée")

p_ajouter.set_defaults(func=cmd_ajouter)
p_lister.set_defaults(func=cmd_lister)
p_finir.set_defaults(func=cmd_finir)
```

`set_defaults(func=...)` ajoute un attribut `func` au `Namespace`
lorsque la sous-commande correspondante est invoquée. Le main devient
alors trivial :

```python
args = parser.parse_args()
args.func(args)        # dispatch
```

C'est **le** patron à retenir pour toute CLI à sous-commandes.

## 4.5 Squelette complet

Pour fixer les idées, voici la structure type d'un script à
sous-commandes :

```python
import argparse


def cmd_ajouter(args):
    ...

def cmd_lister(args):
    ...


def construire_parser():
    parser = argparse.ArgumentParser(prog="todo")
    subs = parser.add_subparsers(dest="commande", required=True)

    p1 = subs.add_parser("ajouter")
    p1.add_argument("texte")
    p1.set_defaults(func=cmd_ajouter)

    p2 = subs.add_parser("lister")
    p2.set_defaults(func=cmd_lister)

    return parser


def main():
    parser = construire_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

Avantages :

- chaque sous-commande est isolée dans sa propre fonction ;
- ajouter une commande revient à écrire trois lignes
  (`subs.add_parser` + `add_argument` + `set_defaults`) ;
- le main ne change jamais.

## À retenir

- `add_subparsers(dest=..., required=True)` crée un point de
  branchement.
- Chaque sous-commande a son **propre** parser et ses propres
  arguments.
- `set_defaults(func=...)` attache une fonction à un sous-parser ;
  `args.func(args)` dispatche en une ligne.
- Chaque sous-parser dispose automatiquement de son `--help`.

## Démo

Exécuter `04_demo_sous_commandes.py` avec différentes sous-commandes,
puis avec `--help` sur la racine et sur chaque sous-commande.
