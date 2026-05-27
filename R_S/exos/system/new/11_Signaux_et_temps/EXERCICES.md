# Exercices pratiques — dossier 11_Signaux_et_temps

Une fois les trois modules lus et leurs démos exécutées, ces cinq
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

---

## Atelier 1 — Chronomètre simple  ★
*Module 01 — time.monotonic*

Écrire un script `atelier_01.py` qui chronomètre la durée d'un
`time.sleep(1.234)` et l'affiche au millième de seconde près.

**Indices**

- `time.monotonic()` avant et après, puis soustraire.
- `print(f"{duree:.3f} s")` pour trois décimales.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py
Pause de 1,234 s...
Durée mesurée : 1.234 s
```

**Question** : pourquoi utilise-t-on `time.monotonic` plutôt que
`datetime.now()` pour mesurer une durée ?

---

## Atelier 2 — Logger horodaté  ★
*Module 01 — datetime, strftime*

Écrire un script `atelier_02.py` qui définit une fonction
`log(message)` affichant la ligne au format
`2026-05-27T14:30:00 - <message>`, et l'utilise pour afficher trois
messages séparés d'une pause d'une seconde.

**Indices**

- Récupérer l'instant avec `datetime.now()`.
- Le format souhaité est presque ISO 8601 : `%Y-%m-%dT%H:%M:%S`.
- Une pause d'une seconde : `time.sleep(1)`.

**Exemple de sortie attendue**

```
$ python3 atelier_02.py
2026-05-27T14:30:00 - début
2026-05-27T14:30:01 - étape intermédiaire
2026-05-27T14:30:02 - fin
```

---

## Atelier 3 — Arrêt propre sur Ctrl+C  ★★
*Module 02 — signaux*

Écrire un script `atelier_03.py` qui boucle indéfiniment en
affichant un compteur incrémenté chaque seconde. Sur Ctrl+C, le
script doit :

- afficher `Arrêt propre.` ;
- sortir avec le **code retour 0** (et non 130, le défaut de
  `KeyboardInterrupt`).

**Indices**

- `signal.signal(signal.SIGINT, handler)`.
- Le handler peut faire `sys.exit(0)`.
- Vérifier le code retour avec `echo $?` dans le shell.

**Exemple de sortie attendue**

```
$ python3 atelier_03.py
1
2
3
^CArrêt propre.
$ echo $?
0
```

---

## Atelier 4 — Sauvegarde automatique avec `atexit`  ★★
*Module 03 — atexit + JSON*

Écrire un script `atelier_04.py` qui maintient un dictionnaire
`etat = {"compteur": 0}`, incrémente `etat["compteur"]` cinq fois (une
fois par seconde), puis sort normalement. Une fonction enregistrée
avec `atexit` doit **sauvegarder** ce dictionnaire dans un fichier
`etat.json` à la sortie.

Vérifier qu'`etat.json` contient bien `{"compteur": 5}` après la
sortie.

**Indices**

- `import json`, `json.dump(etat, fichier)`.
- `atexit.register(sauver, etat)` pour passer l'objet à la fonction.
- Astuce : pour relancer proprement, supprimer `etat.json` entre
  deux essais.

**Bonus** : ajouter un handler `SIGINT` qui lève `SystemExit`, et
vérifier que Ctrl+C déclenche bien la sauvegarde.

---

## Atelier 5 — Convertisseur de durée  ★★★
*Module 01 — manipulation de durées*

Écrire un script `atelier_05.py` qui propose **deux fonctions** :

```python
def vers_secondes(texte: str) -> int: ...
def vers_texte(secondes: int) -> str: ...
```

- `vers_secondes("1h30m45s")` renvoie `5445`.
- `vers_texte(5445)` renvoie `"1h30m45s"`.

Les unités acceptées sont `h`, `m`, `s`. Toutes peuvent être absentes
(`"45s"`, `"2m"`, `"3h"`, `"1h30s"` sont tous valides). Le script
doit afficher au moins trois cas de test, et vérifier que
`vers_texte(vers_secondes(t)) == t` pour les entrées normalisées.

**Indices**

- Parser : un `re.findall(r"(\d+)([hms])", texte)`.
- Formater : diviser successivement par 3600, puis par 60, le reste.
- Attention : `vers_texte(60)` doit valoir `"1m"`, pas `"0h1m0s"`.

**Exemple de sortie attendue**

```
$ python3 atelier_05.py
1h30m45s -> 5445 s
2m       -> 120 s
3h       -> 10800 s
5445 s   -> 1h30m45s
120 s    -> 2m
```

---

## Pour aller plus loin

Une fois ces ateliers terminés, on sait chronométrer, horodater,
intercepter un signal d'arrêt et brancher du code de nettoyage à la
sortie. Trois briques qui réapparaîtront dans toute application
système un peu sérieuse.
