"""Métier et persistance du carnet de recettes.

Aucun ``print`` ni ``input`` : ce module est du métier pur.
"""

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
