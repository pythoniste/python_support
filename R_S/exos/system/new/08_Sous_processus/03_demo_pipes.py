#!/usr/bin/env python3
"""Demo : input= pour stdin simple, puis Popen pour chaîner deux commandes.

À exécuter :  python3 03_demo_pipes.py

On va reproduire deux fois la même opération `echo "un deux trois" | wc -w`,
d'abord avec run() seul (cas le plus simple, 95 % du temps suffisant),
puis avec deux Popen chaînés (le cas général, plus rare).
"""
import subprocess


def main():
    # === Version 1 : run() avec input=, sans pipe explicite. ===
    # On envoie le texte directement sur le stdin de wc.
    result = subprocess.run(
        ["wc", "-w"],
        input="un deux trois\n",
        capture_output=True,
        text=True,
    )
    print("[1] run() + input=  -> mots =", result.stdout.strip())

    # === Version 2 : deux Popen chaînés via un vrai pipe. ===
    # Équivalent strict de `echo "un deux trois" | wc -w` dans le shell.
    p1 = subprocess.Popen(
        ["echo", "un deux trois"],
        stdout=subprocess.PIPE,    # garder le stdout dans un tube
        text=True,
    )
    p2 = subprocess.Popen(
        ["wc", "-w"],
        stdin=p1.stdout,           # brancher le tube en entrée de p2
        stdout=subprocess.PIPE,
        text=True,
    )
    # Côté parent, on ferme notre copie du tube pour que p1 reçoive EOF.
    p1.stdout.close()
    sortie, _ = p2.communicate()
    print("[2] Popen + Popen   -> mots =", sortie.strip())

    # === Bonus : chaîner avec date | wc -c (compter les caractères). ===
    p1 = subprocess.Popen(["date"], stdout=subprocess.PIPE, text=True)
    p2 = subprocess.Popen(["wc", "-c"], stdin=p1.stdout,
                          stdout=subprocess.PIPE, text=True)
    p1.stdout.close()
    sortie, _ = p2.communicate()
    print("[3] date | wc -c    -> caractères =", sortie.strip())


if __name__ == "__main__":
    main()
