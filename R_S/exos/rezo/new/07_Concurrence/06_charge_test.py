"""Lance 3 clients lents en parallèle et mesure le temps total.

Sur un serveur ITÉRATIF   : ~4,5 s (3 × 1,5 s en série).
Sur un serveur CONCURRENT : ~1,5 s (3 clients simultanés).

C'est la mesure qui rend la concurrence visible.
"""
import subprocess
import time
from pathlib import Path


CLIENTS = ["Alice", "Bob", "Charlie"]
DOSSIER = Path(__file__).resolve().parent


def main() -> None:
    debut = time.perf_counter()
    procs = [
        subprocess.Popen(
            ["python3", str(DOSSIER / "05_clt_lent.py"), nom],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        for nom in CLIENTS
    ]
    for p in procs:
        p.wait()
    duree = time.perf_counter() - debut
    print(f">>> {len(CLIENTS)} clients lents en parallèle : {duree:.2f} s")
    print(f"    Sériel attendu : ~{len(CLIENTS) * 1.5:.1f} s")
    print(f"    Parallèle attendu : ~1,5 s")


if __name__ == "__main__":
    main()
