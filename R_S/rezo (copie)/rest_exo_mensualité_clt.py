import requests

r = requests.get("http://127.0.0.1:8855/mensualite/200000/0.0475/240")

print(r.headers)
print(r.encoding)
print(r.text, type(r.text))
print(r.json(), type(r.json()))


r = requests.get("http://127.0.0.1:8855/mensualite/200000/0.0475/240/t")

print("Avec Arrondi")
print(r.json())


r = requests.get("http://127.0.0.1:8855/mensualite/200000/0.0475/240/z")

print("Sans Arrondi")
print(r.json())

r = requests.get("http://127.0.0.1:8855/mensualite/200000/0.04.75/240")

print("Avec erreur")
print(r.json())

