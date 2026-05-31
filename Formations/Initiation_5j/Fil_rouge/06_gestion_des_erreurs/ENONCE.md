# Étape 06 — Gestion des erreurs

## Contexte

Actuellement, si votre grand-père tape « abcd » quand on lui demande l'année de publication, le programme plante avec un `ValueError`. C'est pas acceptable pour un utilisateur final — on doit **gérer proprement** toutes les entrées invalides.

## Consignes

1. Reprendre le code de l'étape 05.
2. Créer trois exceptions personnalisées dans un nouveau fichier `exceptions.py` (ou en haut de `main.py` pour l'instant) :
   - `LivreInvalide(ValueError)` : titre vide, auteur vide, année non numérique ou hors bornes (800 à année courante + 1), ISBN qui ne fait pas 13 caractères numériques.
   - `LivreExistant(Exception)` : on tente d'ajouter un livre avec un ISBN déjà présent.
   - `CatalogueVide(Exception)` : on tente d'afficher ou de rechercher dans un catalogue vide.
3. La fonction `creer_livre` doit **valider** ses arguments et lever `LivreInvalide` avec un message clair en cas d'entrée invalide.
4. La fonction `ajouter_livre` doit lever `LivreExistant` si l'ISBN existe déjà dans le catalogue.
5. La fonction `saisir_livre` doit **boucler** en cas d'erreur : afficher le message et redemander l'info fautive, jusqu'à obtenir une entrée valide.
6. Le menu ne doit **jamais** crasher sur une entrée invalide, quelle qu'elle soit.

## Attendus

```
Titre : (utilisateur appuie juste sur Entrée)
❌ Le titre ne peut pas être vide.
Titre : Le Petit Prince
Auteur : Antoine de Saint-Exupéry
Année : deux mille
❌ L'année doit être un nombre entier.
Année : 1943
ISBN : 123
❌ L'ISBN doit faire 13 chiffres.
ISBN : 9782070612758
✅ Ajouté le 2026-04-14.
```

## Critères d'acceptation

- [ ] Les trois exceptions personnalisées existent et héritent de la bonne classe.
- [ ] Chaque exception porte un message explicatif (passé au `raise`).
- [ ] La saisie boucle jusqu'à obtenir une valeur valide pour chaque champ.
- [ ] L'ajout d'un livre avec un ISBN déjà présent échoue proprement (message + retour au menu).
- [ ] `pytest tests/test_etape06.py` est vert (tests de validation).
- [ ] Aucun `except Exception:` fourre-tout — on attrape la classe précise.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`except ValueError` trop large** : si on utilise `int()` ailleurs, on va attraper des erreurs qui n'ont rien à voir avec le métier. Préférer ses exceptions personnalisées dès qu'on peut.
- **Oublier de `raise`** dans une condition → l'erreur n'est pas signalée et le programme continue avec des données invalides.
- **Validation côté présentation vs côté métier** : l'idéal est que `creer_livre` valide, pas seulement `saisir_livre`. Comme ça, même un appel programmatique est protégé.
- **Année hors bornes** : `datetime.date.today().year + 1` comme limite supérieure pour accepter les sorties imminentes.
