# Exercices pratiques — dossier 01_Sockets_bas_niveau

Huit ateliers de modification du code de base (`01_tcpsrv.py`,
`02_tcpclt.py`, `03_udpsrv.py`, `04_udpclt.py`).

Chaque atelier indique :

- le ou les fichiers de référence ;
- une difficulté de ★ (facile) à ★★★ (consolidant) ;
- des indices pour démarrer ;
- la sortie attendue lorsque c'est pertinent.

Les corrigés sont fournis dans `CORRIGES/`.

---

## Atelier 1 — Echo serveur  ★
*Fichier de référence : 01_tcpsrv.py*

Modifier le serveur TCP pour qu'il renvoie **exactement** le message
reçu (sans le préfixe « Bonjour » ni le suffixe « . »), sauf pour le
mot-clé `stop` qui doit continuer à arrêter le serveur.

Le client `02_tcpclt.py` ne doit **pas** être modifié.

**Indices**

- Une seule ligne à changer dans `traiter_client`.
- Penser à conserver la gestion du mot-clé `stop`.

**Sortie attendue côté client**

```
    Réponse : b'World'
    Réponse : b'Vous'
    Réponse : b'Arret du serveur.\n'
```

---

## Atelier 2 — Compteur de clients  ★
*Fichier de référence : 01_tcpsrv.py*

Ajouter au serveur TCP un compteur qui s'incrémente à chaque nouvelle
connexion acceptée. Le premier message envoyé à chaque client doit
être : `b"Bienvenue, client #N\n"` (où *N* est le numéro du client).

**Indices**

- Variable à porter hors de `traiter_client`.
- L'envoi de bienvenue se fait **avant** d'entrer dans la boucle des
  messages.

---

## Atelier 3 — Stop côté UDP  ★
*Fichier de référence : 03_udpsrv.py*

Ajouter au serveur UDP la prise en charge du mot-clé `stop` : à
réception, il envoie une confirmation
(`b"Arret du serveur.\n"`) puis sort proprement de la boucle
`while True`.

**Indices**

- Pas de `connexion` à fermer en UDP ; seul le socket serveur, géré
  par le `with`.
- Utiliser `break`.

---

## Atelier 4 — Démontrer le framing  ★★
*Fichiers de référence : 01_tcpsrv.py + 02_tcpclt.py*

Modifier le serveur pour qu'il réponde par un message **long**
(par exemple `b"x" * 5000`). Modifier le client pour qu'il appelle
`recv()` en boucle (au lieu d'une seule fois), accumule les morceaux
et compte le **nombre d'appels** nécessaires pour lire la totalité.

**Indices**

- Le client doit boucler tant que `recv` retourne des données non
  vides (`b""` signale EOF).
- Pour que le client voie EOF, le serveur doit **fermer** la
  connexion après l'envoi.
- Imprimer côté client : le nombre d'appels et la taille totale reçue.

**Question** : on lit 5000 octets en combien d'appels `recv()` ? La
réponse dépend de l'OS, du buffer TCP et du moment — c'est
précisément le point.

---

## Atelier 5 — Timeout côté client  ★★
*Fichier de référence : 02_tcpclt.py*

Ajouter un timeout au client TCP via `settimeout(2)`. Tester en
lançant le client **sans** que le serveur soit démarré : le
`connect()` doit lever une exception. La capturer et imprimer un
message clair.

**Indices**

- `settimeout` s'applique sur le socket, avant le premier appel
  bloquant.
- Selon le système, l'exception peut être `TimeoutError` ou
  `ConnectionRefusedError`. Attraper les deux.

---

## Atelier 6 — Hostname et port en arguments  ★★
*Fichier de référence : 02_tcpclt.py*

Modifier le client TCP pour qu'il accepte le nom d'hôte et le port en
**arguments de ligne de commande** via `argparse`. Le défaut reste
`127.0.0.1:8808`. Tester avec `localhost`, `127.0.0.1`, et `::1`.

**Indices**

- `argparse.ArgumentParser` avec `--hote` et `--port`.
- `socket.getaddrinfo` accepte tous ces formats.
- Utiliser la **première** entrée renvoyée — elle peut être IPv4 ou
  IPv6 selon le système.

---

## Atelier 7 — Client TCP interactif  ★★★
*Fichier de référence : 02_tcpclt.py*

Transformer le client TCP en boucle interactive : tant que
l'utilisateur ne tape pas une ligne **vide**, lire son entrée,
l'envoyer au serveur, imprimer la réponse. À la ligne vide, le
client se déconnecte et sort proprement.

**Indices**

- `while True` autour de `input()`.
- Sortie si `input()` renvoie `""`.
- Ne **pas** envoyer `stop` implicitement à la sortie — laisser le
  serveur disponible pour d'autres clients.

---

## Atelier 8 — Mesurer le RTT  ★★
*Fichier de référence : 02_tcpclt.py*

Pour chaque échange du client, mesurer le **temps aller-retour**
(RTT) entre l'envoi et la réception. Imprimer le résultat en
millisecondes.

**Indices**

- `time.perf_counter()` juste avant `sendall`, juste après `recv`.
- Format `f"{(t1-t0) * 1000:.2f} ms"`.

---

## Pour aller plus loin

Une fois ces ateliers terminés, on est prêt à attaquer le dossier
suivant — **`02_Framing/`** — qui résout proprement le problème mis
en évidence par l'atelier 4.
