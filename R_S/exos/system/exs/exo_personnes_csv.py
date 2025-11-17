with open("personnes.csv") as f:
    dialect = csv.Sniffer().sniff(f.readline())
    reader = csv.reader(f, dialect=dialect)
    performers = list(reader)

print("Les performers sont:")
for performer in performers:
    print("{} {}".format(performer[0], performer[1]))

print("Les performers sont:")
for performer in performers:
    print("{0[0]} {0[1]}".format(performer))

print("Les performers sont:")
for performer in performers:
    print("{0} {1}".format(*performer))


with open("personnes.csv") as f:
    dialect = csv.Sniffer().sniff(f.readline())
    f.seek(0)
    reader = csv.DictReader(f, dialect=dialect)
    performers = list(reader)

print("Les performers sont:")
for performer in performers:
    print("{} {}".format(performer["Prenom"], performer["Nom"]))

print("Les performers sont:")
for performer in performers:
    print("{0[Prenom]} {0[Nom]}".format(performer))

print("Les performers sont:")
for performer in performers:
    print("{Prenom} {Nom}".format(**performer))

