# Exercices de validation — dossier 00_Concepts

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer à `01_Sockets_bas_niveau/`. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la seule constante différente entre la création
d'un socket TCP et la création d'un socket UDP en Python ?

**Q2.** Si l'émetteur appelle deux fois `send(b"hello")` sur un socket
TCP, combien d'appels `recv(1024)` côté récepteur sont nécessaires pour
récupérer la totalité ? Justifier.

**Q3.** Un serveur TCP manipule deux sockets pendant son
fonctionnement. Lesquels, et à quoi servent-ils chacun ?

**Q4.** Que renvoient les expressions suivantes, et pourquoi
diffèrent-elles ?

```python
struct.pack(">I", 1)
struct.pack("<I", 1)
```

**Q5.** Sur un socket configuré avec `setblocking(False)`, quel type
d'exception est levé lorsqu'on appelle `recv()` sans données disponibles ?

**Q6.** Que fait `sock.sendto(b"x", ("127.0.0.1", 1))` quand le port 1
n'a aucun service en écoute ? Comparer avec le comportement équivalent
en TCP.

---

## Réponses

**R1.** Le second argument de `socket.socket()` :
`socket.SOCK_STREAM` pour TCP, `socket.SOCK_DGRAM` pour UDP.

**R2.** **Indéterminé**. TCP ne préserve pas les frontières d'envoi :
les 10 octets peuvent arriver en 1, 2 ou plusieurs `recv()`. C'est
exactement la raison pour laquelle un mécanisme de framing
(délimiteur, longueur préfixée ou longueur fixe) est nécessaire.

**R3.** Le socket **écouteur** (résultat de `socket() + bind() +
listen()`) qui reste passif et accepte les nouvelles connexions ; et
le socket **connecté** renvoyé par `accept()`, dédié à un client
particulier, sur lequel se font les `recv` et `send`. Les deux doivent
être fermés.

**R4.** `b'\x00\x00\x00\x01'` et `b'\x01\x00\x00\x00'`. Le préfixe
`>` encode en big-endian (octet de poids fort en premier), `<` en
little-endian. Les deux conventions stockent la même valeur dans des
ordres inverses.

**R5.** `BlockingIOError` (un alias d'`OSError` avec
`errno = EAGAIN` / `EWOULDBLOCK`).

**R6.** En UDP, `sendto` **réussit silencieusement** : aucune
confirmation n'est attendue, le datagramme part dans le réseau et
sera perdu côté destination. En TCP, `connect` lève immédiatement
`ConnectionRefusedError` car la poignée de main est rejetée par le
système distant. Voir `03_demo_tcp_vs_udp.py`.
