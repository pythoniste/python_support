# Évaluation et plan de refonte — `python_support`

> Document de travail — base de référence pour la refonte du support de formation.
> Dernière mise à jour : 2026-04-14
> Cible Python : **3.14**

---

## Table des matières

1. [Synthèse de l'évaluation](#1-synthèse-de-lévaluation)
2. [Analyse des manques — notebook par notebook](#2-analyse-des-manques--notebook-par-notebook)
3. [Sujets transversaux absents du support](#3-sujets-transversaux-absents-du-support)
4. [Nouveautés Python 3.11 → 3.14 à intégrer](#4-nouveautés-python-311--314-à-intégrer)
5. [Architecture cible](#5-architecture-cible)
6. [Roadmap d'exécution](#6-roadmap-dexécution)

---

## 1. Synthèse de l'évaluation

### 1.1 Pertinence des sujets

**Solide dans l'ensemble**, mais trois problèmes de placement :

- **Initiation** contient des sujets trop avancés : `06 - Decorateurs`, `06 - SQLAlchemy`, et `05 - YAML et TOML` (qui mélange YAML + TOML + ConfigParser + pathlib + shutil + hashlib dans un seul notebook). Ce sont des sujets intermédiaires.
- **Intermédiaire** contient `06 - Metaclasses` qui est clairement avancé — 95 % des développeurs n'en ont jamais besoin. À déplacer dans un module « Python avancé ».
- **Intermédiaire / XML** : DTD, RelaxNG, Schematron et le vrai SAX (expat) sont des sujets de spécialiste, à rendre optionnels.
- **Doublon** : « Programmation fonctionnelle » apparaît dans `02_Types de donnees/09` et dans `03_Algorithmique/04` avec du contenu quasi-identique. À consolider.
- **R_S** est incohérent : un notebook Matplotlib (1,3 Mo) et un Numpy qui n'ont rien à faire dans un cours « Réseau/Système ».

### 1.2 Progressivité

**Points forts :**
- Le Modèle Objet intermédiaire est exemplaire : Classes → Objets → Héritage → Surcharge d'opérateurs.
- `05 - Surcharge d opérateurs` est le modèle à suivre : la classe `Point` est enrichie progressivement (`__add__` → `__sub__` → `__mul__` → `__rmul__` → `__iadd__` → `@total_ordering`).
- Les types de base (`Nombres`, `N-uplets`, `Listes`, `Dictionnaires`) suivent une progression logique avec de bons schémas mémoire pour l'immutabilité.

**Points faibles :**
- `03 - Design patterns` (intermédiaire) est surchargé : Registry, Property, Singleton, Enum, NamedTuple, deque, heapq dans un seul notebook.
- `05 - YAML et TOML` (initiation) mélange 6 sujets indépendants sans transition.
- `05 - Modules essentiels` survole plusieurs modules sans approfondir.
- Les décorateurs arrivent en beginner sans préparation conceptuelle.

### 1.3 Exactitude et modernité

**Déjà modernes :** f-strings, walrus `:=`, `pathlib`, `functools.lru_cache`, `@dataclass(slots=True, frozen=True)`, `operator.itemgetter`, Pydantic **v2** (`model_validate`, `model_dump`), `factory_boy`, `tomllib`, `lxml`, `BeautifulSoup`, `drawsvg`, `odfdo`. Le notebook `Typage statique` utilise la syntaxe Python 3.10+ (`list[int]`, `X | None`, `Self`).

**À moderniser pour 3.14 :**
- `07 - Donnees temporelles` utilise encore `pytz` → **`zoneinfo`** (stdlib depuis 3.9).
- **Type hints absents** dans toute l'Initiation.
- **Aucun usage de `match/case`** alors que plusieurs `if/elif` chaînés s'y prêtent.
- **`unittest`** enseigné sans mentionner **`pytest`**, standard de fait.
- **`lxml`** : `getchildren()` déprécié → itération directe.
- Matplotlib (old) : pylab-style intégral → à réécrire en OO.
- Numpy (old) : `from numpy import *` → `import numpy as np`.

### 1.4 Exemples

**Forces :** exemples concrets et réalistes (bataille navale pour les sets, fiches musiciens pour les dicts, hiérarchie géométrique pour l'héritage, parsing d'ODT réel en XPath, classe `Point` pour la surcharge).

**Faiblesses :**
- **Peu de prose entre les cellules** : ratio markdown/code souvent 20/80. L'apprenant voit le *quoi* mais pas le *pourquoi*.
- **Quasi-aucun exercice explicite**. Seuls `Nombres`, `N-uplets` et `Listes` en contiennent, très basiques.
- Les notebooks de génération de documents (PDF Canvas, SVG, Images) sont très code-heavy (~15 % markdown).

### 1.5 État des `old_notebooks/`

Sur 57 fichiers, **53 sont des coquilles vides** (~250 octets). Les deux dossiers `old_notebooks/` (racine + `02_Intermediaire/old_notebooks/`) sont des **doublons quasi-parfaits** — le second peut être **supprimé sans perte**.

| Notebook | Taille | État | Action |
|---|---|---|---|
| `55 - Numpy.ipynb` | 33 Ko | Correct mais `from numpy import *` | **Garder** et moderniser |
| `56 - Matplotlib.ipynb` | 1,4 Mo | pylab obsolète | **Réécrire** en API OO |
| `57 - SVG.ipynb` | 470 Ko | pygal + cairosvg à jour | **Garder tel quel** |
| `03 - Délimiteurs.ipynb` | 10 Ko | Partiel mais utile | Fondre dans `Initiation/Syntaxe` |

Les 53 autres titres (Cryptographie, Aléatoire, Regex, Images, Son, PDF, OpenDocument, Programmation parallèle/système/réseau, Tests, Optimisation, Web 30 min, Jeu 30 min, SQL, ORM, LDAP, XML, Design patterns…) sont des placeholders. Ils servent de scaffold — liste de sujets à couvrir un jour.

---

## 2. Analyse des manques — notebook par notebook

### 2.1 Initiation — `02_Types de donnees`

#### `01 - Nombres.ipynb`
**Présent :** int, float, opérations, `math`, `statistics`, formatage de base.
**Manque :**
- `decimal.Decimal` (calculs financiers, précision exacte) — **critique**.
- `fractions.Fraction` (nombres rationnels).
- Nombres complexes (`complex`, `cmath`) — au moins une mention.
- **Pièges du flottant IEEE 754** (`0.1 + 0.2 != 0.3`) — essentiel pour tout débutant.
- `math.isclose()` pour comparer des flottants.
- Séparateurs numériques PEP 515 (`1_000_000`).
- `float('inf')`, `float('nan')`, `math.inf`, `math.nan`, `math.isnan()`.
- `int.bit_length()`, `int.bit_count()` (3.10+), conversions de base (`bin`, `oct`, `hex`, `int(s, base)`).
- `round()` vs `math.floor()` vs `math.trunc()` (banker's rounding !).
- `random` basique (à distinguer de `secrets`).
- `pow()` à trois arguments (modulo).

#### `02 - N-uplets.ipynb`
**Présent :** création, déballage, immutabilité, indexation.
**Manque :**
- `collections.namedtuple` — transition naturelle vers les dataclasses plus tard.
- `typing.NamedTuple` (version typée).
- Tuples comme clés de dict (utilisation concrète de l'immutabilité).
- Pattern matching sur tuples (`match case (x, y, z):`).
- Déballage avec `*rest` (PEP 3132).
- Tuple singleton `(x,)` et piège du tuple vide.
- Mention de la différence perf tuple vs liste.

#### `03 - Listes.ipynb`
**Présent :** méthodes, slicing, copie profonde.
**Manque :**
- `sorted()` vs `list.sort()` (retour vs in-place, stabilité).
- Paramètre `key=` avec `lambda`, `operator.itemgetter`, `attrgetter`.
- Module `bisect` (insertion triée, recherche binaire).
- `array.array` (mention : tableau typé homogène).
- Listes comme pile vs `collections.deque` (teaser pour intermédiaire).
- **Piège classique** : `[[0]*3]*3` (références partagées).
- Modification en cours d'itération → `for x in list[:]` ou nouvelle liste.
- `list.reverse()` vs `reversed()` vs `[::-1]`.
- `enumerate(start=1)`, `zip(strict=True)` (3.10+).

#### `04 - Dictionnaires.ipynb`
**Présent :** création, accès, méthodes de base.
**Manque :**
- Opérateurs `|` et `|=` pour fusionner (PEP 584, 3.9+).
- `dict.setdefault()` — souvent sous-utilisé.
- `collections.defaultdict`, `collections.Counter`, `collections.ChainMap`.
- `collections.OrderedDict` (mention : utile uniquement pour `move_to_end` / `popitem(last=False)` depuis que `dict` est ordonné).
- Vues `.keys()`, `.values()`, `.items()` — objets dynamiques, pas des copies.
- Déballage `**dict` dans les appels de fonction et dans la création d'un nouveau dict.
- `match case` sur dict (`case {"name": n, "age": a}:`).
- Comprehensions de dict à conditions.

#### `05 - Ensembles.ipynb`
**Présent :** opérations ensemblistes, cas d'usage.
**Manque :**
- `frozenset` (clés de dict, sets de sets).
- `set.isdisjoint()` — déjà présent mais à souligner vs `&` pour la performance.
- Comprehensions de set explicitement contrastées avec list/dict.
- Piège `{}` = dict vide, pas set vide → utiliser `set()`.
- Opérateurs `<`, `<=` comme sous-ensemble/sur-ensemble.

#### `06 - Chaines de caracteres.ipynb`
**Présent :** méthodes, formatage, immutabilité.
**Manque :**
- f-strings avancés : `f"{x=}"` (debug 3.8+), format specs `:>10`, `:.3f`, `:_`, `:%`, `:b`, `!r`/`!s`/`!a`.
- `str.removeprefix()` / `removesuffix()` (3.9+).
- `str.translate()` / `str.maketrans()`.
- `str.encode()` / `bytes.decode()` explicitement (transition vers `08`).
- Module `textwrap` (wrap, dedent, indent, shorten).
- Module `string` (`string.ascii_letters`, `digits`, `Template`).
- Module `unicodedata` (normalisation NFC/NFD/NFKC/NFKD, catégories).
- Normalisation et comparaison Unicode (café vs café).
- **Expressions régulières** : au moins un teaser avec lien vers un notebook dédié.
- `PEP 701` : f-strings peuvent contenir des guillemets identiques et du multi-ligne (3.12+).

#### `07 - Donnees temporelles.ipynb`
**Présent :** `datetime`, `date`, `time`, `timedelta`, `pytz`, formatage.
**Manque — critique :**
- **`zoneinfo`** (stdlib 3.9+) → doit remplacer `pytz`. Base IANA via `tzdata` sous Windows.
- `datetime.fromisoformat()` / `date.fromisoformat()` (3.11 : support ISO 8601 complet).
- `datetime.UTC` (3.11+) au lieu de `timezone.utc`.
- Module `calendar` (nom des mois, jours fériés, `Calendar`).
- Module `time` (timestamps, `time.monotonic()`, `time.perf_counter()`).
- Problèmes classiques : DST, dates ambiguës, dates naïves vs aware.
- Bibliothèques externes à mentionner : `arrow`, `pendulum`, `whenever` (nouveau, type-safe).
- Parsing libre : `dateutil.parser.parse`.

#### `08 - Booleens nombres et Octets.ipynb`
**Présent :** booléens, bases numériques, encodages, bytes.
**Manque :**
- À **scinder en trois notebooks** : Booléens / Bases numériques / Bytes & encodages.
- Opérateurs bit-à-bit (`&`, `|`, `^`, `~`, `<<`, `>>`) et cas d'usage (masques).
- `bytearray` (bytes mutables), `memoryview` (vue sans copie).
- Module `struct` (pack/unpack binaire) — essentiel pour fichiers binaires et réseau.
- `bytes.hex()` / `bytes.fromhex()`, `base64` (b64encode/b64decode/urlsafe).
- Dangers de `bool` comme sous-classe de `int` (`True + True == 2`).
- BOM UTF-8/UTF-16 et détection (`chardet`, `charset-normalizer`).

#### `09 - Programmation fonctionnelle.ipynb`
**Présent :** map, filter, comprehensions, lambda.
**Manque :**
- `functools.reduce` (avec avertissement Guido).
- `functools.partial` — pattern très fréquent.
- `functools.cache` (3.9+) et `lru_cache`.
- `functools.singledispatch` / `singledispatchmethod`.
- `itertools` profond : `chain`, `islice`, `takewhile`, `dropwhile`, `groupby`, `tee`, `product`, `permutations`, `combinations`, `accumulate`, `count`, `cycle`, `repeat`, `pairwise` (3.10+), `batched` (3.12+).
- Closures et variable de capture tardive (piège du `lambda` dans les boucles).
- Générateurs (`yield`), générateurs délégués (`yield from`).
- Expressions génératrices vs compréhensions (mémoire).
- `PEP 709` : comprehensions inlinées en 3.12 (perfs).
- Bibliothèques externes à mentionner : `toolz`, `returns`.

### 2.2 Initiation — `03_Algorithmique`

#### `01 - Syntaxe.ipynb`
**Présent :** conditions, boucles, exceptions, context managers.
**Manque :**
- **`match case`** (PEP 634, 3.10+) — omission majeure.
- `try` / `except` / `else` / `finally` — le `else` est rarement expliqué.
- Chaînage d'exceptions (`raise ... from ...`).
- Exceptions personnalisées (classe héritant d'`Exception`).
- **Exception groups** et `except*` (PEP 654, 3.11+).
- Plusieurs context managers dans un seul `with` (`with a, b:` ou parenthèses 3.10+).
- `contextlib` (`@contextmanager`, `suppress`, `ExitStack`).
- `PEP 657` : localisation précise des erreurs dans les tracebacks (3.11+).
- Walrus `:=` en conditions et boucles (avec cas d'usage concret).
- `pass`, `...` (Ellipsis), `continue`, `break`, `else` de boucle (le `for/else` mystérieux).

#### `02 - Fonctions.ipynb`
**Présent :** signature, paramètres, valeurs par défaut, `*args`/`**kwargs`.
**Manque :**
- **Type hints obligatoires** dans tous les exemples.
- Paramètres positional-only (`/`) et keyword-only (`*`) — déjà mentionnés, à approfondir avec cas d'usage.
- **Piège du paramètre mutable par défaut** (`def f(x=[]):`) — présent à renforcer.
- `functools.wraps` en préfiguration des décorateurs.
- Annotations de retour `-> None`, `-> int | None`.
- Introspection : `inspect.signature()`, `inspect.Signature`.
- Fonctions de première classe (passer une fonction en argument).
- Nested functions et closures.
- Récursivité, limite de pile (`sys.getrecursionlimit`), absence d'optimisation TCO.
- `PEP 695` (3.12+) : nouvelle syntaxe pour génériques `def f[T](x: T) -> T:`.

#### `03 - Algorithmique.ipynb`
**Présent :** itération, comparaisons chaînées, `any`/`all`.
**Manque :**
- **Notation Big-O** et complexité — même basique, c'est fondamental.
- Algorithmes classiques : recherche linéaire, recherche binaire (via `bisect`).
- Tris : mention de Timsort, stabilité, comparaison avec `sorted(key=)`.
- Récursivité vs itération (exemple factorielle, Fibonacci).
- Mémoïsation (`@cache`) comme introduction à la programmation dynamique.
- Algorithmes sur dict/set : intersection de listes O(n+m) vs O(n·m).
- Structures de données : rappel tableau associatif vs table de hachage.

#### `04 - Programmation fonctionnelle.ipynb`
**À supprimer** (doublon avec `02_Types/09`). Consolider.

#### `05 - Modules essentiels.ipynb`
**Présent :** `string`, `random`, `functools`, `itertools`, `operator`.
**Manque :**
- `collections` complet (voir notebook Dictionnaires).
- `secrets` (vs `random`) — différenciation sécurité.
- `uuid` (UUID1/4, cas d'usage).
- `pathlib` si pas déjà couvert ailleurs.
- `pprint` (affichage structuré).
- `os` (basique : variables d'env, chemins, liste fichiers).
- `sys` (`argv`, `stdin`, `stdout`, `stderr`, `exit`, `version_info`).
- `logging` — **critique**, à introduire tôt.
- `time` (déjà cité).
- Mention de `platform`.

#### `06 - Decorateurs.ipynb`
**À déplacer en Intermédiaire.** Les décorateurs sont du meta-programming.
**Manque à ajouter :**
- `functools.wraps` (obligatoire, presque toujours oublié).
- Décorateurs paramétrés (décorateur qui retourne un décorateur).
- Décorateurs de classe et de méthode.
- Empilement de décorateurs et ordre d'application.
- Décorateurs natifs : `@staticmethod`, `@classmethod`, `@property`, `@cached_property`, `@functools.cache`, `@dataclass`.
- `contextlib.contextmanager` comme décorateur.

### 2.3 Initiation — `04_Manipulation de donnees`

#### `01 - Fichiers.ipynb`
**Présent :** lecture/écriture, encodages, `with`.
**Manque :**
- **`pathlib`** systématique — toutes les opérations fichier devraient l'utiliser.
- Modes `'x'` (exclusive creation), `'a'`, binaire vs texte en détail.
- `encoding='utf-8'` toujours explicite (jamais implicite).
- `errors='replace'` / `'ignore'` / `'surrogateescape'`.
- `newline=''` pour CSV (souvent oublié).
- `tempfile` (NamedTemporaryFile, TemporaryDirectory).
- `shutil` (copy, copytree, move, rmtree, which, archive make/unpack).
- `io.StringIO` / `io.BytesIO` (fichiers en mémoire, utiles pour tests).
- Lecture ligne par ligne pour gros fichiers (itération sur le fichier).
- `mmap` (mention).
- `os.walk()` vs `Path.rglob()`.
- Permissions et `os.chmod()`.

#### `02 - CSV.ipynb`
**Présent :** `reader`, `DictReader`, `writer`.
**Manque :**
- `csv.Sniffer` pour détecter dialecte et présence d'en-tête.
- `QUOTE_ALL`, `QUOTE_MINIMAL`, `QUOTE_NONNUMERIC`, `QUOTE_NONE`.
- Gestion des valeurs manquantes / `None`.
- Teaser **Pandas** et **Polars** pour les gros volumes.
- Teaser **DuckDB** (SQL directement sur CSV).
- Charset detection (`chardet`/`charset-normalizer`).
- Piège Windows : ouvrir en `newline=''`.

#### `03 - JSON.ipynb`
**Présent :** `load`, `loads`, `dump`, `dumps`.
**Manque :**
- `indent`, `sort_keys`, `ensure_ascii=False`, `separators`.
- Encodeur personnalisé (`cls=MyEncoder` pour datetime, Decimal, set…).
- `object_hook` pour décodeur personnalisé.
- Alternatives rapides : `orjson`, `ujson`, `msgspec`.
- **Validation de schéma** : `jsonschema`, `pydantic`.
- Parcours sans charger tout : `ijson` (streaming).
- JSON Lines (`.jsonl`) — format courant en data.
- Sécurité : jamais `eval()` sur du JSON, toujours `json.loads`.

#### `04 - Pickle.ipynb`
**Présent :** basiques.
**Manque — critique :**
- **AVERTISSEMENT SÉCURITÉ** : `pickle.loads` est RCE sur données non fiables.
- Protocoles (0 à 5), `pickle.HIGHEST_PROTOCOL`.
- `__reduce__`, `copyreg` (comportement avancé).
- Alternatives : `shelve` (pickle + dict persisté), `dbm`.
- Alternatives sérialisation sûres : JSON, msgpack, protobuf, Avro.

#### `05 - YAML et TOML.ipynb`
**À éclater en plusieurs notebooks :**
- `YAML` seul (`PyYAML`, `ruamel.yaml`, sécurité `safe_load`).
- `TOML` seul (`tomllib` lecture, `tomli-w` écriture, cas d'usage `pyproject.toml`).
- `ConfigParser` seul (INI).
- `pathlib` dans un notebook dédié ou section propre.
- `shutil` dans Fichiers.
- `hashlib` dans un notebook Cryptographie.

#### `06 - SQLAlchemy.ipynb`
**À déplacer en Intermédiaire**, mais **le SQL manque totalement en amont**. Voir section 3 — il faut créer :
1. Un notebook **SQL fondamental avec `sqlite3`** (stdlib) couvrant SELECT, INSERT, UPDATE, DELETE, JOIN, transactions, paramétrage (injection SQL !).
2. Un notebook **SQLAlchemy Core** (expression language, pas ORM) — requêtes bas niveau typées.
3. Le notebook actuel **SQLAlchemy ORM** en fin de chaîne.

### 2.4 Intermédiaire — `01 - Modele objet`

#### `01 - Classes.ipynb`
**Présent :** attributs, méthodes, introspection.
**Manque :**
- **`__slots__`** — économie mémoire, interdiction d'attributs dynamiques.
- Attributs de classe vs d'instance (piège du mutable partagé).
- `@staticmethod`, `@classmethod` distinction claire avec cas d'usage.
- `@property`, `@x.setter`, `@x.deleter`.
- `@cached_property` (3.8+).
- `__init_subclass__` (hook à l'héritage).
- `__set_name__` et descripteurs (intro).
- `type(obj)` vs `isinstance()`, `issubclass()`.

#### `02 - Objets.ipynb`
**Présent :** init, relations, `__str__`, `__repr__`.
**Manque :**
- `__new__` vs `__init__` (création vs initialisation).
- Cycle de vie complet : `__new__`, `__init__`, `__del__` (avec avertissement finalizer non garanti).
- `weakref` (références faibles, cache sans fuite mémoire).
- Identité (`is`) vs égalité (`==`).
- Hashabilité : `__hash__` et `__eq__` cohérents.
- `__format__` (custom format specs).
- `__bool__`, `__len__` et conversion en booléen.
- `__dir__` (custom `dir()`).

#### `03 - Design patterns.ipynb`
**À scinder.** Patterns GoF à couvrir correctement :
- **Création** : Factory Method, Abstract Factory, Builder, Prototype, Singleton.
- **Structure** : Adapter, Decorator (en plus du décorateur Python), Facade, Proxy, Composite, Bridge, Flyweight.
- **Comportement** : Strategy, Observer, Command, State, Template Method, Iterator, Visitor, Chain of Responsibility, Mediator, Memento.
- Patterns pythoniques spécifiques : EAFP vs LBYL, context manager, iterator protocol, descriptors.

#### `04 - Heritage.ipynb`
**Présent :** MRO, `super()`, héritage multiple.
**Manque :**
- Classes abstraites : `abc.ABC`, `@abstractmethod`, `ABCMeta`.
- **Protocols** (PEP 544, typing) — duck typing structurel, souvent préférable à l'héritage.
- Liskov Substitution Principle — pratique.
- Composition over inheritance (discussion).
- Mixins (cas d'usage concret).
- Diamond problem et résolution par MRO (C3 linearization).
- `functools.singledispatch` comme alternative à la surcharge de méthode.

#### `05 - Surcharge d operateurs.ipynb`
**Excellent**, peu de manques.
**À ajouter :**
- `__enter__` / `__exit__` (context manager protocol).
- `__call__` (objets appelables).
- `__getattr__` / `__setattr__` / `__delattr__` / `__getattribute__`.
- `__getitem__` / `__setitem__` / `__delitem__` / `__contains__` (protocole conteneur).
- `__iter__` / `__next__` (protocole itérateur).
- `__enter__`/`__exit__` pour objets context-manager.
- `__reduce__` pour pickle.
- `NotImplemented` (différent de `NotImplementedError`).

#### `06 - Metaclasses.ipynb`
**À déplacer en Avancé.** À compléter avec :
- Descripteurs (`__get__`, `__set__`, `__delete__`) — prérequis conceptuel.
- `__init_subclass__` comme alternative souvent suffisante.
- Class decorators comme autre alternative.
- Cas d'usage réels : ORM (SQLAlchemy), Django models, ABC.

### 2.5 Intermédiaire — `02 - Objets types`

#### `01 - Typage statique.ipynb`
**Présent :** type hints modernes.
**Manque :**
- **`Protocol`** (PEP 544) — duck typing structurel typé.
- **`TypedDict`** (PEP 589) — dicts avec forme connue.
- **`Literal`**, `Final`, `ClassVar`.
- **`NewType`** (types distincts).
- **`@overload`** pour signatures multiples.
- **Generics** : `Generic[T]`, `TypeVar`, `ParamSpec`, `Concatenate`.
- **PEP 695** (3.12+) : nouvelle syntaxe `class Stack[T]:` et `def first[T](x: list[T]) -> T:`.
- **PEP 696** (3.13+) : `TypeVar` avec defaults.
- `Annotated` et métadonnées (`Annotated[int, Range(0, 100)]`).
- `Self` type (PEP 673, 3.11+) — déjà montré, à expliciter.
- `TYPE_CHECKING` pour imports uniquement-type.
- Variance : covariance, contravariance, invariance.
- `mypy` vs `pyright` (utilisation, config, stricte/non-stricte).
- Stubs (`.pyi`) et `typeshed`.
- `@runtime_checkable` pour Protocols.

#### `02 - Objets avances.ipynb`
**Présent :** Enum, IntEnum, StrEnum, Flag, NamedTuple, deque, heapq.
**Manque :**
- `enum.auto()` expliqué.
- API fonctionnelle des Enum (`Color = Enum('Color', 'RED GREEN BLUE')`).
- `@unique` decorator.
- `verify()` et `FlagBoundary` (3.11+).
- `collections.ChainMap` (rarement vu, utile pour config en couches).
- `collections.OrderedDict` (cas résiduels).
- `queue.Queue`, `queue.LifoQueue`, `queue.PriorityQueue` (thread-safe).
- `types.MappingProxyType` (vue lecture seule sur dict).

#### `03 - dataclasses.ipynb`
**Présent :** tous les paramètres, pièges du mutable.
**Manque :**
- `__post_init__` — personnalisation après init générée.
- `InitVar` — champs d'init non stockés.
- `field(metadata=...)` — annotations custom.
- `dataclasses.asdict()`, `astuple()`, `replace()`, `fields()`, `is_dataclass()`.
- Comparaison avec `attrs` (lib historique, souvent plus puissante).
- Comparaison avec `msgspec.Struct` (perfs extrêmes).
- Comparaison avec `NamedTuple` typé.
- Dataclass inheritance (héritage avec défauts, piège MRO).

#### `04 - pydantic.ipynb`
**Présent :** BaseModel, validation, v2 APIs.
**Manque :**
- `@field_validator`, `@model_validator(mode='before'/'after')`.
- `@computed_field`.
- `Field(..., gt=0, lt=100, pattern=r'...')`.
- `model_config = ConfigDict(...)` (strict, frozen, populate_by_name…).
- `TypeAdapter` pour valider hors BaseModel.
- `RootModel` (remplace `__root__` de v1).
- **`pydantic-settings`** — config 12-factor.
- Sérialisation custom : `@field_serializer`, `@model_serializer`.
- Alias et conversion camelCase ↔ snake_case.
- Pydantic + FastAPI (teaser).
- Pydantic dataclasses vs BaseModel (quand utiliser quoi).

### 2.6 Intermédiaire — `03 - Tests`

#### `01 - tests unitaires.ipynb`
**Présent :** doctest, unittest, mocking, skip.
**Manque — critique :**
- **`pytest`** entier : fixtures (function/class/module/session scope), `@pytest.fixture`, `@pytest.mark.parametrize`, `monkeypatch`, `tmp_path`, `capsys`, `caplog`, `@pytest.mark.skipif`, `xfail`.
- `pytest-cov`, `pytest-xdist`, `pytest-mock`, `pytest-asyncio`.
- **Property-based testing** : `hypothesis`.
- Assertions avancées : `pytest.approx`, `pytest.raises`.
- Structure de tests : conftest.py, arrange-act-assert.
- Mocks plus profonds : `spec`, `side_effect`, `return_value`, `autospec`, `create_autospec`.
- Fake vs Mock vs Stub vs Spy (vocabulaire).
- Test doubles in-memory (in-memory sqlite, fakeredis).
- Couverture : `coverage.py`, seuils, exclusions.
- Snapshot testing (`syrupy`).
- Tox / nox pour matrices d'environnements.

#### `02 - Factory.ipynb`
**Présent :** factory_boy avec Faker.
**Manque :**
- `polyfactory` (alternative plus récente, native pydantic).
- `mimesis` (alternative à Faker).
- Intégration pytest (fixtures qui retournent factories).

#### `03 - test integration.ipynb`
**Présent :** Behave (BDD).
**Manque :**
- `pytest-bdd` (alternative plus intégrée).
- Tests d'API HTTP : `httpx`, `respx`, `requests-mock`.
- Tests base de données : `pytest-postgresql`, `testcontainers`.
- Tests end-to-end web : Playwright, Selenium (teaser).

### 2.7 Intermédiaire — `04 - XML`

#### `01 - XML et DOM.ipynb`
**Manque :**
- **Namespaces XML** — critique, souvent mal compris (`{uri}local`).
- `xml.etree.ElementTree` (stdlib) en parallèle de `lxml` (lib externe).
- CDATA, entités, processing instructions.
- `getchildren()` déprécié → itération directe.
- Sécurité : `defusedxml` (protection contre XML bombs, XXE).

#### `02 - Validation.ipynb`
**À condenser.** Focus XSD (le plus utilisé). DTD/RelaxNG/Schematron → section optionnelle.

#### `03 - SAX.ipynb`
**À déplacer** en side track XML avancé.
**Manque :** `iterparse` de lxml (streaming mémoire-efficace), cas d'usage volumineux.

#### `04 - XPath et XSLT.ipynb`
**Manque :** XPath 2.0/3.0 (via `elementpath`), CSS selectors (`lxml.cssselect`).

#### `05 - HTML.ipynb`
**Manque :**
- Sélecteurs CSS dans BeautifulSoup (`soup.select()`).
- Parsing robuste de HTML cassé (html5lib).
- Sérialisation (pretty-print, minification).

### 2.8 Intermédiaire — `05 - Generation de documents`

**Présent :** PDF Canvas, Platypus, ODT, ODS, ODP, Images (Pillow), SVG (drawsvg).

**Manque :**
- **Word `.docx`** — `python-docx`, très demandé en entreprise.
- **Excel `.xlsx`** explicite : `openpyxl` (lecture/écriture, styles, formules), `xlsxwriter` (écriture rapide).
- **Templating** : `Jinja2` pour texte, `docxtpl` pour Word, `python-pptx` pour PowerPoint.
- **PDF lecture** : `pypdf`, `pdfplumber`, `pymupdf` (fitz) — extraction texte, tableaux, images.
- **Remplissage de formulaires PDF**.
- **WeasyPrint** / `pdfkit` : HTML → PDF (workflow très pratique).
- **ReportLab Charts** (`reportlab.graphics`).
- **QR codes, codes-barres** : `qrcode`, `python-barcode`, `treepoem`.
- **OCR** : `pytesseract` (teaser).
- Pillow plus profond : `ImageDraw`, `ImageFont`, `ImageFilter`, `ImageEnhance`, EXIF.

---

## 3. Sujets transversaux absents du support

Ces sujets manquent **totalement** et doivent être couverts — répartis entre main courses et side tracks.

### 3.1 Bases du développement professionnel (à insérer tôt — Initiation)

- **Environnements virtuels** : `venv`, `virtualenv`, `uv` (recommandé), `poetry`, `pipenv`, `conda`.
- **Gestionnaire de paquets** : `pip`, `uv`, `pipx` (pour applis), `pip-tools`.
- **Structure de projet moderne** : `pyproject.toml` (PEP 621), layout `src/`, `__init__.py`, namespace packages.
- **Packaging** : `build`, `twine`, publication PyPI.
- **Modules et imports** : imports absolus vs relatifs, `__name__ == '__main__'`, circular imports, `__all__`.
- **Shebangs, encoding lines, __future__**.
- **Formatage & lint** : `ruff` (remplace black/isort/flake8/pylint), `mypy`, `pyright`.
- **Pre-commit hooks**.
- **Git + Python** : `.gitignore`, hooks.

### 3.2 Entrée/sortie et interaction utilisateur

- **CLI** : `argparse` (stdlib), `click`, `typer` (basé sur type hints), `rich-click`.
- **TUI** : `rich` (très populaire), `textual` (framework TUI complet), `prompt_toolkit`.
- **Interactive** : `input()`, `getpass` (saisie masquée).
- **Progress bars** : `tqdm`, `rich.progress`.

### 3.3 Logging & debugging

- **`logging`** profond : loggers hiérarchiques, handlers (File, Rotating, Stream, SMTP, HTTP), formatters, filters, dictConfig, niveaux.
- **Alternatives** : `loguru` (simplicité), `structlog` (logs structurés JSON), `picologging`.
- **Debugging** : `pdb`, `breakpoint()` (3.7+), `pdb++`, `ipdb`, intégration IDE.
- **Post-mortem debugging** : `python -m pdb script.py`, `pdb.post_mortem()`.
- **Traceback** : `traceback` module, amélioration `rich.traceback`, `better-exceptions`.

### 3.4 Profiling & performance

- **Timing** : `timeit`, `time.perf_counter`, `%timeit` en Jupyter.
- **Profilers** : `cProfile`, `profile`, `line_profiler`, `py-spy` (production), `scalene`, `memray`.
- **Memory** : `tracemalloc`, `memory_profiler`, `objgraph`.
- **Optimisation** : Cython, Numba, PyPy, mypyc, nuitka.
- **Benchmarking** : `pyperf`, `asv`.

### 3.5 Concurrence & parallélisme

- **`threading`** : threads, locks, conditions, events, Queue, ThreadLocal.
- **`multiprocessing`** : Process, Pool, Queue, Manager, shared memory.
- **`concurrent.futures`** : ThreadPoolExecutor, ProcessPoolExecutor — **API à privilégier**.
- **GIL** expliqué + **PEP 703** (free-threaded Python, 3.13 expérimental, 3.14 stable).
- **`asyncio`** : event loop, coroutines, `async`/`await`, tasks, gather, wait, Semaphore, Lock, Queue.
- **Bibliothèques async** : `httpx`, `aiohttp`, `asyncpg`, `aiofiles`, `trio`, `anyio`.
- **Patterns** : producer/consumer, map/reduce, fan-out/fan-in.
- **PEP 734** : multiple interpreters in stdlib (3.13+).

### 3.6 Réseau & HTTP (critique — manquant)

- **Sockets bas niveau** : TCP/UDP (déjà dans R_S, à nettoyer).
- **HTTP clients** : `urllib` (stdlib, mention), **`requests`** (standard), **`httpx`** (sync + async, recommandé).
- **REST APIs** : consommation, retries (`tenacity`, `backoff`), rate limiting, auth (Bearer, OAuth2).
- **WebSockets** : `websockets`, `aiohttp`.
- **Scraping** : `requests` + BeautifulSoup, `Scrapy` (framework).
- **SSE** (Server-Sent Events).
- **gRPC** (mention).

### 3.7 Bases de données (critique — manquant)

**Ordre d'apprentissage recommandé :**

1. **SQL fondamental** avec **`sqlite3`** (stdlib, zéro dépendance) :
   - CREATE, SELECT, INSERT, UPDATE, DELETE.
   - JOIN (INNER, LEFT, RIGHT, FULL).
   - WHERE, GROUP BY, HAVING, ORDER BY, LIMIT.
   - Transactions, ACID, rollback/commit.
   - **Injection SQL et requêtes paramétrées** (critique sécurité).
   - Index, contraintes, clés étrangères.

2. **DB-API 2.0** : connexion, curseur, fetch, pattern générique.

3. **SQLAlchemy Core** : expression language, pas d'ORM. Requêtes typées sans modèle.

4. **SQLAlchemy ORM** : Declarative, relationships, sessions (notebook actuel).

5. **Alembic** : migrations.

6. **ORMs alternatifs** : `SQLModel` (Pydantic + SQLAlchemy), `Peewee`, `Tortoise ORM` (async), `Django ORM` (cadre Django).

7. **Bases NoSQL** :
   - **Redis** (`redis-py`) : cache, queues, pub/sub.
   - **MongoDB** (`pymongo`, `motor` async).
   - **Elasticsearch**.

8. **Data formats modernes** : Parquet (`pyarrow`), DuckDB (SQL sur fichiers, analytics).

### 3.8 Cryptographie & sécurité

- **Hachage** : `hashlib` (SHA-256, SHA-3, BLAKE2), `hmac`.
- **Hachage mot de passe** : **jamais MD5/SHA**, toujours `bcrypt`, `argon2-cffi`, `passlib`.
- **Secrets** : module `secrets` vs `random`, génération de tokens, comparaison constante.
- **Cryptographie** : bibliothèque `cryptography` (Fernet symétrique, RSA, AES), `pynacl`.
- **JWT** : `pyjwt`, `authlib`.
- **TLS/SSL** : module `ssl`, vérification certificats.
- **OWASP Top 10** appliqué à Python : injection, auth, secrets hardcoded, désérialisation (pickle !), XSS (Jinja2 autoescape).
- **Secrets management** : variables d'env, `python-dotenv`, vaults (Vault, AWS Secrets Manager).
- **`pip-audit`**, `safety` (CVE scanning).

### 3.9 Expressions régulières (manquant — critique)

- Module `re` : `match`, `search`, `findall`, `finditer`, `sub`, `split`, `compile`.
- Syntaxe : classes, quantificateurs, ancres, groupes, lookahead/lookbehind, backrefs.
- Flags : `re.I`, `re.M`, `re.S`, `re.X` (verbose).
- Groupes nommés `(?P<name>...)`.
- Pièges : greedy vs lazy, catastrophic backtracking.
- **`regex`** (lib externe, plus puissante : Unicode properties, variable-width lookbehind).
- Cas d'usage : validation, extraction, remplacement, tokenisation.

### 3.10 Dates avancées & internationalisation

- **`zoneinfo`** (voir plus haut).
- Bibliothèques externes : `arrow`, `pendulum`, **`whenever`** (type-safe, nouveau).
- **`babel`** : i18n, formatage locale.
- **`gettext`** (stdlib) : traductions.
- **`locale`** : formatage nombres/dates par région.

### 3.11 Data science (side track)

- **NumPy** : arrays, dtypes, broadcasting, vectorisation, linalg, random.
- **Pandas** : DataFrame, Series, I/O, indexing, groupby, merge/join, resample, pivot.
- **Polars** : DataFrame moderne, lazy, rapide (alternative à Pandas).
- **DuckDB** : SQL analytique sur fichiers.
- **Matplotlib** (OO), **Seaborn**, **Plotly**, **Altair** (déclaratif), **Bokeh**.
- **Jupyter** au-delà des notebooks : widgets, ipywidgets, Voilà.
- **scikit-learn** (teaser ML).
- **PyTorch** / **TensorFlow** (teaser deep learning, hors scope sans doute).

### 3.12 Web (side track)

- **Flask** : micro-framework classique.
- **FastAPI** : async, type hints, OpenAPI auto, standard moderne.
- **Django** : full-stack, batteries included (cours à part, énorme).
- **Starlette** (base de FastAPI).
- **WSGI vs ASGI** : gunicorn, uvicorn, hypercorn.
- **Templates** : Jinja2.
- **Formulaires** : WTForms, `python-multipart`.
- **Auth** : sessions, JWT, OAuth2.

### 3.13 Système, OS, scripting

- **`os`** : env, path, exec, fork.
- **`subprocess`** : `run`, `Popen`, pipes, shell=False (sécurité), timeouts, capture.
- **`shutil`** : copies, archives, disk usage, which.
- **`signal`** : gestion des signaux Unix.
- **`pathlib`** profond.
- **`glob`**, **`fnmatch`**.
- **`tempfile`**.
- **`platform`**.
- **Alternatives shell** : `sh`, `plumbum`, `invoke`, `fabric`.
- **Cron avec Python** : `apscheduler`, `schedule`, `croniter`.

### 3.14 Interopérabilité & extensions C

- **`ctypes`** : appels à des libs C.
- **`cffi`** : alternative plus propre.
- **C extensions** (CPython API) — mention.
- **Cython** : compilation vers C.
- **`pybind11`** : C++ bindings.
- **`maturin`** : bindings Rust (de plus en plus courant).

### 3.15 Outillage et qualité

- **Linting** : `ruff` (prend la place de black, isort, flake8, pylint — à enseigner en premier).
- **Type checking** : `mypy`, `pyright`, `pyre`, `pytype`.
- **Formatage** : `ruff format`, `black`.
- **Imports** : `ruff check --select I`, `isort`.
- **Docstrings style** : Google, NumPy, Sphinx.
- **Documentation** : `Sphinx`, `MkDocs` (+ Material), `pdoc`, `mkdocstrings`.
- **CI/CD** : GitHub Actions pour Python (matrice de versions, cache, publication).
- **Release** : `bump-my-version`, `python-semantic-release`.

### 3.16 GUI (side track optionnel)

- `tkinter` (stdlib, didactique).
- `PyQt6` / `PySide6` (professionnel, complexe).
- `kivy` (mobile, touch).
- `toga` / `beeware` (cross-platform moderne).
- `dearpygui` (gamedev-ish, rapide).

### 3.17 Jeu vidéo (side track optionnel)

- `pygame`, `pygame-ce`.
- `arcade`.
- `pyglet`.

### 3.18 Multimédia

- **Images** : Pillow (couvert), `OpenCV`, `scikit-image`, `imageio`.
- **Audio** : `pydub`, `librosa`, `sounddevice`, `wave` (stdlib).
- **Vidéo** : `moviepy`, `imageio-ffmpeg`, `av` (PyAV).

---

## 4. Nouveautés Python 3.11 → 3.14 à intégrer

### Python 3.11
- **Exception Groups** (PEP 654) : `ExceptionGroup`, `except*`.
- **`Self` type** (PEP 673).
- **`Required` / `NotRequired`** dans TypedDict (PEP 655).
- **`LiteralString`** (PEP 675) — sécurité SQL.
- **Performance** : +10-60 % vs 3.10 (Faster CPython).
- **`tomllib`** (PEP 680).
- **`StrEnum`**.
- **Améliorations tracebacks** (PEP 657) : flèches ^^^.
- **`datetime.UTC`**, `fromisoformat` complet.

### Python 3.12
- **PEP 695** : nouvelle syntaxe génériques `class Stack[T]:`.
- **PEP 701** : f-strings plus flexibles (quotes identiques, multi-ligne, commentaires, backslashes).
- **PEP 709** : inlined comprehensions (perfs).
- **PEP 669** : `sys.monitoring` (profilers low-overhead).
- **`@override`** decorator (PEP 698).
- **`itertools.batched`**.
- **`pathlib.Path.walk`** (remplace `os.walk`).
- **Buffer protocol** (PEP 688).

### Python 3.13
- **PEP 703** : **GIL optionnel** (free-threaded), build expérimental.
- **PEP 744** : JIT expérimental.
- **PEP 667** : `locals()` sémantique consistante.
- **PEP 730** : iOS officiellement supporté.
- **PEP 738** : Android.
- **`typing.TypeIs`** (PEP 742) — plus précis que `TypeGuard`.
- **`TypeVar` defaults** (PEP 696).
- **Meilleure REPL** (éditeur multi-ligne, couleurs).
- **`copy.replace()`**.
- **`dbm.sqlite3`**.
- **`os.process_cpu_count()`**.

### Python 3.14 (cible)
- **PEP 649** : **deferred evaluation of annotations** (lazy annotations, remplace `from __future__ import annotations`).
- **PEP 750** : t-strings (template strings) — très pertinent pour SQL/HTML safe.
- **PEP 779** : free-threaded Python officiellement supporté (plus expérimental).
- **PEP 758** : `except`/`except*` sans parenthèses autorisé.
- **PEP 765** : interdiction `return`/`break`/`continue` dans `finally`.
- **PEP 784** : module `compression.zstd` (Zstandard dans la stdlib).
- **PEP 768** : safe external debugger attachement.
- **`asyncio` improvements**.
- **Nouvelles syntaxes** à surveiller selon état final du release.

**Actions :**
- Un notebook dédié **"Nouveautés Python 3.11→3.14"** en fin d'Intermédiaire ou en side track.
- Mentions régulières `(nouveau en 3.x)` dans tous les notebooks.

---

## 5. Architecture cible

```
python_support/
│
├── 01_Initiation/                      # COURS DÉBUTANT
│   ├── 01_Presentation/                # Python, installation, venv, Jupyter, REPL
│   ├── 02_Syntaxe/                     # Variables, opérateurs, conditions, boucles, match/case, exceptions
│   ├── 03_Types_de_donnees/
│   │   ├── 01_Nombres.ipynb            # int, float, decimal, fractions, complex, pièges IEEE
│   │   ├── 02_Booleens.ipynb           # bool, opérateurs logiques, truthiness
│   │   ├── 03_Chaines.ipynb            # str, f-strings, méthodes, unicode
│   │   ├── 04_Listes.ipynb
│   │   ├── 05_Tuples.ipynb
│   │   ├── 06_Dictionnaires.ipynb
│   │   ├── 07_Ensembles.ipynb
│   │   ├── 08_Donnees_temporelles.ipynb # zoneinfo, datetime, calendar
│   │   └── 09_Bytes_et_encodages.ipynb
│   ├── 04_Fonctions/                   # Signatures, type hints, args/kwargs, closures, lambda
│   ├── 05_Programmation_fonctionnelle/ # map/filter/reduce, comprehensions, generators, itertools/functools
│   ├── 06_Modules_et_packages/         # import, __name__, structure projet, venv
│   ├── 07_Entrees_sorties/
│   │   ├── 01_Fichiers.ipynb           # pathlib, open, encodages
│   │   ├── 02_CSV.ipynb
│   │   ├── 03_JSON.ipynb
│   │   ├── 04_Arguments_CLI.ipynb      # sys.argv, argparse basique
│   │   └── 05_Logging_basique.ipynb
│   ├── 08_Bonnes_pratiques/            # PEP 8, docstrings, ruff, tests basiques avec pytest
│   └── 09_Projet_fil_rouge/            # Mini-projet consolidant tout
│
├── 02_Intermediaire/                   # COURS INTERMÉDIAIRE
│   ├── 01_Modele_objet/                # Classes, Objets, Héritage, Surcharge
│   ├── 02_Typage_et_structures/        # Type hints avancés, Protocol, TypedDict, Generics
│   ├── 03_Dataclasses_et_validation/   # dataclasses, attrs, pydantic v2, msgspec
│   ├── 04_Enumerations_et_collections/ # Enum, NamedTuple, deque, heapq, Counter, defaultdict, ChainMap
│   ├── 05_Decorateurs_et_metaprog/     # Décorateurs, cached_property, context managers, descriptors
│   ├── 06_Design_patterns/             # GoF + pythoniques
│   ├── 07_Modules_avances/             # itertools, functools, operator profonds
│   ├── 08_Tests/
│   │   ├── 01_pytest.ipynb             # fixtures, parametrize, marks
│   │   ├── 02_mocking.ipynb
│   │   ├── 03_factories.ipynb          # factory_boy, polyfactory
│   │   ├── 04_property_based.ipynb     # hypothesis
│   │   ├── 05_bdd.ipynb                # behave / pytest-bdd
│   │   └── 06_coverage_et_ci.ipynb
│   ├── 09_Persistance/
│   │   ├── 01_Pickle_et_shelve.ipynb   # avec avertissement sécurité
│   │   ├── 02_YAML.ipynb
│   │   ├── 03_TOML.ipynb
│   │   ├── 04_ConfigParser.ipynb
│   │   ├── 05_SQL_avec_sqlite3.ipynb   # SQL FONDAMENTAL + injection + transactions
│   │   ├── 06_SQLAlchemy_Core.ipynb    # Expression language
│   │   ├── 07_SQLAlchemy_ORM.ipynb     # Existant modernisé
│   │   └── 08_Alembic.ipynb            # Migrations
│   ├── 10_Regex/                       # MANQUE CRITIQUE
│   ├── 11_Logging/                     # Stdlib complet + loguru/structlog
│   ├── 12_HTTP_et_API/
│   │   ├── 01_httpx.ipynb              # sync + async
│   │   ├── 02_REST_consommation.ipynb
│   │   └── 03_FastAPI_intro.ipynb
│   ├── 13_XML/                         # DOM, XPath, HTML, defusedxml (sécurité)
│   ├── 14_Generation_de_documents/
│   │   ├── 01_PDF_Platypus.ipynb       # Existant
│   │   ├── 02_Word_docx.ipynb          # NOUVEAU
│   │   ├── 03_Excel_openpyxl.ipynb     # NOUVEAU
│   │   ├── 04_ODT_ODS_ODP.ipynb        # Existant
│   │   ├── 05_HTML_vers_PDF.ipynb      # WeasyPrint
│   │   ├── 06_Templates_Jinja.ipynb
│   │   ├── 07_Images_Pillow.ipynb      # Existant approfondi
│   │   ├── 08_SVG.ipynb                # Existant
│   │   └── 09_QR_et_codes_barres.ipynb
│   └── 15_Packaging/                   # pyproject.toml, build, publish, uv
│
├── 03_Avance/                          # COURS AVANCÉ (nouveau, optionnel)
│   ├── 01_Metaclasses_et_descripteurs/
│   ├── 02_Concurrence/                 # threading, mp, concurrent.futures, GIL, PEP 703
│   ├── 03_Asyncio/                     # Complet
│   ├── 04_Performance/                 # Profiling, Cython, Numba
│   ├── 05_Internals/                   # Bytecode, dis, gc, weakref
│   └── 06_Nouveautes_3_11_a_3_14/
│
├── Side_Tracks/                        # TRACKS SPÉCIALISÉS
│   ├── Systeme_et_Reseau/              # Ex-R_S nettoyé + TP Palindrome + TP Sys-Rezo
│   ├── Data_Science/                   # NumPy, Pandas, Polars, DuckDB
│   ├── Data_Visualization/             # Matplotlib OO, Seaborn, Plotly, Altair, SVG, pygal
│   ├── Cryptographie_et_Securite/      # hashlib, cryptography, bcrypt, JWT, OWASP
│   ├── Web_Backend/                    # Flask, FastAPI, Django (teaser)
│   ├── XML_avance/                     # DTD, RelaxNG, Schematron, SAX, iterparse
│   ├── CLI_et_TUI/                     # argparse, click, typer, rich, textual
│   ├── Multimedia/                     # Pillow avancé, audio, vidéo, OCR
│   ├── PDF_avance/                     # Lecture/extraction, formulaires
│   ├── Scientific_Computing/           # SciPy, sympy
│   ├── Jeu_video/                      # pygame-ce
│   └── GUI/                            # tkinter, PySide6
│
├── Exercices/                          # Par cours
│   ├── 01_Initiation/
│   ├── 02_Intermediaire/
│   └── Side_Tracks/
│
├── Corriges/                           # Miroir structure Exercices
│   ├── 01_Initiation/
│   ├── 02_Intermediaire/
│   └── MAPPING.md
│
├── EN/                                 # Mirror EN (gel temporaire, réactivation en fin)
│
└── EVALUATION_ET_PLAN.md               # Ce fichier
```

---

## 6. Roadmap d'exécution

### Phase 0 — Préparation (1 jour)
- [x] Évaluation complète (ce document).
- [ ] Valider l'arborescence cible avec l'utilisateur.
- [ ] Créer la nouvelle arborescence vide en branche dédiée.
- [ ] `.gitignore` propre (`.ipynb_checkpoints`, `__pycache__`, `.venv`).

### Phase 1 — Ménage (1 jour, zéro risque)
- [ ] Supprimer `02_Intermediaire/old_notebooks/` (doublon).
- [ ] Supprimer `01_Initiation/02_Types de donnees/03 - Lists.ipynb` (orphelin EN).
- [ ] Ranger `bar_chart.svg`, `bottle_palindrome.py` dans `Exercices/` ou `old_notebooks/`.
- [ ] Déplacer Matplotlib/Numpy/SVG des `old_notebooks/` vers `Side_Tracks/Data_Visualization/` et `Side_Tracks/Data_Science/` (juste le déplacement, pas la réécriture).
- [ ] Geler `EN/` (README indiquant le statut snapshot 2025-06).

### Phase 2 — Prototype pédagogique (2-3 jours)
- [ ] Réécrire **UN notebook modèle** complet : `01_Initiation/03_Types_de_donnees/01_Nombres.ipynb`.
  - Beaucoup de prose explicative.
  - Type hints systématiques.
  - 5 exercices gradués (facile → difficile) avec corrigés séparés.
  - Modernisation Python 3.14.
  - Toutes les additions de la section 2.1.
- [ ] Valider le format avec l'utilisateur avant d'industrialiser.

### Phase 3 — Migration Initiation (1-2 semaines)
- [ ] Appliquer le format validé aux 9 notebooks des types de données.
- [ ] Créer `01_Presentation/` et `02_Syntaxe/` (refonte de l'ancien `03_Algorithmique`).
- [ ] Refondre `04_Fonctions/`.
- [ ] Consolider `05_Programmation_fonctionnelle/` (fusion du doublon).
- [ ] Créer `06_Modules_et_packages/` (nouveau).
- [ ] Refondre `07_Entrees_sorties/`.
- [ ] Créer `08_Bonnes_pratiques/` (nouveau).
- [ ] Créer `09_Projet_fil_rouge/` (nouveau).

### Phase 4 — Migration Intermédiaire (2-3 semaines)
- [ ] Déplacer : Décorateurs, SQLAlchemy depuis Initiation.
- [ ] Scinder : Design patterns, Objets avancés.
- [ ] Refondre : tests (ajouter pytest, hypothesis).
- [ ] Créer **SQL avec sqlite3** en prérequis SQLAlchemy (critique).
- [ ] Créer : Regex, Logging, HTTP/API, Word/Excel.
- [ ] Migrer Métaclasses vers `03_Avance/`.

### Phase 5 — Side tracks (selon demande, 1 semaine chacun)
- [ ] Système & Réseau : nettoyer `R_S/`, wrapper `rezo/`.
- [ ] Data Visualization : réécrire Matplotlib en OO.
- [ ] Data Science : moderniser NumPy + nouveaux Pandas/Polars.
- [ ] Cryptographie & Sécurité (nouveau).
- [ ] Autres selon priorité.

### Phase 6 — Exercices & corrigés (transverse)
- [ ] Pour chaque notebook, 3 à 5 exercices gradués.
- [ ] Structure `Exercices/` miroir du cours.
- [ ] `Corriges/MAPPING.md` traçant chaque corrigé.

### Phase 7 — EN sync (à la fin)
- [ ] Retraduire les notebooks impactés une fois FR figé.

### Phase 8 — Infra continue
- [ ] CI : exécution des notebooks (nbconvert, `jupyter nbconvert --execute`).
- [ ] `ruff` + `mypy` sur le code extrait.
- [ ] Vérifier que tous les notebooks s'exécutent avec Python 3.14.

---

## 7. Programmes des formations

> Cette section formalise l'organisation physique du repo en **cinq formats de formation** à partir de la même source de notebooks, ainsi que le détail jour-par-jour de chaque programme et la structure des fils rouges.

### 7.1 Principe de source unique

Le repo est organisé en **trois espaces** aux rôles stricts :

| Dossier | Rôle | Édité par |
|---|---|---|
| `Bibliotheque_notebooks/` | **Source unique** de tous les notebooks (organisation de la section 5) | Manuellement |
| `Formations/<format>/` | Packages prêts à distribuer : notebooks + fil rouge + programme | Généré par `tools/build_formation.py` |
| `tools/` | Scripts de build et de vérification | Manuellement |

Les cinq formats (Initiation 5j, Initiation 3j, Intermédiaire 5j, Intermédiaire 3j, Avancé 5j) sont générés à partir de la même source :

- Les **formats 5 j** par **copie directe** des notebooks listés dans un manifeste YAML.
- Les **formats 3 j** par **`nbconvert` + `TagRemovePreprocessor`** qui retire les cellules tagguées à la génération.

**Règles d'or :**

1. On n'édite **jamais** directement dans `Formations/<format>/<Jx>/` — ces dossiers sont regénérés. Ils sont au `.gitignore` ou versionnés automatiquement par la CI.
2. Le `Fil_rouge/` de chaque formation est édité **à la main dans `Formations/<format>/Fil_rouge/`** et est versionné (il n'est pas généré — c'est un projet Python classique).
3. Un stagiaire reçoit **un seul dossier** (`Formations/<format>/`) qui contient absolument tout ce dont il a besoin.

### 7.2 Convention de tags de cellules

Chaque cellule des notebooks peut porter un ou plusieurs tags. Le filtrage 5 j / 3 j se fait exclusivement via ces tags.

| Tag | Sens | Comportement 5 j | Comportement 3 j |
|---|---|---|---|
| *(aucun)* | Tronc commun | Affiché | Affiché |
| `skip-3j` | Approfondissement, cas avancé | Affiché | **Retiré** |
| `exo-facile` | Exercice niveau facile | Affiché | Affiché |
| `exo-moyen` | Exercice niveau intermédiaire | Affiché | Affiché |
| `exo-difficile` | Exercice challenge | Affiché | **Retiré** |
| `deep-dive` | Section d'approfondissement fouillée | Affiché (replié par défaut) | **Retiré** |
| `bonus` | Contenu bonus si temps | Affiché (replié par défaut) | **Retiré** |
| `correction` | Corrigé d'un exercice | Affiché (replié par défaut) | Affiché (replié par défaut) |

Le repli par défaut utilise la métadonnée JupyterLab `"jupyter": {"source_hidden": true}` sur les cellules, ou `"jp-MarkdownHeadingCollapsed": true` sur les titres markdown pour replier toute une section.

### 7.3 Arborescence physique complète

```
python_support/
│
├── Bibliotheque_notebooks/             # SOURCE UNIQUE — édité à la main
│   ├── Initiation/                     # (contenu détaillé en section 5)
│   ├── Intermediaire/
│   ├── Avance/
│   └── Side_tracks/
│
├── Formations/                         # PACKAGES GÉNÉRÉS (sauf Fil_rouge/)
│   ├── Initiation_5j/
│   │   ├── PROGRAMME.md                # mapping jour ↔ notebooks
│   │   ├── J1_prise_en_main/
│   │   ├── J2_types_de_donnees/
│   │   ├── J3_fonctions_algorithmique/
│   │   ├── J4_modules_et_fichiers/
│   │   ├── J5_qualite_packaging_livrable/
│   │   └── Fil_rouge/                  # projet classique, 10 étapes (édité à la main)
│   ├── Initiation_3j/
│   │   ├── PROGRAMME.md
│   │   ├── J1_.../
│   │   ├── J2_.../
│   │   ├── J3_.../
│   │   └── Fil_rouge/                  # projet différent, 6 étapes
│   ├── Intermediaire_5j/
│   │   ├── PROGRAMME.md
│   │   ├── J1_.../
│   │   ├── ...
│   │   └── Fil_rouge/                  # 10 étapes
│   ├── Intermediaire_3j/
│   │   └── Fil_rouge/                  # projet différent, 6 étapes
│   └── Avance_5j/
│       └── Fil_rouge/                  # 10 étapes
│
├── tools/
│   ├── build_formation.py              # Bibliotheque_notebooks → Formations/<format>/
│   ├── build_3j.py                     # TagRemovePreprocessor pour variantes 3j
│   ├── check_notebooks.py              # exécution + ruff + mypy sur le code extrait
│   ├── init_fil_rouge.py               # scaffolding d'une nouvelle étape
│   ├── manifests/
│   │   ├── initiation_5j.yaml
│   │   ├── initiation_3j.yaml
│   │   ├── intermediaire_5j.yaml
│   │   ├── intermediaire_3j.yaml
│   │   └── avance_5j.yaml
│   └── README.md
│
├── EN/                                 # Gelé (snapshot 2025-06), réactivé en fin
└── EVALUATION_ET_PLAN.md               # Ce fichier
```

### 7.4 Script de build 3 j

`tools/build_3j.py` applique un `TagRemovePreprocessor` de nbconvert :

```python
from nbconvert.preprocessors import TagRemovePreprocessor
from nbconvert.exporters import NotebookExporter
from traitlets.config import Config

c = Config()
c.TagRemovePreprocessor.remove_cell_tags = {
    "skip-3j",
    "exo-difficile",
    "deep-dive",
    "bonus",
}
c.TagRemovePreprocessor.enabled = True

exporter = NotebookExporter(config=c)
exporter.register_preprocessor(TagRemovePreprocessor(config=c), enabled=True)
```

### 7.5 Programme — Initiation 5 jours

**Cible :** débutant Python (éventuellement développeur d'un autre langage).
**Objectif :** écrire des scripts Python modernes autonomes, manipuler des données, structurer un projet livrable.
**Fil rouge :** 📚 **Gestionnaire de bibliothèque personnelle** — catalogue de livres, emprunts, import/export.

#### Contenu jour par jour

| Jour | Matin | Après-midi |
|---|---|---|
| **J1 — Prise en main** | Installation, venv (`uv`), REPL, Jupyter/IDE · Variables, types primitifs (`int`, `float`, `str`, `bool`) · Opérateurs et expressions · `print`, `input` | Conditions (`if`/`elif`/`else`, intro `match/case`) · Boucles (`for`, `while`), `break`/`continue`, `else` de boucle |
| **J2 — Types de données** | Listes et tuples · Dictionnaires et ensembles · Compréhensions de base | Chaînes et f-strings (dont `{x=}`) · `datetime`, `date`, `timedelta`, `zoneinfo` (mention) |
| **J3 — Fonctions & algorithmique** | Fonctions : paramètres, retours, défauts, `*args`/`**kwargs` · Type hints (introduction) · Portée, closures (intro) | Exceptions (`try`/`except`/`else`/`finally`) · Exceptions personnalisées · Debugging avec `breakpoint()` |
| **J4 — Modules & fichiers** | Modules standard : `math`, `random`, `statistics`, `pathlib` · Imports, organisation en plusieurs fichiers, `__main__` | Fichiers texte, encodages · CSV (`csv.DictReader`/`DictWriter`) · JSON |
| **J5 — Qualité, packaging, livrable** | PEP 8, docstrings · `ruff` (format + lint) · `pyproject.toml` (PEP 621) · Structure `src/` | `logging` basique · CLI avec `argparse` + entry point console · Intro `pytest` (3 tests) · Build wheel avec `uv build` · Finalisation fil rouge |

#### Fil rouge — 10 étapes (1 par demi-journée)

| # | Moment | Intitulé | Compétences mobilisées |
|---|---|---|---|
| 01 | J1 matin | **Premier script** : saisir et afficher un livre | variables, types, `input`, `print`, f-strings |
| 02 | J1 après-midi | **Menu interactif** : ajouter, afficher, quitter | conditions, boucle principale, `match/case` |
| 03 | J2 matin | **Catalogue en mémoire** : liste de livres (dicts) | listes, dicts, itération |
| 04 | J2 après-midi | **Recherche et tri** par titre/auteur/date | compréhensions, `sorted(key=)`, dates |
| 05 | J3 matin | **Découpe en fonctions** avec type hints | fonctions, paramètres, retours typés |
| 06 | J3 après-midi | **Gestion des erreurs** : exceptions personnalisées | classes d'exception, `raise`, `try`/`except` |
| 07 | J4 matin | **Organisation en modules** (`catalogue.py`, `ui.py`, `__main__.py`) | imports, structure projet |
| 08 | J4 après-midi | **Persistance CSV et JSON** | `pathlib`, `csv`, `json` |
| 09 | J5 matin | **Packaging** : `pyproject.toml` + entry point CLI | `argparse`, `uv build` |
| 10 | J5 après-midi | **Qualité et livrable** : logging, tests, README, wheel distribué | `logging`, `pytest`, wheel |

### 7.6 Programme — Initiation 3 jours

**Même thèmes, version compressée.** Les notebooks sont **générés automatiquement** depuis les notebooks 5 j via filtrage des tags (`skip-3j`, `exo-difficile`, `deep-dive`, `bonus`).

**Fil rouge différent et plus court :** 📝 **Carnet de recettes** — projet distinct pour éviter la confusion si un stagiaire enchaîne les deux formats.

#### Contenu jour par jour

| Jour | Matin | Après-midi |
|---|---|---|
| **J1 — Syntaxe & types** | Installation, variables, types primitifs, opérateurs · Conditions, boucles | Listes, tuples, dicts · Chaînes et f-strings |
| **J2 — Fonctions & fichiers** | Fonctions, paramètres, retours · Exceptions basiques | Fichiers texte + `pathlib` · CSV · JSON |
| **J3 — Modules & livrable** | Modules standard, imports, organisation | `pyproject.toml` minimal + entry point · Finalisation fil rouge |

#### Fil rouge — 6 étapes (1 par demi-journée)

| # | Moment | Intitulé |
|---|---|---|
| 01 | J1 matin | Premier script : saisir et afficher une recette |
| 02 | J1 après-midi | Menu interactif + liste de recettes en mémoire |
| 03 | J2 matin | Découpe en fonctions + gestion d'erreurs |
| 04 | J2 après-midi | Persistance JSON |
| 05 | J3 matin | Découpe en modules |
| 06 | J3 après-midi | `pyproject.toml` minimal + CLI + livrable |

### 7.7 Programme — Intermédiaire 5 jours

**Cible :** développeur maîtrisant la syntaxe, les types, les fonctions, les fichiers.
**Objectif :** OO complète, typage moderne, tests professionnels, persistance SQL, outillage et packaging pro.
**Fil rouge :** 🏢 **API métier de réservation de salles de réunion**.

#### Contenu jour par jour

| Jour | Matin | Après-midi |
|---|---|---|
| **J1 — Modèle objet** | Classes, attributs, méthodes, `__init__`, `__str__`/`__repr__` · `@staticmethod`, `@classmethod`, `@property`, `@cached_property` | Héritage, `super()`, MRO · Surcharge d'opérateurs · ABC et `Protocol` |
| **J2 — Typage & structures** | Type hints modernes (`int \| None`, `list[T]`, `Protocol`, `TypedDict`, `Literal`, `Self`) · `mypy` en démo · PEP 695 | `@dataclass` complet (`slots`, `frozen`, `post_init`, `field`) · Pydantic v2 (validators, serializers, settings) · `Enum`, `NamedTuple`, `collections` avancés |
| **J3 — Décorateurs & modules avancés** | Décorateurs simples et paramétrés, `functools.wraps` · Context managers, `contextlib` · Design patterns pythoniques (Registry, Factory, Singleton, Strategy) | `itertools`, `functools`, `operator` profonds · **Regex** (`re`, groupes, flags) · Logging pro (stdlib complet) |
| **J4 — Persistance SQL** | **SQL avec `sqlite3`** : DDL/DML, `JOIN`, transactions, `with` connexion · **Injection SQL** et requêtes paramétrées · SQLAlchemy Core (expression language) | SQLAlchemy ORM 2 (déclaratif, relationships, sessions) · Alembic (démo migrations) · **Teaser profiling** (`timeit`, `cProfile`) |
| **J5 — Tests & packaging** | `pytest` : fixtures, `parametrize`, marks, `monkeypatch`, `tmp_path`, `caplog` · Mocking (`unittest.mock`, `spec`, `side_effect`) · `factory_boy` | Packaging moderne : `pyproject.toml`, `uv`, `ruff`, `mypy` · Documentation (docstrings, `mkdocs` démo) · Finalisation fil rouge |

#### Fil rouge — 10 étapes (1 par demi-journée)

| # | Moment | Intitulé | Compétences mobilisées |
|---|---|---|---|
| 01 | J1 matin | **Modèles OO** : `Salle`, `Utilisateur`, `Reservation` | classes, `__init__`, `__repr__`, properties |
| 02 | J1 après-midi | **Hiérarchie de salles** : `SalleReunion`, `SalleFormation`, comparaisons | héritage, surcharge d'opérateurs, Protocol |
| 03 | J2 matin | **Typage complet** des modèles, `mypy --strict` propre | type hints avancés |
| 04 | J2 après-midi | **Validation Pydantic** des entrées utilisateur | dataclasses vs BaseModel, validators, serializers |
| 05 | J3 matin | **Décorateurs métier** : `@log`, `@timer`, `@requires_auth` | décorateurs paramétrés, `functools.wraps` |
| 06 | J3 après-midi | **Registry + regex** pour types de salles et validation de codes | design patterns, `re` |
| 07 | J4 matin | **Persistance SQL directe** : schéma, CRUD, transactions | `sqlite3`, SQL paramétré, injection |
| 08 | J4 après-midi | **Migration vers SQLAlchemy ORM** | ORM 2, relationships, sessions |
| 09 | J5 matin | **Suite de tests** : fixtures, parametrize, mocks, factories | `pytest`, `factory_boy` |
| 10 | J5 après-midi | **Packaging et livrable** : wheel, CLI, README | `pyproject.toml`, `uv build`, `ruff`, `mypy` |

### 7.8 Programme — Intermédiaire 3 jours

**Version compressée, notebooks générés depuis les 5 j via filtrage des tags.**
Sacrifices principaux : descripteurs, SQLAlchemy ORM (on reste en `sqlite3` direct + Core en démo), Alembic, `factory_boy`, property-based testing, regex avancées, `mkdocs`.

**Fil rouge différent :** 📒 **Gestion d'inventaire de matériel informatique** — projet distinct pour les stagiaires qui suivraient les deux formats.

#### Contenu jour par jour

| Jour | Matin | Après-midi |
|---|---|---|
| **J1 — OO & typage** | Classes, héritage, `super()`, MRO · Surcharge d'opérateurs · Protocol/ABC | Type hints modernes · `@dataclass` · Pydantic v2 base |
| **J2 — Décorateurs & SQL** | Décorateurs, context managers · `itertools`/`functools` essentiels · Regex (base) | **SQL avec `sqlite3`** · Injection SQL · SQLAlchemy Core (démo) |
| **J3 — Tests & packaging** | `pytest` (fixtures, parametrize, mocks) · Logging | `pyproject.toml`, `uv`, `ruff`, `mypy` · Finalisation fil rouge |

#### Fil rouge — 6 étapes (1 par demi-journée)

| # | Moment | Intitulé |
|---|---|---|
| 01 | J1 matin | Modèles OO avec héritage (`Ordinateur`, `Imprimante`, `EquipementReseau`) |
| 02 | J1 après-midi | Validation Pydantic des entrées |
| 03 | J2 matin | Décorateurs `@log` et `@validate` |
| 04 | J2 après-midi | Persistance SQL avec `sqlite3` |
| 05 | J3 matin | Tests pytest (fixtures, parametrize) |
| 06 | J3 après-midi | Packaging minimal + CLI + livrable |

### 7.9 Programme — Avancé 5 jours

**Cible :** développeur Python confirmé.
**Objectif :** métaprogrammation, concurrence et asyncio, performance et profiling, sécurité de base, packaging avancé, nouveautés Python 3.14.
**Fil rouge :** 🚀 **Pipeline de données asynchrone** — ingestion depuis API → traitement parallèle → stockage → exposition async, avec profiling mesuré.

#### Contenu jour par jour

| Jour | Matin | Après-midi |
|---|---|---|
| **J1 — Métaprogrammation & internals** | Descripteurs (`__get__`, `__set__`, `__set_name__`) · `__init_subclass__`, class decorators · Métaclasses (`type`, cas ORM) | ABC vs `Protocol` (choix architectural) · `__slots__`, `weakref`, `gc` · Bytecode et `dis` (teaser) · `inspect` |
| **J2 — Concurrence** | `threading`, GIL expliqué · `multiprocessing`, `Pool`, shared memory · `concurrent.futures` (API à privilégier) | Primitives de synchro (`Lock`, `Semaphore`, `Event`, `Queue`) · **PEP 703 free-threaded Python 3.14** · Patterns producer/consumer, fan-out |
| **J3 — Asyncio complet** | Event loop, coroutines, tasks · `async`/`await`, `gather`, `as_completed` · `asyncio.Queue`, `Lock`, `Semaphore` | `httpx` async, `aiohttp` · Structured concurrency (`TaskGroup`, `anyio`) · Backpressure, timeouts, cancellation |
| **J4 — Performance & profiling** | Profiling CPU : `cProfile`, `line_profiler`, `py-spy` · Profiling mémoire : `tracemalloc`, `memray` | Benchmarking rigoureux (`pyperf`) · Optimisation algorithmique et structures · Cython / Numba / `mypyc` (teasers) |
| **J5 — Sécurité, packaging, nouveautés** | **Crypto basiques** : `hashlib` (SHA-256, BLAKE2), `hmac` · Hachage mots de passe (`argon2-cffi`) · Module `secrets` · Chiffrement symétrique (`cryptography.fernet`) | Logs structurés (`structlog`) · Packaging avancé (wheels, `pyproject.toml` complet, publication PyPI/TestPyPI) · **Nouveautés Python 3.11 → 3.14** (PEP 654, 673, 695, 701, 703, 649, 750) · Finalisation fil rouge |

#### Fil rouge — 10 étapes (1 par demi-journée)

| # | Moment | Intitulé | Compétences mobilisées |
|---|---|---|---|
| 01 | J1 matin | **Framework de validation** à base de descripteurs pour les messages | descripteurs, `__set_name__` |
| 02 | J1 après-midi | **Système de plugins** pour les transformers | `__init_subclass__`, registry, ABC |
| 03 | J2 matin | **Ingestion CPU-bound parallélisée** | `ProcessPoolExecutor`, `concurrent.futures` |
| 04 | J2 après-midi | **Batch processing avec shared memory** | `multiprocessing.shared_memory`, `Queue` |
| 05 | J3 matin | **Ingestion async** depuis une API HTTP externe | `asyncio`, `httpx`, coroutines |
| 06 | J3 après-midi | **Pipeline async avec backpressure** | `TaskGroup`, `Semaphore`, `asyncio.Queue` |
| 07 | J4 matin | **Profiling CPU** et identification des goulots | `cProfile`, `py-spy`, flamegraph |
| 08 | J4 après-midi | **Profiling mémoire** et optimisations mesurées | `tracemalloc`, `memray`, benchmarks `pyperf` |
| 09 | J5 matin | **Sécurisation** : hachage, tokens, chiffrement des données sensibles | `hashlib`, `secrets`, `argon2`, `fernet` |
| 10 | J5 après-midi | **Packaging et observabilité** : wheel, `structlog`, README, publication TestPyPI | `structlog`, `pyproject.toml`, `uv build` |

### 7.10 Structure d'un fil rouge sur disque

Chaque fil rouge vit dans `Formations/<format>/Fil_rouge/` et est un **projet Python classique** (pas un notebook) :

```
Formations/Initiation_5j/Fil_rouge/
├── README.md                     # contexte métier, objectifs, livrable final attendu
├── 01_premier_script/
│   ├── ENONCE.md                 # consignes + attendus + critères d'acceptation
│   ├── starter/                  # code de départ avec squelettes et tests
│   │   ├── pyproject.toml
│   │   ├── src/bibliotheque/
│   │   │   └── __init__.py
│   │   └── tests/
│   │       └── test_etape01.py
│   └── solution/                 # projet COMPLET et fonctionnel à ce stade
│       ├── pyproject.toml
│       ├── src/bibliotheque/
│       │   └── __init__.py
│       └── tests/
│           └── test_etape01.py
├── 02_menu_interactif/
│   ├── ENONCE.md
│   ├── starter/
│   └── solution/
├── ...
├── 10_qualite_et_livrable/
│   ├── ENONCE.md
│   └── solution/                 # projet final de référence
└── ressources/                   # CSV, JSON d'exemple, fichiers de test
    ├── livres_exemple.csv
    └── emprunts_exemple.json
```

**Règles :**

- Chaque `solution/` est **cumulative** et **autonome** : le stagiaire peut l'exécuter tel quel (`cd solution && uv run python -m bibliotheque`) et s'en servir de reprise s'il a pris du retard à l'étape suivante.
- Le `starter/` contient les **tests déjà écrits** : le stagiaire sait qu'il a fini quand `pytest` passe au vert.
- Les éléments « à écrire » par le stagiaire sont stubés dans le `starter/` avec `raise NotImplementedError("étape 07 : implémenter ...")`.
- Les CSV/JSON de `ressources/` sont partagés entre toutes les étapes et ne varient pas.

### 7.11 Modèle d'`ENONCE.md` pour une étape

```markdown
# Étape 07 — Organisation en modules

## Contexte
À ce stade, le catalogue de livres fonctionne mais tout est dans un seul
fichier de 200 lignes. Il est temps de découper proprement pour préparer
la persistance (étape 08) et le packaging (étape 09).

## Consignes
1. Créer trois modules dans `src/bibliotheque/` :
   - `catalogue.py` : structure de données + ajout / recherche / suppression
   - `ui.py` : affichage, menu, saisie
   - `__main__.py` : point d'entrée et orchestration
2. Déplacer le code existant dans ces modules sans rien casser.
3. Utiliser des imports **absolus** (`from bibliotheque.catalogue import ...`).
4. Le programme doit pouvoir se lancer avec `python -m bibliotheque`.

## Attendus
- Les trois fichiers existent avec les bonnes responsabilités.
- Aucun import circulaire.
- Les tests de `tests/test_etape07.py` (fournis dans le `starter/`) passent.
- `python -m bibliotheque` affiche le menu interactif comme à l'étape 06.

## Critères d'acceptation
- [ ] `pytest tests/test_etape07.py` est vert.
- [ ] `ruff check src/` ne remonte aucune erreur.
- [ ] Aucun `print` dans `catalogue.py` (réservé à `ui.py`).
- [ ] `catalogue.py` ne connaît pas `ui.py` (dépendance unidirectionnelle).

## Temps estimé
1 h 30

## Solution
Voir `solution/` pour une proposition complète.
**À consulter après tentative personnelle** (au moins 45 minutes de recherche).

## Pièges fréquents
- Oublier l'arborescence `src/` (les imports ne fonctionnent plus).
- Imports circulaires si `catalogue.py` essaie d'afficher des messages.
- `python bibliotheque/` au lieu de `python -m bibliotheque` → `ModuleNotFoundError`.
```

### 7.12 Scripts `tools/`

| Script | Rôle |
|---|---|
| `build_formation.py` | Copie les notebooks depuis `Bibliotheque_notebooks/` vers `Formations/<format>/` selon un manifeste YAML par format. |
| `build_3j.py` | Applique `TagRemovePreprocessor` de nbconvert pour générer les variantes 3 j. Invoqué par `build_formation.py` quand le manifeste est marqué `format: 3j`. |
| `check_notebooks.py` | Exécute chaque notebook (`jupyter nbconvert --execute`), vérifie la syntaxe, lance `ruff` et `mypy` sur le code extrait. Utilisé en CI. |
| `init_fil_rouge.py` | Scaffolde une nouvelle étape de fil rouge avec un `ENONCE.md` prérempli, un `starter/` vide et une `solution/` copiée depuis l'étape précédente. |

#### Exemple de manifeste

```yaml
# tools/manifests/initiation_5j.yaml
format: Initiation_5j
mode: 5j                              # "5j" = copie directe, "3j" = via build_3j
source_root: Bibliotheque_notebooks/Initiation

days:
  - id: J1
    title: Prise en main
    notebooks:
      - 01_Presentation/01_Installation.ipynb
      - 01_Presentation/02_REPL_et_Jupyter.ipynb
      - 02_Syntaxe/01_Variables_et_types.ipynb
      - 02_Syntaxe/02_Conditions_et_boucles.ipynb
  - id: J2
    title: Types de données
    notebooks:
      - 03_Types_de_donnees/01_Nombres.ipynb
      - 03_Types_de_donnees/02_Booleens.ipynb
      - 03_Types_de_donnees/04_Listes.ipynb
      - 03_Types_de_donnees/05_Tuples.ipynb
      - 03_Types_de_donnees/06_Dictionnaires.ipynb
      - 03_Types_de_donnees/07_Ensembles.ipynb
      - 03_Types_de_donnees/03_Chaines.ipynb
      - 03_Types_de_donnees/08_Donnees_temporelles.ipynb
  # ... J3, J4, J5
```

### 7.13 Règles de progressivité stricte

En vigueur depuis 2026-04-14. Le guide complet et les exemples sont dans `tools/conventions_redaction.md`.

1. **Progressivité stricte** — un notebook n'utilise jamais une notion introduite dans un notebook postérieur, y compris dans le code, les exercices, les corrections, les commentaires et les formats d'affichage.

2. **En-tête de prérequis obligatoire** — chaque notebook commence par une cellule markdown listant ce que le stagiaire connaît déjà et ce qu'il n'a pas encore vu. Sert de contrat d'écriture et de rappel.

3. **Une cellule de code = un concept** — pas de gros blocs empilant plusieurs exemples. Un exemple par cellule, ré-exécutable indépendamment. C'est pédagogiquement essentiel pour la mémorisation et le tâtonnement.

4. **Patterns d'affichage selon le niveau** :
   - *Avant `03_Chaines.ipynb`* : `print("Label :", valeur)` et `round(x, 2)` — pas de f-strings.
   - *Après `03_Chaines.ipynb`* : `f"{valeur:.2f}"` et formats f-string complets.

5. **Style d'exercices selon le niveau** :
   - *Avant `04_Fonctions.ipynb`* : exercices en **scripts impératifs**, pas de `def`, pas de type hints, pas de listes / tuples / dicts dans le code utilisateur.
   - *Après `04_Fonctions.ipynb`* : exercices en **fonctions typées** avec `mypy --strict` vert.

6. **Corrections en `<details>` HTML** — dans une cellule markdown, avec ligne vide obligatoire entre `<summary>` et le bloc code. Non-exécutables mais visibles partout (JupyterLab, VS Code, GitHub, HTML exporté). Le stagiaire recopie dans sa propre cellule s'il veut exécuter.

Une **checklist avant commit** est fournie en fin de `conventions_redaction.md` pour valider mécaniquement chaque notebook.

---

## Annexe A — Checklist de modernisation par notebook

À appliquer mécaniquement sur chaque notebook migré :

- [ ] En-tête avec objectifs pédagogiques clairs (markdown).
- [ ] Prérequis listés explicitement.
- [ ] Type hints sur toutes les fonctions (`int | None`, pas `Optional`).
- [ ] `zoneinfo` à la place de `pytz`.
- [ ] `tomllib` à la place de `toml` ou `tomlkit` (lecture).
- [ ] `pathlib.Path` à la place de `os.path`.
- [ ] `match/case` où pertinent.
- [ ] `except*` et `ExceptionGroup` mentionnés si pertinent.
- [ ] f-strings avec `{x=}` pour le debug.
- [ ] `import numpy as np`, `import matplotlib.pyplot as plt`.
- [ ] Mention `pytest` en parallèle de `unittest`.
- [ ] Pydantic v2 APIs (`model_validate`, pas `parse_obj`).
- [ ] Ratio markdown/code tendu vers 50/50 au moins.
- [ ] 3 à 5 exercices gradués à la fin.
- [ ] Ressources externes en fin de notebook (doc officielle, PEPs).
- [ ] Testé sur Python 3.14 à l'exécution.

## Annexe B — Bibliothèques externes à recommander (par défaut)

| Catégorie | Recommandation | Alternative(s) |
|---|---|---|
| Package manager | **`uv`** | pip, poetry, pdm |
| Linter/formatter | **`ruff`** | black, isort, flake8, pylint |
| Type checker | **`mypy`** | pyright, pyre |
| Test runner | **`pytest`** | unittest (stdlib) |
| Property testing | **`hypothesis`** | — |
| HTTP client | **`httpx`** | requests |
| Validation | **`pydantic` v2** | attrs, msgspec, cattrs |
| CLI | **`typer`** | argparse, click |
| TUI | **`rich`** / **`textual`** | prompt_toolkit |
| Dates | **`whenever`** | arrow, pendulum, dateutil |
| ORM | **`SQLAlchemy` 2** | SQLModel, Peewee |
| Migrations | **`Alembic`** | — |
| Web framework | **`FastAPI`** | Flask, Django, Starlette |
| Templates | **`Jinja2`** | — |
| Logging | **stdlib `logging`** | loguru, structlog |
| Task scheduling | **`apscheduler`** | schedule, celery |
| Async HTTP | **`httpx`** / **`aiohttp`** | — |
| DataFrame | **`polars`** ou **`pandas`** | — |
| Viz | **`matplotlib`** (OO) | seaborn, plotly, altair |
| Excel | **`openpyxl`** (read/write) / **`xlsxwriter`** (write) | — |
| Word | **`python-docx`** | — |
| PDF gen | **`reportlab`** | weasyprint (HTML→PDF) |
| PDF read | **`pymupdf`** (fitz) | pypdf, pdfplumber |
| Images | **`Pillow`** | OpenCV, scikit-image |
| Crypto | **`cryptography`** | pynacl |
| Passwords | **`argon2-cffi`** | bcrypt, passlib |
| JWT | **`pyjwt`** | authlib |

---

*Fin du document — à faire évoluer au fil de la refonte.*
