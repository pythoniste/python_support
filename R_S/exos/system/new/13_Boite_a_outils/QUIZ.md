# Quiz de validation — dossier 13_Boite_a_outils

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer aux chapitres suivants. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Quelle est la différence pratique entre
`tempfile.TemporaryDirectory()` et `tempfile.mkdtemp()` ? Laquelle des
deux faut-il choisir par défaut, et pourquoi ?

**Q2.** Sous macOS, que renvoie `platform.system()` ? Quelle erreur
classique cela provoque-t-il quand on écrit du code qui se branche sur
l'OS détecté ?

**Q3.** On veut hasher en SHA-256 un fichier de 10 Gio. Pourquoi est-il
**hors de question** d'écrire :

```python
with open(chemin, "rb") as f:
    h = hashlib.sha256(f.read())
```

et quel est le motif correct ?

**Q4.** Un développeur utilise `random.choices(...)` pour générer un
jeton de session de 32 caractères. Pourquoi est-ce une mauvaise idée,
et quel module faut-il utiliser à la place ?

**Q5.** Pourquoi compare-t-on deux signatures HMAC avec
`hmac.compare_digest(a, b)` plutôt qu'avec `a == b` ?

**Q6.** Un collègue stocke un mot de passe sous la forme
`base64.b64encode(b"motdepasse")` dans un fichier `.env`, persuadé que
c'est « chiffré ». Que faut-il lui répondre ?

---

## Réponses

**R1.** `TemporaryDirectory()` est un **context manager** : utilisé
dans un bloc `with`, il crée le dossier et le **supprime
automatiquement** à la sortie, même en cas d'exception. `mkdtemp()`
crée le dossier et renvoie son chemin, mais **ne le supprime jamais
tout seul** : si on l'oublie, le dossier reste, et on pollue
progressivement `/tmp` à chaque exécution. Dans 99 % des cas, on
prend `TemporaryDirectory()`.

**R2.** `platform.system()` renvoie `"Darwin"` sous macOS — c'est le
nom du noyau historique du système. Beaucoup de codes écrits par des
débutants testent `if platform.system() == "macOS":`, qui n'est jamais
vrai, et la branche correspondante n'est donc jamais prise. Il faut
comparer à `"Darwin"`.

**R3.** Parce que `f.read()` charge **tout** le fichier en mémoire
d'un seul coup : 10 Gio de RAM nécessaires, ce qui ne tient sur
quasiment aucune machine. Le motif correct lit **par blocs** (typiquement
4096 octets) et appelle `h.update(bloc)` à chaque tour de boucle ; la
mémoire utilisée reste constante quelle que soit la taille du fichier.

**R4.** Le module `random` est un générateur **pseudo-aléatoire** non
cryptographique : sa graine peut être devinée à partir d'observations
successives, et la documentation Python interdit explicitement de
l'utiliser pour générer des secrets. Pour un token de session ou
toute autre valeur qui doit être imprévisible, on utilise le module
**`secrets`** (`secrets.token_urlsafe`, `secrets.token_hex`,
`secrets.token_bytes`), qui s'appuie sur le générateur cryptographique
du système d'exploitation.

**R5.** Parce que `a == b` s'arrête à la **première** différence
d'octets : l'opération prend plus de temps quand les chaînes commencent
par les mêmes caractères. Un attaquant qui mesure ce temps peut, en
théorie, deviner la signature **caractère par caractère**. La fonction
`hmac.compare_digest` (équivalente à `secrets.compare_digest`) compare
**toujours** en parcourant les deux chaînes en entier, en temps
constant, ce qui ferme cette fenêtre d'attaque.

**R6.** Que **base64 n'est pas un chiffrement**. C'est un simple
**encodage** : n'importe qui dispose de `base64.b64decode` et retrouve
la chaîne d'origine sans clé, sans secret, sans rien à savoir. Stocker
un mot de passe « en base64 » dans un fichier de configuration équivaut
à le stocker **en clair**. Pour protéger un secret, il faut soit ne
pas le stocker du tout (le passer en variable d'environnement injectée
au lancement), soit utiliser un vrai chiffrement (bibliothèque
`cryptography`, gestionnaire de secrets, etc.).
