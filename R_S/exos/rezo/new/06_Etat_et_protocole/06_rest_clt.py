"""Client REST du service mensualité.

À utiliser avec 05_rest_srv.py. Tout le travail réseau est délégué
à `requests` — code utile minimal.
"""
import requests


URL = "http://127.0.0.1:8808/mensualite/{c}/{t}/{d}"

DEMANDES = [
    (200_000, 0.0475, 300, "Achat principal"),
    (100_000, 0.03,   240, "Investissement locatif"),
    (50_000,  0.0,    60,  "Prêt familial"),
]


def main():
    for capital, taux, duree, libelle in DEMANDES:
        r = requests.get(URL.format(c=capital, t=taux, d=duree))
        data = r.json()
        if "mensualite" in data:
            print(f"  [{libelle:25s}] mensualité = {data['mensualite']:>10.2f} €")
        else:
            print(f"  [{libelle:25s}] erreur : {data.get('erreur')}")


if __name__ == "__main__":
    main()
