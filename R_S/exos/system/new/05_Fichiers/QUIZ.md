# Quiz de validation — dossier 05_Fichiers

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Pourquoi est-il préférable d'écrire
`with open(chemin, "r", encoding="utf-8") as f:` plutôt que
`f = open(chemin, "r"); ...; f.close()` ? Donner deux raisons.

**Q2.** Que vaut `ligne` à la sortie de la boucle suivante, sur un
fichier dont les trois lignes sont `alpha`, `beta`, `gamma` (chacune
suivie d'un `\n`) ?

```python
with open("f.txt", "r", encoding="utf-8") as f:
    for ligne in f:
        print(ligne)
```

Quel défaut visuel observe-t-on à l'affichage et comment le corriger ?

**Q3.** Quelle est la différence entre les modes `"w"`, `"a"` et `"x"`
quand le fichier visé existe déjà ?

**Q4.** Comparer `f.write("toto")` et `print("toto", file=f)` : quelle
différence concrète y a-t-il dans le fichier produit, et pourquoi ?

**Q5.** On veut lire le fichier `logo.png`. Quel mode utiliser, et
pourquoi ne **pas** préciser `encoding=` dans ce cas ?

**Q6.** Un collègue fournit un fichier `donnees.txt` exporté depuis un
tableur Windows. À la lecture en `encoding="utf-8"`, on voit apparaître
un caractère `﻿` en tout début de fichier qui empêche le parseur de
faire son travail. Que se passe-t-il et comment le résoudre ?

---

## Réponses

**R1.** D'abord, `with` garantit que le fichier est **refermé** même
si une exception est levée à l'intérieur du bloc (sécurité). Ensuite,
c'est plus court et plus lisible : on n'a pas à se rappeler de l'appel
`.close()` ni à protéger l'ouverture par un `try/finally`.

**R2.** Chaque `ligne` vaut respectivement `"alpha\n"`, `"beta\n"`,
`"gamma\n"` : le `\n` final est **conservé** par l'itération. À
l'affichage, on observe une **ligne vide** entre chaque mot, car
`print` ajoute son propre `\n` par-dessus celui déjà présent. On
corrige avec `print(ligne.rstrip("\n"))` ou `print(ligne, end="")`.

**R3.** `"w"` **écrase** entièrement le contenu existant — c'est le
mode le plus dangereux. `"a"` **ajoute** à la fin sans toucher au
reste, idéal pour un journal. `"x"` **échoue** avec `FileExistsError`
si le fichier existe déjà, idéal quand on veut créer un nouveau
fichier sans risquer d'en écraser un autre.

**R4.** `f.write("toto")` écrit **exactement** la chaîne donnée, sans
ajout. `print("toto", file=f)` écrit `"toto\n"` car `print` ajoute par
défaut un saut de ligne (paramètre `end="\n"`). Pour obtenir le même
résultat avec `write`, il faut écrire `f.write("toto\n")` à la main.

**R5.** Un PNG est un format **binaire** : il faut le mode `"rb"`
(`r` + `b`). On n'utilise **pas** `encoding=` en mode binaire parce
qu'on récupère des `bytes` bruts, sans aucune interprétation. Préciser
un encodage produirait une erreur (et de toute façon il n'y a pas
d'encodage pour une image).

**R6.** Le fichier contient un **BOM UTF-8** (`\xef\xbb\xbf`), une
marque ajoutée en tête par certains outils Windows. Lu avec
`encoding="utf-8"`, il apparaît comme un caractère parasite en début
de fichier. La solution est d'ouvrir avec `encoding="utf-8-sig"`, qui
consomme silencieusement le BOM s'il est présent et ne fait rien
sinon — c'est sans risque dans les deux cas.
