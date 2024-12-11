
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

# Résultat attendu:

result = [
    ["Machine", "Nominale", 1000, 200, 1200],
    ["Travaux", "Intermédiaire", 1000, 100, 1100],
    ["Réfection", "Réduit", 1000, 55, 1055],
    ["Tournevis", "Nominale", 20, 4, 24],
]

"""
On veut créer une fonction pour calculer les frais kilométriques

https://www.service-public.fr/particuliers/actualites/A14686
"""


