# 03 — `input()` et lecture utilisateur

## 3.1 La fonction `input()`

`input(prompt)` affiche `prompt` (sans saut de ligne), attend que
l'utilisateur tape quelque chose et appuie sur Entrée, puis renvoie le
texte saisi.

```python
nom = input("Quel est ton prénom ? ")
print(f"Bonjour {nom}")
```

Trois faits qu'on retient une fois pour toutes :

1. `input()` est **bloquant** : le programme attend tant que l'utilisateur
   n'a pas appuyé sur Entrée.
2. Le retour est **toujours une `str`**, même si l'utilisateur tape `42`.
3. Le saut de ligne final n'est **pas** inclus dans la chaîne renvoyée.

```python
reponse = input("Ton âge ? ")
print(type(reponse))           # <class 'str'>
```

## 3.2 Convertir vers un nombre

Pour obtenir un entier, on convertit explicitement avec `int(...)` ;
pour un flottant, avec `float(...)` :

```python
age_str = input("Ton âge ? ")
age = int(age_str)
print(f"Dans 10 ans tu auras {age + 10} ans.")
```

Ou plus concis :

```python
age = int(input("Ton âge ? "))
```

**Attention** : si l'utilisateur tape autre chose qu'un entier, `int(...)`
lève `ValueError` :

```
$ python3
>>> int("trente")
Traceback (most recent call last):
  ...
ValueError: invalid literal for int() with base 10: 'trente'
```

## 3.3 Gérer les saisies invalides avec `try/except`

On ne fait jamais confiance à une saisie utilisateur. La forme canonique
est `try/except ValueError` :

```python
saisie = input("Combien d'années ? ")
try:
    annees = int(saisie)
except ValueError:
    print("Ce n'est pas un entier.")
    annees = 0
```

Cela évite que le programme plante sur une faute de frappe.

## 3.4 Boucle de validation simple

Pour **redemander** tant que la saisie est invalide, on enveloppe la
lecture dans un `while True` qu'on quitte explicitement avec `break` :

```python
while True:
    saisie = input("Entre un entier entre 1 et 100 : ")
    try:
        n = int(saisie)
    except ValueError:
        print("Ce n'est pas un entier, réessaye.")
        continue
    if 1 <= n <= 100:
        break
    print("Hors plage, réessaye.")

print(f"Merci, j'ai bien {n}.")
```

Le motif est :

1. lire ;
2. tenter de convertir (échec → message + `continue`) ;
3. vérifier les contraintes métier (hors plage → message + `continue`) ;
4. en cas de succès, `break`.

## 3.5 Lire un mot de passe avec `getpass`

Quand on demande un mot de passe, **on ne veut pas** qu'il s'affiche
à l'écran pendant qu'il est tapé. La fonction `input` ne sait pas faire
cela ; on utilise le module `getpass` de la bibliothèque standard :

```python
import getpass

mdp = getpass.getpass("Mot de passe : ")
print(f"Tu as tapé {len(mdp)} caractères.")
```

Pendant la saisie, **rien ne s'affiche** : pas même des étoiles. Le
curseur ne bouge pas. C'est volontaire : aucune information ne fuit, pas
même la longueur, sur le terminal ou dans un éventuel partage d'écran.

Pour faire **confirmer** un mot de passe (saisi deux fois), on compare :

```python
import getpass

while True:
    mdp = getpass.getpass("Nouveau mot de passe : ")
    confirmation = getpass.getpass("Confirmation : ")
    if mdp == confirmation:
        break
    print("Les deux saisies diffèrent, réessaye.")

print("Mot de passe enregistré.")
```

Remarque : `getpass.getpass` peut afficher un avertissement
`GetPassWarning` quand le terminal ne sait pas masquer l'écho (rare en
usage standard, fréquent dans certains IDE). Dans ce cas, il retombe sur
`input` — donc l'écho **n'est plus masqué**. C'est une limite à connaître.

## À retenir

- `input(prompt)` renvoie **toujours une `str`** ; convertir avec
  `int()` ou `float()` pour traiter des nombres.
- Une conversion qui échoue lève `ValueError` : on l'attrape avec
  `try/except` et on redemande.
- Un schéma classique : `while True: lire ; valider ; break si OK`.
- `getpass.getpass` lit un mot de passe **sans écho**. Comparer deux
  saisies pour confirmer.

## Démo

Exécuter `03_demo_input.py` et répondre aux trois invites (entier,
flottant, mot de passe).
