# Quiz de validation — dossier 06_OS_et_Shutil

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant
de passer au chapitre suivant (`07_Compression`). Les réponses se
trouvent en fin de document — tenter d'y répondre **sans** consulter
au préalable.

## Questions

**Q1.** Quelle est la différence pratique entre `shutil.copy(src, dst)`
et `shutil.copy2(src, dst)` ? Dans quel cas faut-il **impérativement**
utiliser `copy2` ?

**Q2.** On veut parcourir un dépôt Git mais **sans** descendre dans le
dossier `.git`. Quelle technique permet, avec `os.walk`, d'élaguer le
parcours sur place ? Pourquoi `Path.rglob` se prête-t-il moins bien à
cet usage ?

**Q3.** Que fait exactement la ligne suivante, et pourquoi est-elle
typiquement appelée « idempotente » ?

```python
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

**Q4.** On veut rendre un script `mon_outil.py` directement exécutable
sous Unix (`./mon_outil.py`). Quel appel Python configure les bons
droits, et pourquoi ne **doit-on pas** écrire `chmod(755)` (sans
préfixe) ?

**Q5.** `shutil.rmtree("/tmp/cache")` est appelé dans un script. Citer
**deux** précautions à prendre **avant** cette ligne pour éviter une
catastrophe en cas de bug ou de variable mal initialisée.

**Q6.** Un collègue écrit :

```python
shutil.move(source, destination)
```

où `destination` est un fichier qui existe **déjà**. Que se passe-t-il,
et comment se protéger d'une perte de données accidentelle ?

---

## Réponses

**R1.** `shutil.copy` copie **uniquement le contenu** : la copie reçoit
la date du jour et les droits par défaut. `shutil.copy2` copie **en
plus** les métadonnées (date de modification, date d'accès, droits
Unix). `copy2` est obligatoire pour toute **sauvegarde** ou
**archivage** où l'historique temporel doit être préservé. C'est aussi
ce qu'utilise `shutil.copytree` en interne par défaut.

**R2.** Avec `os.walk`, on **modifie `dirnames` sur place** (la liste
est mutable) : `dirnames.remove(".git")`. `os.walk` lit cette liste
pour décider où descendre ensuite ; retirer un nom revient à élaguer.
`Path.rglob` n'expose pas ce point de contrôle : il *yielde* déjà tous
les `Path` récursivement, on ne peut que filtrer **après coup**, donc
on paie quand même le coût du parcours dans les dossiers indésirables.

**R3.** La ligne crée le dossier `a/b/c` :

- `parents=True` : si `a` ou `a/b` n'existe pas, ils sont créés
  aussi (équivalent de `mkdir -p` en shell).
- `exist_ok=True` : si le dossier final existe déjà, aucune
  exception n'est levée.

L'opération est **idempotente** : on peut la **rejouer** autant de
fois qu'on veut, le résultat est le même (le dossier existe) et
aucune erreur n'est levée. C'est très utile dans les scripts qu'on
relance sans précautions.

**R4.** L'appel est :

```python
Path("mon_outil.py").chmod(0o755)
```

Le préfixe **`0o`** indique un littéral **octal**. `0o755` vaut
`4*64 + 9*8 + 5 = 493` en décimal et correspond aux droits
`rwxr-xr-x`. Écrire `chmod(755)` (sans préfixe) demande des droits
de valeur **décimale** 755, dont la représentation binaire ne
correspond **pas** au trio rwx voulu : on obtient des droits aberrants.

**R5.** Plusieurs précautions possibles, en citer deux :

- **Imprimer le chemin** juste avant : `print(cible)` permet de
  repérer une variable vide ou mal construite.
- Vérifier par **`assert cible.is_dir()`** que la cible existe et
  est bien un dossier.
- Vérifier par **`assert str(cible).startswith("/un/préfixe/sûr")`**
  qu'on est dans une zone autorisée.
- **Tester d'abord** sur un `tempfile.TemporaryDirectory()` peuplé
  artificiellement.
- Demander une **confirmation explicite** (`input(...)`) avant le
  `rmtree`.
- Implémenter un **mode `--dry-run`** qui affiche ce qui *serait*
  supprimé sans rien toucher.

**R6.** `shutil.move` **écrase silencieusement** la destination si
c'est un fichier — les anciennes données sont perdues sans avertissement.
Pour se protéger, vérifier soi-même :

```python
if destination.exists():
    raise FileExistsError(destination)
shutil.move(source, destination)
```

C'est la même précaution qu'avec `Path.rename` et `os.rename`. Aucune
fonction de la stdlib ne demande de confirmation à l'utilisateur ;
c'est au script de le faire si nécessaire.
