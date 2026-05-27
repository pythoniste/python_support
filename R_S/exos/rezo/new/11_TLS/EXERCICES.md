# Exercices pratiques — dossier 11_TLS

Six ateliers pour pratiquer TLS.

---

## Atelier 1 — Inspecter le certificat d'un site public  ★
*Fichier de référence : 01_https_client.py*

Modifier le client pour qu'il affiche, après la requête, les
informations du certificat distant : émetteur, sujet, dates de
validité.

**Indices** : `urllib3.poolmanager` ou `ssl.create_default_context()`
+ `getpeercert()` via une connexion raw. Plus simple : utiliser
`requests` + `r.raw._connection.sock.getpeercert()`.

---

## Atelier 2 — Désactiver la vérification (et son risque)  ★
*Fichier de référence : 04_tls_clt.py*

Modifier le client pour qu'il accepte n'importe quel certificat
(`verify=False` en requests, `CERT_NONE` en ssl). Tester sur le
serveur local. Documenter en commentaire **pourquoi c'est dangereux
en production**.

---

## Atelier 3 — mTLS (authentification mutuelle)  ★★★
*Fichiers de référence : 02_generer_cert.py + 03_tls_srv.py*

Générer un second certificat pour le **client**. Modifier le
serveur pour exiger un certificat client (`verify_mode = CERT_REQUIRED`).
Le client doit charger sa propre clé + cert.

---

## Atelier 4 — Mesurer le coût du handshake TLS  ★★
*Fichier de référence : requests*

Comparer le temps de 10 requêtes successives avec une `Session`
(handshake 1 fois, keep-alive) vs sans session (handshake à chaque
fois). Le ratio devrait être ~5–10× sur HTTPS.

---

## Atelier 5 — Génération avec cryptography  ★★
*Fichier de référence : 02_generer_cert.py*

Étendre le générateur pour accepter `nom_commun` et `validite_jours`
en arguments argparse. Bonus : ajouter plusieurs SAN.

---

## Atelier 6 — TLS 1.3 forcé  ★★
*Fichier de référence : 03_tls_srv.py*

Configurer le contexte pour n'accepter QUE TLS 1.3 (la dernière
version, sortie en 2018). Vérifier qu'un client TLS 1.2 est
refusé.

**Indices** : `contexte.minimum_version = ssl.TLSVersion.TLSv1_3`.
