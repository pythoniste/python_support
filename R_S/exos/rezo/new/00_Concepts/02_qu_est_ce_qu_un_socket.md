# 02 — Qu'est-ce qu'un socket ?

## 2.1 Un objet, trois caractéristiques

Pour le système d'exploitation, un socket est un **descripteur de
fichier** comme un autre — exactement comme un fichier ouvert ou un
tube (`pipe`). Sous Linux, on peut littéralement le voir dans
`/proc/<pid>/fd/`.

En Python, ce descripteur est encapsulé par la classe `socket.socket`.
Pour le construire, trois arguments :

```python
s = socket.socket(famille, type, protocole)
```

### La famille (`family`)

Indique le type d'adresse utilisé.

| Constante     | Adresse                       |
|---------------|-------------------------------|
| `AF_INET`     | IPv4 (`("127.0.0.1", 8808)`)  |
| `AF_INET6`    | IPv6                          |
| `AF_UNIX`     | chemin de fichier local       |

### Le type

Indique la sémantique des échanges.

| Constante       | Sémantique                                    |
|-----------------|-----------------------------------------------|
| `SOCK_STREAM`   | Flux fiable et ordonné (TCP)                  |
| `SOCK_DGRAM`    | Datagrammes indépendants (UDP)                |
| `SOCK_RAW`     | Paquets bruts (nécessite root)                 |

### Le protocole

Quasiment toujours `0` en pratique : il est déduit du couple
`(famille, type)`. `SOCK_STREAM` + `AF_INET` ⇒ TCP. `SOCK_DGRAM` +
`AF_INET` ⇒ UDP.

## 2.2 La forme canonique

Dans tout le cours, on verra cette ligne **des dizaines de fois** :

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # = TCP/IPv4
```

ou bien :

```python
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # = UDP/IPv4
```

C'est la *seule* différence visible entre un programme TCP et un
programme UDP : la constante de type passée au constructeur.

## 2.3 Toujours via `with`

Un socket est une **ressource OS** ; s'il n'est pas fermé, il fuit. La
bonne forme est :

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    ...   # utiliser s
# À la sortie du bloc, le descripteur est libéré automatiquement.
```

À éviter (mais omniprésent dans les vieux exemples) :

```python
s = socket.socket(...)
...
s.close()   # oublié si une exception se déclenche entre les deux
```

## 2.4 À retenir

- Un socket est un descripteur OS, encapsulé par `socket.socket`.
- Trois axes : `family`, `type`, `proto`.
- `SOCK_STREAM` ↔ TCP, `SOCK_DGRAM` ↔ UDP.
- Toujours l'utiliser dans un bloc `with`.

## Démo

Exécuter `02_demo_socket.py`.
