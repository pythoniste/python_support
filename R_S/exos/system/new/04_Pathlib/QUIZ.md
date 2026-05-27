# Quiz de validation — dossier 04_Pathlib

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Que renvoient `p.stem`, `p.suffix` et `p.suffixes` pour
`p = Path("archive.tar.gz")` ? Pourquoi `stem` n'est-il pas
simplement `"archive"` ?

**Q2.** Quelle est la différence pratique entre `Path("a") / "b"` et
`os.path.join("a", "b")` ? Citer **deux** avantages concrets de la
première forme.

**Q3.** On écrit :

```python
p = Path("/tmp/inexistant.txt")
print(p.is_file())
print(p.stat())
```

Quel est le comportement de chaque ligne ? Pourquoi le diffèrent-elles
sur un chemin qui n'existe pas ?

**Q4.** Citer la différence entre `.absolute()` et `.resolve()` sur un
`Path` relatif. Quelle est celle des deux qui touche au système de
fichiers, et pourquoi ?

**Q5.** Quel motif `glob` correspond à tous les fichiers `.py` :

- du **seul** dossier courant ?
- du dossier courant **et** de tous ses sous-dossiers ?

Citer la méthode `pathlib` à utiliser dans chaque cas.

**Q6.** Pourquoi `Path(".").rglob("*.py")` peut-il être **lent** sur
un dossier comme `/` ou `~` ? Que renvoie exactement la méthode, et
comment éviter de tout charger en mémoire ?

---

## Réponses

**R1.** `stem` vaut `"archive.tar"`, `suffix` vaut `".gz"`, `suffixes`
vaut `['.tar', '.gz']`. `pathlib` considère seulement la **dernière**
extension comme « le » suffixe ; tout ce qui précède appartient au
stem. Pour obtenir `"archive"` seul, il faut retirer toutes les
extensions une à une (par exemple via `p.name.split('.')[0]`).

**R2.** `os.path.join` prend et rend des **chaînes** ; `Path("a") /
"b"` rend un objet `Path`. Avantages concrets : (a) on peut chaîner
des opérations sur le résultat (`.exists()`, `.parent`, etc.) sans
réimporter `os.path` ; (b) la lecture est plus naturelle pour les
chemins longs : `racine / "data" / "2026" / "fichier.csv"` se lit
de gauche à droite, sans virgules.

**R3.** `p.is_file()` renvoie `False` sans lever d'exception, c'est
sûr de l'appeler sur un chemin absent. `p.stat()` lève
`FileNotFoundError` : la méthode interroge réellement le système de
fichiers pour récupérer la taille, la mtime, etc., ce qui exige que
le fichier existe. La règle : les méthodes booléennes d'inspection
(`exists`, `is_file`, `is_dir`, `is_symlink`) sont sûres ; `stat`
ne l'est pas.

**R4.** `.absolute()` préfixe simplement le chemin par `Path.cwd()`
**sans** toucher au disque : les `..` et les liens symboliques sont
conservés tels quels. `.resolve()` produit la forme **canonique**
(absolue, sans `.` ni `..`, avec liens suivis) en interrogeant le
système de fichiers. C'est `.resolve()` qui touche au disque ; en cas
de doute, on la préfère.

**R5.** Pour le seul dossier courant : `Path(".").glob("*.py")`.
Pour le dossier courant et tous ses sous-dossiers :
`Path(".").rglob("*.py")` (ou, de manière équivalente,
`Path(".").glob("**/*.py")`).

**R6.** Sur un dossier énorme, `rglob` doit examiner **chaque
entrée** de l'arborescence : ça peut faire des millions d'inodes. Mais
la méthode renvoie un **itérateur** d'objets `Path`, pas une liste :
rien n'est chargé d'avance. Pour limiter le coût mémoire, on
itère directement (`for p in ...:`) au lieu d'appeler `list(...)`, et
on peut s'arrêter dès qu'on a trouvé ce qu'on cherche avec `break`
ou `next()`.
