import string
from bottle import route, run, template


def est_palindrome(chaine):
    chaine = chaine.lower()
    for c in string.whitespace + string.punctuation:
        chaine = chaine.replace(c, "")
    return chaine == chaine[::-1]


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)


@route("/palindrome/<word>")
def palindrome(word):
    verb = "est" if st_palindrome(word) else "n'est pas"
    return template('<b>Le mot {{word}} {{verb}} un palindrome</b>!', word=word, verb=verb)


run(host='localhost', port=8085)

