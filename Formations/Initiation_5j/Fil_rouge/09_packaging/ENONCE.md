# Étape 09 — Packaging

## Contexte

Votre grand-père ne lancera pas `python -m bibliotheque` — il veut taper juste `bibliotheque` dans son terminal. Il faut donc **empaqueter** le projet comme un vrai package Python distribuable.

## Consignes

1. Reprendre le code de l'étape 08.
2. Créer (ou compléter) le `pyproject.toml` à la racine avec tout ce qui est nécessaire à un package moderne :
   - Section `[project]` : `name`, `version`, `description`, `requires-python = ">=3.14"`, `authors`, `readme = "README.md"`, `license`.
   - Section `[project.scripts]` : un entry point `bibliotheque = "bibliotheque.__main__:main"`.
   - Section `[build-system]` : `requires = ["hatchling"]`, `build-backend = "hatchling.build"`.
   - Section `[tool.hatch.build.targets.wheel]` : `packages = ["src/bibliotheque"]`.
3. Transformer `__main__.py` pour qu'il **expose une fonction `main()`** (au lieu d'avoir le code à plat), appelée par `if __name__ == "__main__": main()`.
4. Remplacer les appels utilisateur par `argparse` pour gérer des arguments optionnels :
   - `--charger FICHIER` : charge un catalogue au démarrage.
   - `--format csv|json` : format par défaut pour les sauvegardes.
5. Installer le package en **mode éditable** avec `uv` :
   ```bash
   uv pip install -e .
   ```
6. Vérifier que la commande `bibliotheque` fonctionne depuis n'importe où :
   ```bash
   cd /tmp
   bibliotheque --help
   bibliotheque --charger ~/livres.json
   ```

## Attendus

```bash
$ bibliotheque --help
usage: bibliotheque [-h] [--charger FICHIER] [--format {csv,json}]

Gestionnaire de bibliothèque personnelle.

options:
  -h, --help          show this help message and exit
  --charger FICHIER   Charge un catalogue au démarrage
  --format {csv,json} Format par défaut pour les sauvegardes (défaut: json)
```

## Critères d'acceptation

- [ ] `pyproject.toml` est valide (`uv pip install -e .` réussit).
- [ ] La commande `bibliotheque` est installée et accessible dans le `PATH`.
- [ ] `bibliotheque --help` affiche l'aide argparse.
- [ ] `bibliotheque --charger <fichier>` charge le catalogue au démarrage.
- [ ] `__main__.py` contient bien une fonction `main()`.
- [ ] `pytest tests/test_etape09.py` est vert (vérifie l'import de `bibliotheque.__main__.main`).

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Entry point mal écrit** : `bibliotheque = "bibliotheque.__main__:main"` — deux-points entre le module et la fonction, pas un point.
- **Fonction `main()` manquante** : si `__main__.py` a du code à plat, l'entry point ne trouvera rien à appeler.
- **Oublier le `src/` layout dans `[tool.hatch.build.targets.wheel]`** → le wheel est vide.
- **`argparse` trop compliqué** : on ne veut que 2-3 options optionnelles. `add_argument("--charger", type=Path, default=None)` suffit.
- **Installer sans `-e`** : chaque modification de code demanderait une réinstallation. `-e` crée un lien symbolique — idéal en dev.
