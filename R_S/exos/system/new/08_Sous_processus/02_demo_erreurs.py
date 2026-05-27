#!/usr/bin/env python3
"""Demo : les quatre cas d'erreur autour de subprocess.run.

À exécuter :  python3 02_demo_erreurs.py

On va déclencher volontairement les quatre situations courantes :
- succès classique (code 0) ;
- échec avec code != 0 sans check ;
- échec avec code != 0 et check=True (CalledProcessError) ;
- dépassement de timeout (TimeoutExpired) ;
- programme inexistant (FileNotFoundError).
"""
import subprocess


def main():
    # 1) Succès : ls / renvoie 0.
    result = subprocess.run(["ls", "/"], capture_output=True, text=True)
    print("[1] ls /            -> returncode =", result.returncode)

    # 2) Échec silencieux : sans check=True, pas d'exception.
    result = subprocess.run(
        ["ls", "/n_existe_pas"],
        capture_output=True, text=True,
    )
    print("[2] ls inexistant   -> returncode =", result.returncode,
          "(pas d'exception levée)")

    # 3) check=True : la même commande lève maintenant CalledProcessError.
    try:
        subprocess.run(["ls", "/n_existe_pas"], check=True,
                       capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        print("[3] check=True      -> CalledProcessError, code =", exc.returncode)

    # 4) timeout : sleep 5, mais on n'attend qu'une seconde.
    try:
        subprocess.run(["sleep", "5"], timeout=1.0)
    except subprocess.TimeoutExpired as exc:
        print("[4] sleep 5         -> TimeoutExpired après", exc.timeout, "s")

    # 5) Programme inexistant : avant même de tourner.
    try:
        subprocess.run(["binaire_qui_n_existe_vraiment_pas"])
    except FileNotFoundError as exc:
        print("[5] binaire absent  -> FileNotFoundError :", exc.filename)


if __name__ == "__main__":
    main()
