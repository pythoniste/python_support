# 12_WebSockets — Communication bidirectionnelle

HTTP est **requête / réponse** : le client demande, le serveur
répond. Pas idéal pour ce qui doit aller du serveur vers le client
sans demande explicite (notifications push, chat, cours de bourse,
mises à jour live).

**WebSocket** résout ça : une connexion TCP unique, **bidirectionnelle**,
qui survit à la fin d'une "requête". Standard RFC 6455.

## Comment ça marche

1. Le client envoie une requête HTTP classique avec
   `Upgrade: websocket`.
2. Le serveur répond `101 Switching Protocols`.
3. À partir de là, **la même connexion TCP** transporte des
   **frames WebSocket** dans les deux sens.

Le protocole frame WS est simple :
- en-tête de 2 à 14 octets ;
- payload masqué côté client (sécurité historique) ;
- types : texte, binaire, ping, pong, close.

## Plan

| Fichier               | Sujet                                          |
|-----------------------|------------------------------------------------|
| `01_echo_srv.py`      | Serveur WS d'echo (bibliothèque `websockets`)  |
| `02_echo_clt.py`      | Client WS d'echo                               |
| `03_chat_srv.py`      | Serveur de chat (broadcast)                    |
| `04_chat_clt.py`      | Client de chat                                 |
| `05_browser_demo.html`| Page HTML qui se connecte en WS depuis le navigateur |

## Dépendance

```bash
pip install websockets
```

Le module stdlib **n'a pas** de support WebSocket. La bibliothèque
`websockets` (PyPI) est le standard de facto, async-first.

## Comment exécuter

```
python3 01_echo_srv.py     # terminal 1
python3 02_echo_clt.py     # terminal 2

python3 03_chat_srv.py     # terminal 1
python3 04_chat_clt.py Alice    # terminal 2
python3 04_chat_clt.py Bob      # terminal 3
```

Pour la démo navigateur : ouvrir `05_browser_demo.html` dans Firefox
ou Chrome après avoir lancé `01_echo_srv.py`. C'est le moment où
l'on voit que **tout client WS** (Python, JavaScript, …) interagit
identiquement.

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur WebSocket.
- `EXERCICES.md` : 6 ateliers.
- `GUIDE_FORMATEUR.md` : plan minuté.
