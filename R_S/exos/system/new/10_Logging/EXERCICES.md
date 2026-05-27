# Exercices pratiques — dossier 10_Logging

Une fois les trois modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** la journalisation dans
des scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Du `print` au `logging`  ★
*Module 01 — pourquoi logging*

On part du mini-script suivant, qui mélange diagnostic et résultat :

```python
def diviser(a, b):
    print("Entrée dans diviser :", a, b)
    if b == 0:
        print("Erreur : division par zéro")
        return None
    print("Calcul OK")
    return a / b


print("Programme démarré")
print("Résultat :", diviser(10, 2))
print("Résultat :", diviser(10, 0))
print("Programme terminé")
```

Réécrire ce script en `atelier_01.py` de sorte que :

- la ligne « Programme démarré / terminé » utilise `logging.info` ;
- les traces internes (`Entrée dans diviser`, `Calcul OK`) utilisent
  `logging.debug` ;
- l'erreur de division par zéro utilise `logging.error` ;
- le **résultat utile** (`Résultat : 5.0`) reste affiché avec `print`,
  parce que c'est la sortie du programme, pas un journal.

Configurer le seuil sur `DEBUG` pour vérifier que tout apparaît, puis
sur `WARNING` pour vérifier qu'il ne reste que l'erreur.

**Indices**

- `logging.basicConfig(level=logging.DEBUG, format="...")` une seule fois.
- Format conseillé :
  `"%(asctime)s %(levelname)-8s %(name)s : %(message)s"`.
- Ne pas confondre **résultat du programme** (stdout, `print`) et
  **journal** (stderr, `logging`).

---

## Atelier 2 — DEBUG vers fichier, WARNING vers console  ★★
*Module 03 — handlers*

Écrire un script `atelier_02.py` qui :

- crée un logger nommé d'après le module (`getLogger(__name__)`) ;
- attache un `FileHandler` vers `app.log` au seuil `DEBUG` ;
- attache un `StreamHandler` (console) au seuil `WARNING` ;
- émet un message à chacun des cinq niveaux.

Vérifier que la console ne montre que `WARNING`, `ERROR`, `CRITICAL` et
que le fichier `app.log` contient les **cinq** lignes.

**Indices**

- Le seuil du logger lui-même doit être `DEBUG`, sinon les messages
  bas niveau seront filtrés *avant* d'atteindre le handler fichier.
- `FileHandler("app.log", mode="w", encoding="utf-8")`.
- Ne pas oublier `logger.setLevel(logging.DEBUG)`.

**Sortie attendue côté console**

```
WARNING  : quota proche de la limite
ERROR    : connexion refusée
CRITICAL : arrêt du service
```

---

## Atelier 3 — Deux loggers, deux niveaux  ★★
*Module 03 — loggers nommés*

Écrire un script `atelier_03.py` qui simule deux composants : `auth` et
`db`. Créer deux loggers :

```python
log_auth = logging.getLogger("auth")
log_db   = logging.getLogger("db")
```

Régler `auth` au niveau `INFO` et `db` au niveau `WARNING`. Émettre,
pour chaque logger, un message à chacun des cinq niveaux. Constater que
les messages `DEBUG` n'apparaissent jamais, et que `auth` montre
`INFO+` tandis que `db` ne montre que `WARNING+`.

**Indices**

- Configurer la sortie avec `basicConfig` (un seul handler racine
  suffit pour cet atelier).
- `logger.setLevel(...)` se règle indépendamment sur chaque logger.
- Le format `%(name)s` montrera bien `auth` ou `db` à chaque ligne.

---

## Atelier 4 — Effet du seuil  ★
*Module 02 — basicConfig*

Écrire un script `atelier_04.py` qui prend le seuil en argument :

```
python3 atelier_04.py DEBUG
python3 atelier_04.py INFO
python3 atelier_04.py WARNING
python3 atelier_04.py ERROR
python3 atelier_04.py CRITICAL
```

Pour chaque exécution, configurer `logging` avec le seuil demandé, puis
émettre **les cinq niveaux**. Observer ce qui s'affiche selon le seuil.

**Indices**

- `getattr(logging, "DEBUG")` renvoie l'entier `10`. C'est l'astuce
  pour convertir une chaîne en niveau.
- Penser à valider l'argument (s'il n'existe pas, message d'erreur sur
  stderr et `sys.exit(2)`).
- `sys.argv[1]` pour l'argument.

**Sortie attendue avec seuil = `ERROR`**

```
ERROR    : message niveau ERROR
CRITICAL : message niveau CRITICAL
```

---

## Atelier 5 — Logger un dictionnaire en JSON  ★★★
*Module 03 — formatters, contenu structuré*

Lorsqu'on veut journaliser un événement riche (utilisateur, action,
durée, ...), une approche pratique est de logger le tout sous forme
**JSON sérialisé**. Le journal reste lisible par un humain *et*
analysable par une machine.

Écrire un script `atelier_05.py` qui :

- définit un dictionnaire `evenement = {"user": "ada", "action":
  "login", "duree_ms": 42}` ;
- le sérialise en JSON avec `json.dumps(...)` ;
- le passe en `message` à `logger.info(...)`.

Réutiliser ensuite le code pour logger une douzaine d'événements
factices. Vérifier que chaque ligne de journal est une chaîne JSON
valide (les copier dans un script qui les relit avec `json.loads`).

**Indices**

- `json.dumps(evenement, ensure_ascii=False)` pour conserver les
  accents éventuels.
- Le format de log peut être réduit à `"%(message)s"` si on veut
  qu'**uniquement** le JSON apparaisse (utile pour un pipeline
  d'analyse).
- Ne pas confondre : `logging` formate le message, `json.dumps` formate
  le contenu **dedans**.

**Bonus** : ajouter un champ `"ts": <timestamp ISO>` dans chaque
dictionnaire, calculé avec `datetime.datetime.now().isoformat()`.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait remplacer chaque `print` de
diagnostic par un appel `logging` adapté, configurer plusieurs
destinations en parallèle, et structurer ses messages pour qu'ils
restent exploitables longtemps après leur écriture.
