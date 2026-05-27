# Quiz de validation — dossier 09_Environnement

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer au chapitre suivant. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la différence pratique entre `os.environ["HOME"]`
et `os.environ.get("HOME", "/tmp")` ? Quand préférer chaque forme ?

**Q2.** Un script Python exécute `os.environ["FOO"] = "bar"`, puis
s'arrête. De retour dans le shell qui a lancé le script, on tape
`echo $FOO`. Que voit-on, et pourquoi ?

**Q3.** Après `config.read("app.ini")`, on écrit
`port = config["database"]["port"]`. Quel est le type de `port`, et
comment obtenir un vrai `int` à la place ?

**Q4.** Pourquoi `tomllib.load` exige-t-il que le fichier soit ouvert
en mode binaire (`"rb"`) plutôt qu'en mode texte ?

**Q5.** Sur quelle version de Python le module `tomllib` est-il
disponible dans la bibliothèque standard ? Que faire sur les versions
antérieures ?

**Q6.** Trois sources définissent la même option `port` :
le fichier de configuration la fixe à `5000`, la variable
d'environnement `APP_PORT` à `6000`, et la ligne de commande passe
`--port 7000`. Quelle valeur le programme doit-il utiliser, et
pourquoi cet ordre est-il conventionnel ?

---

## Réponses

**R1.** `os.environ["HOME"]` lève une `KeyError` si la variable est
absente. `os.environ.get("HOME", "/tmp")` renvoie `"/tmp"` à la place,
sans exception. On utilise la première forme quand l'absence est une
**vraie erreur** qui doit interrompre le programme ; la seconde quand
on tolère l'absence avec une valeur par défaut raisonnable.

**R2.** `echo $FOO` n'affiche **rien** (ligne vide). Les modifications
de `os.environ` ne sont visibles que dans le **processus Python** en
cours et dans ses sous-processus. Elles ne remontent jamais au shell
parent : c'est une règle fondamentale d'Unix, un enfant ne peut pas
modifier l'environnement de son parent.

**R3.** Le type est `str` (chaîne de caractères) — `configparser` lit
toujours en chaîne. Pour obtenir un `int`, utiliser
`config.getint("database", "port")`. De même `getfloat` et
`getboolean` pour les autres types natifs.

**R4.** TOML impose **UTF-8** pour ses fichiers, et `tomllib` veut
contrôler lui-même le décodage des octets pour respecter strictement
la spécification (notamment la gestion des fins de ligne et des
caractères de contrôle). Ouvrir en mode texte délèguerait ce décodage
à Python avant l'analyse, ce qui pourrait introduire des
incohérences. D'où l'exigence de `open(..., "rb")`.

**R5.** Depuis **Python 3.11**. Sur Python 3.10 ou antérieur,
`tomllib` n'existe pas dans la stdlib ; il faut installer le paquet
externe `tomli` (qui a la même API).

**R6.** La valeur retenue est **`7000`**, fournie par la ligne de
commande. L'ordre conventionnel est
**CLI > env > fichier > défaut**. La CLI gagne parce qu'elle
représente une intention explicite et immédiate de l'utilisateur.
L'environnement passe avant le fichier parce qu'il reflète le
contexte d'exécution (orchestrateur, conteneur, session) qui doit
pouvoir surcharger ce qui est embarqué. Le défaut est le filet de
sécurité quand aucune source ne fournit la valeur.
