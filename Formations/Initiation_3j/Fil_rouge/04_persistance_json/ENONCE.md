# Étape 04 — Persistance JSON

## Contexte

Les recettes disparaissent quand le programme s'arrête. On va les sauvegarder dans un fichier JSON.

## Consignes

1. Ajouter deux fonctions :
   - `sauvegarder(carnet: list[dict], chemin: Path) -> None`
   - `charger(chemin: Path) -> list[dict]`
2. Utiliser `pathlib.Path`, `json.dump(... indent=2, ensure_ascii=False)`.
3. Ajouter au menu :
   - `(3) Sauvegarder` : demande un chemin puis sauvegarde.
   - `(4) Charger` : demande un chemin puis remplace le carnet.
4. Un fichier introuvable affiche une erreur sans crasher.

## Attendus

```
Votre choix : 3
Chemin : /tmp/recettes.json
✅ 2 recettes sauvegardées dans /tmp/recettes.json

Votre choix : 4
Chemin : /tmp/recettes.json
✅ 2 recettes chargées depuis /tmp/recettes.json
```

## Critères d'acceptation

- [ ] `pathlib.Path` est utilisé partout.
- [ ] Le JSON est lisible (indent=2, accents conservés).
- [ ] Un fichier inexistant affiche une erreur claire.
- [ ] Round-trip parfait : sauvegarder puis recharger donne le même carnet.

## Temps estimé

1 h 30.

## Solution

Voir `solution/main.py`.

## Pièges fréquents

- **`ensure_ascii=True`** (défaut) → accents encodés en `\uXXXX`, illisibles.
- **`open()` sans `encoding="utf-8"`** → dépend du système, fragile.
