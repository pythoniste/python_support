# Étape 10 — Qualité et livrable

## Contexte

Le programme fonctionne, il est installable, il a une CLI. C'est le dernier sprint : on ajoute des **logs** (pour déboguer en production), des **tests automatiques** (pour détecter les régressions), un **README** (pour la passation) et on construit un **wheel** distribuable que votre grand-père pourra installer sur son PC.

## Consignes

### 1. Logging

1. Remplacer les `print` « de debug » (ceux qui servent à suivre l'exécution, pas à parler à l'utilisateur) par du `logging`.
2. Configurer le logger dans `__main__.py` :
   ```python
   logging.basicConfig(
       level=logging.INFO,
       format="%(asctime)s [%(levelname)s] %(message)s",
   )
   ```
3. Logger chaque ajout de livre en `INFO` et chaque erreur en `WARNING`.
4. Les messages destinés à l'utilisateur (menu, saisie) restent en `print` — ils ne sont pas des logs.

### 2. Tests pytest

Écrire au minimum **5 tests** dans `tests/test_bibliotheque.py` :

1. `test_creer_livre_valide` : création d'un livre correct.
2. `test_creer_livre_invalide_leve_exception` : année à 3000 lève `LivreInvalide`.
3. `test_ajouter_livre_duplicate` : deux livres avec le même ISBN lèvent `LivreExistant`.
4. `test_rechercher_case_insensitive` : `rechercher("ORWELL")` trouve `"George Orwell"`.
5. `test_sauvegarder_charger_round_trip` : sauvegarde puis rechargement donne le même catalogue (utiliser `tmp_path`).

Pour `tmp_path`, c'est une **fixture pytest** qui fournit un dossier temporaire unique par test.

### 3. README.md

Écrire un `README.md` à la racine qui contient :

- Nom et description du projet.
- Installation (`uv pip install -e .` ou, plus tard, `pipx install bibliotheque`).
- Utilisation (exemples de commandes).
- Format des fichiers CSV et JSON attendus.
- Auteur et licence.

### 4. Build et vérification finale

```bash
uv build                    # produit dist/bibliotheque-0.1.0-py3-none-any.whl
uv pip install dist/bibliotheque-*.whl  # installe le wheel
bibliotheque --help         # doit fonctionner
pytest                      # tous les tests passent
ruff check src/ tests/      # pas d'erreur
```

## Attendus

Au terme de cette étape, votre grand-père reçoit :

- Un **fichier `bibliotheque-0.1.0-py3-none-any.whl`** qu'il peut installer d'une seule commande.
- Une commande `bibliotheque` qu'il tape dans son terminal.
- Un README qui explique tout.

## Critères d'acceptation

- [ ] Les `print` de debug sont remplacés par `logging`.
- [ ] `logging.basicConfig` est appelé une seule fois dans `main()`.
- [ ] `tests/test_bibliotheque.py` contient au moins 5 tests.
- [ ] `pytest` est vert avec `-v`.
- [ ] `README.md` existe et suit la structure demandée.
- [ ] `uv build` produit un wheel dans `dist/`.
- [ ] `uv pip install` le wheel dans un venv propre → la commande `bibliotheque` fonctionne.
- [ ] `ruff check` ne remonte aucune erreur.

## Temps estimé

2 heures.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`logging.basicConfig` appelé plusieurs fois** : il ne fait rien aux appels suivants. Le configurer une seule fois, au plus haut niveau.
- **Mélanger `print` et `logging`** pour les messages utilisateur : garder une règle claire. `print` = dialogue avec l'humain, `logging` = trace d'exécution.
- **Tests qui dépendent de l'ordre** : pytest ne garantit pas l'ordre. Chaque test doit être **indépendant**. Utiliser des fixtures pour le setup.
- **`tmp_path` partagé** : il est **unique par test**, pas partagé — c'est justement son intérêt.
- **Oublier de mettre à jour `version`** dans `pyproject.toml` avant `uv build` : le wheel garde l'ancien numéro. Bump avant chaque build.

## Bravo !

Vous avez un vrai package Python. C'est la base de tout ce que vous écrirez en Python dans votre carrière. Les étapes suivantes (que vous explorerez dans des formations avancées) sont : **Git**, **CI/CD**, **publication sur PyPI**, **documentation avec Sphinx/MkDocs**, **base de données** pour remplacer le CSV/JSON, **interface web** avec FastAPI…
