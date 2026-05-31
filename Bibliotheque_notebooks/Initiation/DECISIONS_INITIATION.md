# Décisions fortes — Initiation

*Document vivant qui consigne les choix pédagogiques faits lors de la rédaction des notebooks d'Initiation. Relire avant toute modification qui touche à la progressivité.*

---

## 1. Progressivité stricte

La règle d'or : **aucun notebook n'utilise une notion introduite plus loin**. Aucune forward reference n'est tolérée, même dans un commentaire.

Conséquences pratiques :

- jusqu'à `03_Chaines.ipynb` inclus : **pas de f-strings**. On utilise `print("label :", var)` avec des virgules ;
- jusqu'à `04_Fonctions/01_Signatures.ipynb` exclu : **pas de `def`**. Les exercices sont des **scripts** ;
- à partir de `04_Fonctions/02_Type_hints_intro.ipynb` : **les type hints sont obligatoires** dans tous les exercices, et `mypy --strict` doit passer ;
- les dicts / sets / tuples ne sont pas utilisés dans les exercices de `01_Nombres`, `02_Booleens`, `03_Chaines` — on s'appuie sur `range` et les variadics `min`/`max`/`sum`.

## 2. Ordre des chapitres J3 : syntaxe → fonctions → retour syntaxe

Décision potentiellement surprenante : `02_Syntaxe/06_Exceptions.ipynb` et `02_Syntaxe/07_Debugging.ipynb` sont **placés après** `04_Fonctions/*`, pas après `02_Syntaxe/05_Boucles`.

Raison : les exceptions sont infiniment plus utiles dès qu'on écrit des fonctions typées — `raise ValueError(...)` dans une fonction qui vérifie un paramètre est l'usage le plus fréquent. Les présenter **après** `def` + type hints permet de donner tout de suite des exercices en fonction.

Le plan affiché à l'étudiant reste respecté : les deux notebooks exceptions/debugging vivent bien dans `02_Syntaxe/`, seule l'**ordre de présentation** les déplace en J3.

## 3. `zoneinfo`, pas `pytz`

Choix fait explicitement dans `03_Types_de_donnees/08_Donnees_temporelles.ipynb` : on utilise **`zoneinfo`** (stdlib depuis Python 3.9, PEP 615) et on **ne mentionne pas `pytz`**, sauf comme note historique `deep-dive`.

`pytz` reste très répandu dans les bases de code anciennes, mais :

- il n'est pas dans la stdlib ;
- son API (`localize`, `normalize`) est plus confuse que celle de `zoneinfo` ;
- Python recommande officiellement `zoneinfo` depuis 3.9.

Pour un cours d'**initiation** en 2026, on ne commence pas par `pytz`.

## 4. Les *type hints* sont introduits **immédiatement après** `def`

L'ordre est :

1. `04_Fonctions/01_Signatures_et_parametres.ipynb` — `def`, params, `*args`, `**kwargs`, mutable default.
2. `04_Fonctions/02_Type_hints_intro.ipynb` — annotations, `list[int]`, `dict[str, int]`, `int | None`, mention de `mypy --strict`.
3. `04_Fonctions/03_Portee_et_closures.ipynb` — LEGB, closures.

À partir du point 2, **tous** les exercices sont typés. Le premier notebook de fonctions reste non-typé par souci de progressivité (introduire deux concepts neufs d'un coup — `def` et les annotations — est coûteux).

## 5. Syntaxe moderne des annotations

Décisions :

- `list[int]` et non `List[int]` (PEP 585, Python 3.9+) ;
- `int | None` et non `Optional[int]` (PEP 604, Python 3.10+) ;
- `str | int` et non `Union[str, int]`.

Les versions historiques (`typing.List`, `typing.Optional`, `typing.Union`) sont brièvement mentionnées en `deep-dive` car elles existent dans du code ancien.

## 6. Un exemple par cellule de code

Règle appliquée systématiquement :

- une cellule de code ne contient **qu'un seul** concept à la fois ;
- exception : les cellules qui introduisent une structure composite (une fonction complète avec son appel) comptent comme une unité.

Conséquence : les notebooks d'initiation sont **longs** en nombre de cellules (80-120) mais **chaque cellule est courte** (1-5 lignes). C'est ce qui permet au stagiaire de ré-exécuter et modifier librement.

## 7. Corrections en `<details>`, pas en cellule taguée

Toutes les corrections d'exercices utilisent le bloc HTML natif :

```markdown
<details>
<summary>📖 Voir la correction</summary>

```python
...
```

</details>
```

**Jamais** de cellule code taguée `correction`. Raison : le bloc `<details>` rend pareil dans JupyterLab, VS Code, GitHub et nbviewer, et il n'est pas exécutable — ce qui force le stagiaire à **recopier** (donc lire).

## 8. Exercices gradués — convention

Chaque notebook comporte :

- 3 exercices **faciles** (`exo-facile`) ;
- 2 à 3 exercices **moyens** (`exo-moyen`) ;
- 1 à 2 exercices **difficiles** (`exo-difficile`).

En version 3 jours, les `exo-difficile` sont retirés, donc le tronc commun 3j reste un parcours cohérent.

## 9. Tags utilisés

| Tag | Sens |
|---|---|
| *(aucun)* | Tronc commun |
| `skip-3j` | Approfondissement 5 j uniquement |
| `exo-facile` / `exo-moyen` / `exo-difficile` | Exercices gradués |
| `deep-dive` | Section d'approfondissement |
| `bonus` | Contenu bonus si temps (peu utilisé en Initiation) |

Les tags `exo-difficile` et `deep-dive` sont **retirés en 3 jours** par `tools/build_3j.py`.

## 10. `uv` comme outil de référence

Tous les exemples de ligne de commande utilisent `uv` :

- `uv build` plutôt que `python -m build` ;
- `uv sync` / `uv add` plutôt que `pip install` ;
- `uv run ruff check .` plutôt que `ruff check .`.

Les alternatives classiques (`pip`, `build`, `twine`) sont mentionnées en note pour ceux qui ne peuvent pas installer `uv`.

## 11. `ruff` plutôt que black+flake8+isort+pyupgrade

`08_Bonnes_pratiques_et_packaging/02_Ruff.ipynb` présente Ruff comme **le** linter/formatter, remplaçant l'ensemble de la chaîne historique. Les outils remplacés sont listés pour contextualiser, mais on n'apprend pas à les utiliser individuellement.

Raison : en 2026, un projet neuf n'installe plus 5 outils séparés pour faire du linting. Ruff fait tout, plus vite.

## 12. Hatchling comme build backend par défaut

Le chapitre `03_Pyproject_toml.ipynb` montre Hatchling. Setuptools est mentionné comme « historique toujours valide », Poetry-core comme « si vous utilisez Poetry », mais l'exemple de référence est **Hatchling**.

Raison : Hatchling est piloté par la PSF (Python Packaging Authority), c'est le backend moderne recommandé pour un projet neuf, et il fonctionne parfaitement avec `uv`.

## 13. `argparse` plutôt que `click`/`typer` en Initiation

Choix : en initiation, on reste sur `argparse` (stdlib). `click` et `typer` sont mentionnés en synthèse comme « alternatives plus élégantes » mais ne sont pas enseignés.

Raison : un stagiaire qui démarre doit comprendre ce qui se passe sans magie. `argparse` est verbeux mais transparent. Les alternatives viendront au cours intermédiaire.

## 14. Encodage explicite obligatoire

Dans `07_Entrees_sorties/01_Fichiers_et_pathlib.ipynb` et tous les exercices qui ouvrent un fichier :

```python
open(chemin, 'r', encoding='utf-8')
Path(chemin).read_text(encoding='utf-8')
```

**Jamais** de `open(chemin)` sans `encoding`. Raison : PEP 597, et Python 3.15 va en faire une erreur.

## 15. `newline=''` obligatoire avec `csv`

Expliqué explicitement dans `07_Entrees_sorties/02_CSV.ipynb`. Tous les exercices l'utilisent systématiquement.

## 16. JSON : `ensure_ascii=False` et `indent=2` par défaut pour l'humain

Convention : pour du JSON destiné à un humain (README, fichier de config, dump pédagogique), on écrit systématiquement :

```python
json.dumps(data, ensure_ascii=False, indent=2)
```

Pour du JSON destiné à une API (machine-to-machine), format compact par défaut — cf. notes en `deep-dive`.

## 17. Mention de `pytest` minimale en Initiation

`08_Bonnes_pratiques_et_packaging/06_Pytest_intro.ipynb` couvre :

- un test simple avec `assert` ;
- `pytest.raises` ;
- la structure `tests/` ;
- une mention de paramétrage et des fixtures `tmp_path`, `capsys`.

**Pas** de :

- fixtures custom avec `@pytest.fixture` ;
- `conftest.py` ;
- tests paramétrés avancés ;
- hypothesis / property testing.

Ces sujets reviennent au cours intermédiaire.

## 18. Longueur cible : 80-120 cellules

Objectif qualité pour les 22 notebooks de ce lot. La convention historique disait 60-100, mais on vise un peu plus dense pour :

- laisser de la place aux mini-exemples en bloc ;
- multiplier les quiz / récap ;
- donner assez de pratique par notebook.

La version 3 j coupera mécaniquement ~30 % du volume via les tags.

## 19. Cheat sheets en fin de notebook

Les notebooks des outils (Ruff, pyproject, pytest, logging, argparse, build wheel) se terminent par une **cheat sheet** — un tableau ou un bloc de commandes prêtes à copier.

Raison pédagogique : ces notebooks sont souvent re-consultés **après** la formation, comme une référence. La cheat sheet est ce que le stagiaire reviendra chercher.

## 20. Ressources externes à la fin de chaque notebook

Tout notebook se termine par une section **Ressources externes** listant :

- la doc officielle Python (toujours) ;
- 1 à 3 PEP pertinents ;
- éventuellement 1 ressource tierce de référence.

Conventions :

- URLs stables (pas de blogs individuels) ;
- titres descriptifs en français ;
- ordre : doc officielle → PEPs → autres.

---

*Ce document est rédigé à la fin du lot des 22 notebooks restants. Il sera mis à jour quand d'autres décisions seront prises.*
