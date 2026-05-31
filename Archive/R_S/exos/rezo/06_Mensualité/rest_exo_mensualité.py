from bottle import route, run

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


if __name__ == "__main__":

    @route('/mensualite/<K>/<t>/<n>', method='GET')
    @route('/mensualite/<K>/<t>/<n>/<a>', method='GET')
    def mensualite(K, t, n, a=False):
        errors= []
        if a == "t":
            a = True
        else:
            a = False
        try:
            K = int(K)
        except ValueError as e:
            errors.append(str("Erreur saisie capital"))
        try:
            t = float(t)
        except ValueError as e:
            errors.append(str("Erreur saisie taux"))
        try:
            n = int(n)
        except ValueError as e:
            errors.append(str("Erreur saisie nbre mensualite"))
        if errors:
            return {'success': False, 'erreur': errors}
        return {'success': True, 'result': calcul_mensualité(K, t, n, arrondi=a)}
    run(host='127.0.0.1', port=8855)

