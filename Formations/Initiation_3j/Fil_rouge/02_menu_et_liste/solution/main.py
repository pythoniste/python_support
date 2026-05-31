"""Étape 02 — Menu et liste de recettes en mémoire."""

recettes: list[dict] = []

while True:
    print()
    print("==== Carnet de recettes ====")
    print("(1) Ajouter une recette")
    print("(2) Lister les recettes")
    print("(q) Quitter")
    choix = input("Votre choix : ").strip().lower()

    if choix == "1":
        nom = input("Nom : ")
        brut = input("Ingrédients (séparés par des virgules) : ")
        temps = int(input("Temps (minutes) : "))
        ingredients = [mot.strip() for mot in brut.split(",") if mot.strip()]
        recettes.append({"nom": nom, "ingredients": ingredients, "temps": temps})
        print("✅ Ajoutée !")
    elif choix == "2":
        if not recettes:
            print("« Aucune recette dans le carnet. »")
        else:
            for numero, recette in enumerate(recettes, start=1):
                print(f"{numero}. « {recette['nom']} » — {recette['temps']} min")
                print(f"   Ingrédients : {', '.join(recette['ingredients'])}")
    elif choix == "q":
        print("À bientôt !")
        break
    else:
        print(f"❌ Choix inconnu : {choix!r}")
