# Fil rouge — 📚 Gestionnaire de bibliothèque personnelle

## Contexte métier

Votre grand-père a chez lui une bibliothèque de plusieurs centaines de livres, sans aucun inventaire. Il vous demande un petit programme Python pour l'aider à **cataloguer, rechercher et prêter** ses livres. Les exigences sont simples :

- Il doit pouvoir ajouter un livre avec titre, auteur, année et ISBN.
- Il doit pouvoir lister ses livres et rechercher par titre ou auteur.
- Il doit pouvoir noter les prêts (à qui, quand) et les retours.
- Les données doivent survivre à la fermeture du programme (fichier).
- Le programme doit être livrable sous forme de commande qu'il pourra installer sur son ordinateur.

Ce projet vous accompagne sur les 5 jours de la formation. À chaque demi-journée, vous enrichissez le programme d'une nouvelle capacité. À la fin du J5, vous disposez d'un **package Python distribuable** avec tests, logs, CLI et documentation.

## Structure des étapes

Chaque dossier `NN_titre/` contient :

- **`ENONCE.md`** : les consignes, attendus et critères d'acceptation de l'étape.
- **`starter/`** : un projet de départ avec `pyproject.toml`, un squelette de `src/bibliotheque/`, et des tests pytest déjà écrits. Vous implémentez le code manquant jusqu'à ce que les tests passent.
- **`solution/`** : une proposition de solution **complète et cumulative**. Elle contient le projet entier à ce stade, pas seulement un diff. À consulter **après** tentative personnelle.

Le dossier `ressources/` contient les fichiers de données d'exemple (CSV, JSON) partagés entre toutes les étapes.

## Progression

| # | Moment | Étape | Livrable de l'étape |
|---|---|---|---|
| 01 | J1 matin | Premier script | Un script `main.py` qui saisit et affiche un livre |
| 02 | J1 après-midi | Menu interactif | Boucle principale avec menu (ajouter/lister/quitter) |
| 03 | J2 matin | Catalogue en mémoire | Liste de livres structurés (dict) avec date d'ajout |
| 04 | J2 après-midi | Recherche et tri | Recherche par titre/auteur, tri multi-critères |
| 05 | J3 matin | Découpe en fonctions + type hints | Code modulaire, `mypy` vert |
| 06 | J3 après-midi | Gestion des erreurs | Exceptions personnalisées, validation des entrées |
| 07 | J4 matin | Organisation en modules | `src/bibliotheque/` avec `catalogue.py`, `ui.py`, `__main__.py` |
| 08 | J4 après-midi | Persistance CSV et JSON | Sauvegarde et chargement du catalogue |
| 09 | J5 matin | Packaging | `pyproject.toml` + entry point CLI via `uv` |
| 10 | J5 après-midi | Qualité et livrable | Logging, tests pytest, README, wheel distribuable |

## Livrable final (fin J5)

À la fin de l'étape 10, vous devez pouvoir exécuter :

```bash
cd 10_qualite_et_livrable/solution
uv build
uv pip install dist/bibliotheque-*.whl
bibliotheque    # lance votre programme installé
pytest          # tous les tests passent
ruff check .    # aucune erreur de lint
```

## Comment utiliser ce fil rouge ?

1. **Lire l'`ENONCE.md`** de l'étape en cours.
2. **Copier le `starter/`** ailleurs (par exemple dans un dossier `mon_travail/` à côté). C'est votre espace de travail.
3. **Implémenter** le code manquant. Lancer `pytest` régulièrement pour vérifier votre progression.
4. **Comparer avec `solution/`** une fois terminé (ou après 45 minutes de recherche infructueuse — pas avant !).
5. **Passer à l'étape suivante** en repartant de votre code si tout est vert, ou de la `solution/` précédente si vous avez pris du retard.

Bon courage !
