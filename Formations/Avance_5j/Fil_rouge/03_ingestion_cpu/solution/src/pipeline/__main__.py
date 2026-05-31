"""Point d'entree CLI du pipeline."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from pipeline.reader import read_all_csv
from pipeline.writer import write_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Point d'entree principal."""
    parser = argparse.ArgumentParser(description="Pipeline de donnees capteurs")
    parser.add_argument("--inbox", type=Path, required=True, help="Dossier des CSV entrants")
    parser.add_argument("--outbox", type=Path, required=True, help="Dossier de sortie JSON")
    parser.add_argument("--workers", type=int, default=4, help="Nombre de processus")
    args = parser.parse_args()

    logger.info("Lecture des CSV depuis %s", args.inbox)
    readings = read_all_csv(args.inbox, max_workers=args.workers)
    logger.info("%d lectures chargees", len(readings))

    output_path = args.outbox / "output.json"
    write_json(readings, output_path)
    logger.info("Resultats ecrits dans %s", output_path)


if __name__ == "__main__":
    main()
