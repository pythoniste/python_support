# Étape 01 — Modèles orientés objet

## Contexte

C'est le début de la formation intermédiaire. Vous maîtrisez les bases de Python (variables, fonctions, fichiers). Il est temps de structurer votre code avec des **classes**. Vous allez modéliser les trois entités principales du système de réservation.

## Consignes

1. Créer trois classes dans `src/reservation/modeles.py` :

   - **`Salle`** : attributs `nom` (str), `capacite` (int), `equipements` (list[str]).
   - **`Utilisateur`** : attributs `nom` (str), `email` (str).
   - **`Reservation`** : attributs `salle` (Salle), `utilisateur` (Utilisateur), `date` (str au format ISO), `duree_minutes` (int).

2. Chaque classe doit implémenter :
   - `__init__` avec validation minimale (pas de nom vide, capacité > 0, durée > 0).
   - `__str__` pour un affichage lisible.
   - `__repr__` pour un affichage technique.

3. Ajouter une méthode `Salle.a_equipement(nom: str) -> bool`.

4. Ajouter une méthode `Reservation.fin()` qui renvoie l'heure de fin (chaîne).

## Attendus

```python
salle = Salle("Everest", 10, ["vidéoprojecteur", "tableau blanc"])
print(salle)          # Salle Everest (10 places)
print(repr(salle))    # Salle(nom='Everest', capacite=10, equipements=[...])

user = Utilisateur("Alice", "alice@entreprise.fr")
resa = Reservation(salle, user, "2025-06-15T09:00", 60)
print(resa)           # Réservation Everest par Alice le 2025-06-15T09:00 (60 min)
```

## Critères d'acceptation

- [ ] Les trois classes existent dans `modeles.py`.
- [ ] `__init__` lève `ValueError` si les données sont invalides.
- [ ] `__str__` et `__repr__` sont implémentés pour chaque classe.
- [ ] `Salle.a_equipement` fonctionne (case-insensitive).
- [ ] Les tests du starter passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier `self`** dans `__init__` — erreur classique du débutant en OO.
- **`__repr__` trop verbeux** — il doit permettre de recréer l'objet, pas raconter sa vie.
- **Validation dans `__str__`** au lieu de `__init__` — valider au plus tôt.
