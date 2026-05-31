# Étape 01 — Premier script

## Contexte

C'est la première demi-journée de la formation. Vous venez d'installer Python, de créer un environnement virtuel avec `uv` et d'écrire votre premier `print("Hello")`. Votre grand-père attend son programme de bibliothèque — commençons petit.

## Consignes

1. Créer un fichier `main.py` à la racine du projet.
2. Écrire un programme qui :
   - demande le **titre** d'un livre (`input`),
   - demande l'**auteur** du livre,
   - demande l'**année de publication** (qui sera convertie en `int`),
   - affiche un message de confirmation formaté avec les trois informations.
3. Le programme doit se lancer avec `python main.py`.

## Attendus

Voici un exemple d'exécution :

```
$ python main.py
Titre : Le Petit Prince
Auteur : Antoine de Saint-Exupéry
Année : 1943
✅ Livre enregistré : « Le Petit Prince » de Antoine de Saint-Exupéry (1943)
```

## Critères d'acceptation

- [ ] Le fichier `main.py` existe et se lance sans erreur.
- [ ] Le programme utilise **trois `input()`** séparés.
- [ ] L'année est convertie en `int` (avec `int(input(...))`).
- [ ] Le message de confirmation utilise une **f-string**.
- [ ] Le caractère `✅` (ou équivalent) apparaît dans le message.

## Temps estimé

45 minutes.

## Solution

Voir `solution/main.py` pour une proposition complète.
**À consulter après tentative personnelle** (au moins 20 minutes de recherche).

## Pièges fréquents

- **Oublier `int(...)` sur l'année** → l'année sera une chaîne et vous ne pourrez pas faire d'arithmétique dessus plus tard.
- **Concaténer avec `+`** au lieu d'utiliser une f-string → fonctionne mais plus laid et plus fragile (les types doivent être tous `str`).
- **Accents dans le terminal** → si vous voyez des caractères bizarres, vérifiez que votre terminal est en UTF-8.
