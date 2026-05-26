# 03_Socketserver — Le framework standard de Python

Le dossier 02 (paire 3) a montré que `socket.makefile()` encapsule la
lecture/écriture par lignes. Ce dossier va un cran plus loin : la
bibliothèque standard fournit un **framework** qui encapsule aussi la
boucle d'`accept`, la gestion des connexions, la fermeture propre, et
la délégation à un handler par client. C'est le module
**`socketserver`**.

L'objectif n'est pas d'apprendre une nouvelle API — c'est de voir que
**tout ce qu'on a écrit manuellement dans les dossiers 01 et 02 est
déjà fourni**, et que le code utile devient extrêmement court.

## Plan

| Fichier         | Rôle                                            |
|-----------------|-------------------------------------------------|
| `01_tcpsrv.py`  | Serveur TCP via `TCPServer` + `StreamRequestHandler` |
| `02_tcpclt.py`  | Client TCP (raw, une connexion par message)     |
| `03_udpsrv.py`  | Serveur UDP via `UDPServer` + `DatagramRequestHandler` |
| `04_udpclt.py`  | Client UDP (raw)                                |

Toutes les paires utilisent le port `8808`.

## Comment exécuter

Le serveur tourne en boucle infinie ; **on l'arrête avec Ctrl-C** (il
n'y a plus de mot-clé `stop` ici — voir l'atelier 7 pour l'ajouter,
et le dossier `07_Concurrence/` pour comprendre pourquoi c'est lié
à la concurrence).

```
# Terminal 1
python3 01_tcpsrv.py

# Terminal 2
python3 02_tcpclt.py
```

## Ce qui est démontré

- **`TCPServer + StreamRequestHandler`** : la boucle d'accept et la
  bufferisation `recv/send` sont entièrement gérées par le framework.
  Le code utile du serveur tient en ~6 lignes.
- **`self.rfile` / `self.wfile`** : ce sont exactement les objets
  retournés par `socket.makefile()` (cf. dossier 02, paire 3).
- **Un handler par connexion** : le framework instancie une classe
  `Handler` par client. C'est le modèle classique des serveurs
  textuels (HTTP/1, SMTP, IRC, FTP…).
- **`DatagramRequestHandler`** pour UDP : même principe, adapté à
  l'absence de connexion.

## Ce qui est volontairement reporté

- **Concurrence** (`ThreadingMixIn`, `ForkingMixIn`) : la boucle reste
  séquentielle ici, un seul client à la fois. L'atelier 5 et le
  dossier `07_Concurrence/` traitent la suite.
- **Stop propre** : sans concurrence, on ne peut pas appeler
  `server.shutdown()` depuis un handler sans deadlock. L'atelier 7
  montre l'astuce (un thread auxiliaire), le dossier 07 explique
  pourquoi.

## Comparaison avec les dossiers précédents

| Aspect             | 01_Sockets_bas_niveau | 02_Framing (paire 3) | 03_Socketserver |
|--------------------|-----------------------|----------------------|-----------------|
| Boucle d'`accept`  | manuelle              | manuelle             | **framework**   |
| Fermeture connexion | `with` explicite     | `with` explicite     | **framework**   |
| Framing            | naïf (recv simple)    | makefile + readline  | makefile + readline (auto) |
| Lignes de code utile (serveur) | ~25            | ~25                  | **~10**         |

## Validation et mise en pratique

- `QUIZ.md` : 6 questions courtes.
- `EXERCICES.md` : 8 ateliers, du simple echo au protocole binaire
  multi-client.
