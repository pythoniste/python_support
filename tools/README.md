# tools/

Scripts de construction et de vérification pour `python_support`.

## Scripts

| Script | Rôle |
|---|---|
| `build_formation.py` | Construit un package `Formations/<format>/` depuis un manifeste YAML. Mode `5j` = copie directe, mode `3j` = filtrage de tags via `build_3j.py`. |
| `build_3j.py` | Applique `TagRemovePreprocessor` pour retirer les cellules `skip-3j`, `exo-difficile`, `deep-dive`, `bonus`. Utilisable seul ou comme librairie. |
| `check_notebooks.py` | Exécute chaque notebook de `Bibliotheque_notebooks/`, puis lance `ruff` et `mypy` sur le code extrait. Utilisé en CI. |
| `init_fil_rouge.py` | Scaffolde une nouvelle étape de fil rouge avec `ENONCE.md`, `starter/` et `solution/` héritée de l'étape précédente. |

## Manifestes

Un manifeste par format dans `tools/manifests/` :

- `initiation_5j.yaml`, `initiation_3j.yaml`
- `intermediaire_5j.yaml`, `intermediaire_3j.yaml`
- `avance_5j.yaml`

Chaque manifeste indique son `format`, son `mode` (`5j` ou `3j`), sa `source_root`, et la liste ordonnée des notebooks par jour.

## Dépendances

```bash
uv pip install nbconvert nbformat pyyaml ruff mypy jupyter
```

## Usage typique

```bash
# Construire un format
python tools/build_formation.py initiation_5j

# Construire tous les formats
python tools/build_formation.py --all

# Vérifier la bibliothèque entière
python tools/check_notebooks.py

# Créer une nouvelle étape de fil rouge
python tools/init_fil_rouge.py Initiation_5j 03 catalogue_en_memoire
```
