# Etape 10 -- Packaging et observabilite

## Contexte

Le pipeline est complet : il lit, transforme, ecrit, gere la backpressure, est profile et securise. Il reste a le rendre **observable** en production (logs structures, metriques) et a le **packager** proprement pour le distribuer.

## Consignes

### 1. Logs structures avec structlog

1. Remplacer tous les `logging` et `print` de debug par `structlog` :
   - Configurer `structlog` dans `__main__.py` avec un rendu JSON en production et un rendu console en dev.
   - Chaque evenement de log doit inclure des champs structures : `event`, `stage`, `file`, `count`, `duration_ms`, etc.
   - Logger les metriques cles : nombre de fichiers traites, nombre de lectures valides/invalides, temps par etage.

2. Creer `src/pipeline/metrics.py` :
   - `PipelineMetrics` : dataclass qui accumule les metriques (fichiers lus, lectures valides, lectures invalides, temps total, temps par etage).
   - `format_report(metrics: PipelineMetrics) -> str` : formatte un rapport lisible.

### 2. Packaging avance

1. Mettre a jour `pyproject.toml` :
   - Version `1.0.0`.
   - Toutes les dependances (`aiofiles`, `cryptography`, `structlog`).
   - Entry point CLI : `pipeline = "pipeline.__main__:main"`.
   - Entry points pour les plugins (groupe `pipeline.plugins`).
   - Metadonnees completes (auteur, licence, classifiers, urls).

2. Creer un `README.md` a la racine du projet :
   - Description, installation, utilisation, architecture, plugins, securite.

3. Verifier :
   ```bash
   uv build
   uv pip install dist/pipeline-*.whl
   pipeline --help
   pipeline --inbox data/inbox --outbox data/outbox --async --sign --encrypt
   pytest
   ruff check .
   ```

### 3. Finalisation

- S'assurer que **tous les tests** des etapes precedentes passent toujours.
- S'assurer que `ruff check` et `mypy --strict src/` sont verts.
- Le pipeline doit etre **executable de bout en bout** depuis le wheel installe.

## Criteres d'acceptation

- [ ] `structlog` est configure avec rendu JSON (prod) et console (dev).
- [ ] Chaque etage du pipeline log des evenements structures.
- [ ] `PipelineMetrics` accumule et rapporte les metriques.
- [ ] `pyproject.toml` contient toutes les dependances et les entry points.
- [ ] Les plugins sont decouverts via entry points (pas seulement via import direct).
- [ ] `uv build` produit un wheel fonctionnel.
- [ ] `pipeline --help` affiche l'aide avec toutes les options.
- [ ] `pytest` est vert avec `-v`.
- [ ] `ruff check` ne remonte aucune erreur.

## Temps estime

2 heures.

## Solution

Voir `solution/`.

## Pieges frequents

- **`structlog` non configure** : sans configuration explicite, `structlog` utilise un rendu par defaut qui peut ne pas convenir.
- **Entry points et plugins** : les entry points sont declares dans `pyproject.toml` sous `[project.entry-points."pipeline.plugins"]`. Ils ne sont actifs que quand le package est installe.
- **Oublier des dependances** dans `pyproject.toml` : le wheel s'installe mais plante a l'import.
- **Tests qui importent des modules non installes** : utiliser `uv pip install -e ".[dev]"` pour le dev.

## Bravo !

Vous avez un vrai pipeline de donnees asynchrone, profile, securise et distributable. Les extensions possibles : base de donnees pour les resultats, API REST pour le monitoring, deploiement en conteneur Docker, integration avec un message broker (RabbitMQ, Kafka)...
