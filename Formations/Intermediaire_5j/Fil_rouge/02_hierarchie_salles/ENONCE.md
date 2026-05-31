# Étape 02 — Hiérarchie de salles

## Contexte

L'entreprise distingue deux types de salles : les **salles de réunion** (avec visioconférence possible) et les **salles de formation** (avec postes informatiques). On va modéliser cette hiérarchie avec l'héritage et ajouter la surcharge d'opérateurs pour comparer les salles.

## Consignes

1. Créer deux sous-classes de `Salle` dans `modeles.py` :

   - **`SalleReunion`** : ajoute un attribut `visio` (bool, par défaut `False`).
   - **`SalleFormation`** : ajoute un attribut `nb_postes` (int).

2. Chaque sous-classe doit :
   - Appeler `super().__init__` correctement.
   - Surcharger `__str__` pour ajouter l'info spécifique.

3. Surcharger les opérateurs de comparaison sur `Salle` :
   - `__eq__` : deux salles sont égales si même `nom`.
   - `__lt__` : comparaison par `capacite` (pour `sorted()`).
   - `__hash__` : basé sur `nom` (pour pouvoir mettre les salles dans un `set`).

4. Ajouter une méthode de classe `Salle.from_dict(data: dict) -> Salle` qui crée une salle depuis un dictionnaire.

## Attendus

```python
s1 = SalleReunion("Everest", 10, ["vidéoprojecteur"], visio=True)
s2 = SalleFormation("Labo", 20, ["tableau"], nb_postes=15)
print(s1)           # Salle de réunion Everest (10 places, visio)
print(s2)           # Salle de formation Labo (20 places, 15 postes)
print(s1 < s2)      # True (10 < 20)
```

## Critères d'acceptation

- [ ] `SalleReunion` et `SalleFormation` héritent de `Salle`.
- [ ] `super().__init__` est appelé dans chaque sous-classe.
- [ ] `__eq__`, `__lt__`, `__hash__` fonctionnent sur `Salle`.
- [ ] `Salle.from_dict` crée une instance depuis un dict.
- [ ] Les tests du starter passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier `super().__init__`** → les attributs de la classe parente ne sont pas initialisés.
- **`__eq__` sans `__hash__`** → les salles ne peuvent plus être dans un `set` ou comme clé de `dict`.
- **Comparer des types différents dans `__eq__`** → retourner `NotImplemented` si l'autre objet n'est pas une `Salle`.
