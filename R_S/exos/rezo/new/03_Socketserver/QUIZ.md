# Quiz — dossier 03_Socketserver

Six questions pour vérifier que le passage au framework `socketserver`
est bien compris.

## Questions

**Q1.** À quoi correspondent exactement `self.rfile` et `self.wfile`
dans une classe `StreamRequestHandler` ?

**Q2.** Quelle est la différence entre `BaseRequestHandler` et
`StreamRequestHandler` ?

**Q3.** Pourquoi `handle()` est-il appelé **une fois par connexion** ?
Que doit-on faire si on veut échanger plusieurs messages dans la
même connexion ?

**Q4.** Comment passe-t-on d'un serveur `TCPServer` séquentiel à un
serveur capable de traiter plusieurs clients en parallèle ?

**Q5.** Le serveur de ce dossier (sans mixin de concurrence) traite-t-il
les clients en parallèle ou en série ? Que se passe-t-il si un client
arrive pendant qu'un autre est en cours de traitement ?

**Q6.** Pourquoi ne peut-on pas appeler `self.server.shutdown()`
directement depuis `handle()` ?

---

## Réponses

**R1.** À exactement les objets retournés par `socket.makefile()` en
mode binaire : `"rb"` pour `rfile`, `"wb"` pour `wfile`. C'est ce qui
permet d'utiliser `readline()` et `write()` avec la même sémantique
qu'un fichier ordinaire.

**R2.** `BaseRequestHandler` donne accès au socket brut via
`self.request` (sur lequel on appelle `recv` / `send` à la main).
`StreamRequestHandler` étend `BaseRequestHandler` en construisant
automatiquement `rfile`/`wfile` à partir de `makefile()`. On choisit
`BaseRequestHandler` pour un protocole binaire à préfixe de longueur
(par exemple), `StreamRequestHandler` pour un protocole textuel ligne
par ligne.

**R3.** C'est le **contrat** du framework : il accepte une connexion,
instancie une classe handler, appelle `handle()`, puis ferme la
connexion à la sortie. Pour échanger plusieurs messages dans la
même connexion, mettre une boucle `while True` à l'intérieur de
`handle()` qui lit jusqu'à EOF (voir atelier 3).

**R4.** Par mixin : déclarer une classe qui hérite à la fois de
`socketserver.ThreadingMixIn` (ou `ForkingMixIn`) **et** de
`socketserver.TCPServer`. L'ordre compte : le mixin doit être en
premier. Voir atelier 5.

**R5.** En **série**. `TCPServer.serve_forever` attend la fin du
handler courant (donc la fermeture de la connexion en cours) avant
d'accepter une nouvelle connexion. Si un deuxième client arrive
pendant ce traitement, sa connexion **attend dans la file d'écoute**
(taille fixée par `request_queue_size`, défaut 5). Au-delà, le client
reçoit `ConnectionRefusedError`.

**R6.** Parce que `shutdown()` doit obligatoirement être appelée
depuis un thread **différent** de celui qui exécute `serve_forever()`,
sous peine de deadlock. Comme `handle()` s'exécute dans le même
thread que `serve_forever()` (en l'absence de mixin de concurrence),
un appel direct à `self.server.shutdown()` provoque un blocage
définitif. Solution canonique : déléguer à un thread auxiliaire
(`threading.Thread(target=self.server.shutdown).start()`), traité
dans l'atelier 7.
