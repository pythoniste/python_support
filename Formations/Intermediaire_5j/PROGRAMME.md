# Intermédiaire Python — 5 jours

**Cible :** développeur maîtrisant la syntaxe, les types, les fonctions, les fichiers.
**Objectif :** OO complète, typage moderne, tests professionnels, persistance SQL, outillage et packaging pro.
**Fil rouge :** 🏢 API métier de réservation de salles de réunion (voir `Fil_rouge/README.md`).

## Programme jour par jour

### J1 — Modèle objet
- **Matin :** Classes, attributs, méthodes, `__init__`, `__str__`/`__repr__` · `@staticmethod`, `@classmethod`, `@property`, `@cached_property`
- **Après-midi :** Héritage, `super()`, MRO · Surcharge d'opérateurs · ABC et `Protocol`
- **Étapes fil rouge :** 01 (matin), 02 (après-midi)

### J2 — Typage & structures
- **Matin :** Type hints modernes (`int | None`, `list[T]`, `Protocol`, `TypedDict`, `Literal`, `Self`) · `mypy` en démo · PEP 695
- **Après-midi :** `@dataclass` complet (`slots`, `frozen`, `post_init`, `field`) · Pydantic v2 (validators, serializers, settings) · `Enum`, `NamedTuple`, `collections` avancés
- **Étapes fil rouge :** 03 (matin), 04 (après-midi)

### J3 — Décorateurs & modules avancés
- **Matin :** Décorateurs simples et paramétrés, `functools.wraps` · Context managers, `contextlib` · Design patterns pythoniques (Registry, Factory, Singleton, Strategy)
- **Après-midi :** `itertools`, `functools`, `operator` profonds · Regex (`re`, groupes, flags) · Logging pro (stdlib complet)
- **Étapes fil rouge :** 05 (matin), 06 (après-midi)

### J4 — Persistance SQL
- **Matin :** **SQL avec `sqlite3`** : DDL/DML, `JOIN`, transactions, `with` connexion · **Injection SQL** et requêtes paramétrées · SQLAlchemy Core
- **Après-midi :** SQLAlchemy ORM 2 · Alembic (démo migrations) · Teaser profiling (`timeit`, `cProfile`)
- **Étapes fil rouge :** 07 (matin), 08 (après-midi)

### J5 — Tests & packaging
- **Matin :** `pytest` : fixtures, `parametrize`, marks, `monkeypatch`, `tmp_path`, `caplog` · Mocking (`unittest.mock`, `spec`, `side_effect`) · `factory_boy`
- **Après-midi :** Packaging moderne : `pyproject.toml`, `uv`, `ruff`, `mypy` · Documentation · Finalisation fil rouge
- **Étapes fil rouge :** 09 (matin), 10 (après-midi)

## Fil rouge

Le dossier `Fil_rouge/` contient le projet classique (10 étapes).
