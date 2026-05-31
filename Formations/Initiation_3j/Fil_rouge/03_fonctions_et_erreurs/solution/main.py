"""Étape 03 — Fonctions et gestion d'erreurs."""


class RecetteInvalide(ValueError):
    """Données de recette invalides."""


def creer_recette(nom: str, ingredients: list[str], temps: int) -> dict:
    """Construit une recette validée. Lève RecetteInvalide si incorrecte."""
    if not nom or not nom.strip():
        raise RecetteInvalide("Le nom ne peut pas être vide.")
    ingredients_propres = [i.strip() for i in ingredients if i.strip()]
    if not ingredients_propres:
        raise RecetteInvalide("Il faut au moins un ingrédient.")
    if not isinstance(temps, int) or temps < 1:
        raise RecetteInvalide("Le temps doit être un entier ≥ 1.")
    return {
        "nom": nom.strip(),
        "ingredients": ingredients_propres,
        "temps": temps,
    }


def ajouter_recette(carnet: list[dict], recette: dict) -> None:
    """Ajoute une recette au carnet (mutation en place)."""
    carnet.append(recette)


def formater_recette(recette: dict) -> str:
    """Renvoie une chaîne d'affichage d'une recette."""
    return (
        f"« {recette['nom']} » — {recette['temps']} min\n"
        f"   Ingrédients : {', '.join(recette['ingredients'])}"
    )


def _saisir_champ(label: str, validateur):
    """Boucle jusqu'à obtenir une entrée valide."""
    while True:
        brut = input(f"{label} : ")
        try:
            return validateur(brut)
        except RecetteInvalide as exc:
            print(f"❌ {exc}")


def saisir_recette() -> dict:
    """Demande une recette à l'utilisateur avec validation ligne par ligne."""

    def valider_nom(x: str) -> str:
        if not x.strip():
            raise RecetteInvalide("Le nom ne peut pas être vide.")
        return x.strip()

    def valider_ingredients(x: str) -> list[str]:
        parts = [i.strip() for i in x.split(",") if i.strip()]
        if not parts:
            raise RecetteInvalide("Il faut au moins un ingrédient.")
        return parts

    def valider_temps(x: str) -> int:
        try:
            n = int(x)
        except ValueError:
            raise RecetteInvalide("Le temps doit être un nombre entier.") from None
        if n < 1:
            raise RecetteInvalide("Le temps doit être ≥ 1.")
        return n

    nom = _saisir_champ("Nom", valider_nom)
    ingredients = _saisir_champ("Ingrédients (séparés par des virgules)", valider_ingredients)
    temps = _saisir_champ("Temps (minutes)", valider_temps)
    return creer_recette(nom, ingredients, temps)


def afficher_carnet(carnet: list[dict]) -> None:
    """Affiche toutes les recettes du carnet numérotées."""
    if not carnet:
        print("« Aucune recette dans le carnet. »")
        return
    for numero, recette in enumerate(carnet, start=1):
        print(f"{numero}. {formater_recette(recette)}")


def main() -> None:
    """Boucle principale du carnet de recettes."""
    carnet: list[dict] = []
    while True:
        print()
        print("==== Carnet de recettes ====")
        print("(1) Ajouter une recette")
        print("(2) Lister les recettes")
        print("(q) Quitter")
        choix = input("Votre choix : ").strip().lower()

        if choix == "1":
            recette = saisir_recette()
            ajouter_recette(carnet, recette)
            print("✅ Ajoutée !")
        elif choix == "2":
            afficher_carnet(carnet)
        elif choix == "q":
            print("À bientôt !")
            break
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    main()
