import csv

FILENAME = "/home/sch-bm/Téléchargements/frequentation-des-monuments-nationaux.csv"
MONUMENT = "Tours et remparts d'Aigues-Mortes"

with open(FILENAME) as f:
    dialect = csv.Sniffer().sniff(f.read())
    f.seek(0)
    reader = csv.DictReader(f, dialect=dialect)
    data = {d["\ufeffAnnée"]: d["Total"] for d in reader if d["Nom de l'établissement"] == MONUMENT}
    print(data)

