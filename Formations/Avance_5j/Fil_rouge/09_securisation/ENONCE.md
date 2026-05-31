# Etape 09 -- Securisation

## Contexte

Le pipeline traite des donnees de capteurs qui peuvent etre sensibles (installations industrielles, hopitaux). Vous devez garantir l'**integrite** des fichiers (personne ne les a modifies en transit) et le **chiffrement** des sorties pour proteger les donnees au repos.

## Consignes

1. Creer `src/pipeline/integrity.py` :
   - `compute_file_hash(path: Path, algorithm: str = "sha256") -> str` : calcule le hash d'un fichier par blocs (pas tout en memoire). Retourne le digest hexadecimal.
   - `compute_hmac(data: bytes, key: bytes) -> str` : calcule un HMAC-SHA256.
   - `verify_hmac(data: bytes, key: bytes, expected: str) -> bool` : verifie un HMAC en temps constant (`hmac.compare_digest`).
   - `create_manifest(directory: Path) -> dict[str, str]` : cree un dictionnaire `{filename: sha256_hash}` pour tous les fichiers d'un repertoire.
   - `verify_manifest(directory: Path, manifest: dict[str, str]) -> list[str]` : retourne la liste des fichiers dont le hash ne correspond pas.

2. Creer `src/pipeline/crypto.py` :
   - `generate_key() -> bytes` : genere une cle Fernet.
   - `encrypt_file(path: Path, key: bytes) -> Path` : chiffre un fichier avec Fernet, ecrit le resultat dans `path.with_suffix(".enc")`, retourne le chemin.
   - `decrypt_file(path: Path, key: bytes) -> Path` : dechiffre un fichier `.enc`, ecrit le resultat sans le `.enc`, retourne le chemin.

3. Adapter `__main__.py` :
   - Ajouter `--sign` : apres l'ecriture, genere un manifeste HMAC du dossier `outbox/` (la cle est lue depuis la variable d'environnement `PIPELINE_HMAC_KEY`).
   - Ajouter `--encrypt` : chiffre chaque fichier de sortie avec Fernet (la cle est lue depuis `PIPELINE_FERNET_KEY`).

4. Ajouter `cryptography` dans les dependances.

## Criteres d'acceptation

- [ ] Le hash de fichier est calcule par blocs (pas `path.read_bytes()` entier pour les gros fichiers).
- [ ] `verify_hmac` utilise `hmac.compare_digest` (pas `==`).
- [ ] Les fichiers chiffres sont dechiffrables et identiques a l'original.
- [ ] Le manifeste detecte un fichier modifie.
- [ ] Les cles sont lues depuis l'environnement, jamais codees en dur.
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Comparer des HMAC avec `==`** : vulnerable aux timing attacks. Toujours `hmac.compare_digest`.
- **Lire tout le fichier en memoire pour le hash** : sur un fichier de 2 Go, ca explose. Lire par blocs de 8 Ko.
- **Cle Fernet en dur dans le code** : faille de securite. Utiliser les variables d'environnement ou un gestionnaire de secrets.
- **Oublier que Fernet encode en base64** : le fichier chiffre est plus gros que l'original (environ 4/3).
- **`secrets.token_bytes` vs `os.urandom`** : les deux sont cryptographiquement surs, mais `secrets` est l'API recommandee depuis Python 3.6.
