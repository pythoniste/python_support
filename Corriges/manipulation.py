import csv
from pprint import pprint


"""
On a des taxes référencées dans un dictionnaire.
On a des produits avec leur nom et leur prix HT.

On veut rajouter le coût de la TVA et le prix TTC.
"""

taxes = {
    "Nominale": 20,
    "Intermédiaire": 10,
    "Réduit": 5.5,
    "Particulier": 2.1,
    "Kerozène": 0,
}

produits = [
    ["Machine", "Nominale", 1000],
    ["Travaux", "Intermédiaire", 1000],
    ["Réfection", "Réduit", 1000],
    ["Tournevis", "Nominale", 20],
]

# Résultat attendu :

result = [
    ["Machine", "Nominale", 1000, 200, 1200],
    ["Travaux", "Intermédiaire", 1000, 100, 1100],
    ["Réfection", "Réduit", 1000, 55, 1055],
    ["Tournevis", "Nominale", 20, 4, 24],
]

# Commencer par travailler sur :

# obj = ["Machine", "Nominale", 1000]
# # Aller chercher le bon taux de TVA
# taux_tva = taxes[obj[1]]
# # Calculer la TVA et l'ajouter à la liste obj
# obj.append(int(obj[2] * taux_tva / 100))
# # Calculer le TTC et l'ajouter à la liste obj
# # Alternative : obj.append(obj[2] * (1 + taux_tva) / 100)
# obj.append(int(obj[2] + obj[3]))
#
# print(obj)


def transformation(obj: list) -> list:
    # Aller chercher le bon taux de TVA
    taux_tva = taxes[obj[1]]
    # Calculer la TVA et l'ajouter à la liste obj
    obj.append(int(obj[2] * taux_tva / 100))
    # Calculer le TTC et l'ajouter à la liste obj
    # Alternative : obj.append(obj[2] * (1 + taux_tva) / 100)
    obj.append(int(obj[2] + obj[3]))
    return obj


# obj = ["Machine", "Nominale", 1000]
# print(transformation(obj))

pprint(list(map(transformation, produits)))

pprint([transformation(produit) for produit in produits])


dict_result = [
    {
        "nom": "Machine",
        "tva": "Nominale",
        "prix HT": 1000,
        "TVA": 200,
        "prix TTC": 1200,
    },
    {
        "nom": "Travaux",
        "tva": "Intermédiaire",
        "prix HT": 1000,
        "TVA": 100,
        "prix TTC": 1100,
    },
    {
        "nom": "Réfection",
        "tva": "Réduit",
        "prix HT": 1000,
        "TVA": 55,
        "prix TTC": 1055,
    },
    {
        "nom": "Tournevis",
        "tva": "Nominale",
        "prix HT": 20,
        "TVA": 4,
        "prix TTC": 24,
    },
]

with open("produits.csv", "w") as f:
    writer = csv.writer(f, dialect=csv.unix_dialect)
    writer.writerow(["nom", "tva", "prix HT", "TVA", "prix TTC"])
    writer.writerows(result)

with open("produits2.csv", "w") as f:
    writer = csv.DictWriter(f, dialect=csv.unix_dialect, fieldnames=["nom", "tva", "prix HT", "TVA", "prix TTC"])
    writer.writeheader()
    writer.writerows(dict_result)

with open("produits3.csv", "w") as f:
    writer = csv.DictWriter(f, dialect=csv.unix_dialect, fieldnames=["nom", "prix HT", "TVA", "prix TTC"], extrasaction="ignore")
    writer.writeheader()
    writer.writerows(dict_result)

with open("produits4.csv", "w") as f:
    writer = csv.writer(f, dialect=csv.unix_dialect)
    writer.writerow(["nom", "prix HT", "TVA", "prix TTC"])
    writer.writerows([r[0:1] + r[2:] for r in result])

