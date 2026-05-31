# Decisions pedagogiques — Intermediaire 5 jours

Document de reference pour les choix structurants de la formation Intermediaire.

---

## 1. Choix pedagogiques forts

### SQL fondamental avant SQLAlchemy

Le SQL brut avec `sqlite3` est enseigne en premier (notebook 09/01) avant SQLAlchemy Core (09/02) puis ORM (09/03). Raisons :

- un ORM genere du SQL. Diagnostiquer un bug de performance ou une migration exige de **lire** le SQL produit ;
- l'injection SQL et les requetes parametrees sont un sujet de securite critique qui doit etre vu au niveau le plus bas ;
- la comprehension des JOIN, GROUP BY, transactions est un prerequis pour utiliser l'ORM correctement ;
- les stagiaires qui passeront a PostgreSQL, MySQL ou DuckDB auront les bases SQL transferables.

### Pydantic v2 et pas attrs

- Pydantic v2 est le standard de facto pour la validation de donnees structurees en Python (FastAPI, LangChain, etc.) ;
- le moteur Rust (pydantic-core) offre des performances excellentes ;
- l'API `BaseModel` + `@field_validator` + `@model_validator` est coherente et bien documentee ;
- `attrs` est un excellent projet mais n'a pas le meme ecosysteme d'integrations ;
- on enseigne la regle **« Pydantic au bord, dataclass au coeur »** pour la separation des responsabilites.

### Exercices en fonctions typees

A ce niveau, tous les exercices sont ecrits comme des fonctions ou methodes avec :
- type hints modernes (PEP 604 : `int | None`, `list[T]`) ;
- docstrings ;
- l'objectif que `mypy --strict` passe au vert.

Cela force le stagiaire a penser interface et contrat avant implementation.

### Python 3.14 comme cible

Le code utilise les syntaxes les plus recentes :
- `int | None` (PEP 604) au lieu de `Optional[int]`
- `list[T]`, `dict[K, V]` (PEP 585) au lieu de `List[T]`, `Dict[K, V]`
- `type Alias = ...` (PEP 695) pour les alias de type
- `def f[T](...)` (PEP 695) pour les generiques
- `match/case` (PEP 634) la ou c'est pertinent

### Section 12 comme extension thematique

Les 11 notebooks de la section 12 (Calcul numerique et donnees) sont une **extension thematique**. Ils sont :
- auto-suffisants (chacun peut etre pris independamment) ;
- plus courts que les notebooks du coeur (35-65 cellules vs 50-120) ;
- filtres en version 3j ;
- destines a etre approfondis dans les side tracks `Data_science/` et `Data_visualization/`.

---

## 2. Sujets volontairement exclus ou renvoyes a la formation Avancee

| Sujet | Raison de l'exclusion | Formation cible |
|---|---|---|
| Metaclasses (`type`, `__new__`) | Trop avance pour l'Intermediaire | Avance J1 |
| Descripteurs (`__get__`, `__set__`) | Trop avance, `@property` suffit | Avance J1 |
| `asyncio`, `async`/`await` | Sujet complet qui necessite 1-2 jours | Avance J3 |
| `threading`, `multiprocessing` | Concurrence = Avance | Avance J2 |
| Profiling (`cProfile`, `memray`) | Sujet Avance | Avance J4 |
| Securite (crypto, hashing) | Sujet Avance | Avance J5 |
| Property-based testing (Hypothesis) | Trop niche pour 5j | Avance ou side track |
| FastAPI | Framework web hors scope Intermediaire | Side track Web |
| Docker, CI/CD avance | Infrastructure, pas Python | Side track DevOps |

---

## 3. Bibliotheques choisies et justifications

| Bibliotheque | Version | Justification |
|---|---|---|
| **uv** | latest | Remplace pip+pip-tools+virtualenv, ultra-rapide (Rust), lock file deterministe |
| **ruff** | latest | Remplace flake8+isort+black+pylint, 100x plus rapide, meme equipe qu'uv |
| **pydantic** | v2 | Standard de validation, moteur Rust, integre avec FastAPI/SQLAlchemy |
| **SQLAlchemy** | 2.0 | ORM de reference, syntaxe `Mapped[T]` moderne, expression language puissant |
| **Alembic** | latest | Seul outil de migrations pour SQLAlchemy, mature et fiable |
| **pytest** | >= 8 | Standard de facto des tests Python |
| **factory_boy** | latest | Factories de test, integre Faker, SubFactory pour les relations |
| **mypy** | latest | Verificateur de types de reference |

### Pourquoi pas...

- **`pip`** : `uv` est plus rapide, a un lock file, gere les virtualenvs nativement.
- **`black`** : `ruff format` fait la meme chose, integre dans le meme outil.
- **`flake8`** : `ruff check` est un remplacement complet et plus rapide.
- **`attrs`** : `dataclasses` est dans la stdlib, `pydantic` pour la validation. `attrs` n'a pas sa place dans le cursus a ce stade.
- **`peewee`** / `Django ORM` : SQLAlchemy est le plus complet et le plus utilise hors Django.

---

## 4. Decoupage coeur Intermediaire vs section 12

### Coeur (J1-J5, sections 01-11)

Les 26 notebooks du coeur forment un ensemble coherent et progressif :
- **J1** : modele objet complet (classes → ABC → Protocol)
- **J2** : typage et structures (type hints → generiques → dataclasses → Pydantic)
- **J3** : decorateurs, patterns, modules (functools, itertools, regex, logging)
- **J4** : persistance SQL (sqlite3 → SQLAlchemy Core → ORM → Alembic)
- **J5** : tests et packaging (pytest → mocking → factories → pyproject → ruff/mypy)

### Section 12 — Extension thematique (11 notebooks)

La section 12 couvre le **calcul numerique et les donnees** :
- 01-04 : stdlib (`Decimal`, `Fraction`, `statistics`, `random`/`secrets`)
- 05-08 : bibliotheques data (`NumPy`, `Pandas`, `Polars`, `matplotlib`/`seaborn`/`plotly`)
- 09-11 : scientifique et analytique (`SymPy`, `SciPy`, `DuckDB`)

Ces notebooks sont :
- **independants** les uns des autres (sauf progression 05 → 06 → 07) ;
- **plus courts** (35-65 cellules vs 50-120 pour le coeur) ;
- **filtres en version 3j** (tag `skip-3j` sur les sections avancees) ;
- **un tremplin** vers les side tracks specialises.

---

## 5. Fil rouge

Le fil rouge **API metier de reservation de salles de reunion** traverse les 5 jours :
- J1 : classes `Salle`, `Utilisateur`, `Reservation` ; hierarchie de salles
- J2 : typage complet, validation Pydantic des entrees
- J3 : decorateurs metier (`@log`, `@timer`, `@requires_auth`), regex pour codes
- J4 : persistence SQL, migration vers SQLAlchemy ORM
- J5 : tests, factories, packaging

Les exercices de chaque notebook integrent progressivement les briques du fil rouge, creant un projet coherent sur la semaine.

---

*Document cree le 2026-04-14. Mis a jour a chaque modification structurelle de la formation.*
