#!/usr/bin/python3
#-*- coding: utf8 -*-


from csv import DictWriter, unix_dialect



"""
Ce module permet de faire des simulations d'emprunt bancaire
"""




# Fonctions permettant d'effectuer des calculs




def calcul_mensualité(capital, taux_annuel, durée_en_mois, *, arrondi=False):
    """
    Calcul d'une mensualité:

    Paramètres :
    - capital en euros
    - un taux annuel (4.75% vaut 0.0475)
    - durée mensuelle (25 ans font 300 mois)
    - arrondi (booléen, obligatoirement nommé)

    Renvoie la mensualité en euros.

    >>> calcul_mensualité(200000, 4.75/100, 25*12)
    1140.234722762185
    >>> calcul_mensualité(200000, 4.75/100, 25*12, True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: calcul_mensualité() takes exactly 3 positional arguments (4 given)
    >>> calcul_mensualité(200000, 4.75/100, 25*12, arrondi=True)
    1140.23
    """
    resultat = capital * taux_annuel/12 / (1 - (1 + taux_annuel/12)**-durée_en_mois)
    return arrondi and round(resultat, 2) or resultat




def calcul_capital(mensualité, taux_annuel, durée_en_mois, *, arrondi=False):
    """
    Calcul du capital qu'il est possible d'emprunter à partir d'une mensualité:

    Paramètres :
    - la mensualité en euros
    - un taux annuel (4.75% vaut 0.0475)
    - durée mensuelle (25 ans font 300 mois)
    - arrondi (booléen, obligatoirement nommé)

    Renvoie le capital empruntable en euros en euros.

    >>> calcul_capital(1140.234722762185, 4.75/100, 25*12)
    200000.0
    >>> calcul_capital(1140.23, 4.75/100, 25*12, True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: calcul_capital() takes exactly 3 positional arguments (4 given)
    >>> calcul_capital(1140.23, 4.75/100, 25*12, arrondi=True)
    199999.17
    """
    resultat = (1 - (1 + taux_annuel/12)**-durée_en_mois) * mensualité * 12 / taux_annuel
    return arrondi and round(resultat, 2) or resultat




def calcul_amortissement(capital, mensualité, taux_annuel, *, arrondi=False):
    """
    Calcul du capital restant à rembourser à la fin d'un mois

    Paramètres :
    - le capital restant à rembourser au début d'un mois
    - la mensualité remboursée
    - le taux annuel (4.75% vaut 0.0475)
    - arrondi (booléen, obligatoirement nommé)

    Renvoie :
    - le capital restant du à la fin du mois
    - le montant remboursé
    - le montant des intérêts payés sur la période

    >>> calcul_amortissement(200000, 1140.234722762185, 4.75/100)
    (199651.43194390446, 348.56805609553703, 791.6666666666479)
    >>> calcul_amortissement(200000, 1140.23, 4.75/100, True)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: calcul_amortissement() takes exactly 3 positional arguments (4 given)
    >>> calcul_amortissement(200000, 1140.23, 4.75/100, arrondi=True)
    (199651.44, 348.56, 791.67)
    """
    nouveau_capital = capital * (1 + taux_annuel / 12) - mensualité
    remboursé = capital - nouveau_capital
    intérêts = mensualité - remboursé

    if arrondi:
        return round(nouveau_capital, 2), round(remboursé, 2), round(intérêts, 2)
    else:
        return nouveau_capital, remboursé, intérêts




def calcul_tableau_amortissement(capital, taux_annuel, durée_en_mois):
    """
    Générateur permettant de répéter la fonction précédente de manière à
    construire un tableau d'amortissement sur la durée totale de l'emprunt.

    Paramètres :
    - capital emprunté
    - le taux annuel (4.75% vaut 0.0475)
    - durée mensuelle (25 ans font 300 mois)

    Pour les fonctions précédentes, on peut ne vouloir qu'un seul résultat.
    Il est donc cohérent de vouloir l'arrondir de manière à présenter lisiblement
    le résult obtenu. Ici, on va devoir itérer. Par conséquent, un arrondi
    fausserait le résultat d'une itération sur l'autre.

    Ce générateur ne propose donc que de renvoyer les calculs exacts et
    la partie présentation sera assurée par le générateur qui suit.

    Génère, pour chaque rang :
    - un dictionnaire contenant les informations voulues qui sont :
        > le restant dû
        > la somme remboursée pendant le mois courant
        > les intérêts remboursés pendant le mois courant

    Renvoie None, comme tous les générateurs

    >>> gen = calcul_tableau_amortissement(200000, 4.75/100, 25*12)
    >>> next(gen)
    {'restant dû': 199651.43194390446, 'remboursée': 348.56805609553703, 'intérêt': 791.6666666666479}
    >>> next(gen)
    {'restant dû': 199301.48413925356, 'remboursée': 349.947804650903, 'intérêt': 790.2869181112819}
    """
    mensualité = calcul_mensualité(capital, taux_annuel, durée_en_mois)
    while capital > mensualité:
        # Dans l'appel à la fonction "amortissement",
        # on n'utilise volontairement pas le paramètre "arrondi"
        capital, remboursé, intérêt = calcul_amortissement(capital, mensualité, taux_annuel)
        yield {"restant dû": capital, "remboursée": remboursé, "intérêt": intérêt}




# Fonctions permettant un affichage




def _format_tableau_amortissement(iterable):
    """
    Générateur permettant d'afficher un tableau d'amortissement de l'emprunt.
    Ce générateur s'appuie sur le précédent

    Paramètres :
    - générateur du tableau d'amortissement renvoyant les chiffres réels

    Cette méthode prend en charge l'affichage du tableau et le calcul des arrondis

    Génère, pour chaque rang :
    - une chaîne de caractère présentant les différents chiffres :

    Renvoie None, comme tous les générateurs
    >>> gen = print_tableau_amortissement(calcul_tableau_amortissement(200000, 4.75/100, 25*12))
    >>> next(gen)
    '+------------+------------+------------+'
    >>> next(gen)
    '|  199651.43 |     348.57 |     791.67 |'
    >>> next(gen)
    '|  199301.48 |     349.95 |     790.29 |'
    >>> a = [i for i in gen]
    >>> a[-2:]
    ['|    1135.74 |    1131.26 |       8.97 |', '+------------+------------+------------+']
    """
    # écriture de '+------------+------------+------------+' en condensé
    yield ('+'+'-'*12)*3+'+'
    for mois in iterable:
        yield "| %(restant dû)10.2f | %(remboursée)10.2f | %(intérêt)10.2f |" % mois
    # Fin du tableau
    yield ('+'+'-'*12)*3+'+'




def print_tableau_amortissement(capital, taux_annuel, durée_en_mois):
    """TODO"""
    for line in _format_tableau_amortissement(
        calcul_tableau_amortissement(capital, taux_annuel, durée_en_mois)
    ):
        print(line)




# Fonction permettant un export des données




def export_tableau_amortissement(tableau, filename):
    """
    Fonction permettant de créer un fichier CSV contenant le tableau d'amortissement

    Paramètres :
    - générateur du tableau d'amortissement renvoyant les chiffres réels
    - nom du fichier CSV à générer

    Cette méthode prend en charge l'écriture du tableau dans le fichier CSV,
    les valeurs ne sont pas arrondies, cette opération pouvant être faite par l'application lisant le CSV (tableur)

    Génère, pour chaque rang :
    - une chaîne de caractère présentant les différents chiffres :

    Renvoie None, comme tous les générateurs

    >>> export_tableau_amortissement(calcul_tableau_amortissement(200000, 4.75/100, 25*12), 'truc.csv')
    >>> with open('truc.csv') as f:
    ...     content = f.read()
    ... 
    >>> len(content)
    18230
    >>> with open('truc.csv') as f:
    ...     content = f.readlines()
    ... 
    >>> len(content)
    300
    >>> content[0][:-1]
    '"restant dû","remboursée","intérêt"'
    >>> content[1][:-1]
    '"199651.43194390446","348.56805609553703","791.6666666666479"'
    >>> content[-1][:-1]
    '"1135.7390888586137","1131.261180031163","8.973542731022008"'
    """
    with open(filename, 'w') as f:
        writer = DictWriter(f, ("restant dû", "remboursée", "intérêt"), dialect=unix_dialect)
        writer.writeheader()
        # Méthode consistant à écrire toutes les données d'un seul coup:
        writer.writerows(tableau)
        # Méthode consistant à créer une boucle pour les écrire une à une
        # Particulièrement utile si l'on souhaite appliquer une transformation
        # avant écriture, sinon, préférer la méthode 1
        #for ligne in tableau:
        #    writer.writerow(ligne)




# Fin de la déclaration des fonctions.




if __name__ == '__main__':
    # Je suis le programme principal
    # Réalisation de test unitaires
    import doctest
    doctest.testmod()
else:
    # je suis importé
    pass

