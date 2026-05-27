#!/usr/bin/env python3
"""Demo : renommer, supprimer, créer un dossier, ajuster les droits.

À exécuter :  python3 03_demo_renommer.py

Travaille dans un dossier temporaire isolé. Aucun fichier de
l'utilisateur n'est touché.

Observer :
- Path.rename pour renommer ;
- Path.unlink (et missing_ok=True) pour supprimer ;
- Path.mkdir(parents=True, exist_ok=True) pour créer en idempotent ;
- Path.chmod(0o755) avec lecture des droits via st_mode.
"""
import stat
import tempfile
from pathlib import Path


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)

    # 1) Créer un dossier en idempotent : parents + exist_ok.
    cible = base / "a" / "b" / "c"
    cible.mkdir(parents=True, exist_ok=True)
    cible.mkdir(parents=True, exist_ok=True)   # rejouable sans erreur
    print("mkdir   :", cible.relative_to(base), "créé deux fois sans erreur")

    # 2) Créer un fichier puis le renommer.
    f = base / "ancien.txt"
    f.write_text("hello")
    nouveau = f.rename(base / "nouveau.txt")
    print("rename  :", nouveau.name, "(ancien.txt n'existe plus)")
    print("         contenu :", nouveau.read_text())

    # 3) Supprimer un fichier (unlink). missing_ok pour l'idempotence.
    nouveau.unlink()
    print("unlink  : fichier supprimé, existe ?", nouveau.exists())
    nouveau.unlink(missing_ok=True)   # ne lève pas
    print("unlink  : rejoué avec missing_ok=True, OK")

    # 4) Ajuster les droits Unix. On crée un script et on le rend
    # exécutable par tous (0o755 = rwxr-xr-x).
    script = base / "script.sh"
    script.write_text("#!/bin/sh\necho coucou\n")

    avant = stat.filemode(script.stat().st_mode)
    script.chmod(0o755)
    apres = stat.filemode(script.stat().st_mode)
    print(f"chmod   : avant {avant}  ->  après {apres}")

print("\nDossier temporaire supprimé proprement.")
