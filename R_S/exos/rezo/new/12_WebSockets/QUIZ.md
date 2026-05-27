# Quiz — dossier 12_WebSockets

## Questions

**Q1.** Quelle est la différence essentielle entre HTTP et
WebSocket ?

**Q2.** Comment se fait la **bascule** de HTTP vers WebSocket ?

**Q3.** Pourquoi le protocole WebSocket **masque-t-il** les payloads
envoyés par le client ?

**Q4.** Quand utiliser WebSocket plutôt que HTTP/REST ? Donner
trois exemples.

**Q5.** Quel framework `pip install` pour faire du WebSocket en
Python ? Pourquoi pas la stdlib ?

**Q6.** Différence entre WebSocket et **Server-Sent Events (SSE)** ?

---

## Réponses

**R1.** HTTP est **requête / réponse** unidirectionnel : le client
parle, le serveur répond, fin. WebSocket est **bidirectionnel et
persistant** : une seule connexion TCP qui survit, dans laquelle
les deux extrémités peuvent envoyer à tout moment.

**R2.** Le client envoie une **requête HTTP avec en-tête
`Upgrade: websocket`** et `Sec-WebSocket-Key: <token aléatoire>`.
Le serveur accepte avec `101 Switching Protocols` et un
`Sec-WebSocket-Accept` calculé sur la clé. À partir de là, la
même connexion TCP transporte des frames WebSocket.

**R3.** Pour **éviter les attaques de cache poisoning** sur les
proxies HTTP intermédiaires qui n'auraient pas été mis à jour pour
WS. Le masque XOR aléatoire empêche un attaquant de forger des
frames qui ressembleraient à des requêtes HTTP. C'est une mesure
historique de la RFC 6455.

**R4.** (a) **Chat / messagerie** en temps réel. (b) **Notifications
push** depuis le serveur. (c) **Données live** : cours de bourse,
trafic IoT, jeux multijoueurs. Tout cas où le serveur doit pousser
sans que le client redemande.

**R5.** `pip install websockets` (async) ou `websocket-client`
(sync). La stdlib n'inclut pas WebSocket car ce n'est pas un
protocole "fondamental" — il s'agit d'une couche au-dessus de TCP.
La bibliothèque `websockets` est le standard de facto, async-first.

**R6.** **SSE** est unidirectionnel (serveur → client uniquement),
sur HTTP standard, donc plus simple côté infra (passe à travers
les proxies, compatible HTTP/2). **WebSocket** est bidirectionnel,
plus puissant mais nécessite un parsing/framing custom et passe
moins bien à travers certains équipements. Pour des notifications
unidirectionnelles, SSE est souvent suffisant et plus simple.
