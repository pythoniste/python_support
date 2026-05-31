# Étape 05 — Découpe en fonctions avec type hints

## Contexte

Votre `main.py` commence à dépasser 80 lignes et tout est dans une seule grande boucle. C'est **difficile à lire, à tester et à faire évoluer**. On va découper en fonctions avec **une responsabilité chacune** et ajouter des **type hints** pour documenter les signatures.

## Consignes

1. Reprendre le code de l'étape 04.
2. Extraire les opérations métier dans des fonctions dédiées :
   - `creer_livre(titre: str, auteur: str, annee: int, isbn: str) -> dict`
   - `ajouter_livre(catalogue: list[dict], livre: dict) -> None`
   - `rechercher(catalogue: list[dict], terme: str) -> list[dict]`
   - `trier(catalogue: list[dict], critere: str) -> list[dict]`
   - `formater_livre(livre: dict) -> str`
3. Extraire les opérations d'affichage et de saisie dans des fonctions :
   - `afficher_menu() -> None`
   - `saisir_livre() -> dict`
   - `afficher_catalogue(catalogue: list[dict]) -> None`
4. La boucle principale devient une simple fonction `main() -> None` qui **ne contient que** l'orchestration (le switch sur les choix du menu).
5. Toutes les fonctions doivent avoir **des type hints** sur tous les paramètres et la valeur de retour.
6. Ajouter une docstring courte à chaque fonction (1 ligne suffit).

## Attendus

Le comportement extérieur du programme est **identique** à l'étape 04 — c'est du **refactoring pur**. Les tests du `starter/` vérifient justement ça.

## Critères d'acceptation

- [ ] La boucle principale `main()` fait moins de 30 lignes.
- [ ] Aucune opération métier (recherche, tri, formatage) n'est dans `main()`.
- [ ] **Toutes** les fonctions ont des type hints complets.
- [ ] **Toutes** les fonctions ont une docstring.
- [ ] `mypy --strict main.py` ne remonte aucune erreur (vérifié par le test).
- [ ] `pytest tests/test_etape05.py` est vert.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`list[dict]` vs `List[Dict]`** : depuis Python 3.9 on utilise les génériques natifs, pas les `typing.List`. Depuis 3.10, on utilise `X | None` au lieu de `Optional[X]`.
- **Trop découper** : créer une fonction pour chaque ligne ne sert à rien. Regroupez par responsabilité cohérente.
- **État global** : le `catalogue` doit être passé en argument, pas être une variable globale.
- **`None` comme retour implicite** : les fonctions qui modifient le catalogue sans retourner rien doivent déclarer `-> None` explicitement.
