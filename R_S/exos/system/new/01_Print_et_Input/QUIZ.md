# Quiz de validation — dossier 01_Print_et_Input

Six questions courtes pour vérifier qu'on a saisi l'essentiel avant de
passer au chapitre suivant. Les réponses se trouvent en fin de
document — tenter d'y répondre **sans** consulter au préalable.

## Questions

**Q1.** Que produit chacun de ces deux appels, et en quoi diffèrent-ils ?

```python
print("a", "b", "c")
print("a", "b", "c", sep="-", end="!\n")
```

**Q2.** À quoi sert le paramètre `flush=True` de `print` ? Donner un
cas concret où il est nécessaire.

**Q3.** Quelle f-string permet d'afficher la valeur de `pi = 3.14159`
avec exactement deux décimales et un alignement à droite sur 10
caractères au total ? Quel sera le résultat exact, encadré de crochets ?

**Q4.** Que produit l'expression suivante, et à quoi sert cette forme ?

```python
x = 7
print(f"{x * x =}")
```

**Q5.** L'utilisateur a tapé `42` à l'invite `age = input("Âge ? ")`.
Que vaut `type(age)` ? Et `age + 1` lève-t-il une erreur, ou pas ?
Justifier.

**Q6.** En quoi `getpass.getpass("Mot de passe : ")` diffère-t-il de
`input("Mot de passe : ")` du point de vue de l'utilisateur ? Citer
une limite connue de `getpass.getpass`.

---

## Réponses

**R1.** Le premier affiche `a b c` suivi d'un saut de ligne (séparateur
espace par défaut, fin `\n` par défaut). Le second affiche `a-b-c!`
suivi d'un saut de ligne : on a remplacé le séparateur par `-` et la
fin par `!\n`. Cela illustre qu'on contrôle **complètement** ce qui
sépare les valeurs et ce qui clôt la ligne.

**R2.** Python **bufferise** la sortie : ce qu'on écrit avec `print` est
stocké dans un tampon en mémoire et n'apparaît pas immédiatement à
l'écran. `flush=True` force la vidange du tampon, donc l'affichage
immédiat. C'est nécessaire dès qu'on veut voir un message **avant** un
saut de ligne ou avant la fin du programme : barre de progression
(`print(".", end="", flush=True)`), invite « Chargement... » qui
s'allonge en direct, ou affichage avant un `input` qui suit.

**R3.** `f"[{pi:>10.2f}]"`. Résultat : `[      3.14]`. La format spec
`>10.2f` signifie : aligné à droite (`>`), largeur minimale 10, type
flottant avec 2 décimales.

**R4.** Affiche `x * x =49`. La forme `{expression=}` (Python 3.8+)
imprime à la fois le **texte** de l'expression et sa **valeur**. C'est
le format **de débogage** : on évite de retaper deux fois le nom et on
voit immédiatement à quoi correspond la valeur dans la trace.

**R5.** `type(age)` vaut `<class 'str'>` : `input` renvoie **toujours**
une chaîne, même si l'utilisateur a tapé un nombre. `age + 1` lève
`TypeError: can only concatenate str (not "int") to str` car on essaie
d'additionner une chaîne et un entier. Il faut convertir d'abord avec
`int(age)`.

**R6.** Du point de vue de l'utilisateur, `input` **réaffiche** chaque
caractère tapé à l'écran, alors que `getpass.getpass` ne montre **rien**
(pas même des étoiles). C'est indispensable pour les mots de passe.
**Limite** : sur certains terminaux qui ne savent pas masquer l'écho
(certains IDE, environnements non interactifs), `getpass.getpass` émet
un `GetPassWarning` et retombe sur `input` — l'écho n'est alors **plus**
masqué. À tester avant de s'y fier en environnement non standard.
