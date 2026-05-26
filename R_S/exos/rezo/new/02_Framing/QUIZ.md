# Quiz — dossier 02_Framing

Six questions pour auto-évaluer la maîtrise des trois stratégies de
framing.

## Questions

**Q1.** Quels sont les **trois** mécanismes classiques de framing
dans un flux TCP ? Décrire chacun en une phrase.

**Q2.** Pourquoi la stratégie « délimiteur » est-elle inapplicable
quand le contenu peut être quelconque (par exemple un fichier
binaire) ?

**Q3.** Dans le préfixe de longueur, quel boutisme utilise-t-on, et
pourquoi ?

**Q4.** Que renvoie `recv_exactement` si la connexion ferme à
mi-chemin (par exemple après 50 octets sur 100 attendus) ?

**Q5.** Pourquoi `socket.makefile("rwb")` impose-t-il un `flush()`
explicite après chaque `write()` ?

**Q6.** Quel est le lien entre `socket.makefile()` et
`socketserver.StreamRequestHandler.rfile / wfile` (que l'on verra au
dossier 03) ?

---

## Réponses

**R1.** (a) Longueur fixe : chaque message fait exactement *N* octets.
(b) Délimiteur : on choisit un octet (souvent `\n`) qui ne peut pas
apparaître dans le contenu, on lit jusqu'à le rencontrer.
(c) Préfixe de longueur : on écrit d'abord la taille (*N* octets
fixes en binaire), puis le contenu.

**R2.** Parce qu'un fichier binaire **peut contenir** l'octet
délimiteur n'importe où, ce qui rendrait la séparation ambiguë.
Le préfixe de longueur est alors la seule option générale (à part
la longueur fixe pour des messages de taille déterminée).

**R3.** Big-endian (network byte order). Convention héritée des
protocoles réseau historiques. En Python : `struct.pack("!I", n)`,
le `!` documente explicitement l'intention.

**R4.** Une exception `ConnectionError` (avec message indiquant
combien d'octets ont été reçus sur combien étaient attendus). C'est
volontaire : un message incomplet est une erreur, pas un résultat
silencieux.

**R5.** Parce que `makefile` retourne un objet **bufferisé**. Sans
`flush`, les octets restent dans le buffer Python et ne sont jamais
envoyés sur le socket. C'est l'équivalent du flush d'un fichier
ordinaire.

**R6.** `StreamRequestHandler.rfile` et `wfile` sont **exactement**
les objets retournés par `socket.makefile()` (mode `"rb"` et `"wb"`
respectivement). Le dossier 03 ne fait qu'encapsuler cette mécanique
dans un framework plus haut.
