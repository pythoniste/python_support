#!/usr/bin/env python3
"""Demo : appel basique de subprocess.run.

À exécuter :  python3 01_demo_run.py

Observer :
- la commande est passée comme une LISTE (pas une chaîne) ;
- result.stdout, result.stderr, result.returncode ;
- shell=False est implicite (et c'est ce qu'on veut).
"""
import subprocess


def main():
    # 1) Un appel minimal : on lance "echo bonjour" et on capture sa sortie.
    result = subprocess.run(
        ["echo", "bonjour"],
        capture_output=True,
        text=True,
    )
    print("--- echo bonjour ---")
    print("stdout     :", repr(result.stdout))
    print("stderr     :", repr(result.stderr))
    print("returncode :", result.returncode)
    print()

    # 2) Une commande avec plusieurs arguments : "ls -la /tmp".
    #    Un argument = une case dans la liste.
    result = subprocess.run(
        ["ls", "-la", "/tmp"],
        capture_output=True,
        text=True,
    )
    print("--- ls -la /tmp (3 premières lignes) ---")
    for ligne in result.stdout.splitlines()[:3]:
        print(ligne)
    print("returncode :", result.returncode)
    print()

    # 3) Passer du texte sur stdin via input="..." :
    #    équivalent Python de `echo "un deux trois" | wc -w`.
    result = subprocess.run(
        ["wc", "-w"],
        input="un deux trois quatre cinq\n",
        capture_output=True,
        text=True,
    )
    print("--- wc -w (5 mots attendus) ---")
    print("Nombre de mots :", result.stdout.strip())


if __name__ == "__main__":
    main()
