"""Build a formation package from a YAML manifest.

Reads ``tools/manifests/<format>.yaml``, then copies (or strips for 3j
formats) every notebook listed in the manifest into
``Formations/<format>/<day>/``.

The ``Fil_rouge/`` folder is left untouched because it is edited by hand.

Usage
-----
::

    python tools/build_formation.py initiation_5j
    python tools/build_formation.py initiation_3j
    python tools/build_formation.py --all
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

from build_3j import strip_3j
from instrument_notebook import instrument

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = REPO_ROOT / "tools" / "manifests"
FORMATIONS_DIR = REPO_ROOT / "Formations"
COMMON_SOURCE = REPO_ROOT / "Bibliotheque_notebooks" / "_common" / "utils_pedagogie.py"
SETUP_NOTEBOOK_SOURCE = REPO_ROOT / "00_Configuration.ipynb"


def load_manifest(name: str) -> dict:
    path = MANIFESTS_DIR / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Manifest introuvable : {path}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _install_student_helpers(target_root: Path) -> None:
    """Copy utils_pedagogie.py and 00_Configuration.ipynb into a built formation.

    Students opening any notebook of the formation auto-discover the helper
    via the `_common/` folder at the formation root (or one level up from a
    day folder).
    """
    if SETUP_NOTEBOOK_SOURCE.exists():
        shutil.copy2(SETUP_NOTEBOOK_SOURCE, target_root / SETUP_NOTEBOOK_SOURCE.name)
        print(f"  setup {SETUP_NOTEBOOK_SOURCE.name}")
    else:
        print(f"  ⚠  manquant : {SETUP_NOTEBOOK_SOURCE}")

    if COMMON_SOURCE.exists():
        common_dir = target_root / "_common"
        common_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(COMMON_SOURCE, common_dir / COMMON_SOURCE.name)
        print(f"  helper _common/{COMMON_SOURCE.name}")
    else:
        print(f"  ⚠  manquant : {COMMON_SOURCE}")


def build(manifest_name: str) -> None:
    manifest = load_manifest(manifest_name)
    format_name: str = manifest["format"]
    mode: str = manifest["mode"]
    source_root = REPO_ROOT / manifest["source_root"]
    target_root = FORMATIONS_DIR / format_name

    if mode not in {"5j", "3j"}:
        raise ValueError(f"mode invalide : {mode!r} (attendu '5j' ou '3j')")

    print(f"[build_formation] {format_name} (mode={mode})")
    target_root.mkdir(parents=True, exist_ok=True)
    _install_student_helpers(target_root)

    for day in manifest["days"]:
        day_id: str = day["id"]
        day_title: str = day["title"]
        day_slug = f"{day_id}_{day_title.lower().replace(' ', '_').replace('&', 'et')}"
        target_day = target_root / day_slug

        if target_day.exists():
            shutil.rmtree(target_day)
        target_day.mkdir(parents=True, exist_ok=True)

        for nb_rel in day["notebooks"]:
            source_nb = source_root / nb_rel
            target_nb = target_day / Path(nb_rel).name

            if not source_nb.exists():
                print(f"  ⚠  manquant : {source_nb}")
                continue

            if mode == "5j":
                shutil.copy2(source_nb, target_nb)
                action = "copy "
            else:
                strip_3j(source_nb, target_nb)
                action = "strip"

            inserted = instrument(target_nb)
            suffix = f" (+{inserted} cellule{'s' if inserted > 1 else ''} marquer_tentative)" if inserted else ""
            print(f"  {action} {nb_rel}{suffix}")


def list_manifests() -> list[str]:
    return sorted(p.stem for p in MANIFESTS_DIR.glob("*.yaml"))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", help="Nom du manifeste (sans .yaml)")
    parser.add_argument("--all", action="store_true", help="Construire tous les formats")
    args = parser.parse_args(argv[1:])

    if args.all:
        for name in list_manifests():
            build(name)
        return 0

    if not args.manifest:
        parser.print_help()
        print("\nManifestes disponibles :", ", ".join(list_manifests()))
        return 2

    build(args.manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
