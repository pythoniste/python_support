# 03 — Texte ou binaire : choisir le bon mode

## 3.1 Caractères contre octets

Sur le disque, **tout** est stocké sous forme d'**octets** : des entiers
entre 0 et 255. La distinction entre fichier « texte » et fichier
« binaire » n'existe qu'au niveau de l'interprétation qu'on en fait :

| Vue        | Type Python | Exemple                  |
|------------|-------------|--------------------------|
| Texte      | `str`       | `"café"`                 |
| Octets     | `bytes`     | `b"caf\xc3\xa9"`         |

Ces deux objets représentent **la même chose** sur disque, mais Python
les manipule très différemment.

## 3.2 Mode texte (par défaut)

Quand on ouvre **sans** `"b"` dans le mode :

```python
with open("notes.txt", "r", encoding="utf-8") as f:
    contenu = f.read()
print(type(contenu))   # <class 'str'>
```

Python fait **deux conversions** automatiques :

1. Les octets bruts sont **décodés** selon `encoding=` pour produire
   des `str`.
2. Les sauts de ligne sont **normalisés** (`\r\n` Windows ou `\n` Unix
   deviennent toujours `\n` en mémoire).

C'est confortable pour du texte, dangereux pour du contenu binaire.

## 3.3 Mode binaire (`"b"`)

En ajoutant `"b"` au mode :

```python
with open("logo.png", "rb") as f:
    contenu = f.read()
print(type(contenu))   # <class 'bytes'>
```

Aucune conversion : on récupère les octets **tels quels**. Plus
d'`encoding=` à préciser (ce serait une erreur de le faire — le
binaire n'a pas d'encodage).

## 3.4 Quand passer en binaire ?

La règle pratique :

| Type de fichier                          | Mode à utiliser |
|------------------------------------------|-----------------|
| `.txt`, `.csv`, `.json`, `.py`, `.md`    | texte (`"r"`)   |
| `.png`, `.jpg`, `.pdf`, `.zip`, `.mp3`   | binaire (`"rb"`)|
| `.exe`, `.bin`, n'importe quel format brut | binaire (`"rb"`)|
| Si on hésite ou si l'octet de poids fort compte | binaire   |

Ouvrir un PNG en mode texte est **garanti** de produire des erreurs ou
des données corrompues : la moindre conversion de `\r\n` peut décaler
tout le contenu d'un octet.

## 3.5 Encodages : le cas général

`encoding="utf-8"` est le choix par défaut moderne. Voici les
encodages qu'on croise encore :

| Encodage          | Quand le rencontrer                              |
|-------------------|--------------------------------------------------|
| `utf-8`           | Standard universel, à privilégier                |
| `utf-8-sig`       | UTF-8 avec **BOM**, fréquent sous Windows        |
| `latin-1`         | Vieux fichiers européens, Windows historique     |
| `cp1252`          | « ANSI » Windows occidental                      |
| `ascii`           | Texte garanti sans accents                       |

Le **BOM** (Byte Order Mark) est une suite de 2 ou 3 octets parfois
ajoutée au tout début d'un fichier UTF-8 par certains éditeurs
(notamment sous Windows). En UTF-8, c'est la séquence `\xef\xbb\xbf`.
Si on ouvre un tel fichier avec `encoding="utf-8"`, le BOM apparaît
comme un caractère parasite `﻿` en début de chaîne. La solution
est d'utiliser `encoding="utf-8-sig"`, qui **consomme** le BOM
silencieusement.

## 3.6 Gérer les erreurs d'encodage

Si un fichier prétend être UTF-8 mais contient un octet invalide,
Python lève par défaut une `UnicodeDecodeError` :

```python
with open("douteux.txt", "r", encoding="utf-8") as f:
    contenu = f.read()       # boum si l'encodage est faux
```

L'argument `errors=` change ce comportement :

| Valeur        | Effet sur les octets invalides                          |
|---------------|---------------------------------------------------------|
| `"strict"`    | Lève `UnicodeDecodeError` (défaut)                      |
| `"replace"`   | Remplace par le caractère `?` (`�`), sans erreur   |
| `"ignore"`    | Supprime silencieusement les octets fautifs             |

Exemple résilient pour de l'analyse de logs non garantis :

```python
with open("trace.log", "r", encoding="utf-8", errors="replace") as f:
    for ligne in f:
        ...
```

À utiliser **en connaissance de cause** : on perd alors une partie de
l'information. Pour un traitement critique, mieux vaut détecter le
vrai encodage du fichier que masquer le problème.

## 3.7 Passer de l'un à l'autre

On peut convertir explicitement à tout moment :

```python
texte = "café"
octets = texte.encode("utf-8")     # b'caf\xc3\xa9'
retour = octets.decode("utf-8")    # 'café'
```

`encode` part de `str` vers `bytes`, `decode` fait l'inverse. C'est
exactement ce que Python fait pour nous en mode texte, mais ici on
contrôle.

## À retenir

- Sur disque, tout est **octets** ; le mode texte décode au vol.
- Mode `"r"` / `"w"` : on manipule des `str`, on précise `encoding=`.
- Mode `"rb"` / `"wb"` : on manipule des `bytes`, pas d'encoding.
- Format opaque (image, archive, exécutable) → **toujours** binaire.
- `encoding="utf-8-sig"` consomme le BOM des fichiers UTF-8 d'origine
  Windows.
- `errors="replace"` rend la lecture résiliente aux octets corrompus,
  au prix d'une perte d'information.
- `str.encode(enc)` et `bytes.decode(enc)` font la conversion à la
  main.

## Démo

Exécuter `03_demo_binaire.py`.
