"""
On veut créer une fonction pour calculer les frais kilométriques

https://www.service-public.fr/particuliers/actualites/A14686
"""

TABLE = {
    (3, 1): (0.529, 0),
    (3, 2): (0.316, 1065),
    (3, 3): (0.370, 0),
    (4, 1): (0.606, 0),
    (4, 2): (0.340, 1330),
    (4, 3): (0.407, 0),
}


def calcul_frais(cv, km):
    if km <= 5000:
        cas = 1
    elif km <= 20000:
        cas = 2
    else:
        cas = 3
    multiplicateur, offset = TABLE[cv, cas]

    return multiplicateur * km + offset


print(calcul_frais(3, 5000))
print(calcul_frais(3, 5001))
print(calcul_frais(3, 6000))
print(calcul_frais(3, 20000))
print(calcul_frais(3, 20001))


TABLE2 = {
    (3, 1): lambda x: x * 0.529,
    (3, 2): lambda x: x * 0.316 + 1065,
    (3, 3): lambda x: x * 0.370,
    (4, 1): lambda x: x * 0.606,
    (4, 2): lambda x: x * 0.340 + 1330,
    (4, 3): lambda x: x * 0.407,
}


def calcul_frais_2(cv, km):
    if km <= 5000:
        cas = 1
    elif km <= 20000:
        cas = 2
    else:
        cas = 3
    return TABLE2[cv, cas](km)


print(calcul_frais_2(3, 5000))
print(calcul_frais_2(3, 5001))
print(calcul_frais_2(3, 6000))
print(calcul_frais_2(3, 20000))
print(calcul_frais_2(3, 20001))
