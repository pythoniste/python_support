"""Étape 01 — Premier script du carnet de recettes."""

nom = input("Nom : ")
brut = input("Ingrédients (séparés par des virgules) : ")
temps = int(input("Temps (minutes) : "))

ingredients = [mot.strip() for mot in brut.split(",") if mot.strip()]

print(f"✅ Recette enregistrée : « {nom} » — {len(ingredients)} ingrédients — {temps} min")
