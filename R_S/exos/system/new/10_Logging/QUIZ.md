# Quiz de validation — dossier 10_Logging

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Citer les cinq niveaux standards de `logging`, du moins
critique au plus critique. Pour chacun, donner un exemple d'usage en
une phrase.

**Q2.** Par défaut (aucun appel à `basicConfig`), quel est le seuil
effectif du module `logging` ? Vers quel flux les messages
sortent-ils ?

**Q3.** Pourquoi écrit-on systématiquement
`logger = logging.getLogger(__name__)` en haut de chaque module, plutôt
qu'utiliser `logging.info(...)` directement ?

**Q4.** Le code suivant ne montre rien d'autre que `WARNING+`. Pourquoi
et comment corriger ?

```python
logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.DEBUG)
logging.debug("où es-tu ?")
```

**Q5.** Dans la configuration ci-dessous, qu'apparaît-il dans `app.log`
et qu'apparaît-il sur la console ?

```python
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

f = logging.FileHandler("app.log"); f.setLevel(logging.DEBUG)
c = logging.StreamHandler();        c.setLevel(logging.WARNING)
logger.addHandler(f); logger.addHandler(c)

logger.debug("d"); logger.info("i"); logger.warning("w"); logger.error("e")
```

**Q6.** Pourquoi est-il conseillé de **séparer** le résultat utile du
programme (via `print` sur stdout) et les journaux (via `logging` sur
stderr) ? Faire le lien avec `00_Concepts/03_flux_standards.md`.

---

## Réponses

**R1.** Du moins au plus critique : `DEBUG` (détail interne pour le
développeur), `INFO` (étape normale, *« service démarré »*), `WARNING`
(comportement inattendu mais non bloquant, *« config par défaut
utilisée »*), `ERROR` (une opération a échoué, *« connexion refusée »*),
`CRITICAL` (échec grave, *« base de données injoignable, on arrête »*).

**R2.** Le seuil par défaut du logger racine est `WARNING` : seuls les
`WARNING`, `ERROR` et `CRITICAL` apparaissent. La destination par
défaut est `stderr` (pas stdout) — ce qui permet de séparer journaux
et résultat utile via les redirections shell.

**R3.** Pour deux raisons. D'abord, la colonne `%(name)s` du format
indique alors clairement de quel module vient chaque ligne. Ensuite,
on peut régler des seuils ou des handlers spécifiques pour un module
sans toucher au reste de l'application (`logging.getLogger("auth")
.setLevel(logging.DEBUG)`).

**R4.** Le **second** `basicConfig` est **ignoré** : par défaut,
`basicConfig` ne fait rien si la configuration est déjà en place.
Corriger en supprimant l'un des deux appels (recommandé), ou en
passant `force=True` au second :
`logging.basicConfig(level=logging.DEBUG, force=True)`.

**R5.** Dans `app.log` apparaissent les quatre messages (`d`, `i`, `w`,
`e`) car le handler fichier est au seuil `DEBUG`. Sur la console
n'apparaissent que `w` et `e` car le handler console est au seuil
`WARNING`. Le seuil du **logger** (`DEBUG`) laisse tout passer ; ce
sont les seuils des **handlers** qui filtrent ensuite par destination.

**R6.** `print` écrit sur stdout, qui doit rester réservé au
**résultat** du programme (les données que l'utilisateur veut
récupérer avec `> sortie.txt`). `logging` écrit par défaut sur stderr,
qui transporte les **diagnostics**. Cette séparation permet à
l'utilisateur de rediriger ou filtrer chaque flux indépendamment, sans
qu'un message de progression vienne polluer le fichier de résultat.
