"""Strip "3 jours" tagged cells from a notebook.

Applies nbconvert's TagRemovePreprocessor to remove cells tagged with
``skip-3j``, ``exo-difficile``, ``deep-dive`` or ``bonus``.

Usage
-----
As a library::

    from build_3j import strip_3j
    strip_3j("path/to/source.ipynb", "path/to/target.ipynb")

As a CLI::

    python tools/build_3j.py <source.ipynb> <target.ipynb>
"""

from __future__ import annotations

import sys
from pathlib import Path

import nbformat
from nbconvert.preprocessors import TagRemovePreprocessor
from traitlets.config import Config

TAGS_TO_REMOVE: set[str] = {
    "skip-3j", "exo-difficile", "deep-dive", "bonus"
}


def strip_3j(source: Path | str, target: Path | str) -> None:
    """Read ``source`` notebook, remove 3j-excluded cells, write ``target``."""
    source = Path(source)
    target = Path(target)

    nb = nbformat.read(source, as_version=4)

    config = Config()
    config.TagRemovePreprocessor.remove_cell_tags = TAGS_TO_REMOVE
    config.TagRemovePreprocessor.enabled = True

    preprocessor = TagRemovePreprocessor(config=config)
    nb, _ = preprocessor.preprocess(nb, {})

    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, target)


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <source.ipynb> <target.ipynb>", file=sys.stderr)
        return 2
    strip_3j(argv[1], argv[2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
