# Étape 06 — Registry et regex

## Contexte

L'entreprise utilise des **codes de salles** normalisés (ex. `REU-A301`, `FOR-B102`). On va créer un registre dynamique des salles avec un pattern de code, et utiliser des expressions régulières pour valider et extraire les informations de ces codes.

## Consignes

1. Créer `registry.py` avec un **registre** de salles :
   - `SalleRegistry` : classe avec un dictionnaire interne `_salles: dict[str, Salle]`.
   - Méthodes : `enregistrer(salle)`, `obtenir(code)`, `lister()`, `rechercher(pattern)`.
   - Utiliser `__init_subclass__` ou un décorateur de classe pour auto-enregistrer les types de salles.

2. Créer `codes.py` avec des fonctions regex :
   - `valider_code(code: str) -> bool` : le code doit correspondre au pattern `^(REU|FOR|AUD)-[A-Z]\d{3}$`.
   - `extraire_info(code: str) -> dict` : extrait `type` (REU/FOR/AUD), `batiment` (lettre), `numero` (3 chiffres).
   - `trouver_codes(texte: str) -> list[str]` : trouve tous les codes de salles dans un texte libre.

3. Intégrer la validation du code dans `SalleRegistry.enregistrer`.

## Critères d'acceptation

- [ ] `SalleRegistry` fonctionne (enregistrer, obtenir, lister, rechercher).
- [ ] `valider_code` accepte `REU-A301` et refuse `XXX-123`.
- [ ] `extraire_info("REU-A301")` renvoie `{"type": "REU", "batiment": "A", "numero": "301"}`.
- [ ] `trouver_codes` extrait les codes d'un texte.
- [ ] Les tests passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`re.match` vs `re.search`** : `match` ne cherche qu'au début de la chaîne.
- **Oublier `re.IGNORECASE`** ou ne pas le mettre quand il faut : les codes sont en majuscules.
- **Pattern trop laxiste** → accepte des codes invalides. Toujours ancrer avec `^...$`.
