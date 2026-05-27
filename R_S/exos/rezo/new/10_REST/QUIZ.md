# Quiz — dossier 10_REST

## Questions

**Q1.** Citer **quatre** méthodes HTTP utilisées en REST et leur
sémantique.

**Q2.** Différence entre PUT et PATCH ?

**Q3.** Quel code HTTP renvoie-t-on pour : ressource créée, ressource
supprimée sans corps de retour, ressource introuvable, conflit de
duplicata ?

**Q4.** Pourquoi le **versioning** d'une API est-il important ?
Citer deux stratégies.

**Q5.** Quels sont les deux principaux patterns de **pagination** ?
Avantages et inconvénients ?

**Q6.** Une URL `/getUser/1` est-elle REST-conforme ? Pourquoi ?

---

## Réponses

**R1.** GET (lire, idempotent, sans corps) ; POST (créer, non
idempotent) ; PUT (remplacer, idempotent) ; DELETE (supprimer,
idempotent). Bonus : PATCH (modifier partiellement), HEAD (en-têtes
seuls), OPTIONS (capacités CORS).

**R2.** **PUT remplace** la ressource entière : envoyer tous les
champs. **PATCH modifie partiellement** : envoyer uniquement les
champs à changer. PATCH a une sémantique plus floue (JSON Patch,
JSON Merge Patch…) mais reste utile pour les mises à jour
partielles.

**R3.** 201 (Created), 204 (No Content), 404 (Not Found), 409
(Conflict).

**R4.** Permet de **modifier le contrat** sans casser les clients
existants. Stratégies : (a) préfixe d'URL `/v1/`, `/v2/` (le plus
courant) ; (b) en-tête `Accept` (plus pur REST) ; (c) sous-domaine
`v2.api.example.com` ; (d) paramètre `?version=2` (à éviter).

**R5.** **Offset/limit** : `?offset=40&limit=20`. Simple. Coûteux en
base si limite grande. **Cursor-based** : `?cursor=abc123`. Stable
même si la liste change pendant le parcours, plus efficace. Standard
pour les feeds (Twitter, GitHub GraphQL).

**R6.** **Non.** L'URL doit représenter la **ressource**, pas
l'action. La forme correcte est `GET /users/1`. Le verbe HTTP
exprime l'action (GET pour lire), l'URL identifie la ressource.
Mélanger les deux (`/getUser`) est un anti-pattern.
