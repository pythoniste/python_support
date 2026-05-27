# Quiz de validation — dossier 07_Compression

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer au chapitre suivant. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la différence fondamentale entre `gzip` et
`zipfile` ? Quand utilise-t-on l'un plutôt que l'autre ?

**Q2.** Les modules `gzip`, `bz2` et `lzma` partagent la même API.
Citer la fonction commune et les quatre modes d'ouverture les plus
courants.

**Q3.** À quoi sert le paramètre `arcname` de `ZipFile.write` ?
Que se passe-t-il si on l'oublie en passant un chemin absolu comme
`/home/alice/rapport.txt` ?

**Q4.** Qu'est-ce que la faille `zip-slip` ? Comment se protéger
quand on extrait une archive d'origine inconnue ?

**Q5.** Pourquoi `tarfile.open("a.tar.gz", "a:gz")` n'existe-t-il
pas ? Que faudrait-il faire pour « ajouter » un fichier à un
`.tar.gz` existant ?

**Q6.** Sur une archive `.tar.gz` de plusieurs gigaoctets contenant
des milliers de fichiers, on veut récupérer **un seul** fichier précis.
Pourquoi est-ce significativement plus lent qu'avec un `.zip`
équivalent ?

---

## Réponses

**R1.** `gzip` compresse **un seul flux d'octets** (un fichier) et
produit un fichier `.gz`. `zipfile` produit une **archive** qui peut
contenir plusieurs fichiers avec leur arborescence interne. On utilise
`gzip` quand on n'a qu'un fichier à traiter ; `zipfile` (ou
`tarfile`) dès qu'on veut regrouper plusieurs fichiers.

**R2.** Les trois modules exposent `open(chemin, mode)`. Les quatre
modes courants sont :

- `"rb"` : lecture binaire ;
- `"wb"` : écriture binaire ;
- `"rt"` : lecture texte (décodage automatique) ;
- `"wt"` : écriture texte (encodage automatique).

**R3.** `arcname` contrôle le nom **interne** sous lequel l'entrée est
rangée dans l'archive ZIP. Si on l'omet, c'est le chemin passé à
`write` qui est conservé tel quel — y compris s'il est absolu. On se
retrouve alors avec une entrée nommée `/home/alice/rapport.txt` dans
l'archive, ce qui est rarement souhaité (chemins non portables, voire
dangereux à l'extraction).

**R4.** `zip-slip` désigne une archive contenant des entrées dont le
chemin remonte hors du dossier cible (par exemple
`../../etc/passwd`). Une extraction naïve écrit alors **en dehors**
de la zone prévue. Pour se protéger : résoudre chaque chemin
destination et vérifier qu'il reste sous le dossier cible (par
exemple avec `Path.is_relative_to`). Depuis Python 3.12, `zipfile` et
`tarfile` intègrent des filtres ; pour `tarfile.extractall`, préciser
`filter="data"`.

**R5.** Une archive `.tar.gz` est une archive `.tar` **passée
intégralement** dans `gzip`. Pour y ajouter un fichier, il faudrait
décompresser l'archive, y ajouter l'entrée, puis recompresser le
tout : ce n'est pas un ajout en place. Le mode `"a"` n'est donc
disponible que sur les `.tar` **non compressés**. En pratique, on
recrée l'archive depuis le contenu (par exemple après extraction
temporaire) ou on utilise `.zip` qui, lui, supporte l'ajout en place.

**R6.** Le format `.tar` est **séquentiel** : les fichiers sont mis
bout à bout, sans index. Et `gzip` compresse l'archive entière comme
un seul flux — il faut donc **décompresser** tout ce qui précède le
fichier cherché pour atteindre ses octets. À l'inverse, `.zip`
compresse chaque entrée **indépendamment** et tient une table des
matières à la fin du fichier, ce qui permet d'aller directement à la
bonne position et de ne décompresser que l'entrée demandée.
