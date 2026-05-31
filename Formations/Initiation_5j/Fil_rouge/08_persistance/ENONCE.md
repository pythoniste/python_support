# Étape 08 — Persistance CSV et JSON

## Contexte

Jusqu'à présent, tout le travail de votre grand-père disparaît quand il quitte le programme. Inacceptable. On va **sauvegarder** et **charger** le catalogue depuis un fichier — au choix, CSV ou JSON.

## Consignes

1. Reprendre le code de l'étape 07.
2. Dans `catalogue.py`, ajouter quatre fonctions :
   - `sauvegarder_csv(catalogue: list[dict], chemin: Path) -> None`
   - `charger_csv(chemin: Path) -> list[dict]`
   - `sauvegarder_json(catalogue: list[dict], chemin: Path) -> list[dict]`
   - `charger_json(chemin: Path) -> list[dict]`
3. Utiliser **`pathlib.Path`** partout, jamais `open(str)`.
4. Le CSV utilise `csv.DictWriter` / `csv.DictReader`. Attention à `newline=""` à l'ouverture.
5. Le JSON est formaté lisible : `json.dump(..., indent=2, ensure_ascii=False)`.
6. Ajouter deux options au menu :
   - `(5) Sauvegarder` : demande un chemin et un format (csv ou json), sauvegarde.
   - `(6) Charger` : demande un chemin, détecte le format par l'extension, charge.
7. Lors du chargement, le catalogue en mémoire est **remplacé** (pas fusionné).
8. Si le fichier n'existe pas, afficher une erreur et retourner au menu (pas de crash).
9. Les données doivent faire un **round-trip parfait** : sauvegarder puis recharger doit redonner le même catalogue.

## Attendus

```
Votre choix : 5
Chemin : /tmp/biblio.json
Format : (c)sv, (j)son : j
✅ 3 livres sauvegardés dans /tmp/biblio.json

Votre choix : 6
Chemin : /tmp/biblio.json
✅ 3 livres chargés depuis /tmp/biblio.json
```

Exemple de fichier JSON produit :

```json
[
  {
    "titre": "Le Petit Prince",
    "auteur": "Antoine de Saint-Exupéry",
    "annee": 1943,
    "isbn": "9782070612758",
    "date_ajout": "2026-04-14"
  }
]
```

## Critères d'acceptation

- [ ] Les quatre fonctions existent dans `catalogue.py`.
- [ ] Toutes utilisent `pathlib.Path`.
- [ ] L'année reste un `int` après round-trip (attention au CSV qui convertit tout en `str`).
- [ ] Le JSON est **lisible** (indent=2, accents préservés).
- [ ] Un fichier inexistant affiche un message d'erreur sans crasher.
- [ ] `pytest tests/test_etape08.py` est vert (teste le round-trip sur CSV et JSON).

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **CSV sur Windows** : sans `newline=""`, on a des lignes vides entre chaque ligne de données.
- **CSV convertit tout en `str`** : après chargement CSV, il faut reconvertir l'année en `int`. Pas ce souci avec JSON qui préserve les types.
- **`ensure_ascii=True`** (défaut) : écrit `"\u00e9"` au lieu de `"é"`. Toujours passer `ensure_ascii=False` pour du français.
- **`open()` sans `encoding="utf-8"`** : dépend du système, donc fragile. Toujours expliciter.
- **Modifier le catalogue en place pendant qu'on lit le fichier** → comportement imprévisible. Charger dans une liste locale puis remplacer.
