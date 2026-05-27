# 01 — Pourquoi `logging` (et pas `print`)

## 1.1 Le réflexe `print` et ses limites

Quand on découvre Python, on diagnostique en saupoudrant des `print(...)`
dans le code :

```python
print("Entrée dans la fonction")
print("valeur de x :", x)
print("Erreur : fichier manquant")
```

Cette pratique fonctionne pour bricoler, mais elle pose **quatre
problèmes** dès qu'on dépasse la dizaine de lignes :

1. **Pas de niveau de criticité.** Tout est mélangé : information de
   debug, avertissement, erreur fatale. Impossible de distinguer.
2. **Pas de filtrage à l'exécution.** Pour rendre le code silencieux en
   production, il faudrait commenter ou supprimer chaque `print`, puis
   les remettre pour déboguer.
3. **Pas de format uniforme.** Chaque `print` choisit ses propres
   séparateurs, ne dit pas *quand* il s'est produit ni *d'où* il vient.
4. **Une seule destination.** `print` écrit sur `stdout` ; pour aussi
   archiver dans un fichier, il faut tout réécrire.

## 1.2 Ce que propose `logging`

La bibliothèque standard fournit le module `logging`. Il résout les
quatre points d'un coup :

- chaque message porte un **niveau** parmi cinq valeurs prédéfinies ;
- un **seuil** global (ou par module) décide ce qui s'affiche ;
- un **format** unique applique date, niveau et origine à toutes les
  lignes ;
- un même message peut être envoyé en parallèle vers **plusieurs
  destinations** (console, fichier, journal système).

Usage minimal :

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Démarrage")
logging.warning("Disque presque plein")
logging.error("Connexion refusée")
```

## 1.3 Les cinq niveaux

Les niveaux sont des entiers fixes, du moins critique au plus critique.
Un seuil de `WARNING` masque automatiquement `DEBUG` et `INFO`.

| Niveau     | Valeur | Usage typique                                              |
|------------|--------|------------------------------------------------------------|
| `DEBUG`    | 10     | Détails internes utiles au développeur                     |
| `INFO`     | 20     | Étapes normales du programme (« démarré », « connecté »)   |
| `WARNING`  | 30     | Comportement inattendu mais non bloquant                   |
| `ERROR`    | 40     | Une opération a échoué, le programme continue              |
| `CRITICAL` | 50     | Échec grave, le programme va peut-être s'arrêter           |

**Règle simple** : pendant le développement, on travaille au niveau
`DEBUG` ; en production, on remonte le seuil à `INFO` ou `WARNING` pour
ne garder que l'essentiel. **Aucune ligne de code n'est modifiée** :
seul le seuil change.

## 1.4 Quel niveau choisir ?

- *« Je veux voir la valeur d'une variable au passage »* → `DEBUG`.
- *« Le service vient de démarrer / un client vient de se connecter »*
  → `INFO`.
- *« La configuration utilise une valeur par défaut suspecte »*
  → `WARNING`.
- *« Impossible d'écrire dans le fichier de sortie »* → `ERROR`.
- *« La base de données est inaccessible, j'abandonne »* → `CRITICAL`.

## 1.5 Destination par défaut

Par défaut, `logging` écrit sur **`stderr`** (pas `stdout`). Cohérence
avec `00_Concepts/03_flux_standards.md` : les journaux sont des
diagnostics, pas le résultat du programme. On peut ainsi rediriger les
*données utiles* avec `> sortie.txt` sans perdre les journaux à l'écran.

## À retenir

- `print` mélange tout ; `logging` sépare par niveau de criticité.
- Cinq niveaux : `DEBUG` < `INFO` < `WARNING` < `ERROR` < `CRITICAL`.
- Le seuil est ajustable à l'exécution sans toucher au code.
- Format uniforme et destinations multiples viennent gratuitement.
- Sortie par défaut : `stderr`.

## Démo

Exécuter `01_demo_niveaux.py` et observer quels messages s'affichent
selon le seuil configuré.
