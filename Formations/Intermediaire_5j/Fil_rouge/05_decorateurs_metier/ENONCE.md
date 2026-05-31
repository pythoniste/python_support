# Étape 05 — Décorateurs métier

## Contexte

Votre application grandit. Vous voulez ajouter du **logging automatique** sur les fonctions critiques, mesurer les temps d'exécution, et restreindre l'accès à certaines opérations. Les décorateurs sont l'outil idéal.

## Consignes

1. Créer `decorateurs.py` avec trois décorateurs :

   - **`@log_appel`** : logge (avec `logging`) le nom de la fonction, les arguments et le résultat à chaque appel.
   - **`@timer`** : mesure et logge le temps d'exécution de la fonction.
   - **`@autoriser(roles)`** : décorateur paramétré qui vérifie que l'utilisateur passé en premier argument a un rôle dans la liste `roles`. Lève `PermissionError` sinon.

2. Chaque décorateur doit :
   - Utiliser `functools.wraps` pour préserver le `__name__` et le `__doc__`.
   - Fonctionner sur des fonctions avec `*args` et `**kwargs`.

3. Ajouter un attribut `role` à `Utilisateur` (par défaut `"user"`, possible `"admin"`).

4. Appliquer `@log_appel` sur `ajouter_reservation` et `@timer` sur les opérations de recherche.

## Critères d'acceptation

- [ ] `@log_appel`, `@timer`, `@autoriser` existent dans `decorateurs.py`.
- [ ] `functools.wraps` est utilisé dans chaque décorateur.
- [ ] `@autoriser(["admin"])` lève `PermissionError` pour un utilisateur avec rôle `"user"`.
- [ ] Les tests passent.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier `functools.wraps`** → le `__name__` de la fonction décorée devient `wrapper`.
- **Confondre décorateur simple et paramétré** : `@autoriser(["admin"])` a un niveau d'imbrication supplémentaire.
- **`time.time()` vs `time.perf_counter()`** : préférer `perf_counter()` pour les mesures de performance.
