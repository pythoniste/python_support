# 02 — Encodage et fichier source

## 2.1 Pourquoi parler d'encodage ?

Un fichier `.py` n'est rien d'autre que du **texte** stocké en octets
sur le disque. Pour qu'un caractère comme `é` ou `€` y soit représenté
correctement, il faut convenir d'un **encodage** : la règle qui dit
comment un caractère devient une suite d'octets.

| Encodage    | Particularité                                   |
|-------------|-------------------------------------------------|
| ASCII       | 128 caractères seulement, pas d'accents         |
| Latin-1     | 256 caractères, accents occidentaux             |
| UTF-8       | Universel, compatible ASCII, taille variable    |

UTF-8 est devenu le standard de fait sur le Web et dans tous les
systèmes modernes. Un `é` y est codé sur **deux octets**
(`0xC3 0xA9`), un `€` sur trois, un emoji sur quatre, mais une lettre
ASCII reste sur un seul octet.

## 2.2 Python 3 : UTF-8 par défaut

Depuis Python 3, l'encodage par défaut du code source est **UTF-8**.
On peut donc écrire sans rien préciser :

```python
message = "Café — prix : 2,50 €"
print(message)
```

Aucune déclaration d'encodage n'est nécessaire.

## 2.3 L'ancienne déclaration `# -*- coding: utf-8 -*-`

Dans du vieux code Python 2 (ou Python 3 ancien), on rencontre encore :

```python
# -*- coding: utf-8 -*-
```

Cette ligne, héritée d'Emacs, demandait explicitement à l'interpréteur
de lire le fichier en UTF-8. Sous Python 3 elle est **superflue** : le
défaut est déjà UTF-8. On peut la supprimer sans rien casser dans tout
fichier Python 3 moderne.

## 2.4 `str` et `bytes` : aperçu rapide

Python distingue deux types fondamentaux pour représenter du texte :

| Type     | Contient                       | Exemple littéral    |
|----------|--------------------------------|---------------------|
| `str`    | Du texte (suite de caractères) | `"café"`            |
| `bytes`  | Une suite d'**octets** bruts   | `b"caf\xc3\xa9"`    |

Le passage de l'un à l'autre se fait toujours via un encodage :

```python
>>> "café".encode("utf-8")
b'caf\xc3\xa9'
>>> b'caf\xc3\xa9'.decode("utf-8")
'café'
```

Sur disque, dans une socket, dans un tube : tout est **`bytes`**.
Dans le code Python : on manipule plutôt `str`, et on encode/décode aux
frontières. Cette distinction sera approfondie au chapitre 05 sur les
fichiers et la sérialisation.

## 2.5 Vérifier l'encodage d'un fichier

Sous Unix, la commande `file` donne une bonne indication :

```
$ file mon_script.py
mon_script.py: Python script, UTF-8 Unicode text executable
```

En Python, on peut connaître l'encodage utilisé par défaut pour le
texte sortant :

```python
import sys
print(sys.stdout.encoding)   # 'utf-8' sur la plupart des systèmes
```

## À retenir

- Un fichier source `.py` est lu en **UTF-8** par défaut depuis Python 3.
- `# -*- coding: utf-8 -*-` est un vestige inutile en Python 3 moderne.
- `str` = texte ; `bytes` = octets. On passe de l'un à l'autre avec
  `.encode()` et `.decode()`.
- Sur le réseau et dans les fichiers binaires, tout est `bytes`.
- `sys.stdout.encoding` indique l'encodage utilisé en sortie.

## Démo

Exécuter `02_demo_encodage.py`.
