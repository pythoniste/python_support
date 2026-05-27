"""Lecture, valeur par défaut et écriture dans os.environ.

À exécuter :  python3 01_demo_environ.py

Observer :
- la lecture directe et la lecture avec valeur par défaut ;
- setdefault qui n'écrase rien si la variable existe déjà ;
- l'écriture, visible dans le processus courant mais pas dans le shell parent.
"""
import os


# 1) Lecture directe (lève KeyError si HOME n'est pas défini).
print("HOME :", os.environ["HOME"])

# 2) Lecture sûre avec valeur par défaut.
print("USER :", os.environ.get("USER", "<inconnu>"))
print("VARIABLE_INEXISTANTE :", os.environ.get("VARIABLE_INEXISTANTE", "<aucune>"))

# 3) setdefault : initialise si absente, sinon ne touche pas.
os.environ.setdefault("LANG", "C")
print("LANG (après setdefault) :", os.environ["LANG"])

# 4) Écriture : visible dans CE processus, pas dans le shell parent.
os.environ["MON_REGLAGE"] = "42"
print("MON_REGLAGE :", os.environ["MON_REGLAGE"])

# 5) Combien de variables sont définies au total ?
print()
print(f"Total : {len(os.environ)} variable(s) d'environnement.")

# Note : après la fin du script, MON_REGLAGE n'existera plus dans le shell.
# Pour le vérifier :   echo $MON_REGLAGE   (renvoie une ligne vide).
