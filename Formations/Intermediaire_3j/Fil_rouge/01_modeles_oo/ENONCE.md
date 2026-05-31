# Étape 01 — Modèles orientés objet

## Contexte

On modélise le matériel informatique de l'entreprise avec des classes Python.

## Consignes

1. Créer `modeles.py` avec :
   - **`Equipement`** : `nom` (str), `numero_serie` (str), `date_achat` (str ISO), `assigne_a` (str | None).
   - **`Portable`**, **`Ecran`**, **`Serveur`** : sous-classes avec attributs spécifiques (ex. `ram_go` pour Portable, `taille_pouces` pour Ecran, `nb_cpu` pour Serveur).
   - `__init__`, `__str__`, `__repr__`, `__eq__` (sur `numero_serie`), `__hash__`.

2. `Equipement.assigner(nom_utilisateur)` et `Equipement.desassigner()`.

## Critères d'acceptation

- [ ] 4 classes existent avec héritage.
- [ ] `__eq__` et `__hash__` basés sur `numero_serie`.
- [ ] `assigner`/`desassigner` fonctionnent.
- [ ] Les tests passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier `super().__init__`** dans les sous-classes.
- **`__eq__` sans `__hash__`** empêche l'utilisation dans des `set`.
