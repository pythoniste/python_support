"""Étape 01 — Premier script du gestionnaire de bibliothèque.

Saisit les informations d'un livre et affiche une confirmation.
"""

titre = input("Titre : ")
auteur = input("Auteur : ")
annee = int(input("Année : "))

print(f"✅ Livre enregistré : « {titre} » de {auteur} ({annee})")
