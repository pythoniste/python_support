# Quiz — dossier 01_Sockets_bas_niveau

Six questions pour auto-évaluer la maîtrise de l'API socket
bas-niveau, après lecture et exécution des quatre fichiers du dossier.

## Questions

**Q1.** À quoi sert `listen()` côté serveur TCP, et en quoi diffère-t-elle
de `accept()` ?

**Q2.** Pourquoi le code serveur TCP utilise-t-il **deux** instructions
`with` imbriquées, alors que le code serveur UDP n'en utilise qu'une ?

**Q3.** Différence entre `socket.send(data)` et `socket.sendall(data)` ?
Lequel utilise-t-on dans ce dossier, et pourquoi ?

**Q4.** Côté client UDP, on n'appelle jamais `connect()`. Comment fait-on
alors pour préciser à qui on envoie le datagramme ?

**Q5.** L'argument `5` dans `listen(5)` représente quoi exactement ?

**Q6.** `accept()` retourne deux valeurs (`connexion, adresse_client`).
Décrire le rôle de chacune.

---

## Réponses

**R1.** `listen(n)` fait passer le socket de l'état « non attaché » à
l'état **passif** : il marque le socket comme prêt à recevoir des
connexions entrantes, et configure une file d'attente de taille `n`.
`accept()` consomme une connexion de cette file (ou bloque en attente
si la file est vide) et renvoie **un nouveau socket** dédié à ce
client.

**R2.** Le serveur TCP a deux sockets ouverts simultanément :
l'**écouteur** (sortie de `socket() + bind() + listen()`) et le
socket **connecté** à chaque client (sortie de `accept()`). Chacun
doit être fermé. UDP n'a pas de notion de connexion, donc un seul
socket suffit.

**R3.** `send()` peut écrire **moins** d'octets que demandé (renvoie
le nombre effectif). `sendall()` boucle jusqu'à tout écrire (ou lève
une exception). On utilise `sendall()` dans ce dossier pour ne pas
avoir à gérer manuellement les envois partiels — concept lié au
framing, traité au dossier 02.

**R4.** En passant l'adresse cible à chaque appel `sendto(data,
adresse)`. C'est la signature même de `sendto` qui réclame cet
argument supplémentaire par rapport à `send`.

**R5.** La taille **maximale de la file d'attente** des connexions
acceptées par le système mais pas encore consommées par `accept()`.
Au-delà, les nouvelles tentatives sont refusées par le système (le
client reçoit `ConnectionRefusedError`).

**R6.** `connexion` est un nouveau socket, dédié à l'échange avec
ce client précis (c'est sur lui qu'on fait `recv` et `send`).
`adresse_client` est le tuple `(hôte, port)` du client distant, utile
pour la traçabilité ou pour décider d'accepter/refuser selon
l'origine.
