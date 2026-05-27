# 05_Serialisation — Encoder les données utiles

Premier dossier centré sur l'**encodage** des données métier. Le
transport (TCP, en l'occurrence) est fixé ; on compare **trois
stratégies de sérialisation** sur le même cas d'usage :

> Un serveur génère des nombres aléatoires entiers entre 0 et `max`.
> Le client envoie un `max`, reçoit un entier. En agrégeant 1000
> tirages, on vérifie que la distribution est uniforme (moyenne ≈ max/2).

Trois encodages :

| Paire                                  | Encodage                                          |
|----------------------------------------|---------------------------------------------------|
| `01_text_srv.py` + `02_text_clt.py`    | **Texte** : `int(str(n))`, framing par `\n`       |
| `03_binaire_srv.py` + `04_binaire_clt.py` | **Binaire fixe** : `int.to_bytes(4, "big")`, trame de 4 octets |
| `05_json_srv.py` + `06_json_clt.py`    | **JSON** : `{"valeur": n}`, framing par `\n`       |

La logique d'encodage est centralisée dans `encodage.py`. Le module
expose trois paires symétriques `pack_*` / `unpack_*`.

## Comment exécuter

Toutes les paires utilisent le port `8808`. Un seul serveur à la fois.

```
# Paire 1 — encodage texte
python3 01_text_srv.py    # terminal 1
python3 02_text_clt.py    # terminal 2  (1000 tirages, affiche la moyenne)
```

Idem pour les paires `03_binaire_*` et `05_json_*`.

## Protocole applicatif

Tous les paires ont la même sémantique :

- Client envoie un **`max`** (entier non négatif).
- Serveur répond par un **entier aléatoire** dans `[0, max]`.

Le **format** des messages diffère selon l'encodage.

## Ce qui est démontré

- L'encodage est **orthogonal** au transport. Le réseau est identique
  dans les trois paires ; seul change ce qu'on met sur le câble.
- Trois familles classiques : **texte**, **binaire**, **JSON**.
- Les compromis : taille (binaire gagne), lisibilité (JSON gagne),
  simplicité d'écriture (texte gagne).
- Le binaire **impose** une discipline de framing rigoureuse (taille
  fixe ou préfixe de longueur) ; le texte et JSON s'accommodent du
  délimiteur `\n`.

## Ce qui est volontairement reporté

- **UDP** : les ateliers en proposent des variantes.
- **Compression** : atelier 7 (extension).
- **Encodage des nombres flottants** : atelier 4 (extension).

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur les choix d'encodage.
- `EXERCICES.md` : 8 ateliers, dont mesures comparatives et extensions.
- `GUIDE_FORMATEUR.md` : plan détaillé pour l'intervenant.
