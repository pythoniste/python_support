# Plateforme `notebooks.inspyration.net` — Document de conception

> Document de travail — source unique de vérité pour l'implémentation de la plateforme de suivi et de notation des exercices Python.
> Dernière mise à jour : 2026-04-14
> Statut : **spécification validée**, à implémenter (Piste B)

---

## Table des matières

1. [Contexte et objectifs](#1-contexte-et-objectifs)
2. [Décisions validées](#2-décisions-validées)
3. [Architecture générale](#3-architecture-générale)
4. [Flux utilisateur](#4-flux-utilisateur)
5. [Modèle de données](#5-modèle-de-données)
6. [API — surface complète](#6-api--surface-complète)
7. [Format de rubrique](#7-format-de-rubrique)
8. [Calcul des notes](#8-calcul-des-notes)
9. [Authentification et autorisation](#9-authentification-et-autorisation)
10. [Rétention des données](#10-rétention-des-données)
11. [Mode hors ligne](#11-mode-hors-ligne)
12. [Hébergement Ikoula](#12-hébergement-ikoula)
13. [Sécurité et vie privée](#13-sécurité-et-vie-privée)
14. [Plan de réalisation phasé](#14-plan-de-réalisation-phasé)

---

## 1. Contexte et objectifs

Les notebooks Python de `python_support` sont utilisés en formation professionnelle et en école d'ingénieurs. Le formateur a besoin :

- de **suivre en temps réel** l'avancement de chaque stagiaire sur les exercices ;
- de **noter automatiquement** les exercices selon des rubriques définies, avec pondération, pour les élèves ingénieurs qui doivent recevoir une note finale ;
- de **verrouiller la correction** de chaque exercice : un stagiaire ne voit la solution que s'il a produit lui-même un code qui passe les tests.

Les contraintes de terrain sont particulières :

- **Le formateur n'a pas accès au réseau du client**. Il utilise souvent son téléphone en hotspot 4G. Tout doit donc passer par Internet.
- **Les stagiaires ont leurs propres PC**, connectés via la connexion de leur choix (WiFi entreprise, 4G, etc.).
- **Pas de LAN commun garanti** entre formateur et stagiaires.

La solution est une **application web publique** à l'URL fixe `https://notebooks.inspyration.net`, accessible depuis n'importe quelle connexion, et référencée en dur dans le module helper côté stagiaire.

## 2. Décisions validées

| # | Point | Décision |
|---|---|---|
| 1 | DNS et hébergement | `notebooks.inspyration.net` chez **Ikoula** (DNS déjà réservé) |
| 2 | Rubriques de notation | **Hybride** : YAML par défaut dans le repo, override possible côté formateur (stocké en DB) |
| 3 | Auth formateur | **OAuth GitHub et GitLab uniquement**. Pas de mot de passe maison. |
| 4 | Multi-formateurs | **Oui, à terme**. RBAC léger dès le départ (rôles `trainer`, `admin`). |
| 5 | Export des notes | **CSV et PDF**, les deux |
| 6 | Rétention | **Variable par année d'études** : 1ère année → 3 ans, 3ème année → 1 an. Purge quotidienne automatique. |
| 7 | Mode hors ligne | **Buffer local** JSONL dans `~/.python_support/buffer.jsonl`, réémis quand la connexion revient |
| 8 | Pseudonymat | **Optionnel** : le stagiaire peut saisir un pseudonyme dans `00_Configuration.ipynb` |
| 9 | Licence | **Propriétaire** pour l'instant, repo privé |

## 3. Architecture générale

```
┌──────────────────────────────────┐              ┌────────────────────────────────┐
│  Stagiaire                        │   HTTPS     │  notebooks.inspyration.net      │
│                                   │    443      │                                 │
│  JupyterLab                       │ ─────────►  │  Reverse proxy : Caddy          │
│  00_Configuration.ipynb           │             │  + Let's Encrypt auto           │
│  → configurer(nom, session)       │             │                                 │
│  Tous les autres notebooks        │             │  App : FastAPI + Uvicorn        │
│  → verifier_et_reveler()          │             │  DB  : SQLite (PostgreSQL       │
│                                   │             │         plus tard si besoin)    │
│  ~/.python_support/config.json    │             │                                 │
│  ~/.python_support/buffer.jsonl   │             │  Temps réel : Server-Sent       │
└──────────────────────────────────┘              │                Events (SSE)    │
                                                   │                                 │
                                                   │  Auth : OAuth2 GitHub/GitLab    │
                                                   │                                 │
                                                   └────────────────────────────────┘
                                                                  ▲
                                                                  │
                                                                  │ HTTPS
                                                                  │
                                                     ┌────────────┴───────────────┐
                                                     │  Formateur                  │
                                                     │  navigateur web             │
                                                     │  /trainer/sessions/{id}     │
                                                     │  (grille temps réel)        │
                                                     └─────────────────────────────┘
```

### Stack technique validée

| Couche | Technologie | Raison |
|---|---|---|
| Reverse proxy | **Caddy** | TLS Let's Encrypt automatique, config 5 lignes |
| Backend | **FastAPI + Uvicorn** | Moderne, async natif, SSE facile, OpenAPI auto |
| DB | **SQLite** | Zéro infra, 1000 événements/session → largement suffisant |
| Templates | **Jinja2 + htmx** | SPA-like sans bundler, maintenance minimale |
| Auth | **Authlib** pour OAuth2 | Client GitHub et GitLab, bien maintenu |
| PDF | **WeasyPrint** | HTML → PDF propre, cohérent avec les side tracks |
| Tests | **pytest** | Cohérent avec le reste du repo |

## 4. Flux utilisateur

### 4.1 Formateur — création de session

1. Le formateur ouvre `https://notebooks.inspyration.net/trainer/login`.
2. Il se connecte via GitHub ou GitLab (OAuth).
3. À la première connexion, un compte `Trainer` est créé automatiquement avec son nom et son avatar récupérés de l'API du provider.
4. Il crée une session via `/trainer/sessions/new` :
   - Intitulé : « Initiation Python — IUT Lyon mars 2026 »
   - Formation : `Initiation_5j` (sélection dans une liste)
   - Rubrique : `initiation_5j.yaml` (par défaut) ou upload d'un YAML custom
   - Dates : 2026-03-17 au 2026-03-21
   - Mode d'inscription : auto-déclaration (par défaut) ou liste fermée
   - Année d'études des stagiaires : 1 / 2 / 3 / 4 / 5 (détermine la rétention)
5. Le serveur génère un **code session lisible** : `INIT-17MAR-K3F9` (format `<FORMATION>-<DATE>-<4 chars>`).
6. Le formateur **communique ce code** aux stagiaires (SMS, tableau, slide).

### 4.2 Stagiaire — inscription et configuration

1. Le stagiaire télécharge et décompresse son package de formation (`Formations/Initiation_5j/`).
2. Il ouvre JupyterLab sur son PC.
3. Il ouvre **`00_Configuration.ipynb`** à la racine.
4. Il exécute la cellule unique de configuration :
   ```python
   from utils_pedagogie import configurer
   configurer(
       nom="Jean Dupont",         # ou pseudonyme
       session="INIT-17MAR-K3F9",
   )
   ```
5. Le helper POSTe `{nom, session}` au serveur, reçoit un `token` stagiaire unique, et l'enregistre dans `~/.python_support/config.json`.
6. À partir de ce moment, **tous les notebooks** de la formation auto-chargent cette configuration au premier `import utils_pedagogie`.

### 4.3 Stagiaire — exercice

1. Le stagiaire écrit son code dans une cellule.
2. Il exécute une cellule de vérification :
   ```python
   def _tests():
       assert round(fahrenheit, 2) == round(celsius * 9 / 5 + 32, 2)
   verifier_et_reveler(notebook="01_Nombres", exercice=1, tests=_tests)
   ```
3. Le helper :
   - exécute `_tests()` dans le namespace du kernel (qui voit les variables du stagiaire) ;
   - POSTe au serveur un événement `{token, notebook, exercice, status, tentatives, timestamp}` ;
   - si `_tests()` passe : affiche un message de réussite + révèle la correction (cellule Markdown générée par `IPython.display.display`) ;
   - si `_tests()` échoue : affiche le message d'erreur court, **ne révèle pas** la correction.

### 4.4 Formateur — suivi temps réel

1. Le formateur a ouvert `/trainer/sessions/{id}` dans son navigateur.
2. La page souscrit à un endpoint **SSE** `/trainer/sessions/{id}/stream`.
3. Chaque événement POST par un stagiaire déclenche un push SSE qui met à jour la grille HTML (via htmx).
4. Le formateur voit en temps réel qui avance, qui bloque, qui a fini.
5. En fin de session, il bascule sur `/trainer/sessions/{id}/grades` pour **valider les notes**, éventuellement ajouter des commentaires ou override manuel, et **exporter en CSV ou PDF**.

## 5. Modèle de données

```
Trainer
├── id (PK)
├── provider (github | gitlab)
├── provider_id (identifiant chez le provider)
├── email
├── nom
├── avatar_url
├── role (trainer | admin)
└── created_at

Session
├── id (PK)
├── code (unique, ex. "INIT-17MAR-K3F9")
├── trainer_id (FK → Trainer)
├── intitule
├── formation (enum : Initiation_5j, Initiation_3j, …)
├── rubrique_id (FK → Rubrique, nullable si YAML par défaut)
├── debut
├── fin
├── active (bool)
├── annee_etudes (1 à 5)
├── mode_inscription (auto | liste_fermee)
└── created_at

Student
├── id (PK)
├── session_id (FK → Session)
├── nom
├── token (unique, signé)
├── annee_sortie_prevue (calculé : année en cours + (5 - annee_etudes))
├── purge_after (calculé à partir de annee_sortie_prevue)
└── joined_at

Rubrique
├── id (PK)
├── formation (enum)
├── source (default_yaml | custom_upload)
├── trainer_id (nullable, si custom)
├── contenu (JSON sérialisé depuis le YAML)
└── created_at

Event
├── id (PK)
├── student_id (FK → Student)
├── notebook (str, ex. "01_Nombres")
├── exercice (int)
├── status (enum : attempt | failure | success)
├── tentatives (int)
├── message (str, tronqué à 200 chars, nullable)
├── criteres_reussis (JSON : {critere_id: bool})
└── timestamp

Grade
├── id (PK)
├── student_id (FK → Student)
├── notebook
├── exercice
├── score_auto (float, calculé automatiquement)
├── score_manuel (float, override formateur, nullable)
├── score_final (float, = manuel si défini sinon auto)
├── commentaire (str, nullable)
├── graded_by (FK → Trainer, nullable)
└── graded_at (nullable)
```

**Index :**
- `Session.code` unique
- `Student.token` unique
- `Event(student_id, notebook, exercice)` composite pour requêtes rapides de dashboard
- `Student.purge_after` pour la tâche de purge

## 6. API — surface complète

### 6.1 Endpoints publics (stagiaire)

| Méthode | URL | Description |
|---|---|---|
| `GET`  | `/api/health` | Ping, renvoie `{"ok": true, "version": "..."}` |
| `POST` | `/api/sessions/{code}/join` | Inscrit un stagiaire. Body : `{"nom": "..."}`. Retour : `{"token": "...", "student_id": N}`. |
| `POST` | `/api/events` | Envoi d'un événement d'exercice. Header : `X-Student-Token`. Body : voir 6.3. |
| `GET`  | `/api/rubriques/{formation}` | Renvoie la rubrique officielle YAML du format. |

### 6.2 Endpoints formateur (authentifiés via OAuth)

| Méthode | URL | Description |
|---|---|---|
| `GET`  | `/trainer/login` | Page de login avec boutons GitHub / GitLab |
| `GET`  | `/trainer/callback/{provider}` | Callback OAuth |
| `GET`  | `/trainer/logout` | Déconnexion |
| `GET`  | `/trainer/` | Liste des sessions de ce formateur |
| `GET`  | `/trainer/sessions/new` | Formulaire de création |
| `POST` | `/trainer/sessions` | Création effective |
| `GET`  | `/trainer/sessions/{id}` | Tableau de bord temps réel |
| `GET`  | `/trainer/sessions/{id}/stream` | Flux SSE (événements live) |
| `GET`  | `/trainer/sessions/{id}/students` | Liste des stagiaires inscrits |
| `GET`  | `/trainer/sessions/{id}/student/{sid}` | Détail d'un stagiaire (chronologie) |
| `GET`  | `/trainer/sessions/{id}/grades` | Grille de notation |
| `POST` | `/trainer/sessions/{id}/grades/{gid}` | Override manuel d'une note |
| `GET`  | `/trainer/sessions/{id}/export.csv` | Export CSV des notes |
| `GET`  | `/trainer/sessions/{id}/export.pdf` | Export PDF des notes |
| `POST` | `/trainer/sessions/{id}/rubrique` | Upload d'une rubrique custom |
| `POST` | `/trainer/sessions/{id}/close` | Fermeture de session (désactive les events) |

### 6.3 Format de l'événement POST `/api/events`

```json
{
  "notebook": "01_Nombres",
  "exercice": 3,
  "status": "success",
  "tentatives": 2,
  "message": null,
  "criteres_reussis": {
    "execute_sans_erreur": true,
    "c_vers_f_correct": true,
    "f_vers_c_correct": true
  },
  "timestamp": "2026-04-14T14:30:00Z"
}
```

**Contraintes :**
- `status` ∈ `{"attempt", "failure", "success"}`
- `message` tronqué côté client à 200 caractères max
- `criteres_reussis` est optionnel (présent quand le helper applique la rubrique)
- `timestamp` toujours UTC ISO 8601

**Rate limiting :** 60 événements par minute par `token` (largement au-dessus de l'usage normal qui est de 1-2/minute max).

## 7. Format de rubrique

Fichier YAML, un par formation, livré avec le repo dans `tools/rubriques/`.

```yaml
# tools/rubriques/initiation_5j.yaml
formation: Initiation_5j
bareme_total: 20        # note sur 20 /20
description: |
  Rubrique officielle de la formation Initiation Python 5 jours.
  Chaque exercice contribue à la note finale selon sa pondération.

exercices:
  - notebook: 01_Nombres
    numero: 1
    titre: Conversion de température
    ponderation: 1.0
    criteres:
      - id: execute_sans_erreur
        label: Le code s'exécute sans erreur
        ponderation: 0.2
        auto: true
      - id: c_vers_f_correct
        label: celsius → fahrenheit donne le bon résultat
        ponderation: 0.4
        auto: true
      - id: f_vers_c_correct
        label: fahrenheit → celsius donne le bon résultat
        ponderation: 0.4
        auto: true

  - notebook: 01_Nombres
    numero: 2
    titre: Aire et périmètre d'un cercle
    ponderation: 1.0
    criteres:
      - id: aire_correcte
        ponderation: 0.4
        auto: true
      - id: perimetre_correct
        ponderation: 0.4
        auto: true
      - id: arrondi_deux_decimales
        label: Utilise round(..., 2)
        ponderation: 0.2
        auto: true

  - notebook: 01_Nombres
    numero: 3
    titre: Pièges IEEE 754 en pratique
    ponderation: 1.5     # pondéré plus fort car pédagogiquement crucial
    criteres:
      - id: boucle_correcte
        label: La boucle ajoute bien 0.1 dix fois
        ponderation: 0.4
        auto: true
      - id: utilise_isclose
        label: Compare avec math.isclose plutôt qu'avec ==
        ponderation: 0.6
        auto: true

  # … tous les exercices de tous les notebooks
```

## 8. Calcul des notes

### 8.1 Formule

Pour chaque **exercice** :

```
score_exercice = Σ (ponderation_critere × reussite_critere) / Σ ponderation_critere
```

avec `reussite_critere ∈ {0.0, 1.0}` pour les critères auto, éventuellement une valeur `[0.0, 1.0]` pour les critères manuels override.

Pour chaque **stagiaire**, sur l'ensemble de la formation :

```
score_global = Σ (ponderation_exercice × score_exercice) / Σ ponderation_exercice
note_finale  = score_global × bareme_total
```

### 8.2 Exemple

Soit un stagiaire qui a réussi 5 exercices sur 6 dans `01_Nombres`, avec les pondérations 1.0 / 1.0 / 1.5 / 1.0 / 2.0 / 2.0. Il rate l'exercice 4 (pondération 1.0).

```
score_global = (1.0×1 + 1.0×1 + 1.5×1 + 1.0×0 + 2.0×1 + 2.0×1) / (1.0+1.0+1.5+1.0+2.0+2.0)
             = 7.5 / 8.5
             = 0.882
note_finale  = 0.882 × 20 = 17.6/20
```

### 8.3 Override manuel

Le formateur peut pour chaque `Grade` :
- définir `score_manuel` (qui remplace `score_auto` dans `score_final`) ;
- ajouter un `commentaire` ;
- marquer `graded_at` et `graded_by`.

L'override n'efface **jamais** `score_auto` — on garde la trace.

## 9. Authentification et autorisation

### 9.1 Côté formateur

**OAuth 2.0 via Authlib** avec deux providers :

- **GitHub** : scopes `read:user user:email`
- **GitLab** : scopes `read_user email`

Flow standard *authorization code* :

1. Clic « Se connecter avec GitHub » → redirige vers GitHub OAuth.
2. L'utilisateur accepte → callback `/trainer/callback/github?code=...`.
3. Le serveur échange le `code` contre un `access_token`.
4. Il récupère `/user` et `/user/emails`.
5. `Trainer` créé ou retrouvé par `(provider, provider_id)`.
6. Session de navigateur : cookie signé httpOnly + secure + samesite=lax.

**Rôles :**
- `trainer` (par défaut) : peut créer des sessions, voir uniquement les siennes
- `admin` (manuel en DB) : peut voir toutes les sessions, purger, gérer les rubriques globales

### 9.2 Côté stagiaire

**Jeton opaque** généré à l'inscription :

- 32 bytes aléatoires, base64 url-safe.
- Stocké en clair en DB (pas sensible, juste un identifiant de session)
- Stocké dans `~/.python_support/config.json` côté client.
- Passé en header `X-Student-Token` sur chaque appel `/api/events`.
- Invalide automatiquement quand la `Session` est fermée ou purgée.

Pas de mot de passe, pas de lien email, pas de compte persistant. Le stagiaire est lié à **une session spécifique** et rien d'autre.

## 10. Rétention des données

### 10.1 Politique

| Année d'études au début de la formation | Rétention à partir de la date de formation |
|---|---|
| 1ère année | **3 ans** |
| 2ème année | **2 ans** |
| 3ème année | **1 an** |
| 4ème année | **1 an** |
| 5ème année | **1 an** |
| Formation continue (non école) | **1 an** par défaut, configurable |

Formule générale :
```
rétention = max(1, 4 - annee_etudes)   # en années, borné à 1 min
purge_after = date_formation + rétention
```

### 10.2 Purge automatique

Une tâche **quotidienne** (`apscheduler` intégré dans l'app, ou cron système) :

1. Sélectionne les `Student` où `purge_after < now`.
2. Supprime les `Event` et `Grade` associés.
3. Anonymise le `Student` : `nom → "ANONYMISÉ-#{id}"`, `token → null`.
4. Conserve les **statistiques agrégées** (nombre d'exos réussis, note finale) pour analytique globale.
5. Log de la purge dans un fichier séparé pour audit.

## 11. Mode hors ligne

Si la connexion Internet tombe en pleine formation, le helper stagiaire doit continuer de fonctionner.

### 11.1 Buffer local

- Chaque événement qui échoue à être envoyé est écrit dans `~/.python_support/buffer.jsonl` (une ligne JSON par événement).
- À chaque nouvel appel `verifier_et_reveler(...)`, le helper tente d'abord de flusher le buffer (max 100 événements par tentative).
- Si le flush échoue, on écrit le nouvel événement en fin de buffer et on continue localement.
- **La révélation de la correction ne dépend PAS du serveur** — elle est locale, basée sur le résultat de `_tests()`. Le serveur sert uniquement au suivi et à la notation formateur.

### 11.2 Indicateur visuel

À chaque appel, le helper affiche discrètement :
- `🟢 Envoyé` si le POST a réussi
- `🟡 En attente (N événements bufferisés)` sinon

Le stagiaire sait ainsi que ses progrès sont pris en compte même s'il a perdu la connexion.

## 12. Hébergement Ikoula

### 12.1 Configuration

- **VPS Ikoula Cloud** entry (2 vCPU, 4 Go RAM, 40 Go SSD — ~10 €/mois).
- **OS** : Debian 13 (Trixie) pour Python 3.14 disponible via backports ou pyenv.
- **Domaine** : `notebooks.inspyration.net` → A record vers l'IP du VPS.
- **TLS** : Let's Encrypt via Caddy (renouvellement auto).

### 12.2 Stack de déploiement

```
/opt/notebooks-plateforme/
├── app/                         # code FastAPI
├── venv/                        # python -m venv
├── db/
│   └── notebooks.sqlite
├── logs/
│   ├── access.log
│   ├── error.log
│   └── purge.log
└── backups/
    └── notebooks-YYYY-MM-DD.sqlite.gz
```

**Systemd unit** `notebooks-plateforme.service` :

```ini
[Unit]
Description=Notebooks Inspyration plateforme
After=network.target

[Service]
Type=simple
User=notebooks
WorkingDirectory=/opt/notebooks-plateforme
Environment="PATH=/opt/notebooks-plateforme/venv/bin"
ExecStart=/opt/notebooks-plateforme/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Caddyfile** :

```
notebooks.inspyration.net {
    reverse_proxy localhost:8000
    encode gzip
    log {
        output file /var/log/caddy/notebooks.log
    }
}
```

### 12.3 Sauvegardes

- **Snapshot SQLite** quotidien via cron : `sqlite3 db/notebooks.sqlite ".backup 'backups/notebooks-$(date +%F).sqlite'"` puis `gzip`.
- **Rétention** : 30 jours locaux + copie chiffrée vers un bucket S3-compatible chez Ikoula (Ikoula Object Storage).
- **Test de restauration** mensuel (script qui restaure dans un docker throwaway et vérifie).

### 12.4 Monitoring

- **Uptimerobot** gratuit pour ping / 5 min sur `/api/health`.
- **Logs Caddy** + logs app avec rotation `logrotate`.
- Alerte mail si le service redémarre plus de 3 fois en 10 min (via systemd `OnFailure`).

## 13. Sécurité et vie privée

### 13.1 Ce qui est envoyé

| Donnée | Envoyée ? | Stockée ? |
|---|---|---|
| Nom ou pseudonyme du stagiaire | ✅ | ✅ (purgée selon politique) |
| Nom du notebook, numéro d'exercice | ✅ | ✅ |
| Statut (attempt/failure/success) | ✅ | ✅ |
| Nombre de tentatives | ✅ | ✅ |
| Horodatage | ✅ | ✅ |
| Message d'assertion (tronqué 200 chars) | ✅ | ✅ |
| **Code source du stagiaire** | ❌ **JAMAIS** | ❌ |
| Variables, outputs, résultats de calcul | ❌ **JAMAIS** | ❌ |
| Configuration système, IP publique | ❌ | ❌ |

### 13.2 Affichage dans `00_Configuration.ipynb`

Cette cellule markdown est **obligatoire** dans le notebook de configuration :

> **Ce que nous suivons**
>
> Quand vous exécutez un exercice avec `verifier_et_reveler`, nous envoyons au formateur :
> votre nom (ou pseudonyme), le nom du notebook, le numéro de l'exercice, si vous avez réussi,
> le nombre de tentatives, la date et l'heure.
>
> **Nous n'envoyons jamais** votre code, vos outputs, ou le contenu de vos cellules.
>
> Vous pouvez utiliser un pseudonyme (`configurer(nom="Anonyme-42", ...)`) si vous préférez.
> Vos données sont conservées pendant [N] mois après la fin de la formation, puis supprimées.

### 13.3 Sécurité applicative

- HTTPS obligatoire (redirect 443 → 443).
- Cookies formateur : `HttpOnly`, `Secure`, `SameSite=Lax`.
- CSRF protection sur toutes les actions formateur (token par session).
- Rate limit : 60 events/min par stagiaire, 1000 req/min par IP.
- Validation Pydantic stricte sur tous les inputs API.
- Pas de `exec` / `eval` côté serveur sur du contenu stagiaire.
- Audit log séparé pour les actions `admin` et les purges.

### 13.4 RGPD

- **Finalité** explicite (suivi pédagogique + notation) documentée dans `00_Configuration.ipynb`.
- **Droit d'accès** : `GET /api/students/{token}/data` renvoie tout ce qui est stocké pour un stagiaire.
- **Droit de suppression** : `DELETE /api/students/{token}` supprime immédiatement toutes les traces.
- **Durée de conservation** : documentée, appliquée automatiquement.
- **Sous-traitance** : Ikoula hébergeur (France), pas d'autres transferts.

## 14. Plan de réalisation phasé

| Phase | Livrables | Durée | Bloquant suivant |
|---|---|---|---|
| **B1** | `utils_pedagogie.py` local uniquement : `configurer` (mode solo), `verifier_et_reveler` (pas de POST), lecture YAML rubriques. Pas de serveur. | 1-2 j | — |
| **B2** | Backend FastAPI minimal : schéma DB, endpoints `/api/health`, `/api/sessions/{code}/join`, `/api/events`. Pas d'auth formateur encore. Tests `curl`. | 2-3 j | B1 (pour tester end-to-end) |
| **B3** | OAuth GitHub + GitLab, modèle `Trainer`, login/logout, liste sessions | 2 j | B2 |
| **B4** | Frontend formateur : création session, dashboard SSE, htmx | 2-3 j | B3 |
| **B5** | Parsing rubriques YAML, calcul des notes, écran de notation, override, export CSV + PDF | 2 j | B4 |
| **B6** | Mode hors ligne côté client : buffer JSONL, flush automatique, indicateur visuel | 1 j | B1 |
| **B7** | Purge automatique, audit log, endpoints RGPD (accès, suppression) | 1 j | B5 |
| **B8** | Déploiement Ikoula : VPS, Caddy, systemd, sauvegardes, monitoring | 1-2 j | B7 |
| **B9** | Polish : rate limiting, tests de charge, doc, CI/CD | 1-2 j | B8 |

**Total estimé Piste B : 13-18 jours** de développement à temps plein (un développeur).

**Piste A (pédagogie)** tourne **en parallèle** et est indépendante — elle n'a besoin que de B1 (helper local) pour fonctionner en mode solo.

**Ordre recommandé** :
1. Piste A tâches 1-3 (refonte `01_Nombres`, conventions, règles) → utilisable immédiatement.
2. B1 (helper local) → Piste A complète.
3. Scaffolding de `12_Calcul_numerique_et_donnees/` → nouveaux notebooks.
4. B2 → B9 (plateforme) → mise en prod.
5. Le jour de mise en prod, migration des notebooks existants pour ajouter les appels `verifier_et_reveler(...)` — c'est juste ajouter une cellule par exercice.

---

*Fin du document — à faire évoluer au fil de l'implémentation.*
