# Quiz de validation — dossier 00_Concepts

Cinq questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la différence pratique entre le REPL et un script
`.py`, et dans quel cas privilégier l'un ou l'autre ?

**Q2.** À quoi sert la ligne `#!/usr/bin/env python3` en première
ligne d'un script ? Que faut-il faire de plus pour qu'un script soit
lançable par `./mon_script.py` ?

**Q3.** En Python 3, faut-il encore écrire `# -*- coding: utf-8 -*-`
en tête d'un fichier source ? Justifier.

**Q4.** Que fait précisément la commande shell suivante, flux par flux ?

```
python3 mon_script.py > sortie.txt 2> erreurs.txt
```

**Q5.** Un script termine par `sys.exit(2)`. Que vaut `$?` dans le
shell juste après son exécution ? Et quelle est la convention pour
distinguer succès et échec ?

---

## Réponses

**R1.** Le **REPL** (lancé avec `python3` sans argument) évalue chaque
ligne au fur et à mesure ; idéal pour expérimenter, mais le code tapé
disparaît à la sortie. Un **script** `.py` est un fichier texte
conservé sur disque, lancé par `python3 fichier.py` ou directement
sous Unix ; on l'utilise dès qu'on veut réexécuter du code, le
versionner ou le partager.

**R2.** La ligne shebang `#!/usr/bin/env python3` indique au système
quel interpréteur utiliser quand on lance le fichier directement. Il
faut en plus rendre le fichier exécutable avec `chmod +x mon_script.py`.
La forme `env python3` est portable car elle cherche `python3` dans le
`PATH` au lieu d'imposer un chemin absolu fixe.

**R3.** **Non**. Depuis Python 3, l'encodage par défaut du code source
est déjà UTF-8. La déclaration `# -*- coding: utf-8 -*-` est un
vestige de Python 2 ; elle est ignorée (au sens où elle ne change
rien) en Python 3 moderne et peut être supprimée sans effet.

**R4.** `python3 mon_script.py` exécute le script. `> sortie.txt`
redirige sa sortie standard (stdout) vers le fichier `sortie.txt`
(qui est créé ou écrasé). `2> erreurs.txt` redirige sa sortie d'erreur
(stderr) vers `erreurs.txt`. Rien ne s'affiche à l'écran : les deux
flux sont rangés séparément dans deux fichiers.

**R5.** `$?` vaut **2**. La convention universelle est : code retour
**`0`** pour un succès, **toute autre valeur** (typiquement entre 1 et
255) pour un échec. C'est ce que les scripts shell et les outils
d'intégration continue testent pour savoir si une commande a réussi.
