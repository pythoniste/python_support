"""Scaffolde une nouvelle étape de fil rouge.

Crée le dossier ``<NN>_<slug>`` dans le ``Fil_rouge/`` d'une formation avec :

- un ``ENONCE.md`` prérempli (modèle de la section 7.11 de EVALUATION_ET_PLAN.md)
- un ``starter/`` vide avec arborescence ``src/<projet>/`` et ``tests/``
- une ``solution/`` copiée depuis l'étape précédente (ou vide pour l'étape 01)

Usage
-----
::

    python tools/init_fil_rouge.py Initiation_5j 03 catalogue_en_memoire
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FORMATIONS_DIR = REPO_ROOT / "Formations"

ENONCE_TEMPLATE = """\
# Étape {num} — {titre}

## Contexte
*(À compléter : d'où part-on, où veut-on arriver, pourquoi cette étape.)*

## Consignes
1. *(À compléter : tâche 1)*
2. *(À compléter : tâche 2)*

## Attendus
- *(À compléter : critère observable 1)*
- *(À compléter : critère observable 2)*

## Critères d'acceptation
- [ ] `pytest tests/test_etape{num}.py` est vert.
- [ ] `ruff check src/` ne remonte aucune erreur.
- [ ] *(À compléter : autre critère)*

## Temps estimé
*(À compléter)*

## Solution
Voir `solution/` pour une proposition complète.
**À consulter après tentative personnelle** (au moins 45 minutes de recherche).

## Pièges fréquents
- *(À compléter)*
"""

PYPROJECT_TEMPLATE = """\
[project]
name = "{projet}"
version = "0.{num}.0"
requires-python = ">=3.14"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{projet}"]
"""


def previous_step(fil_rouge_dir: Path, num: int) -> Path | None:
    if num <= 1:
        return None
    prefix = f"{num - 1:02d}_"
    for child in sorted(fil_rouge_dir.iterdir()):
        if child.is_dir() and child.name.startswith(prefix):
            return child
    return None


def guess_projet(fil_rouge_dir: Path) -> str:
    readme = fil_rouge_dir / "README.md"
    if readme.exists():
        for line in readme.read_text(encoding="utf-8").splitlines():
            if line.lower().startswith("# "):
                return line[2:].strip().split()[0].lower()
    return "projet"


def create_etape(format_name: str, num: int, slug: str) -> None:
    fil_rouge_dir = FORMATIONS_DIR / format_name / "Fil_rouge"
    if not fil_rouge_dir.exists():
        raise FileNotFoundError(f"Fil_rouge introuvable : {fil_rouge_dir}")

    etape_dir = fil_rouge_dir / f"{num:02d}_{slug}"
    if etape_dir.exists():
        raise FileExistsError(f"L'étape existe déjà : {etape_dir}")

    projet = guess_projet(fil_rouge_dir)
    titre = slug.replace("_", " ").capitalize()

    (etape_dir / "starter" / "src" / projet).mkdir(parents=True)
    (etape_dir / "starter" / "tests").mkdir(parents=True)

    (etape_dir / "starter" / "src" / projet / "__init__.py").write_text("", encoding="utf-8")
    (etape_dir / "starter" / "pyproject.toml").write_text(
        PYPROJECT_TEMPLATE.format(projet=projet, num=num), encoding="utf-8"
    )
    (etape_dir / "starter" / "tests" / f"test_etape{num:02d}.py").write_text(
        f'"""Tests de l\'étape {num:02d} du fil rouge."""\n', encoding="utf-8"
    )

    prev = previous_step(fil_rouge_dir, num)
    if prev is not None and (prev / "solution").exists():
        shutil.copytree(prev / "solution", etape_dir / "solution")
    else:
        (etape_dir / "solution" / "src" / projet).mkdir(parents=True)
        (etape_dir / "solution" / "tests").mkdir(parents=True)
        (etape_dir / "solution" / "src" / projet / "__init__.py").write_text("", encoding="utf-8")
        (etape_dir / "solution" / "pyproject.toml").write_text(
            PYPROJECT_TEMPLATE.format(projet=projet, num=num), encoding="utf-8"
        )

    (etape_dir / "ENONCE.md").write_text(
        ENONCE_TEMPLATE.format(num=f"{num:02d}", titre=titre), encoding="utf-8"
    )

    print(f"✅ Étape créée : {etape_dir.relative_to(REPO_ROOT)}")


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(f"Usage: {argv[0]} <format> <num> <slug>", file=sys.stderr)
        print("Exemple: python tools/init_fil_rouge.py Initiation_5j 03 catalogue", file=sys.stderr)
        return 2
    create_etape(argv[1], int(argv[2]), argv[3])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
