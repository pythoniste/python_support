# Quiz — dossier 04_Palindrome

Six questions pour vérifier qu'on sait **choisir** entre les cinq
transports vus dans le dossier.

## Questions

**Q1.** Quelle est la principale différence entre les paires 1 et 3
(raw TCP vs socketserver TCP) **du point de vue du développeur** ?

**Q2.** Pourquoi la paire 5 (Bottle) n'a-t-elle pas de mot-clé `stop`
intégré au protocole ?

**Q3.** En UDP raw (paire 2), le serveur réutilise la même socket
pour tous les messages. En TCP socketserver (paire 3), il y a une
nouvelle connexion par message. Pourquoi cette différence ?

**Q4.** Le client Bottle (`10_bottle_clt.py`) n'a quasiment aucun
code réseau visible. Pourquoi ?

**Q5.** Pour un service qui doit absolument répondre à 99,9 % des
requêtes, lequel des cinq transports privilégier ? Et lequel
**éviter** ?

**Q6.** Si on veut interopérer avec un client JavaScript dans un
navigateur, quels transports de ce dossier sont possibles ?

---

## Réponses

**R1.** En raw, le développeur gère explicitement la boucle
`accept → recv → traitement → send → close`. En socketserver, le
framework s'en charge ; le développeur n'écrit qu'une classe
`Handler` avec une méthode `handle()`. La logique métier est la même
(`palindrome.py`), seul le code de transport diffère.

**R2.** Parce que **mélanger administration et métier dans le
protocole applicatif est un anti-pattern REST**. En HTTP, l'arrêt
d'un serveur est une opération de gestion externe (signal SIGTERM,
endpoint admin protégé par auth, orchestrateur Kubernetes, etc.). Le
client REST ne doit pas pouvoir mettre le service à genoux avec
une requête publique.

**R3.** UDP n'a **pas de notion de connexion** : le serveur lit
simplement le datagramme suivant sur sa socket existante, peu importe
qui l'envoie. TCP avec `StreamRequestHandler` exécute `handle()` une
fois par connexion, puis ferme — c'est le contrat du framework. Le
client doit donc rouvrir une connexion pour chaque échange (sauf à
mettre une boucle `while` dans `handle()`, cf. dossier 03/atelier 3).

**R4.** Parce que **HTTP est un protocole standard**, parfaitement
encapsulé par la bibliothèque `requests`. Tout le travail (résolution
DNS, connexion TCP, négociation HTTP, parsing de la réponse) est
délégué. Le code utile se limite à construire l'URL et appeler
`.json()` sur la réponse.

**R5.** **À privilégier : TCP** (raw, socketserver, ou Bottle/HTTP) —
livraison garantie, ordre préservé. **À éviter : UDP** — pas de
garantie de livraison ni d'ordre. UDP n'est légitime que si l'on peut
*tolérer* des pertes (streaming, télémétrie haute fréquence) ou si
l'on a une couche applicative de retry (DNS, NFS, QUIC).

**R6.** Uniquement **HTTP/REST** (paire 5). Les navigateurs n'ouvrent
pas de sockets TCP/UDP raw ; ils parlent HTTP et WebSocket. C'est
**l'avantage majeur de REST** pour exposer un service à un public web.
