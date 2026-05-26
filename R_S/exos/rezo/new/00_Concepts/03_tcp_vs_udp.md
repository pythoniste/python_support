# 03 — TCP vs UDP

## 3.1 Pourquoi deux protocoles ?

Sur le même socket Python, en changeant **un seul** argument, on
choisit entre deux modèles de communication très différents :

```python
socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
```

Ils répondent à deux besoins opposés.

## 3.2 TCP : un tuyau fiable

TCP (*Transmission Control Protocol*) est un **flux d'octets** ordonné
et fiable, comme un tuyau entre deux processus.

- **Connexion** : un client doit d'abord se *connecter* à un serveur
  (poignée de main en trois temps). Si le serveur n'est pas joignable,
  on le sait immédiatement.
- **Fiabilité** : tout octet émis est retransmis jusqu'à acquittement.
  Si la livraison reste impossible, l'erreur remonte à l'application.
- **Ordre** : les octets arrivent dans l'ordre où ils ont été émis.
- **Pas de frontières** : TCP voit un flux continu d'octets, **pas** une
  suite de messages. Le module 05 reviendra longuement sur cette
  subtilité.

## 3.3 UDP : un envoi à la volée

UDP (*User Datagram Protocol*) envoie des **datagrammes** : des paquets
indépendants, sans état partagé entre l'émetteur et le récepteur.

- **Pas de connexion** : on envoie à une adresse, point. Le destinataire
  n'a même pas besoin d'exister.
- **Pas de fiabilité** : un datagramme peut être perdu en chemin sans
  aucune notification.
- **Pas d'ordre** : deux datagrammes envoyés successivement peuvent
  arriver dans l'ordre inverse.
- **Frontières préservées** : un envoi de 100 octets est reçu en *un
  seul bloc*, ou pas du tout.

## 3.4 Tableau comparatif

| Critère                 | TCP                  | UDP                  |
|-------------------------|----------------------|----------------------|
| Sémantique              | Flux d'octets        | Datagrammes          |
| Connexion préalable     | Oui                  | Non                  |
| Livraison garantie      | Oui                  | Non                  |
| Ordre garanti           | Oui                  | Non                  |
| Frontières de messages  | **Perdues**          | Préservées           |
| Coût en RTT             | Élevé (poignée)      | Minimal              |
| Numéro IANA             | 6                    | 17                   |
| Constante Python        | `SOCK_STREAM`        | `SOCK_DGRAM`         |

## 3.5 Quel protocole pour quel usage ?

- **TCP** : la quasi-totalité des usages applicatifs — HTTP, SSH, bases
  de données, transferts de fichiers. Tout ce qui ne tolère pas la
  perte.
- **UDP** : streaming vidéo/audio (une trame perdue n'a plus d'intérêt
  une fois la suivante arrivée), jeux en ligne, DNS, découverte de
  services sur le réseau local, télémétrie haute fréquence.

Règle de pouce : **par défaut, TCP**. On ne choisit UDP que lorsqu'on a
une raison précise (latence, multicast, simplicité du protocole de plus
haut niveau).

## 3.6 À retenir

- TCP = flux fiable ordonné, connexion préalable, **frontières perdues**.
- UDP = datagrammes indépendants, sans garantie, **frontières préservées**.
- Une seule constante diffère dans le code Python.

## Démo

Exécuter `03_demo_tcp_vs_udp.py` pour voir concrètement la différence :
TCP signale une erreur quand personne n'écoute, UDP n'en signale aucune.
