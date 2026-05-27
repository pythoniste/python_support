# Quiz — dossier 06_Etat_et_protocole

Six questions sur le choix stateful vs stateless.

## Questions

**Q1.** En une phrase, qu'est-ce qu'un protocole **stateless** ?
Un protocole **stateful** ?

**Q2.** Citer **deux raisons** pour lesquelles un protocole stateful
est plus fragile qu'un protocole stateless.

**Q3.** Pourquoi un protocole **stateful sur UDP** est-il
particulièrement problématique ? Quel piège du repo original
correspond à ce cas ?

**Q4.** REST est-il par nature stateful ou stateless ? Qu'est-ce que
cela implique pour la scalabilité horizontale (plusieurs serveurs
derrière un load-balancer) ?

**Q5.** Dans quelles situations un protocole stateful reste-t-il
quand même approprié ?

**Q6.** Si on veut conserver l'**impression** d'une session côté
client (panier, authentification…) tout en gardant le protocole
stateless, comment fait-on ?

---

## Réponses

**R1.** **Stateless** : chaque requête est autonome et contient toutes
les informations nécessaires au traitement ; le serveur n'a aucune
mémoire entre requêtes. **Stateful** : le serveur conserve un état
entre les messages d'un même client ; les requêtes successives
construisent ou dépendent de cet état.

**R2.** (a) **Reprise après panne** : si le client ou la connexion
tombe à mi-protocole, l'état accumulé est perdu et le serveur doit
le nettoyer. (b) **Concurrence** : il faut un mécanisme
d'identification pour ne pas mélanger les états de plusieurs
clients, ce qui ajoute de la complexité (sessions, locks, etc.).

**R3.** UDP **n'a pas de notion de connexion**. Le serveur ne peut
borner l'état per-client qu'en l'identifiant par `(IP, port)` — peu
fiable (NAT, DHCP, mobilité) et difficile à expirer proprement. Le
piège du repo original est `mensualite_udpsrv2.py` qui utilisait un
attribut **de classe** comme état : tous les clients écrasaient
mutuellement leurs valeurs.

**R4.** **Stateless par design.** Chaque requête HTTP est autonome.
Implication pour la scalabilité : **deux requêtes consécutives du
même client peuvent être traitées par deux serveurs différents**, sans
nécessité de coordination. C'est ce qui rend possible un déploiement
à 1 000 serveurs derrière un load-balancer sans réflexion sur le
routage.

**R5.** Quand l'état est **fondamentalement** lié à la connexion :
- streaming (audio, vidéo, WebSocket) ;
- protocoles « conversationnels » avec négociation (SMTP, FTP, IRC) ;
- bases de données et transactions ;
- shell distant (SSH).

Dans tous ces cas, la session **est** le service, pas une
optimisation.

**R6.** Le protocole reste stateless ; on déplace l'état dans **un
identifiant que le client renvoie à chaque requête** : cookie de
session, JWT, paramètre d'URL signé… Le serveur garde la vraie
donnée dans un cache ou une base, indexé par ce token. Tout serveur
du pool peut traiter n'importe quelle requête tant qu'il a accès
au stockage partagé.
