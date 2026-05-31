"""Affichage et saisie — toutes les fonctions print/input vivent ici."""

from recettes.carnet import RecetteInvalide, creer_recette


def afficher_menu() -> None:
    """Affiche le menu principal."""
    print()
    print("==== Carnet de recettes ====")
    print("(1) Ajouter une recette")
    print("(2) Lister les recettes")
    print("(3) Sauvegarder")
    print("(4) Charger")
    print("(q) Quitter")


def saisir_recette() -> dict:
    """Demande les informations d'une recette en bouclant sur chaque champ."""
    while True:
        nom = input("Nom : ").strip()
        if nom:
            break
        print("Le nom ne peut pas être vide.")

    ingredients_brut = input("Ingrédients (séparés par des virgules) : ")
    ingredients = [i.strip() for i in ingredients_brut.split(",")]

    while True:
        try:
            temps = int(input("Temps de préparation (min) : "))
            if temps < 1:
                print("Le temps doit être ≥ 1.")
                continue
            break
        except ValueError:
            print("Entrez un nombre entier.")

    return creer_recette(nom, ingredients, temps)


def formater_recette(recette: dict) -> str:
    """Renvoie une chaîne formatée pour l'affichage."""
    ingredients = ", ".join(recette["ingredients"])
    return f"{recette['nom']} ({recette['temps']} min) — {ingredients}"


def afficher_carnet(carnet: list[dict]) -> None:
    """Affiche le carnet numéroté."""
    if not carnet:
        print("« Aucune recette dans le carnet. »")
        return
    for numero, recette in enumerate(carnet, start=1):
        print(f"{numero}. {formater_recette(recette)}")
