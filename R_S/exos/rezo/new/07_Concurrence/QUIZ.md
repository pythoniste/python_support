# Quiz — dossier 07_Concurrence

Six questions sur la concurrence en Python.

## Questions

**Q1.** Pourquoi un serveur itératif ne peut-il pas traiter
plusieurs clients à la fois ? Qu'arrive-t-il à un client B qui se
connecte pendant que A est servi ?

**Q2.** Différence fondamentale entre la concurrence par **threads**
et la concurrence par **selectors** (multiplexage I/O) ?

**Q3.** Asyncio est mono-thread. Comment peut-il servir plusieurs
clients **en parallèle** alors ?

**Q4.** Qu'est-ce qu'un programme **« I/O bound »** vs
**« CPU bound »** ? Lequel des deux profite de la concurrence
par threads ou asyncio ?

**Q5.** La **GIL** de Python (Global Interpreter Lock) empêche-t-elle
le parallélisme dans un serveur réseau ?

**Q6.** Pour 5 000 clients connectés simultanément (chat, websockets,
streaming), quelle approche choisir ? Et pour un système où chaque
client fait du **calcul intensif** côté serveur ?

---

## Réponses

**R1.** Parce que l'appel `accept()` n'est invoqué qu'après le
**retour** du traitement du client courant. Pendant le traitement,
les nouvelles connexions sont **mises en attente dans la file
`listen()`** (max 5 par défaut). Au-delà, elles sont refusées
(`ConnectionRefusedError`).

**R2.** **Threads** : parallélisme **préemptif** géré par l'OS.
Un thread par client, code strictement synchrone, l'OS bascule
entre threads. Coût : ~1 Mo de pile par thread, plus le coût
du context-switch.

**Selectors** : parallélisme **coopératif** par multiplexage I/O.
Un seul thread, plusieurs sockets surveillés simultanément par
`select`/`epoll`/`kqueue`. Le code est en callbacks ou boucle
explicite. Très économe en RAM, mais moins lisible.

**R3.** Parce qu'asyncio fait de la **concurrence**, pas du
parallélisme. À chaque `await`, la coroutine **lâche la main** et
la boucle d'événements peut exécuter une autre coroutine prête.
Tout se passe dans le même thread, donc pas de course de données.
C'est utile quand le programme passe son temps à **attendre** (I/O)
plutôt qu'à calculer.

**R4.** Un programme **I/O bound** passe la majeure partie de son
temps à attendre une opération externe (réseau, disque, base de
données). Un programme **CPU bound** passe la majeure partie de
son temps dans des calculs. La concurrence (threads, asyncio) ne
sert qu'aux programmes I/O bound. Pour le CPU bound, il faut du
**vrai parallélisme** : multi-processus (`multiprocessing`) ou
extensions C.

**R5.** **Non.** La GIL empêche deux threads Python d'exécuter du
**bytecode** en même temps. Mais elle est **libérée pendant les
opérations I/O** (`recv`, `send`, `sleep`, accès disque, etc.). Un
serveur réseau passe sa vie à attendre de l'I/O : la GIL n'est
pas un goulot. C'est précisément pourquoi le multi-thread reste
parfaitement viable pour les serveurs Python.

**R6.** 5 000 clients connectés : **asyncio** (chaque "client" est
une coroutine, coûte ~quelques Ko, scalable au million). Calcul
intensif côté serveur : **multi-processus** (un worker par cœur
CPU). On combine souvent : asyncio pour le frontend (accepter les
connexions), processus séparés pour le calcul lourd (via
`concurrent.futures.ProcessPoolExecutor` ou une file de messages
type Redis/Celery).
