
from calcul import moyenne

def afficher(*args):
    print(f"les nombres sont {args}")
    calcul = moyenne(*args)
    print(f"la moyenne est {calcul}")

