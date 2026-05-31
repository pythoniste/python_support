"""Exécute chaque notebook de Bibliotheque_notebooks et vérifie sa qualité.

Pour chaque ``*.ipynb`` trouvé :

1. Exécute le notebook en place via ``jupyter nbconvert --execute``.
2. Extrait le code Python (toutes les cellules code) dans un fichier temporaire.
3. Lance ``ruff check`` puis ``mypy --ignore-missing-imports`` sur ce code.

Retourne un code de sortie non nul si au moins un notebook a échoué.

Usage
-----
::

    python tools/check_notebooks.py                 # toute la bibliothèque
    python tools/check_notebooks.py Initiation      # un sous-arbre
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import nbformat

REPO_ROOT = Path(__file__).resolve().parent.parent
BIBLIO_ROOT = REPO_ROOT / "Bibliotheque_notebooks"


def extract_code(nb_path: Path) -> str:
    nb = nbformat.read(nb_path, as_version=4)
    return "\n\n".join(
        cell.source for cell in nb.cells if cell.cell_type == "code" and cell.source.strip()
    )


def run(cmd: list[str]) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output


def check_notebook(nb_path: Path) -> list[str]:
    errors: list[str] = []

    code, out = run(
        [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            str(nb_path),
        ]
    )
    if code != 0:
        errors.append(f"execute: {out}")
        return errors

    py_code = extract_code(nb_path)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tmp:
        tmp.write(py_code)
        tmp_path = Path(tmp.name)

    try:
        code, out = run(["ruff", "check", str(tmp_path)])
        if code != 0:
            errors.append(f"ruff: {out}")

        code, out = run(["mypy", "--ignore-missing-imports", str(tmp_path)])
        if code != 0:
            errors.append(f"mypy: {out}")
    finally:
        tmp_path.unlink(missing_ok=True)

    return errors


def iter_notebooks(subpath: Path) -> list[Path]:
    return sorted(p for p in subpath.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts)


def main(argv: list[str]) -> int:
    target = BIBLIO_ROOT
    if len(argv) > 1:
        target = BIBLIO_ROOT / argv[1]

    if not target.exists():
        print(f"Cible introuvable : {target}", file=sys.stderr)
        return 2

    notebooks = iter_notebooks(target)
    if not notebooks:
        print(f"Aucun notebook sous {target}")
        return 0

    failures: dict[Path, list[str]] = {}
    for nb in notebooks:
        print(f"→ {nb.relative_to(REPO_ROOT)}")
        errs = check_notebook(nb)
        if errs:
            failures[nb] = errs

    if failures:
        print(f"\n❌ {len(failures)} notebook(s) en échec :")
        for nb, errs in failures.items():
            print(f"  - {nb.relative_to(REPO_ROOT)}")
            for err in errs:
                print(f"      {err.splitlines()[0]}")
        return 1

    print(f"\n✅ {len(notebooks)} notebook(s) OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
