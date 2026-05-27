# Quiz — dossier 11_TLS

## Questions

**Q1.** Quelles sont les **trois** garanties principales offertes
par TLS ?

**Q2.** Pourquoi un certificat auto-signé est-il rejeté par
défaut par les clients HTTPS (navigateurs, requests, etc.) ?

**Q3.** Que se passe-t-il pendant le **handshake TLS** ? Citer
trois étapes.

**Q4.** Différence entre **TLS** et **mTLS** (mutual TLS) ?

**Q5.** En production, où **terminate-t-on** habituellement le TLS
dans une architecture moderne ? Pourquoi pas dans le code Python ?

**Q6.** Que signifie le code `ssl.SSLError: HANDSHAKE_FAILURE` côté
serveur ?

---

## Réponses

**R1.** (a) **Confidentialité** : tout le contenu est chiffré
symétriquement. (b) **Intégrité** : un MAC sur chaque enregistrement
détecte toute modification. (c) **Authentification du serveur**
par certificat X.509 signé par une autorité de confiance.

**R2.** Parce que la chaîne de confiance remonte à une **autorité
de certification (CA)**. Un certificat auto-signé n'est pas dans
la chaîne — n'importe qui peut le générer pour n'importe quel
domaine. Sans confiance préalable, le client ne peut pas distinguer
un vrai serveur d'un attaquant. La parade : ajouter explicitement
le certificat au store de confiance du client (`verify=path` en
requests, `load_verify_locations` en ssl).

**R3.** (a) **ClientHello / ServerHello** : négocier la version
TLS et la suite cryptographique. (b) **Envoi du certificat
serveur** : le client le vérifie contre les CA installées.
(c) **Échange de clé** : Diffie-Hellman éphémère ou similaire pour
établir une clé de session. Ensuite, tout est chiffré avec cette
clé.

**R4.** **TLS** : seul le serveur est authentifié par certificat.
Le client peut s'identifier ensuite par login/mot de passe, token,
etc. **mTLS** : le client présente AUSSI un certificat ;
authentification mutuelle au niveau TLS. Utilisé dans les
architectures zero-trust et les communications inter-services.

**R5.** Au niveau du **reverse proxy** (nginx, Caddy, traefik,
HAProxy, …) ou du **load-balancer** (AWS ALB, GCP LB, …). Raisons :
gestion centralisée des certificats Let's Encrypt, performance
(termination optimisée en C), simplification du code applicatif
(qui ne fait que du HTTP en clair sur localhost), rotation
automatique des certificats.

**R6.** Le client et le serveur n'ont pas pu se mettre d'accord sur
les paramètres de la session. Causes possibles : pas de cipher
suite commune, version TLS incompatible (par ex client TLS 1.0 vs
serveur min TLS 1.2), certificat refusé par le client (auto-signé
non whitelisté), absence du SNI requis.
