# 05 — Le problème du framing

## 5.1 Le piège fondamental

C'est *le* concept que les premiers programmes réseau ignorent
silencieusement, jusqu'au jour où un bug inexplicable apparaît en
production. Le dossier `01_Intro/` du repo d'origine en est plein.

**TCP est un flux d'octets, pas une suite de messages.**

Si l'émetteur appelle :

```python
s.send(b"Bonjour ")
s.send(b"le ")
s.send(b"monde !")
```

… le récepteur peut :

- lire tout en une fois (`recv(100)` → `b"Bonjour le monde !"`) ;
- ou lire morceau par morceau, à des découpages **arbitraires**
  (`b"Bonjour le m"`, puis `b"onde !"`) ;
- ou lire `b"Bonjou"` et bloquer en attendant la suite.

Les **frontières** des appels à `send()` côté émetteur sont **perdues**
côté récepteur. Le système se réserve le droit de regrouper ou de
fragmenter à sa guise.

## 5.2 Pourquoi UDP est différent

UDP **préserve les frontières** : un `sendto(100 octets)` produit un
seul datagramme de 100 octets, lu en un seul `recvfrom(100)`. C'est
souvent la raison principale pour laquelle UDP est choisi.

En contrepartie, UDP impose ses propres contraintes :

- taille maximale d'un datagramme (~ 65 507 octets, en pratique
  beaucoup moins si l'on veut éviter la fragmentation IP) ;
- un datagramme peut être perdu sans préavis ;
- l'ordre n'est pas garanti.

## 5.3 Conséquence pratique côté TCP

Cette ligne, omniprésente dans le code naïf :

```python
data = s.recv(1024)
```

… ne reçoit **pas** « un message ». Elle reçoit « entre 1 et 1024
octets, ce que le système a sous la main au moment de l'appel ». Si
l'application en face envoyait un message structuré, il faut le
**délimiter** explicitement.

## 5.4 Les trois solutions classiques

### a) Longueur fixe

Tous les messages font exactement *N* octets. On lit exactement *N* octets.

```
[ 16 octets ][ 16 octets ][ 16 octets ]
```

Simple, mais peu flexible (taille gaspillée ou insuffisante).

### b) Délimiteur

On choisit un octet (typiquement `\n`) qui ne peut **pas** apparaître
dans le contenu, et on lit jusqu'à le rencontrer.

```
Bonjour\nle\nmonde !\n
```

C'est exactement ce que fait
`socketserver.StreamRequestHandler.rfile.readline()` — qu'on
rencontrera dans `03_Socketserver/`. C'est la solution que
`01_Intro/tcpsrv.py` *aurait dû* utiliser.

### c) Préfixe de longueur

On écrit d'abord la taille du message (sur *N* octets fixes, en
binaire), puis le contenu.

```
[0x00 0x00 0x00 0x0B] Hello world
```

Le récepteur lit toujours *N* octets, en déduit la taille, puis lit
exactement cette taille. C'est ce que font HTTP/2, gRPC, beaucoup de
protocoles binaires.

## 5.5 L'outil indispensable : `recv_exactement`

Quelle que soit la solution choisie, on a besoin d'une fonction qui
lit **exactement N octets**, en bouclant sur les `recv()` partiels :

```python
def recv_exactement(sock, n):
    """Lit exactement n octets sur sock, ou lève ConnectionError."""
    morceaux = []
    restant = n
    while restant:
        bloc = sock.recv(restant)
        if not bloc:
            raise ConnectionError("Connexion fermée prématurément")
        morceaux.append(bloc)
        restant -= len(bloc)
    return b"".join(morceaux)
```

Cette fonction sera reprise telle quelle dans le dossier `02_Framing/`.

## 5.6 À retenir

- TCP = flux, pas messages. Les frontières de `send` sont perdues.
- `recv(N)` peut renvoyer **moins** de N octets. Toujours boucler.
- Trois solutions de délimitation : longueur fixe, délimiteur,
  préfixe de longueur.
- UDP n'a pas ce problème (mais en a d'autres).

## Démo

Exécuter `05_demo_framing.py` pour observer la collation des envois.
