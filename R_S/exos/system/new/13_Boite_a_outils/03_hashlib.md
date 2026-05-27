# 03 — `hashlib` : empreintes cryptographiques

## 3.1 Qu'est-ce qu'une empreinte ?

Une **empreinte** (ou *hash*, ou *condensat*) est une chaîne de taille
fixe calculée à partir de données de taille quelconque. Deux propriétés
essentielles :

- **Déterministe** : la même entrée donne toujours la même sortie.
- **Sensible** : changer un seul octet en entrée modifie radicalement
  la sortie.

On s'en sert pour :

- vérifier qu'un fichier n'a pas été altéré (intégrité) ;
- comparer deux fichiers sans lire leur contenu deux fois ;
- détecter des doublons dans un grand ensemble ;
- (avec précaution) stocker des mots de passe — mais ce n'est plus le
  rôle d'`hashlib` seul.

## 3.2 Les algorithmes courants

| Algorithme  | Taille de sortie | Recommandé pour              |
|-------------|------------------|------------------------------|
| `md5`       | 128 bits (32 hex)| Intégrité **non sensible** uniquement |
| `sha1`      | 160 bits (40 hex)| Idem, à éviter pour le neuf  |
| `sha256`    | 256 bits (64 hex)| **Choix par défaut**         |
| `sha512`    | 512 bits (128 hex)| Quand on veut plus de marge |

**MD5 et SHA-1 sont considérés comme cassés en cryptographie** : il
existe des techniques pour fabriquer deux entrées différentes qui ont
la même empreinte. Ils restent acceptables pour de la simple
vérification d'intégrité contre des erreurs accidentelles (un fichier
corrompu au téléchargement), **pas** pour de la sécurité. En cas de
doute, prendre `sha256`.

## 3.3 Utilisation en deux temps

`hashlib` suit toujours le même modèle : on crée un objet, on l'alimente
en octets avec `update()`, puis on demande l'empreinte avec
`hexdigest()`.

```python
import hashlib

h = hashlib.sha256()
h.update(b"hello ")
h.update(b"world")
print(h.hexdigest())
# b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
```

`update()` accepte **uniquement** des `bytes`. Pour une chaîne, il faut
encoder :

```python
h = hashlib.sha256()
h.update("café".encode("utf-8"))
print(h.hexdigest())
```

`hexdigest()` renvoie l'empreinte en hexadécimal lisible. Pour les
octets bruts (plus compact, à stocker dans une base de données par
exemple), il existe aussi `digest()`.

## 3.4 Empreinte d'un fichier — lecture par blocs

Hasher un fichier en chargeant tout en mémoire est une mauvaise idée :
sur un fichier de plusieurs gigaoctets, on sature la RAM. La forme
canonique lit le fichier **par blocs**, exactement comme pour une copie
binaire :

```python
import hashlib

TAILLE_BLOC = 4096   # 4 Kio

def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        while True:
            bloc = f.read(TAILLE_BLOC)
            if not bloc:           # b"" = fin de fichier
                break
            h.update(bloc)
    return h.hexdigest()
```

Ce motif marche sur n'importe quel fichier, quelle que soit sa taille.
À retenir tel quel : on le recopie souvent.

## 3.5 Comparer deux fichiers via leur empreinte

Quand on veut savoir si deux fichiers ont **strictement** le même
contenu :

```python
def memes_fichiers(a, b):
    return sha256_fichier(a) == sha256_fichier(b)
```

Avantage par rapport à une comparaison octet par octet : on peut
calculer l'empreinte d'un côté, la transmettre, et la comparer sur une
autre machine. C'est exactement ce que font les fichiers `SHA256SUMS`
qui accompagnent les images d'OS à télécharger.

## 3.6 Et pour les mots de passe ?

`hashlib.sha256("motdepasse".encode())` n'est **pas** une bonne façon de
stocker un mot de passe : trop rapide à calculer, donc cassable par
force brute. Pour ce cas précis, la stdlib offre une fonction dédiée :

```python
import hashlib, secrets

sel = secrets.token_bytes(16)
empreinte = hashlib.scrypt(b"motdepasse", salt=sel, n=2**14, r=8, p=1)
```

Ce n'est pas le sujet de ce chapitre, mais on retient le principe :
**jamais de simple `sha256` pour un mot de passe**, toujours une
fonction de dérivation lente (`scrypt`, `pbkdf2_hmac`, `argon2`).

## À retenir

- Une empreinte est une chaîne de taille fixe, déterministe, très
  sensible aux modifications de l'entrée.
- `sha256` est le choix par défaut ; `md5`/`sha1` uniquement pour de
  l'intégrité non sensible.
- Le motif `hashlib.sha256()` → `update(bytes)` → `hexdigest()` est la
  base.
- Pour un fichier : lecture par blocs de 4 Kio en mode `"rb"`.
- Pour comparer deux fichiers, comparer leurs empreintes hexadécimales.
- Pour les mots de passe, **jamais** `sha256` seul : `scrypt`,
  `pbkdf2_hmac` ou équivalent.

## Démo

Exécuter `03_demo_hashlib.py`.
