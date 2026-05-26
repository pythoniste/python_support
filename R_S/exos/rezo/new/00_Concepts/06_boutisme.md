# 06 — Boutisme (endianness)

## 6.1 Le problème

Un entier sur plusieurs octets peut être stocké dans deux ordres
opposés. Pour la valeur `1` sur 4 octets :

```
big-endian    : 00 00 00 01     (octet de poids fort en premier)
little-endian : 01 00 00 00     (octet de poids faible en premier)
```

Les deux conventions existent depuis les années 1970. Les processeurs
x86, x86-64 et ARM (par défaut) utilisent **little-endian**. Les
protocoles réseau utilisent traditionnellement **big-endian**, appelé
pour cette raison **« network byte order »**.

## 6.2 Pourquoi ça nous concerne

Tant qu'on échange des chaînes en UTF-8 (octet par octet), aucun
problème : l'ordre des octets est implicitement préservé.

**Dès qu'on utilise un protocole binaire** (par exemple
`int.to_bytes(4, "big")` comme dans `05_Random/conv2.py`), émetteur et
récepteur doivent se mettre d'accord. Si l'un encode en big-endian et
l'autre décode en little-endian, on lit un nombre faux **sans erreur
visible**.

## 6.3 Les outils Python

### Méthodes des entiers

```python
n = 1
n.to_bytes(4, "big")     # b'\x00\x00\x00\x01'
n.to_bytes(4, "little")  # b'\x01\x00\x00\x00'

int.from_bytes(b"\x00\x00\x00\x01", "big")     # 1
int.from_bytes(b"\x00\x00\x00\x01", "little")  # 16777216
```

### Module `struct`

Permet d'encoder plusieurs valeurs à la fois selon un format compact :

```python
import struct
struct.pack(">I", 1)   # b'\x00\x00\x00\x01'   (> = big-endian)
struct.pack("<I", 1)   # b'\x01\x00\x00\x00'   (< = little-endian)
struct.pack("!I", 1)   # b'\x00\x00\x00\x01'   (! = network = big)
```

Le préfixe `!` est à privilégier dans le code réseau : il indique
explicitement l'intention « network byte order ».

| Format | Type C   | Taille | Notes                |
|--------|----------|--------|----------------------|
| `b`    | int8     | 1      | signé                |
| `B`    | uint8    | 1      | non signé            |
| `h`    | int16    | 2      | signé                |
| `H`    | uint16   | 2      | non signé            |
| `i`    | int32    | 4      | signé                |
| `I`    | uint32   | 4      | non signé            |
| `q`    | int64    | 8      | signé                |
| `Q`    | uint64   | 8      | non signé            |
| `f`    | float32  | 4      | IEEE 754             |
| `d`    | float64  | 8      | IEEE 754             |

## 6.4 Convention

Sauf raison contraire :

- **Toujours utiliser big-endian** (« network byte order ») dans un
  protocole binaire.
- **Toujours utiliser le préfixe `!`** dans les chaînes de format
  `struct`, pour rendre l'intention explicite.

## 6.5 À retenir

- Big-endian = poids fort en premier ; little-endian = poids faible en premier.
- Convention réseau : big-endian (« network byte order »).
- `int.to_bytes(N, "big")` ou `struct.pack("!I", n)` en Python.
- Tout protocole binaire **doit** documenter son boutisme.

## Démo

Exécuter `06_demo_boutisme.py`.
