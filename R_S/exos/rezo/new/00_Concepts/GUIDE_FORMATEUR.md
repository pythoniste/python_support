# Guide formateur — dossier 00_Concepts

Document à l'usage exclusif de l'intervenant. À ne pas distribuer aux
apprenants : il révèle la trame, les pièges anticipés et les corrigés
implicites.

## Vue d'ensemble

| Élément                          | Durée      |
|----------------------------------|------------|
| Introduction                     | 5 min      |
| Module 01 — Adresses             | 10 min     |
| Module 02 — Socket comme objet   | 8 min      |
| Module 03 — TCP vs UDP           | 12 min     |
| Module 04 — Cycle de vie         | 15 min     |
| **Pause**                        | 10 min     |
| Module 05 — Framing              | 18 min     |
| Module 06 — Boutisme             | 10 min     |
| Module 07 — Bloquant             | 8 min      |
| Quiz collectif                   | 12 min     |
| **Pause**                        | 10 min     |
| Ateliers 1 + 2 (échauffement)    | 28 min     |
| Ateliers 3 + 4 (familiarisation) | 31 min     |
| **Pause**                        | 10 min     |
| Atelier 5 (framing)              | 27 min     |
| Atelier 6 (framing + boutisme)   | 33 min     |
| Ateliers 7 + 8 (synthèse)        | 34 min     |
| Conclusion + ouverture           | 5 min      |
| **Total**                        | **4 h 46** |

Format : séance pleine d'environ 4 h 46, avec trois pauses
réparties. Si découpage en deux demi-journées imposé par
l'organisation, le point de coupe le plus équilibré se situe **après
les ateliers d'échauffement (1 + 2)** : séance 1 ≈ 2 h 26, séance 2
≈ 2 h 25 — prévoir 5 min de reprise au début de la séance 2.

## À préparer avant la séance

- Python 3.10+ installé sur le poste de démonstration.
- Vidéoprojecteur ; police de terminal lisible à distance (taille 16+).
- Vérifier au préalable que **les 7 démos** passent sur le poste de
  démo (`for f in 0?_demo_*.py; do python3 "$f"; done`).
- Avoir le fichier `CORRIGES/atelier_*.py` ouvert dans un onglet
  séparé (non projeté) pour piloter les ateliers sans bafouiller.
- Ouvrir `QUIZ.md` et `EXERCICES.md` côté apprenants — sans afficher
  les réponses du quiz.

## Introduction (5 min)

**Message clé à passer** : ce dossier n'est *pas* du code réseau, c'est
le vocabulaire **sans lequel** le code des dossiers suivants ne fera
pas sens. Personne ne lance un serveur ; on regarde, on inspecte, on
mesure.

**Annoncer** : pour chaque module, on lit la théorie, on lance la
démo, on discute. Pas de copie de code en aveugle.

---

## Module 01 — Adresses (10 min)

**Objectif** : donner le vocabulaire `(hôte, port)`, distinguer
`127.0.0.1` et `0.0.0.0`, introduire `getaddrinfo`.

**Points à insister verbalement**

- Un service réseau, c'est *toujours* deux informations : où (l'hôte)
  et qui (le port).
- `127.0.0.1` ≠ `0.0.0.0`. La distinction est souvent source de bugs :
  un serveur qui *écoute sur 127.0.0.1* est invisible depuis
  l'extérieur, même si le pare-feu est ouvert.
- `gethostbyname` est **IPv4 only**. À ne plus utiliser en code neuf.
  Une seule fonction à retenir : `getaddrinfo`.

**Démo** : `01_demo_adresses.py`. Avant de lancer, faire **prédire**
le nombre d'enregistrements de `example.com`. La plupart répondront
« 1 » ou « 2 ». L'observation des 4 entrées (2 IPv4 + 2 IPv6) crée
l'aha moment.

**Piège à anticiper** : sur Debian/Ubuntu, l'hôte local résout sur
`127.0.1.1` (et non `127.0.0.1`) — c'est volontaire (convention pour
les démons qui résolvent leur propre nom). À mentionner si on le voit
dans la sortie, sinon passer.

**Transition** : « On sait *où* parler. Maintenant, *avec quoi*. »

---

## Module 02 — Socket comme objet (8 min)

**Objectif** : démystifier le mot « socket ». Un descripteur OS comme
un fichier.

**Points à insister**

- Sous Linux, on peut **littéralement** voir un socket dans
  `/proc/<pid>/fd/`. Le mot « socket » n'est pas magique.
- Trois axes : `family`, `type`, `proto`. Les deux premiers comptent,
  le troisième est presque toujours `0`.
- **Toujours** `with`. C'est l'occasion d'expliquer que le code de
  référence (`01_Intro/` original) ne le fait pas, et que c'est une
  source de fuite de descripteurs.

**Démo** : `02_demo_socket.py`. Le `fileno = -1` après le `with` est
le moment frappant : la ressource OS a réellement été libérée.

**Transition** : « Un socket, deux choix de sémantique : TCP ou UDP. »

---

## Module 03 — TCP vs UDP (12 min)

**Objectif** : ancrer les deux sémantiques. À la fin du module,
l'apprenant doit pouvoir choisir entre les deux protocoles dans un
cas réel.

**Points à insister**

- Une *seule* constante change dans le code Python : `SOCK_STREAM` vs
  `SOCK_DGRAM`. Tout le reste change ailleurs, dans la sémantique.
- TCP = tuyau, UDP = lettres. Image à utiliser et réutiliser.
- **Frontières** : c'est le mot-clé du module suivant (framing). Le
  glisser ici sans le développer.

**Démo** : `03_demo_tcp_vs_udp.py`. Faire prédire avant le lancement :
« Que se passe-t-il si on parle à un port fermé ? » La symétrie des
deux comportements (refus instantané vs silence absolu) est le point
mémorable.

**Piège à anticiper** : certains apprenants demanderont « pourquoi
choisir UDP si on perd des paquets ? ». Donner trois exemples :
streaming audio (la prochaine trame rattrape), DNS (question/réponse
en un aller-retour, retransmission par la couche applicative), jeux
en ligne (latence > exactitude).

**Transition** : « Avant de coder, on regarde les états par lesquels
passe un socket. »

---

## Module 04 — Cycle de vie (15 min)

**Objectif** : poser les diagrammes serveur/client TCP et UDP côte à
côte. C'est le module le plus dense en vocabulaire (bind, listen,
accept, connect…).

**Points à insister**

- Côté serveur TCP, **deux** sockets coexistent : l'écouteur et le
  socket connecté issu de `accept`. Mal compris, ce point provoque des
  bugs de « le serveur ne répond plus » dès qu'on multiplexe.
- UDP n'a *ni* `listen`, *ni* `accept`. Plus simple en surface, mais
  cela veut dire qu'il faut tout faire à la main (sessions, retries,
  etc.) au niveau applicatif si on en a besoin.
- `bind(0)` = « OS, choisis-moi un port libre ». Très pratique en
  tests automatisés. Le mentionner sans s'attarder.

**Démo** : `04_demo_cycle_de_vie.py`. Insister sur le passage de
`('0.0.0.0', 0)` à `('127.0.0.1', 48xxx)` après `bind()` — c'est la
matérialisation de l'« attachement ».

**Pièges à anticiper**

- « Pourquoi `0.0.0.0` avant `bind` et `127.0.0.1` après ? » →
  Avant bind, le socket n'a pas d'adresse — `0.0.0.0` est la valeur
  par défaut. Après bind, on a explicitement demandé `127.0.0.1`.
- « Pourquoi `listen(5)` ? » → 5 est la taille de la file d'attente
  des connexions non encore acceptées. La valeur exacte importe peu
  ici, on en reparlera à la concurrence.

**Transition** : « Maintenant qu'on sait connecter, **lire des
messages**. Et là, surprise. »

---

## ⏸ Pause (10 min)

## Module 05 — Framing (18 min) — **module crucial**

**Objectif** : éradiquer la croyance que `recv(1024)` reçoit « un
message ». C'est le concept qui rend tout le reste du cours
intelligible.

**Points à insister, dans l'ordre**

1. « TCP est un flux, pas une suite de messages. » À répéter
   littéralement deux fois.
2. Les frontières de `send()` sont **perdues** côté `recv()`.
3. Trois solutions classiques : longueur fixe, délimiteur, préfixe de
   longueur. La deuxième est la plus simple, la troisième la plus
   répandue en pratique.
4. UDP préserve les frontières — mais a ses propres limites.

**Démo** : `05_demo_framing.py`. Insister sur le contraste : trois
`send()` côté émetteur, **un seul** `recv()` côté récepteur, tout
arrive collé. Faire dire à voix haute : « les frontières d'envoi ont
disparu ».

Présenter ensuite la fonction `recv_exactement` du module : c'est
*la* fonction qui sera reprise systématiquement dans la suite du
cours. Faire copier-coller mentalement.

**Pièges à anticiper**

- « Mais ça marche dans `01_Intro/tcpsrv.py` du repo original, non ? »
  → Oui, *en local sur la même machine* avec des messages courts.
  Dès qu'on traverse un vrai réseau, le bug apparaît. C'est
  exactement pour cela que la nouvelle version du dossier 01 utilise
  un délimiteur explicite.
- « Et `readline()` de `socketserver` ? » → Excellente question :
  c'est *exactement* la solution du délimiteur `\n` implémentée par
  Python. On y reviendra au dossier 03.

**Transition** : « Si on choisit le préfixe de longueur, sur combien
d'octets on l'écrit et dans quel sens ? »

---

## Module 06 — Boutisme (10 min)

**Objectif** : comprendre qu'un protocole binaire **doit** documenter
son boutisme, sinon les deux extrémités lisent des nombres différents.

**Points à insister**

- Convention réseau = **big-endian**, alias « network byte order ».
- En Python, deux outils : `int.to_bytes(N, "big")` et
  `struct.pack("!I", n)`. Privilégier le préfixe `!` dans struct, qui
  documente l'intention.
- Tant qu'on est en UTF-8, **aucun** problème de boutisme — l'ordre
  des octets est implicitement préservé.

**Démo** : `06_demo_boutisme.py`. Le bloc final, où les mêmes 4 octets
donnent 167 772 160 ou 10 selon l'interprétation, est le moment
mémorable.

**Piège à anticiper** : « Pourquoi le réseau est en big-endian alors
que x86 est en little-endian ? » → Choix historique : protocoles
réseau définis dans les années 1970 sur des architectures
big-endian. Aujourd'hui c'est une convention figée.

**Transition** : « Dernier concept avant de pouvoir coder pour de vrai :
qu'est-ce qui se passe quand on attend ? »

---

## Module 07 — Bloquant (8 min)

**Objectif** : poser le vocabulaire (bloquant, timeout, non bloquant)
sans entrer dans la concurrence. Tease le dossier 07_Concurrence/.

**Points à insister**

- Par défaut, un socket *bloque*. Pour un programme à un seul client,
  c'est très bien.
- Trois modes : bloquant (défaut), timeout (compromis), non bloquant
  (lève BlockingIOError). Le choix dépend du nombre de sockets à gérer.
- C'est sur le mode non bloquant que reposent `selectors` et `asyncio`.
  Ne pas développer, juste planter le drapeau.

**Démo** : `07_demo_bloquant.py`. 200 ms vs 0 ms est la mesure qui
parle d'elle-même.

**Transition vers le quiz** : « On a tout le vocabulaire. Vérifions. »

---

## Quiz collectif (12 min)

Ouvrir `QUIZ.md` côté apprenants. **Cacher les réponses** (ne
projeter que la section Questions).

Protocole conseillé :

1. 5 min individuelles, papier ou notes locales. Pas d'IDE ouverte.
2. 7 min de correction collective : pour chaque question, prendre
   une réponse au hasard, corriger, faire compléter par la salle.
3. Q4 et Q6 sont les plus discriminantes — y consacrer plus de temps.

Si la salle a manifestement décroché sur le framing, refaire un
passage rapide sur le module 05 — c'est le concept qui doit être
solide avant d'attaquer le code des dossiers suivants.

## ⏸ Pause (10 min)

## Ateliers pratiques guidés (2 h 43, tous en présentiel)

Les huit ateliers sont regroupés par niveau et par sujet pour rythmer
la pratique. Chaque atelier est décomposé en **quatre phases** :
lecture collective de la consigne, résolution par l'apprenant,
projection d'une (ou deux) solution(s) du groupe, puis projection du
corrigé de référence.

| Bloc            | Atelier | Module  | Lecture | Résolution | Projection groupe | Corrigé | Sous-total |
|-----------------|---------|---------|---------|------------|-------------------|---------|------------|
| Échauffement    | 1       | 01      | 1 min   | 10 min     | 2 min             | 1 min   | 14 min     |
| Échauffement    | 2       | 02      | 1 min   | 10 min     | 2 min             | 1 min   | 14 min     |
| Familiarisation | 3       | 03      | 2 min   | 11 min     | 3 min             | 1 min   | 17 min     |
| Familiarisation | 4       | 04      | 1 min   | 10 min     | 2 min             | 1 min   | 14 min     |
| **Pause**       |         |         |         |            |                   |         | **10 min** |
| Cœur            | 5       | 05      | 2 min   | 19 min     | 4 min             | 2 min   | 27 min     |
| Cœur            | 6       | 05 + 06 | 2 min   | 24 min     | 5 min             | 2 min   | 33 min     |
| Synthèse        | 7       | 06      | 1 min   | 10 min     | 2 min             | 1 min   | 14 min     |
| Synthèse        | 8       | 07      | 2 min   | 13 min     | 4 min             | 1 min   | 20 min     |

**Lecture du tableau**

- *Lecture* : lecture à voix haute de la consigne par le formateur,
  avec explicitation des indices. Quelques secondes laissées en plus
  pour les premières questions de cadrage.
- *Résolution* : temps pendant lequel les apprenants codent (en
  individuel ou pair-programming, selon le mode du bloc — voir
  ci-dessous). Le formateur passe entre les postes pour débloquer.
  Ces durées intègrent une marge d'environ 30 % par rapport à un
  rythme « expert » — l'objectif est que la majorité de la salle
  termine, pas une minorité.
- *Projection groupe* : un (ou deux pour les ateliers les plus
  longs) volontaire projette son code et le commente. Discussion
  collective.
- *Corrigé* : projection rapide du fichier
  `CORRIGES/atelier_NN.py`, en pointant une ou deux différences avec
  la solution du volontaire.

**Mode de travail par bloc**

- Échauffement (1 + 2) : démo guidée, puis chacun reproduit.
- Familiarisation (3 + 4) : pair-programming.
- Cœur (5) : individuel, le formateur passe entre les postes.
- Cœur (6) : pair-programming — c'est l'atelier le plus exigeant.
- Synthèse (7 + 8) : individuel, plus mécanique.

Pour les blocs à deux ateliers, traiter les deux en parallèle (la
moitié de la salle commence par l'un, l'autre moitié par l'autre) si
le temps presse — sinon en série.

**Pièges connus**

- *Atelier 1* : oublier que `getaddrinfo` peut renvoyer des doublons
  (un même IP via plusieurs entrées). Le corrigé déduplique.
- *Atelier 2* : oubli classique du `with` triple (imbrication
  inutile). Le corrigé utilise `with a, b, c` sur une seule ligne,
  occasion de montrer cette syntaxe.
- *Atelier 3* : confondre `connect()` (TCP) et `sendto()` (UDP). Un
  apprenant tentera `sendto` sur un socket TCP — bonne occasion
  d'expliquer pourquoi ça ne marche pas.
- *Atelier 4* : surprise des adresses vides (`''`). C'est *la*
  question pédagogique : « qu'est-ce qu'un socket anonyme ? ». Y
  consacrer une minute supplémentaire si la salle accroche.
- *Atelier 5* : la version naïve `recv(1)` octet par octet **marche**
  mais est inefficace. Le bonus pédagogique est précisément cette
  conscience.
- *Atelier 6* : la tentation est d'utiliser `recv(longueur)` au lieu
  de `recv_exactement`. Si quelqu'un tombe dedans, **ne pas
  corriger immédiatement** : laisser le test échouer sur un message
  long, puis revenir au concept du module 05.
- *Atelier 7* : certains apprenants déduiront « j'ai juste à inverser
  les octets, c'est plus simple ». C'est précisément ce que fait
  l'option little-endian. Faire formuler cette équivalence à voix
  haute.
- *Atelier 8* : confusion fréquente entre `TimeoutError` et
  `BlockingIOError`. Deux exceptions distinctes pour deux modes
  distincts — à insister.

## Conclusion + ouverture (5 min)

**Ce qu'on a couvert** : `(hôte, port)`, socket comme descripteur OS,
TCP vs UDP, cycle de vie, **framing**, boutisme, modes d'attente.

**Ce qui vient ensuite** : `01_Sockets_bas_niveau/` — on écrit *le
même* code que `01_Intro/` du repo original, mais propre : `with`,
`getaddrinfo`, gestion correcte du framing.

**Phrase de clôture suggérée** : « À partir de maintenant, chaque
ligne de code réseau que vous écrirez peut être justifiée par un
des sept modules de ce dossier. Si une ligne ne vous évoque rien,
c'est un signal : revenir ici. »

---

## Annexe — FAQ anticipée

**« Pourquoi pas asyncio dès le départ ? »**
Parce qu'`asyncio` est une abstraction *sur* les sockets. Sans
comprendre le bloc en dessous, on ne sait pas pourquoi `await
sock.recv()` rend la main. La concurrence est traitée au dossier
`07_Concurrence/`, après que les bases soient solides.

**« Pourquoi pas IPv6 partout ? »**
Pour ne pas surcharger le premier contact. `getaddrinfo` est
introduit dès le module 01 ; à partir de là, l'apprenant *peut*
écrire du code IPv6-ready. Les exemples ultérieurs restent en IPv4
pour rester lisibles.

**« Le SSL/TLS, c'est dans ce dossier ? »**
Non, dossier dédié (`11_TLS/`). Le but du dossier 00 est de bâtir
l'intuition sur les sockets en clair ; la couche cryptographique
arrive une fois les fondations posées.

**« Quand voit-on un vrai client/serveur fonctionnel ? »**
Au dossier 01, immédiatement après celui-ci. Le présent dossier
prépare exactement ce que le suivant va manipuler.
