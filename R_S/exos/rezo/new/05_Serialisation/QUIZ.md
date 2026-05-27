# Quiz — dossier 05_Serialisation

Six questions sur les choix d'encodage.

## Questions

**Q1.** Quels sont les **trois critères principaux** à arbitrer
quand on choisit un encodage de protocole applicatif ?

**Q2.** Pourquoi un encodage binaire **impose-t-il** un framing
rigoureux (taille fixe ou préfixe de longueur), alors que texte ou
JSON peuvent se contenter d'un délimiteur ?

**Q3.** Pour la valeur 42, on observe : texte = 3 octets, binaire = 4 octets,
JSON = 15 octets. Pourquoi JSON est-il **plus volumineux** que texte
pour un entier seul ? Quand devient-il plus économique ?

**Q4.** Notre encodage binaire utilise `struct.pack("!I", n)` (uint32
big-endian). Quelle est la **valeur maximale** que l'on peut encoder ?
Comment passer outre cette limite ?

**Q5.** Pour un protocole entre **microservices** dans un cluster
(haute fréquence d'appels, faible latence souhaitée), lequel des trois
encodages privilégier ? Et pour un **service public** consommé par des
développeurs tiers ?

**Q6.** Pourquoi le client moyenne-t-il sur **1000 tirages** au lieu
d'en faire un seul ?

---

## Réponses

**R1.** (a) **Compacité** : taille sur le réseau, importante pour la
bande passante et la latence. (b) **Lisibilité** : facilité de
déboguer avec un dump ou un sniffer. (c) **Extensibilité** : pouvoir
ajouter un champ sans casser les clients existants.

**R2.** Parce qu'un encodage binaire **peut contenir n'importe quel
octet**, y compris `\n`. Si on l'utilisait comme délimiteur, on ne
saurait pas distinguer la fin d'un message d'un octet aléatoire à
l'intérieur du payload. Texte et JSON, eux, n'utilisent qu'un
sous-ensemble d'octets (caractères imprimables UTF-8 + structure
JSON), ce qui laisse `\n` comme délimiteur sûr.

**R3.** JSON encode **le nom du champ** (`"valeur"`), la **valeur**
sous forme textuelle, plus la ponctuation (`{`, `"`, `:`, espace, `}`).
Pour un seul nombre, le surcoût est énorme. JSON devient plus
économique quand on transporte **plusieurs champs structurés** :
le coût fixe de la ponctuation s'amortit, et on évite d'avoir à
définir un protocole binaire ad hoc.

**R4.** `uint32` big-endian → valeur max **2³² − 1 = 4 294 967 295**.
Au-delà, `struct.pack` lève `struct.error`. Solutions : (a) passer
à `uint64` (`"!Q"`, 8 octets), valeur max ≈ 1,8 × 10¹⁹ ; (b) passer à
un **préfixe de longueur** suivi d'un nombre d'octets variable
(traité par l'atelier 8) ; (c) si la valeur peut être négative,
passer en signed (`!i` / `!q`).

**R5.** Microservices : **binaire**, idéalement via Protocol Buffers,
MessagePack ou Avro — compact, rapide à parser, schéma versionné.
Service public : **JSON** ou GraphQL — débogable au navigateur,
documenté par `OpenAPI`, parseur disponible dans tout langage. Le
critère humain (qui débogue ? qui code le client ?) prime souvent.

**R6.** Pour **vérifier empiriquement l'uniformité** de la
distribution. Un seul tirage ne dit rien sur la qualité du générateur.
La moyenne sur N tirages converge vers `max/2` si la distribution est
uniforme — c'est la loi des grands nombres. Sur 1000 tirages, on
attend une moyenne dans `[max/2 ± qq %]`.
