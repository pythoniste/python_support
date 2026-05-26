# Exercices pratiques — dossier 00_Concepts

Une fois les sept modules lus et leurs démos exécutées, ces huit ateliers
permettent de **mettre en pratique** les concepts dans des scripts
courts. Aucun serveur tiers n'est requis : tout se fait en local, via
`socket.socketpair()` quand un échange est nécessaire.

Chaque atelier indique :

- le module concerné ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue (lorsque pertinent).

Les corrigés peuvent être fournis dans un dossier dédié `CORRIGES/`
sur demande, une fois les ateliers tentés.

---

## Atelier 1 — Inspecter un nom de domaine  ★
*Module 01 — adresses, DNS*

Écrire un script `atelier_01.py` qui prend un nom de domaine en
argument de ligne de commande et affiche :

- toutes les adresses IPv4 trouvées ;
- toutes les adresses IPv6 trouvées ;
- le nombre total d'enregistrements.

**Indices**

- `sys.argv[1]` pour récupérer l'argument.
- `socket.getaddrinfo(nom, None)` retourne tous les enregistrements.
- Filtrer sur `famille == socket.AF_INET` (IPv4) ou
  `socket.AF_INET6`.

**Exemple de sortie attendue**

```
$ python3 atelier_01.py google.com
IPv4 : 142.250.179.110
IPv6 : 2a00:1450:4007:80f::200e
Total : 2 enregistrement(s)
```

---

## Atelier 2 — Trois familles de sockets  ★
*Module 02 — qu'est-ce qu'un socket*

Écrire un script qui crée trois sockets dans un même `with` imbriqué :

- `AF_INET / SOCK_STREAM` (TCP)
- `AF_INET / SOCK_DGRAM` (UDP)
- `AF_UNIX / SOCK_STREAM` (socket Unix local)

Pour chacun, imprimer `fileno()`, `family.name`, `type.name`.

**Question** : si on instancie les trois en parallèle (un seul `with`
imbriqué), les trois `fileno()` doivent-ils être nécessairement
différents ? Pourquoi ?

---

## Atelier 3 — TCP ou UDP, au choix  ★★
*Module 03 — TCP vs UDP*

Écrire un script paramétré par `argparse` avec un argument
`--protocole tcp|udp` qui tente de contacter `127.0.0.1:1` avec un
timeout de 1 seconde. Le script doit afficher clairement le résultat
opposé selon le mode choisi :

- TCP → « connexion refusée » ;
- UDP → « datagramme envoyé, aucune confirmation possible ».

**Indices**

- `argparse.ArgumentParser` avec `choices=["tcp", "udp"]`.
- `socket.SOCK_STREAM` pour TCP, `socket.SOCK_DGRAM` pour UDP.
- En TCP, attraper `ConnectionRefusedError` ; en UDP, vérifier que
  `sendto()` retourne le nombre d'octets envoyés et ne lève rien.

---

## Atelier 4 — Anatomie d'une paire de sockets  ★
*Module 04 — cycle de vie*

`socket.socketpair()` retourne deux sockets **déjà connectés**.
Imprimer pour chacun :

- `fileno()` ;
- `getsockname()` (adresse locale) ;
- `getpeername()` (adresse du correspondant).

**Question** : pourquoi les adresses sont-elles vides (`''`) ?
Que signifie « anonyme » dans ce contexte, et en quoi cela diffère-t-il
d'un socket TCP/IPv4 classique ?

---

## Atelier 5 — Implémenter readline à la main  ★★
*Module 05 — framing par délimiteur*

Écrire une fonction `recv_ligne(sock) -> bytes` qui lit **octet par
octet** jusqu'à rencontrer `b"\n"`, et renvoie la ligne **sans** le
délimiteur. Tester avec un `socketpair` en envoyant
`b"bonjour\nle monde\n"` côté émetteur, puis en appelant `recv_ligne`
deux fois côté récepteur.

**Indices**

- `sock.recv(1)` lit exactement un octet.
- Accumuler dans une liste de morceaux, puis `b"".join(...)`.
- Arrêter la boucle dès qu'on voit `b"\n"`.

**Bonus** : pourquoi est-ce inefficace en pratique ? Quelle structure
de données permettrait d'optimiser (sans changer la sémantique) ?

---

## Atelier 6 — Le protocole à préfixe de longueur  ★★★
*Modules 05 + 06 — framing + boutisme*

Écrire deux fonctions :

```python
def envoyer_message(sock, message: bytes) -> None: ...
def recevoir_message(sock) -> bytes: ...
```

implémentant un protocole où chaque message est précédé de sa longueur
encodée sur **4 octets en network byte order**.

Tester avec un `socketpair` :

1. envoyer trois messages de tailles différentes (par exemple
   `b"a"`, `b"bb"`, `b"ccc"`) ;
2. relire les trois et vérifier qu'on retrouve exactement les
   originaux, dans le même ordre.

**Indices**

- `struct.pack("!I", n)` pour encoder la longueur.
- `struct.unpack("!I", quatre_octets)[0]` pour la décoder.
- Réutiliser `recv_exactement` du module 05.

---

## Atelier 7 — Trois manières de lire le même nombre  ★
*Module 06 — boutisme*

Sur le réseau, on reçoit les quatre octets bruts
`b"\x00\x00\x00\x2A"`. Calculer en Python :

- la valeur lue en **big-endian** (network byte order) ;
- la valeur lue en **little-endian** ;
- la valeur obtenue en **inversant** d'abord l'ordre des octets puis
  en lisant le résultat en big-endian.

Imprimer les trois et vérifier que les valeurs 2 et 3 sont identiques.
Pourquoi ?

---

## Atelier 8 — Mesurer deux modes d'attente  ★★
*Module 07 — bloquant / non bloquant*

Écrire un script qui mesure (avec `time.perf_counter()`) la durée
d'un `recv()` sur un `socketpair` vide :

1. avec `settimeout(0.2)` ;
2. avec `setblocking(False)`.

Vérifier que le premier prend approximativement 200 ms et le second
quasiment 0 ms.

**Question** : pourquoi ne peut-on pas tester aussi simplement le mode
bloquant par défaut (sans timeout) ? Que faudrait-il pour le faire ?

---

## Pour aller plus loin

Une fois ces ateliers terminés, on est prêt à attaquer le code réel
des dossiers suivants — où les concepts seront mis en œuvre dans des
clients et serveurs complets.
