# 02 — Code retour et erreurs

Quand on lance un programme externe, **plusieurs choses peuvent mal
tourner**. Cette fiche recense les quatre cas typiques et la manière
dont `subprocess.run` les expose côté Python.

## 2.1 Le code retour

À sa fin, la commande externe rend au système un entier — son **code
retour** (voir `00_Concepts/03_flux_standards.md`). `subprocess.run`
le range dans `result.returncode` :

```python
result = subprocess.run(["ls", "/repertoire/qui/n_existe_pas"],
                        capture_output=True, text=True)
print(result.returncode)    # 2 (par exemple) ; != 0 donc échec
print(result.stderr)        # ls: cannot access ...
```

Par défaut, `run` ne lève **aucune exception** si le code retour est
différent de 0. C'est à nous de tester `result.returncode == 0` si on
veut détecter l'échec.

## 2.2 `check=True` : laisser Python lever l'erreur

Si on préfère qu'une commande qui échoue stoppe le programme appelant,
on ajoute `check=True`. Python lève alors `subprocess.CalledProcessError` :

```python
import subprocess

try:
    subprocess.run(["ls", "/n_existe_pas"], check=True)
except subprocess.CalledProcessError as exc:
    print("Code retour :", exc.returncode)
    print("Commande    :", exc.cmd)
```

Quand utiliser `check=True` ? Quand on veut un comportement « ça doit
marcher, sinon on s'arrête ». Quand utiliser la version sans `check` ?
Quand le code de retour fait partie du résultat — par exemple `grep`
qui renvoie `1` quand il n'a rien trouvé (ce n'est pas une vraie
erreur).

## 2.3 `timeout` : limiter le temps d'exécution

Si la commande risque de **traîner** ou de bloquer, on impose une
limite en secondes :

```python
try:
    subprocess.run(["sleep", "5"], timeout=1.0)
except subprocess.TimeoutExpired as exc:
    print(f"Trop long : {exc.cmd} a dépassé {exc.timeout} s")
```

Python tue alors le sous-processus et lève `subprocess.TimeoutExpired`.
`timeout` est exprimé en **secondes** (`float` accepté).

## 2.4 Programme introuvable : `FileNotFoundError`

Si la commande n'existe pas dans le `PATH` (faute de frappe, programme
non installé), c'est l'OS qui se plaint, **avant même** que la
commande démarre. Python remonte un `FileNotFoundError` :

```python
try:
    subprocess.run(["commande_qui_n_existe_pas"])
except FileNotFoundError as exc:
    print("Programme introuvable :", exc.filename)
```

À distinguer du cas précédent : ici, la commande **n'a pas tourné du
tout**. Il n'y a pas de `returncode`, pas de `stdout`, pas de `stderr`.

## 2.5 Tableau récapitulatif

| Situation                          | Comportement de `run`                | Comment l'attraper                  |
|------------------------------------|---------------------------------------|--------------------------------------|
| Commande réussie (code 0)          | Renvoie `CompletedProcess`            | Tester `result.returncode == 0`      |
| Commande échouée (code != 0)       | Renvoie `CompletedProcess`            | Tester `result.returncode != 0`      |
| Idem, mais avec `check=True`       | Lève `CalledProcessError`             | `try / except CalledProcessError`    |
| Dépassement du `timeout`           | Lève `TimeoutExpired`                 | `try / except TimeoutExpired`        |
| Programme introuvable              | Lève `FileNotFoundError`              | `try / except FileNotFoundError`     |
| Droits insuffisants pour exécuter  | Lève `PermissionError`                | `try / except PermissionError`       |

Les trois dernières exceptions héritent toutes d'`OSError` (sauf
`CalledProcessError`, qui est dans le module `subprocess`).

## 2.6 Le patron complet

Un appel défensif typique ressemble à :

```python
import subprocess

try:
    result = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True,
        timeout=5.0,
        check=True,
    )
except FileNotFoundError:
    print("git n'est pas installé")
except subprocess.TimeoutExpired:
    print("git a mis trop de temps à répondre")
except subprocess.CalledProcessError as exc:
    print(f"git a échoué (code {exc.returncode}) : {exc.stderr}")
else:
    print(result.stdout)
```

C'est verbeux, mais chaque exception décrit une situation différente
qui demande souvent une réaction différente.

## À retenir

- Par défaut, un code retour non nul ne **lève rien** ; tester
  `result.returncode`.
- `check=True` transforme un code non nul en `CalledProcessError`.
- `timeout=N` impose une limite en secondes ; au-delà, `TimeoutExpired`.
- Programme inexistant → `FileNotFoundError` (avant exécution).
- Toutes ces erreurs s'attrapent classiquement avec `try / except`.

## Démo

Exécuter `02_demo_erreurs.py`.
