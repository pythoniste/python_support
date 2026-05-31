# Décisions techniques et pédagogiques — Cours Avancé 5 j

Ce document trace les arbitrages structurants du cours Avancé. Il complète
`tools/conventions_redaction.md` (qui décrit le style) et la section 7.9 de
`EVALUATION_ET_PLAN.md` (qui décrit le programme).

## 1. Public et positionnement

Le cours Avancé s'adresse à des développeurs Python **confirmés** qui ont déjà
suivi l'Intermédiaire ou possèdent une expérience équivalente. Toutes les
notions de l'Intermédiaire sont considérées comme acquises : modèle objet,
type hints modernes, dataclasses, décorateurs, contexts managers, tests,
packaging, logging, SQL, regex. Les notebooks peuvent donc utiliser librement
fonctions typées, classes, décorateurs, etc., et se concentrer sur le
contenu pointu.

## 2. Métaclasses et descripteurs en J1 (pas en Intermédiaire)

Les descripteurs et surtout les métaclasses sont puissants mais dangereux. Ils
ont été volontairement **sortis** du cours Intermédiaire :

- En Intermédiaire, on enseigne `@dataclass`, `@property`, `__init_subclass__`
  et les décorateurs de classe — qui couvrent 95 % des besoins réels.
- En Avancé, on montre **comment ça marche dessous** (descripteur data vs
  non-data, résolution d'attribut, `__set_name__`) et **quand** la
  métaprogrammation lourde se justifie (ORM SQLAlchemy, ABC, frameworks).
- Le message est explicite : *« préférez `__init_subclass__` ou un décorateur
  de classe ; la métaclasse est un dernier recours »*.

## 3. Free-threaded Python (PEP 703) traité en détail

À l'horizon Python 3.14, le GIL devient **optionnel**. Nous avons choisi de
consacrer un notebook entier (J2) à la PEP 703 pour trois raisons :

1. **C'est un changement d'architecture** pour la communauté : le passage de
   « officiellement expérimental » (3.13) à « officiellement supporté » (3.14).
2. Les stagiaires confirmés **doivent savoir mesurer** ce que le free-threaded
   apporte (ou n'apporte pas) à leur charge de travail avant de l'adopter.
3. Le GIL est le premier sujet cité en entretien pour « performance Python » :
   il faut pouvoir en parler avec précision, pas avec des mythes.

Le notebook explique le build `--disable-gil`, la compatibilité des C
extensions, les implications sur `threading` et `multiprocessing`, et
surtout **comment profiler** pour savoir si migrer en vaut la peine.

## 4. Asyncio de référence, `anyio` mentionné, `trio` teasé

Nous avons tranché contre un cours `trio` pur pour les raisons suivantes :

- **`asyncio` est la stdlib**, tous les projets professionnels y sont exposés.
  Il serait contre-productif d'enseigner une API alternative en premier.
- **`asyncio.TaskGroup` (PEP 654, 3.11+)** apporte la structured concurrency
  directement dans la stdlib. La valeur ajoutée de `trio` sur ce point est
  très réduite en 3.11+.
- **`anyio`** est présenté comme le pont : mêmes primitives au-dessus d'asyncio
  ou de trio, API plus propre que asyncio stdlib. Idéal pour une bibliothèque
  qui veut rester neutre (httpx, FastAPI, Starlette l'utilisent).
- `trio` est cité en ressources pour la culture générale mais n'est pas
  enseigné en profondeur.

## 5. Profiling : `tracemalloc` stdlib et `py-spy` en prod

### Mémoire : `tracemalloc` plutôt que `guppy3`/`pympler`

- `tracemalloc` est **dans la stdlib** depuis 3.4 : aucune dépendance, aucun
  souci d'installation, intégration immédiate.
- `guppy3` est puissant mais son API est datée et son installation fragile
  sur les Python récents.
- Pour un profiling plus fin (allocations C, flamegraph mémoire), on
  recommande `memray` (Bloomberg) qui devient le standard de fait en 2024+.

### CPU : `cProfile` + `py-spy` en prod

- `cProfile` (stdlib) reste le point d'entrée pour profiler un script.
- `line_profiler` pour descendre à la ligne (requiert `@profile`).
- **`py-spy`** est le standard pour la prod : **sampling profiler**,
  attachable à un process en cours, **sans modifier le code ni installer la
  lib dans le venv cible**. C'est le bon outil pour profiler un service
  Django/FastAPI en production sans le redémarrer.

## 6. Sécurité : `cryptography` et Argon2

### `cryptography` plutôt que `pycrypto` / `pycryptodome`

- `pycrypto` est **mort** depuis 2014. À ne plus jamais utiliser.
- `pycryptodome` est un fork maintenu mais l'écosystème Python se consolide
  autour de `cryptography` (pyca/cryptography) :
  - API **haut niveau** (`Fernet`) et **bas niveau** (hazmat) séparées,
  - audit de sécurité régulier,
  - backend Rust performant et sûr.
- Nous enseignons `Fernet` pour le symétrique, et mentionnons les primitives
  RSA/AES « hazmat » en teaser.

### Argon2id plutôt que bcrypt ou PBKDF2

- **Argon2id** est le vainqueur du *Password Hashing Competition* (2015).
- Résistant aux attaques GPU et ASIC, paramétrable en mémoire et en temps.
- `argon2-cffi` est la bibliothèque Python de référence.
- `bcrypt` reste acceptable mais est mentionné comme « legacy » : les
  nouveaux projets doivent utiliser Argon2id.
- SHA-1 et MD5 ne sont présentés **que** pour comparaison historique et
  interopérabilité (ex. lecture d'anciens fichiers).

## 7. Nouveautés 3.11 → 3.14 jugées critiques

Le notebook `06_Packaging_avance_et_nouveautes/03_Nouveautes_3_11_a_3_14.ipynb`
couvre ces PEPs parce qu'elles changent concrètement la façon d'écrire du
code :

| PEP | Version | Impact direct |
|---|---|---|
| 654 — Exception Groups | 3.11 | `TaskGroup`, `except*`, gestion d'erreurs concurrentes |
| 673 — `Self` | 3.11 | Type hints corrects pour chaînes fluentes et builders |
| 695 — Generic Syntax | 3.12 | `def f[T](...)` au lieu de `TypeVar` boilerplate |
| 701 — f-strings flexibles | 3.12 | Plus de restrictions de quoting, backslashes autorisés |
| 703 — Free-threaded | 3.13 exp → 3.14 officiel | GIL optionnel, parallélisme réel |
| 709 — Comprehensions inlinées | 3.12 | Gain de perf automatique |
| 649 — Lazy annotations | 3.14 | Fin de `from __future__ import annotations` |
| 750 — t-strings | 3.14 | Template strings typées pour i18n / templating sûr |
| 779 — GIL rendu officiellement optionnel | 3.14 | Consolidation de la 703 |

D'autres PEPs (657 fine-grained errors, 710 explicit deps) sont mentionnées
en passant mais ne reçoivent pas de section dédiée.

## 8. Taille des notebooks et arbitrages

Cible : **100-180 cellules** par notebook, plus que l'Intermédiaire, car à ce
niveau la densité conceptuelle est élevée et chaque exemple doit être montré
complètement (sans forward reference, mais avec toute la nuance).

Les tags `deep-dive`, `skip-3j` et `bonus` sont utilisés à bon escient pour
permettre de resserrer en 3 j (mais l'Avancé n'a pas de version 3 j officielle
— les tags servent à proposer des parcours d'approfondissement à la maison).

## 9. Ce qu'on n'enseigne **pas** (et pourquoi)

- **Django / Flask / FastAPI** : cours dédiés, pas dans le socle Avancé.
- **Machine learning / data science avancée** : vus en Intermédiaire avec
  NumPy / Pandas / Polars ; un cours spécifique est disponible.
- **Rust bindings (PyO3)** : trop spécifique, mentionné en ressources.
- **`trio` en profondeur** : voir section 4.
- **`nogil` hack historique** : remplacé par la PEP 703.

---

*Document à jour pour Python 3.14 (2026).*
