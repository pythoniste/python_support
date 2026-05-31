"""Inject a `marquer_tentative` cell after each "# Votre code ici" placeholder.

A notebook is considered instrumentable when it contains markdown cells
matching ``### Exercice N`` followed by a code cell whose content is the
placeholder ``# Votre code ici`` (with optional surrounding whitespace).

After instrumentation, the placeholder cell is followed by a new code cell
calling ``marquer_tentative(notebook=<stem>, exercice=N)`` — students execute
it once they have written their answer to signal an attempt to the trainer.

The transformation is idempotent: a notebook already instrumented is detected
(by the presence of a ``marquer_tentative`` call) and left untouched.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

EXERCICE_RE = re.compile(r"^\s*###\s+Exercice\s+(\d+)\b", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"^\s*#\s*Votre\s+code\s+ici\s*$", re.IGNORECASE)
INSTRUMENTED_MARKER = "marquer_tentative"


def _cell_source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def _is_placeholder_cell(cell: dict) -> bool:
    if cell.get("cell_type") != "code":
        return False
    return bool(PLACEHOLDER_RE.match(_cell_source(cell)))


def _is_instrumented_cell(cell: dict) -> bool:
    return cell.get("cell_type") == "code" and INSTRUMENTED_MARKER in _cell_source(cell)


def _build_instrumentation_cell(notebook_stem: str, exercice: int) -> dict:
    source = (
        "# ▶ Une fois votre solution écrite ci-dessus, exécutez cette cellule\n"
        "# pour signaler à votre formateur que vous avez tenté l'exercice.\n"
        "import sys\n"
        "from pathlib import Path\n"
        "for _p in (Path.cwd(), *Path.cwd().parents):\n"
        '    if (_p / "_common" / "utils_pedagogie.py").exists():\n'
        '        sys.path.insert(0, str(_p / "_common")); break\n'
        "from utils_pedagogie import marquer_tentative\n"
        f'marquer_tentative(notebook="{notebook_stem}", exercice={exercice})\n'
    )
    return {
        "cell_type": "code",
        "metadata": {"tags": ["instrumentation-auto"]},
        "execution_count": None,
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def instrument(notebook_path: Path) -> int:
    """Instrument the notebook in place. Returns the number of cells inserted."""
    raw = notebook_path.read_text(encoding="utf-8")
    nb = json.loads(raw)
    cells = nb.get("cells", [])
    stem = notebook_path.stem

    new_cells: list[dict] = []
    inserted = 0
    current_exercice: int | None = None

    for idx, cell in enumerate(cells):
        new_cells.append(cell)

        if cell.get("cell_type") == "markdown":
            m = EXERCICE_RE.search(_cell_source(cell))
            if m:
                current_exercice = int(m.group(1))
            continue

        if current_exercice is None or not _is_placeholder_cell(cell):
            continue

        next_cell = cells[idx + 1] if idx + 1 < len(cells) else None
        if next_cell and _is_instrumented_cell(next_cell):
            current_exercice = None
            continue

        new_cells.append(_build_instrumentation_cell(stem, current_exercice))
        inserted += 1
        current_exercice = None

    if inserted == 0:
        return 0

    nb["cells"] = new_cells
    notebook_path.write_text(
        json.dumps(nb, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return inserted


def instrument_dir(root: Path) -> tuple[int, int]:
    """Instrument every .ipynb under ``root``. Returns (files_touched, cells_inserted)."""
    files_touched = 0
    total_inserted = 0
    for nb_path in sorted(root.rglob("*.ipynb")):
        if nb_path.name.startswith("00_Configuration"):
            continue
        if "/.ipynb_checkpoints/" in str(nb_path):
            continue
        inserted = instrument(nb_path)
        if inserted:
            files_touched += 1
            total_inserted += inserted
    return files_touched, total_inserted


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python tools/instrument_notebook.py <path>")
        sys.exit(2)

    target = Path(sys.argv[1])
    if target.is_dir():
        files, cells = instrument_dir(target)
        print(f"Instrumented {cells} cell(s) across {files} notebook(s) under {target}")
    else:
        inserted = instrument(target)
        print(f"Instrumented {inserted} cell(s) in {target}")
