# Exercices pratiques — dossier 05_Fichiers

Une fois les trois modules lus et leurs démos exécutées, ces six
ateliers permettent de **mettre en pratique** les concepts dans des
scripts courts. Aucune dépendance tierce : tout se fait avec la
bibliothèque standard.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés sont fournis dans `CORRIGES/`, à consulter **après** avoir
tenté chaque atelier. Chaque corrigé crée lui-même son fichier d'entrée
de test : on peut donc tous les exécuter tels quels, sans rien
préparer.

---

## Atelier 1 — Compter les lignes sans tout charger  ★
*Module 01 — itération sur un fichier*

Écrire un script `atelier_01.py` qui prend un chemin de fichier
texte et affiche son nombre de lignes. Le script doit fonctionner même
sur un fichier de plusieurs gigaoctets : il est donc **interdit**
d'utiliser `f.read()` ou `f.readlines()`.

**Indices**

- Itérer directement : `for ligne in f:`.
- Un compteur entier initialisé à 0 suffit.
- `sys.argv[1]` pour récupérer le chemin.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py mon_fichier.txt
mon_fichier.txt : 1234 ligne(s)
```

---

## Atelier 2 — Copier un fichier ligne à ligne  ★
*Module 01 + 02 — lire et écrire*

Écrire un script `atelier_02.py` qui copie un fichier source vers un
fichier destination en **lisant et écrivant ligne à ligne**. Le script
doit refuser d'écraser le fichier destination s'il existe déjà.

**Indices**

- Ouvrir la source en `"r"`, la destination en `"x"`.
- Itérer sur la source, écrire chaque ligne **telle quelle** (avec son
  `\n` final déjà inclus).
- Attraper `FileExistsError` pour produire un message clair.

**Exemple de sortie attendue**

```
$ python3 atelier_02.py source.txt copie.txt
Copie terminee : 42 ligne(s) ecrites dans copie.txt
```

---

## Atelier 3 — Journal horodaté  ★
*Module 02 — mode "a", append*

Écrire un script `atelier_03.py` qui prend un message en argument et
l'ajoute à la fin d'un fichier `app.log`, **précédé d'un horodatage**
au format ISO (`2026-05-26T18:42:11`). Le fichier doit être créé s'il
n'existe pas, conservé tel quel sinon.

**Indices**

- Mode `"a"` : crée le fichier au besoin, ajoute à la fin sinon.
- `datetime.datetime.now().isoformat(timespec="seconds")`.
- Une seule ligne par appel : `f"{horodatage} {message}\n"`.

**Exemple d'exécution**

```
$ python3 atelier_03.py "demarrage du service"
$ python3 atelier_03.py "traitement OK"
$ python3 atelier_03.py "fin"
$ cat app.log
2026-05-26T18:42:11 demarrage du service
2026-05-26T18:42:18 traitement OK
2026-05-26T18:42:25 fin
```

---

## Atelier 4 — Inverser le contenu d'un fichier  ★★
*Module 01 + 02 — lecture complète + écriture*

Écrire un script `atelier_04.py` qui lit un fichier texte et écrit
dans un second fichier les **mêmes lignes en ordre inverse** (dernière
ligne en premier). Les sauts de ligne doivent rester corrects.

**Indices**

- `f.readlines()` renvoie déjà la liste, et `list.reverse()` ou la
  syntaxe `[::-1]` inversent l'ordre.
- Attention si la dernière ligne du fichier source ne se termine pas
  par un `\n` : elle se retrouverait collée à la précédente dans le
  fichier inversé.
- `f.writelines(lignes_inversees)` recolle tout.

**Exemple**

```
source.txt :          destination.txt :
alpha                 gamma
beta                  beta
gamma                 alpha
```

---

## Atelier 5 — Compter les occurrences d'un mot  ★★
*Module 01 + 03 — lecture texte + encodage robuste*

Écrire un script `atelier_05.py` qui prend un chemin de fichier et un
mot en argument, et affiche **combien de fois ce mot apparaît**.
Comptage **insensible à la casse**, mots considérés comme des
séquences séparées par des espaces ou de la ponctuation. Le script
doit rester robuste si le fichier contient des octets douteux
(utiliser `errors="replace"`).

**Indices**

- `ligne.lower()` pour normaliser la casse.
- Pour découper en mots : le module `re` avec `re.findall(r"\w+",
  texte)`.
- Compter avec `collections.Counter` ou un simple `sum(...)`.
- Ouvrir avec `encoding="utf-8", errors="replace"`.

**Exemple de sortie attendue**

```
$ python3 atelier_05.py poeme.txt rose
Le mot 'rose' apparait 3 fois.
```

---

## Atelier 6 — Copie binaire par blocs de 4 Kio  ★★★
*Module 03 — mode binaire, lecture par blocs*

Écrire un script `atelier_06.py` qui copie un fichier **binaire**
(image, archive, exécutable) octet pour octet depuis une source vers
une destination, **par blocs de 4096 octets**. Le script doit
fonctionner même si le fichier source fait plusieurs gigaoctets : la
consommation mémoire doit rester bornée par la taille du bloc.

**Indices**

- Modes `"rb"` et `"wb"` (pas d'`encoding=` en binaire).
- Boucle `while True:` qui lit `f_src.read(4096)`.
- `read(n)` renvoie une chaîne d'octets de longueur ≤ `n` ; quand le
  fichier est terminé, elle renvoie `b""` — c'est la condition d'arrêt.
- Vérifier ensuite que les deux fichiers sont identiques avec
  `hashlib.sha256` ou simplement leur taille.

**Bonus** : afficher la progression toutes les `N` blocs sur
`sys.stderr`, sans polluer la sortie standard.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on peut attaquer le chapitre
**06_OS_et_Shutil** pour les opérations de **haut niveau** (copier,
déplacer, supprimer un fichier entier sans lire son contenu) et
**07_Compression** pour appliquer les mêmes modes (`"r"`, `"rb"`,
`"w"`, `"wb"`) à des archives `.gz` ou `.zip`.
