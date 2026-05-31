"""Étape 04 — Persistance JSON du carnet de recettes."""

from __future__ import annotations

import json
from pathlib import Path


class RecetteInvalide(ValueError):
    """Données de recette invalides."""


def creer_recette(nom: str, ingredients: list[str], temps: int) -> dict:
    """Construit une recette validée."""
    if not nom or not nom.strip():
        raise RecetteInvalide("Le nom ne peut pas être vide.")
    ingredients_propres = [i.strip() for i in ingredients if i.strip()]
    if not ingredients_propres:
        raise RecetteInvalide("Il faut au moins un ingrédient.")
    if not isinstance(temps, int) or temps < 1:
        raise RecetteInvalide("Le temps doit être un entier ≥ 1.")
    return {"nom": nom.strip(), "ingredients": ingredients_propres, "temps": temps}


def ajouter_recette(carnet: list[dict], recette: dict) -> None:
    """Ajoute une recette au carnet."""
    carnet.append(recette)


def formater_recette(recette: dict) -> str:
    """Renvoie une chaîne d'affichage d'une recette."""
    return (
        f"« {recette['nom']} » — {recette['temps']} min\n"
        f"   Ingrédients : {', '.join(recette['ingredients'])}"
    )


def _saisir_champ(label: str, validateur):
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
    """Affiche toutes les recettes du carnet."""
    if not carnet:
        print("« Aucune recette dans le carnet. »")
        return
    for numero, recette in enumerate(carnet, start=1):
        print(f"{numero}. {formater_recette(recette)}")


def sauvegarder(carnet: list[dict], chemin: Path) -> None:
    """Sauvegarde le carnet dans un fichier JSON lisible."""
    chemin = Path(chemin)
    with chemin.open("w", encoding="utf-8") as fichier:
        json.dump(carnet, fichier, indent=2, ensure_ascii=False)


def charger(chemin: Path) -> list[dict]:
    """Charge un carnet depuis un fichier JSON."""
    chemin = Path(chemin)
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with chemin.open("r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)
    if not isinstance(donnees, list):
        raise ValueError("Le fichier JSON ne contient pas une liste.")
    return donnees


def main() -> None:
    """Boucle principale du carnet de recettes."""
    carnet: list[dict] = []
    while True:
        print()
        print("==== Carnet de recettes ====")
        print("(1) Ajouter une recette")
        print("(2) Lister les recettes")
        print("(3) Sauvegarder")
        print("(4) Charger")
        print("(q) Quitter")
        choix = input("Votre choix : ").strip().lower()

        if choix == "1":
            recette = saisir_recette()
            ajouter_recette(carnet, recette)
            print("✅ Ajoutée !")
        elif choix == "2":
            afficher_carnet(carnet)
        elif choix == "3":
            chemin = Path(input("Chemin : ").strip())
            try:
                sauvegarder(carnet, chemin)
            except OSError as exc:
                print(f"❌ Erreur d'écriture : {exc}")
                continue
            print(f"✅ {len(carnet)} recettes sauvegardées dans {chemin}")
        elif choix == "4":
            chemin = Path(input("Chemin : ").strip())
            try:
                carnet = charger(chemin)
            except (FileNotFoundError, ValueError) as exc:
                print(f"❌ {exc}")
                continue
            print(f"✅ {len(carnet)} recettes chargées depuis {chemin}")
        elif choix == "q":
            print("À bientôt !")
            break
        else:
            print(f"❌ Choix inconnu : {choix!r}")


if __name__ == "__main__":
    main()
