# Starter étape 08

Partez d'une copie de la `solution/` de l'étape 07, puis :

1. Ajoutez dans `src/bibliotheque/catalogue.py` les quatre fonctions
   `sauvegarder_csv`, `charger_csv`, `sauvegarder_json`, `charger_json`.
2. Ajoutez au menu de `src/bibliotheque/__main__.py` les options `(5)
   Sauvegarder` et `(6) Charger`.
3. Utilisez `pathlib.Path` partout, et attention à reconvertir
   l'année en `int` lors du chargement CSV (qui renvoie tout en `str`).
