"""Helper to build Intermediate-level notebooks quickly — no external deps.

Usage in each generator script:

    import sys; sys.path.insert(0, "/home/sch/Documents/repositories/python_support/tools")
    from nbkit import NB, save
    nb = NB(title="...", objectifs=[...], ...)
    save(nb, "chemin/vers/notebook.ipynb")
"""
from __future__ import annotations

import json
import os
import uuid


def _new_id() -> str:
    return uuid.uuid4().hex[:8]


def _split_source(text: str) -> list[str]:
    """Split source into lines, preserving newlines except for last line."""
    if not text:
        return []
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + "\n")
        else:
            if line:
                result.append(line)
    return result


def _md(src: str, tags=None, collapsed=False) -> dict:
    meta: dict = {}
    if tags:
        meta["tags"] = list(tags)
    if collapsed:
        meta["jp-MarkdownHeadingCollapsed"] = True
    return {
        "cell_type": "markdown",
        "id": _new_id(),
        "metadata": meta,
        "source": _split_source(src),
    }


def _code(src: str, tags=None) -> dict:
    meta: dict = {}
    if tags:
        meta["tags"] = list(tags)
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": _new_id(),
        "metadata": meta,
        "outputs": [],
        "source": _split_source(src),
    }


class NB:
    def __init__(
        self,
        title: str,
        objectifs: list[str],
        prereqs_connus: list[str],
        prereqs_pas_encore: list[str],
        plan: list[str],
    ):
        self.cells: list = []
        puces = "\n".join(f"- {o}" for o in objectifs)
        self.cells.append(
            _md(
                f"# {title}\n\n## Objectifs pédagogiques\n\n"
                f"À la fin de ce notebook, vous saurez :\n\n{puces}"
            )
        )
        connus = "\n".join(f"- {p}" for p in prereqs_connus)
        futur = "\n".join(f"- {p}" for p in prereqs_pas_encore) if prereqs_pas_encore else "- *(rien à signaler à ce stade)*"
        self.cells.append(
            _md(
                "## Prérequis — ce que vous connaissez déjà\n\n"
                "À ce stade de la formation intermédiaire, vous maîtrisez :\n\n"
                f"{connus}\n\n"
                "Ce que nous n'avons **pas encore vu** (et que nous n'utiliserons donc pas "
                "dans ce notebook) :\n\n"
                f"{futur}"
            )
        )
        items = "\n".join(f"{i + 1}. {p}" for i, p in enumerate(plan))
        self.cells.append(_md(f"## Plan\n\n{items}"))

    def hr(self):
        self.cells.append(_md("---"))

    def section(self, heading: str, intro: str = "", tags=None):
        self.hr()
        body = f"## {heading}"
        if intro:
            body += f"\n\n{intro}"
        self.cells.append(_md(body, tags=tags))

    def sub(self, heading: str, intro: str = "", tags=None):
        body = f"### {heading}"
        if intro:
            body += f"\n\n{intro}"
        self.cells.append(_md(body, tags=tags))

    def md(self, text: str, tags=None):
        self.cells.append(_md(text, tags=tags))

    def code(self, src: str, tags=None):
        self.cells.append(_code(src, tags=tags))

    def pair(self, md_text: str, code_src: str, tags=None):
        self.md(md_text, tags=tags)
        self.code(code_src, tags=tags)

    def _exo(self, difficulty: str, n: int, titre: str, enonce: str, correction: str, starter: str = "# Votre code ici\n"):
        tag = f"exo-{difficulty}"
        libelle = {"facile": "facile", "moyen": "moyen", "difficile": "difficile"}[difficulty]
        self.cells.append(
            _md(
                f"### Exercice {n} — {titre} *({libelle})*\n\n{enonce}",
                tags=[tag],
            )
        )
        self.cells.append(_code(starter, tags=[tag]))
        corr = correction.rstrip("\n")
        self.cells.append(
            _md(
                f"<details>\n<summary>\U0001f4d6 Voir la correction</summary>\n\n```python\n{corr}\n```\n\n</details>",
                tags=[tag],
            )
        )

    def exo_facile(self, n, titre, enonce, correction, starter="# Votre code ici\n"):
        self._exo("facile", n, titre, enonce, correction, starter)

    def exo_moyen(self, n, titre, enonce, correction, starter="# Votre code ici\n"):
        self._exo("moyen", n, titre, enonce, correction, starter)

    def exo_difficile(self, n, titre, enonce, correction, starter="# Votre code ici\n"):
        self._exo("difficile", n, titre, enonce, correction, starter)

    def exos_intro(self, texte: str = "Les exercices sont gradués. Tous utilisent des fonctions typées (PEP 604)."):
        self.hr()
        self.cells.append(_md(f"## Exercices\n\n{texte}"))

    def synthese(self, table_md: str, regles: list[str]):
        self.hr()
        puces = "\n".join(f"{i + 1}. {r}" for i, r in enumerate(regles))
        self.cells.append(
            _md(f"## Synthèse\n\n{table_md}\n\n### Règles à retenir\n\n{puces}")
        )

    def ressources(self, doc: list[str], peps: list[str] | None = None, lectures: list[str] | None = None):
        self.hr()
        parts = ["## Ressources externes", "", "### Documentation officielle"]
        parts += [f"- {d}" for d in doc]
        if peps:
            parts += ["", "### PEPs de référence"]
            parts += [f"- {p}" for p in peps]
        if lectures:
            parts += ["", "### Lectures complémentaires"]
            parts += [f"- {l}" for l in lectures]
        self.cells.append(_md("\n".join(parts)))


def save(nb: NB, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    notebook = {
        "cells": nb.cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.14",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, ensure_ascii=False, indent=1)
    print(f"[ok] {path} — {len(nb.cells)} cells")
