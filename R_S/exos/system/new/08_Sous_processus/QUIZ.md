# Quiz de validation — dossier 08_Sous_processus

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant
de passer au chapitre suivant. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Pourquoi est-il fortement recommandé de passer la commande
sous forme de **liste** (par exemple `["ls", "-la"]`) plutôt qu'en
chaîne de caractères avec `shell=True` ? Donner l'exemple d'un risque
concret.

**Q2.** Après un appel `result = subprocess.run([...], capture_output=True,
text=True)`, quels sont les trois attributs principaux de `result`
qu'on consulte, et que contient chacun d'eux ?

**Q3.** Quelle différence pratique entre un appel avec `check=False`
(par défaut) et un appel avec `check=True` lorsque le sous-processus
renvoie un code retour `1` ?

**Q4.** Compléter le tableau : à chaque situation, associer
l'exception levée (ou l'absence d'exception).

| Situation                                       | Comportement |
|-------------------------------------------------|--------------|
| Le programme n'existe pas dans le `PATH`        | ?            |
| Le programme se termine avec code 3, sans check | ?            |
| Le programme se termine avec code 3, check=True | ?            |
| `timeout=1.0` mais le programme prend 5 s       | ?            |

**Q5.** On veut faire l'équivalent Python de la commande shell :

```
echo "abcde" | wc -c
```

Donner les deux manières possibles vues dans le chapitre, en précisant
laquelle est préférable dans 95 % des cas.

**Q6.** Pourquoi, après avoir chaîné deux `Popen` via un tube, est-il
important d'appeler `p1.stdout.close()` côté parent avant le
`p2.communicate()` ?

---

## Réponses

**R1.** Une liste est passée **telle quelle** au système : pas
d'analyse, pas de découpage, pas de réinterprétation. À l'inverse,
`shell=True` confie la chaîne à un shell qui interprète les
métacaractères (`;`, `|`, `&&`, espaces non échappés, glob...). Si
l'un des morceaux vient d'un utilisateur, on ouvre la porte à une
**injection de commande**. Exemple :
`subprocess.run(f"cat {nom}", shell=True)` avec
`nom = "fichier.txt; rm -rf ~"` exécute aussi `rm -rf ~`. Avec
`subprocess.run(["cat", nom])`, le nom est juste un argument littéral
à `cat` — au pire, le fichier n'existe pas.

**R2.** `result.stdout` contient tout ce que la commande a écrit sur
sa sortie standard ; `result.stderr` tout ce qu'elle a écrit sur son
flux d'erreur ; `result.returncode` est l'entier renvoyé au système
(`0` = succès, autre = échec). Sans `text=True`, ces deux premiers
sont des `bytes` ; avec, des `str`.

**R3.** Avec `check=False` (par défaut), `run` renvoie normalement
l'objet `CompletedProcess` et c'est à l'appelant de tester
`result.returncode`. Avec `check=True`, un code non nul **lève
immédiatement** `subprocess.CalledProcessError`, qui contient le code,
la commande et éventuellement stdout/stderr. À utiliser quand on
considère qu'un échec doit interrompre le programme.

**R4.**

| Situation                                       | Comportement                |
|-------------------------------------------------|------------------------------|
| Le programme n'existe pas dans le `PATH`        | `FileNotFoundError`          |
| Le programme se termine avec code 3, sans check | Pas d'exception, `returncode = 3` |
| Le programme se termine avec code 3, check=True | `CalledProcessError`         |
| `timeout=1.0` mais le programme prend 5 s       | `TimeoutExpired`             |

**R5.** Première manière (préférée dans 95 % des cas) :

```python
subprocess.run(["wc", "-c"], input="abcde\n",
               capture_output=True, text=True)
```

Seconde manière (chaînage explicite via `Popen`) :

```python
p1 = subprocess.Popen(["echo", "abcde"], stdout=subprocess.PIPE, text=True)
p2 = subprocess.Popen(["wc", "-c"], stdin=p1.stdout,
                      stdout=subprocess.PIPE, text=True)
p1.stdout.close()
sortie, _ = p2.communicate()
```

La première est plus courte et suffit dès qu'on n'a pas besoin de
parallélisme entre les deux étapes. La seconde n'est nécessaire que
pour des flux importants ou des commandes longues à exécuter en
parallèle.

**R6.** Le tube entre `p1` et `p2` a deux extrémités côté lecture :
celle de `p2` (qui veut lire) et celle gardée par notre processus
parent (qui ne lit jamais). Tant que **quelqu'un** détient une copie
de l'extrémité d'écriture, `p2` ne recevra pas d'EOF et continuera
d'attendre. En faisant `p1.stdout.close()` côté parent, on s'assure
que dès que `p1` se termine, `p2` reçoit bien la fin de flux et peut
terminer à son tour. Sans ce `close()`, on risque un **interblocage**.
