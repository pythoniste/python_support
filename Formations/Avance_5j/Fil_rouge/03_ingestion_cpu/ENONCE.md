# Etape 03 -- Ingestion CPU parallele

## Contexte

Le repertoire `inbox/` contient des centaines de fichiers CSV. Les lire et les parser un par un est trop lent. Le parsing CSV est une operation CPU-bound (decodage, validation des types, construction des objets `SensorReading`). Vous allez paralleliser la lecture avec `concurrent.futures.ProcessPoolExecutor`.

## Consignes

1. Creer `src/pipeline/reader.py` :
   - `parse_csv(path: Path) -> list[SensorReading]` : lit un CSV (colonnes : `sensor_id,temperature,humidity,pressure`) et renvoie une liste de `SensorReading`. Les lignes invalides sont ignorees avec un log `warning`.
   - `read_all_csv(inbox: Path, max_workers: int = 4) -> list[SensorReading]` : utilise `ProcessPoolExecutor` pour parser tous les CSV du dossier en parallele. Retourne la liste aplatie de toutes les lectures.

2. Creer `src/pipeline/writer.py` :
   - `write_json(readings: list[SensorReading], path: Path) -> None` : ecrit les lectures au format JSON (liste de dicts).

3. Creer `src/pipeline/__main__.py` :
   - Point d'entree CLI minimal : `python -m pipeline --inbox data/inbox --outbox data/outbox`.
   - Utilise `argparse` pour les arguments.
   - Enchaine : lecture parallele -> affichage du nombre de lectures -> ecriture JSON.

4. Ajouter des fichiers CSV de test dans `tests/fixtures/`.

## Criteres d'acceptation

- [ ] `parse_csv` gere correctement les lignes invalides (log + skip).
- [ ] `read_all_csv` utilise `ProcessPoolExecutor` et est plus rapide que la version sequentielle sur 10+ fichiers.
- [ ] `write_json` produit du JSON valide et lisible.
- [ ] `__main__.py` fonctionne en ligne de commande.
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Passer des objets non-picklables** au pool : `SensorReading` doit etre picklable (pas de lambda, pas de closure dans les attributs).
- **Oublier `if __name__ == "__main__"`** dans `__main__.py` : sans ca, le multiprocessing sur Windows relance le module en boucle.
- **Ne pas fermer le pool** : utiliser le context manager `with ProcessPoolExecutor(...)`.
- **Ignorer les exceptions dans les futures** : appeler `.result()` pour propager les erreurs.
