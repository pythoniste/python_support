# 01 — Adresses : IP, port, hôte, DNS

## 1.1 Une adresse réseau = couple `(hôte, port)`

Pour identifier un service sur le réseau, deux informations sont
nécessaires :

- **L'hôte** identifie une *machine* (plus précisément, une interface
  réseau de cette machine).
- **Le port** identifie un *processus* qui écoute sur cette machine.

En Python, cela se traduit presque toujours par un tuple :

```python
adresse = ("127.0.0.1", 8808)
```

## 1.2 L'hôte

L'hôte peut être donné sous trois formes :

| Forme           | Exemple         | Remarque                              |
|-----------------|-----------------|---------------------------------------|
| Adresse IPv4    | `192.168.1.10`  | 4 octets, notation décimale pointée   |
| Adresse IPv6    | `::1`           | 16 octets, notation hexadécimale      |
| Nom symbolique  | `example.com`   | Résolu par DNS                        |

### Trois adresses spéciales à connaître

- `127.0.0.1` (alias `localhost`) : **boucle locale**. Seuls les
  processus de cette même machine peuvent s'y connecter. C'est ce qu'on
  utilise pour tous les exercices du cours.
- `0.0.0.0` côté **serveur** : « écoute sur **toutes** les interfaces
  réseau de la machine ». À utiliser si l'on veut être joignable depuis
  l'extérieur.
- `::` : équivalent IPv6 de `0.0.0.0`.

## 1.3 Le port

Un entier sur 16 bits, donc de **0 à 65535**.

| Plage         | Usage                                                          |
|---------------|----------------------------------------------------------------|
| 0 – 1023      | Ports réservés (HTTP=80, HTTPS=443, SSH=22…). Nécessite des droits administrateur sous Linux. |
| 1024 – 49151  | Ports « enregistrés » par l'IANA (PostgreSQL=5432, etc.).      |
| 49152 – 65535 | Ports **éphémères**, libres d'usage. Les exercices du cours s'y trouvent (8808, 8809, …). |

## 1.4 DNS en une phrase

Le DNS (*Domain Name System*) transforme un nom (`example.com`) en
adresse IP. En Python, la fonction à utiliser est
**`socket.getaddrinfo`**, qui gère IPv4 *et* IPv6 en une seule fois.

```python
socket.getaddrinfo("example.com", 80, type=socket.SOCK_STREAM)
```

Il existe une fonction plus simple, `socket.gethostbyname`, mais elle
est limitée à IPv4 — à éviter en code moderne.

## 1.5 À retenir

- Une adresse = `(hôte, port)`.
- `127.0.0.1` ≠ `0.0.0.0` (n'écoute pas la même chose côté serveur).
- Utiliser `getaddrinfo` pour résoudre un nom.

## Démo

Exécuter `01_demo_adresses.py` puis relire les commentaires inline.
