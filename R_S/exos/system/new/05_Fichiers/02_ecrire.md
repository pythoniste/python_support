# 02 — Écrire dans un fichier

## 2.1 Trois modes d'écriture

Écrire dans un fichier, c'est ouvrir avec l'un des trois modes
suivants. Le choix dépend de **ce qu'on veut faire si le fichier existe
déjà** :

| Mode  | Si le fichier existe              | Si le fichier n'existe pas |
|-------|-----------------------------------|----------------------------|
| `"w"` | **Écrase** entièrement            | Crée un nouveau fichier    |
| `"a"` | **Ajoute** à la fin               | Crée un nouveau fichier    |
| `"x"` | **Lève `FileExistsError`**        | Crée un nouveau fichier    |

Le mode `"w"` est le plus dangereux : ouvrir un fichier important en
`"w"` par erreur le **vide instantanément**, avant même la première
écriture. Quand on veut juste ajouter, c'est `"a"`. Quand on veut
créer un fichier sans risquer d'écraser un fichier existant, c'est
`"x"`.

```python
with open("journal.log", "a", encoding="utf-8") as f:
    f.write("nouvelle entrée\n")
```

## 2.2 La méthode `f.write()`

`write(chaine)` écrit la chaîne donnée et **renvoie le nombre de
caractères écrits**. À noter :

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("première ligne")
    f.write("seconde ligne")
```

Le contenu obtenu est :

```
première lignesecondes ligne
```

…sur une **seule** ligne. Contrairement à `print`, `write` **n'ajoute
pas** de `\n`. À nous de l'écrire explicitement :

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("première ligne\n")
    f.write("seconde ligne\n")
```

C'est le piège le plus fréquent à l'écriture.

## 2.3 `f.writelines()` — une liste de chaînes

Malgré son nom, `writelines()` **n'ajoute pas non plus** de retour à
la ligne. Elle écrit simplement chaque chaîne de la liste, à la suite :

```python
lignes = ["alpha\n", "beta\n", "gamma\n"]
with open("lettres.txt", "w", encoding="utf-8") as f:
    f.writelines(lignes)
```

Si on oublie les `\n` dans les éléments de la liste, tout sort collé sur
une seule ligne. Une formulation un peu plus sûre :

```python
mots = ["alpha", "beta", "gamma"]
with open("lettres.txt", "w", encoding="utf-8") as f:
    f.writelines(m + "\n" for m in mots)
```

## 2.4 `print(..., file=f)` — la forme la plus simple

`print` accepte un argument `file=` qui change la destination. Comme
`print` ajoute un `\n` par défaut, c'est souvent **la forme la plus
lisible** pour écrire ligne à ligne :

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    print("première ligne", file=f)
    print("seconde ligne", file=f)
```

Cette fois, le retour à la ligne est ajouté automatiquement, comme à
l'écran. On peut aussi formater :

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    nom = "Ada"
    score = 42
    print(f"Joueur : {nom}, score : {score}", file=f)
```

## 2.5 Mode `"a"` pour les journaux

Le mode `"a"` (*append*) est l'allié des journaux : chaque ouverture
réserve la position d'écriture **à la fin** du fichier, sans rien
toucher au contenu existant. C'est aussi **sûr** en présence de
plusieurs processus écrivant tour à tour, là où `"w"` ferait perdre des
données.

```python
from datetime import datetime

ligne = f"{datetime.now().isoformat()} démarrage\n"
with open("app.log", "a", encoding="utf-8") as f:
    f.write(ligne)
```

## 2.6 Mode `"x"` pour ne rien écraser

Quand on génère un nouveau fichier dont le nom doit être **unique**
(par exemple un export horodaté), le mode `"x"` (*exclusive create*)
sert de garde-fou :

```python
try:
    with open("export.csv", "x", encoding="utf-8") as f:
        f.write("nom;score\n")
except FileExistsError:
    print("Le fichier existe déjà ; refus d'écraser.")
```

On évite ainsi de perdre par erreur un export antérieur.

## À retenir

- Trois modes d'écriture : `"w"` (écrase), `"a"` (ajoute), `"x"`
  (échoue si le fichier existe).
- `f.write()` n'ajoute **pas** de `\n` automatique : à insérer
  manuellement.
- `f.writelines(iterable)` non plus, malgré son nom.
- `print(..., file=f)` ajoute le `\n` comme à l'écran : la forme la
  plus lisible.
- `"a"` est l'option naturelle pour un journal ; `"x"` pour ne jamais
  écraser un fichier existant.
- L'encodage `encoding="utf-8"` reste de mise à l'écriture comme à la
  lecture.

## Démo

Exécuter `02_demo_ecrire.py`.
