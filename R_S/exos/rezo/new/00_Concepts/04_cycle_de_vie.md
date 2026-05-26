# 04 — Cycle de vie client / serveur

## 4.1 Le principe

Côté serveur comme côté client, un socket passe par une succession
d'**états** entre sa création et sa fermeture. L'API socket de Python
n'invente rien : elle suit fidèlement le cycle de vie défini par l'API
BSD (années 1980), reprise par tous les systèmes modernes.

On parle d'un cycle de vie en quatre temps :

- **Création** (`socket()`)
- **Préparation** (varie selon serveur/client, TCP/UDP)
- **Échange** (`recv`/`send`)
- **Fermeture** (`close()`, ou sortie du `with`)

C'est la phase 2 qui diffère selon le rôle et le protocole.

## 4.2 Serveur TCP

```
socket()  →  bind()  →  listen()  →  accept()  →  recv/send  →  close()
                                         │
                                         └── (boucle : un accept par client)
```

- `socket()` : crée le descripteur. Aucune adresse n'y est encore associée.
- `bind(adresse)` : attache le socket au couple `(hôte, port)`.
- `listen(n)` : passe en mode écoute. `n` = taille de la file d'attente.
- `accept()` : bloque jusqu'à ce qu'un client se connecte, puis
  **renvoie un nouveau socket** dédié à ce client. Le socket d'origine
  continue d'écouter.
- `recv` / `send` se font sur le **nouveau** socket renvoyé par
  `accept`, jamais sur l'écouteur.

## 4.3 Client TCP

```
socket()  →  connect()  →  send/recv  →  close()
```

Plus court : un client n'écoute jamais, il se connecte. `connect()`
déclenche la poignée de main en trois temps.

## 4.4 Serveur UDP (et client UDP)

```
socket()  →  bind()  →  recvfrom/sendto  →  close()
```

Pas de `listen`, pas de `accept`. UDP n'a pas de notion de connexion :
on lit les datagrammes au fur et à mesure qu'ils arrivent.

Le client UDP est encore plus simple :

```
socket()  →  sendto/recvfrom  →  close()
```

Pas même besoin de `bind` : le système d'exploitation attribue un port
éphémère au premier envoi.

## 4.5 Tableau récapitulatif

| Phase                  | Serveur TCP      | Client TCP        | Serveur UDP            | Client UDP             |
|------------------------|------------------|-------------------|------------------------|------------------------|
| Création               | `socket(STREAM)` | `socket(STREAM)`  | `socket(DGRAM)`        | `socket(DGRAM)`        |
| Adresse locale fixée   | `bind`           | (implicite)       | `bind`                 | (implicite)            |
| Mise en écoute         | `listen`         | —                 | —                      | —                      |
| Établir la connexion   | `accept`         | `connect`         | —                      | —                      |
| Échange                | `recv` / `send`  | `send` / `recv`   | `recvfrom` / `sendto`  | `sendto` / `recvfrom`  |
| Fermeture              | `close` (× 2)    | `close`           | `close`                | `close`                |

À noter : **TCP comporte deux sockets côté serveur**, l'écouteur et
celui issu de `accept`. Il faut fermer les deux. C'est ce qui explique
le double `close` qu'on verra plus loin dans le cours.

## 4.6 À retenir

- TCP serveur : `socket → bind → listen → accept → recv/send → close`.
- TCP client : `socket → connect → send/recv → close`.
- UDP : pas de `listen`, pas de `accept` — uniquement `bind` côté serveur.
- `accept()` rend un **nouveau** socket dédié au client.

## Démo

Exécuter `04_demo_cycle_de_vie.py` pour visualiser les états successifs.
