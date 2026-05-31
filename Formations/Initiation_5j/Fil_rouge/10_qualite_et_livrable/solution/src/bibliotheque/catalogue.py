"""Logique métier et persistance du catalogue de livres."""

from __future__ import annotations

import csv
import json
import logging
from datetime import date
from pathlib import Path

from bibliotheque.exceptions import CatalogueVide, LivreExistant, LivreInvalide

logger = logging.getLogger(__name__)

_CHAMPS_CSV = ["titre", "auteur", "annee", "isbn", "date_ajout"]


def creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict:
    """Construit un livre validé. Lève ``LivreInvalide`` en cas de donnée fautive."""
    if not titre or not titre.strip():
        raise LivreInvalide("Le titre ne peut pas être vide.")
    if not auteur or not auteur.strip():
        raise LivreInvalide("L'auteur ne peut pas être vide.")
    annee_max = date.today().year + 1
    if not isinstance(annee, int) or annee < 800 or annee > annee_max:
        raise LivreInvalide(f"L'année doit être entre 800 et {annee_max}.")
    if not (isinstance(isbn, str) and len(isbn) == 13 and isbn.isdigit()):
        raise LivreInvalide("L'ISBN doit faire 13 chiffres.")
    return {
        "titre": titre.strip(),
        "auteur": auteur.strip(),
        "annee": annee,
        "isbn": isbn,
        "date_ajout": date.today().isoformat(),
    }


def ajouter_livre(catalogue: list[dict], livre: dict) -> None:
    """Ajoute un livre au catalogue. Lève ``LivreExistant`` sur doublon d'ISBN."""
    for existant in catalogue:
        if existant["isbn"] == livre["isbn"]:
            raise LivreExistant(f"ISBN déjà présent : {livre['isbn']}")
    catalogue.append(livre)
    logger.info("Livre ajouté : %s (%s)", livre["titre"], livre["isbn"])


def rechercher(catalogue: list[dict], terme: str) -> list[dict]:
    """Renvoie les livres dont titre ou auteur contient ``terme``."""
    if not catalogue:
        raise CatalogueVide("Le catalogue est vide.")
    terme_cf = terme.casefold()
    return [
        livre
        for livre in catalogue
        if terme_cf in livre["titre"].casefold()
        or terme_cf in livre["auteur"].casefold()
    ]


def trier(catalogue: list[dict], critere: str) -> list[dict]:
    """Trie une copie du catalogue selon 't', 'a' ou 'n'."""
    clefs = {
        "t": lambda livre: livre["titre"].casefold(),
        "a": lambda livre: livre["auteur"].casefold(),
        "n": lambda livre: livre["annee"],
    }
    if critere not in clefs:
        raise ValueError(f"Critère de tri inconnu : {critere!r}")
    return sorted(catalogue, key=clefs[critere])


def sauvegarder_csv(catalogue: list[dict], chemin: Path) -> None:
    """Sauvegarde le catalogue en CSV."""
    chemin = Path(chemin)
    with chemin.open("w", encoding="utf-8", newline="") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=_CHAMPS_CSV)
        ecrivain.writeheader()
        for livre in catalogue:
            ecrivain.writerow(livre)
    logger.info("Sauvegarde CSV : %d livres dans %s", len(catalogue), chemin)


def charger_csv(chemin: Path) -> list[dict]:
    """Charge un catalogue depuis un fichier CSV."""
    chemin = Path(chemin)
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    catalogue: list[dict] = []
    with chemin.open("r", encoding="utf-8", newline="") as fichier:
        for ligne in csv.DictReader(fichier):
            catalogue.append(
                {
                    "titre": ligne["titre"],
                    "auteur": ligne["auteur"],
                    "annee": int(ligne["annee"]),
                    "isbn": ligne["isbn"],
                    "date_ajout": ligne["date_ajout"],
                }
            )
    logger.info("Chargement CSV : %d livres depuis %s", len(catalogue), chemin)
    return catalogue


def sauvegarder_json(catalogue: list[dict], chemin: Path) -> None:
    """Sauvegarde le catalogue en JSON lisible."""
    chemin = Path(chemin)
    with chemin.open("w", encoding="utf-8") as fichier:
        json.dump(catalogue, fichier, indent=2, ensure_ascii=False)
    logger.info("Sauvegarde JSON : %d livres dans %s", len(catalogue), chemin)


def charger_json(chemin: Path) -> list[dict]:
    """Charge un catalogue depuis un fichier JSON."""
    chemin = Path(chemin)
    if not chemin.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with chemin.open("r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)
    if not isinstance(donnees, list):
        raise ValueError("Le fichier JSON ne contient pas une liste.")
    logger.info("Chargement JSON : %d livres depuis %s", len(donnees), chemin)
    return donnees
