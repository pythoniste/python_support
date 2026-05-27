# Quiz de validation — dossier 02_Sys

Cinq questions ouvertes pour vérifier qu'on a saisi l'essentiel avant
de passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Que contient exactement `sys.argv` quand on lance la commande
suivante, et combien d'éléments la liste comporte-t-elle ?

```
$ python3 mon_script.py --mode rapide fichier.txt
```

**Q2.** Quelle est la différence pratique entre `sys.exit(1)` et
`sys.exit("argument manquant")` ? Sur quel flux le second écrit-il, et
quel code retour le shell observe-t-il ?

**Q3.** Pourquoi écrire les messages de progression sur `sys.stderr`
plutôt que sur `sys.stdout` ? Donner un cas concret où la séparation
est indispensable.

**Q4.** À quoi sert `sys.stdin.isatty()` ? Donner un cas concret où le
résultat de cette méthode change le comportement du script.

**Q5.** Décrire flux par flux ce que fait la commande suivante :

```
$ python3 producteur.py 2>&1 | python3 consommateur.py > donnees.txt
```

---

## Réponses

**R1.** `sys.argv` vaut `['mon_script.py', '--mode', 'rapide',
'fichier.txt']` : **quatre** éléments au total. Le premier (`argv[0]`)
est toujours le nom (ou le chemin) du script ; les trois autres sont
les arguments tels qu'ils ont été tapés, dans l'ordre, sous forme de
chaînes. Le shell se charge de découper la ligne sur les espaces
**avant** de transmettre la liste à Python.

**R2.** `sys.exit(1)` arrête le script et rend le code retour `1` au
shell, **sans** écrire de message. `sys.exit("argument manquant")`
écrit la chaîne sur **stderr** (avec un saut de ligne final) **puis**
sort avec le code retour `1`. C'est un raccourci pratique pour
signaler une erreur d'utilisation en une seule ligne, sans avoir à
enchaîner un `print(..., file=sys.stderr)` puis un `sys.exit(1)`.

**R3.** Parce qu'on veut pouvoir **rediriger stdout** vers un fichier
sans que ce fichier soit pollué par les messages d'information. Cas
typique :

```
$ python3 script.py > donnees.csv
Progression : 10%
Progression : 50%
```

Si la progression était écrite sur stdout, elle se retrouverait
mélangée aux données utiles dans `donnees.csv` et casserait
l'utilisation aval (un programme qui parse le CSV, par exemple). En
l'envoyant sur stderr, on garde stdout propre pour la donnée et stderr
visible pour l'humain.

**R4.** `sys.stdin.isatty()` renvoie `True` si stdin est branché sur
un **terminal interactif**, et `False` s'il est branché sur un
**fichier ou un pipe**. Un cas concret : afficher un *prompt*
(« Tapez votre texte, Ctrl+D pour terminer ») uniquement quand un
humain est devant ; en mode pipe, ce message serait inutile, voire
gênant s'il atterrit dans le flux de données.

**R5.** Décomposition :

- `python3 producteur.py 2>&1` lance le producteur en **fusionnant**
  sa stderr dans sa stdout. Les deux flux du producteur sortent donc
  ensemble par le même tuyau.
- `|` branche ce tuyau combiné sur la stdin de `consommateur.py`. Le
  consommateur reçoit donc à la fois les données et les messages
  d'erreur du producteur, mélangés.
- `> donnees.txt` redirige la stdout **du consommateur** vers le
  fichier `donnees.txt`. La stderr du consommateur, elle, n'est pas
  redirigée et reste visible à l'écran.

Résultat net : `donnees.txt` contient ce que le consommateur a écrit
sur sa stdout après avoir traité l'union des deux flux du producteur.
