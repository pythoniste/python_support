import csv
import pygal

FILENAME = "/home/sch-bm/Documents/repositories/python_support/Exercices/Primary Energy Consumption by source - World, 1980-2016 (in TWh).csv"

COLUMNS = ["Oil","Coal","Gas","Hydroelectricity","Nuclear","Biomass and Waste","Wind","Fuel Ethanol","Solar, Tide, Wave, Fuel Cell","Geothermal","Biodiesel"]


with open(FILENAME, encoding="utf-8-sig") as f:
    dialect = csv.Sniffer().sniff(f.read())
    f.seek(0)
    reader = csv.DictReader(f, dialect=dialect)
    raw_data = list(reader)

def to_number(datum: str) -> float:
    return float(datum.replace(",", ".").strip() if datum else 0)

base = {column: to_number(raw_data[0][column]) for column in COLUMNS}
diff = {column: [] for column in COLUMNS}

for raw_datum in raw_data[1:]:
    for column in COLUMNS:
        diff[column].append(to_number(raw_datum[column]) - base[column])
    base = {column: to_number(raw_datum[column]) for column in COLUMNS}

graph = pygal.Line()
graph.title = 'Increase of each source of energy (in TWh)'
for key, values in diff.items():
    graph.add(key,  values)

graph.render_to_file('diff_consumption.svg')


AFFECTATION = {
    "Oil": "Fossile",
    "Coal": "Fossile",
    "Gas": "Fossile",
    "Hydroelectricity": "Renewable",
    "Nuclear": "Renewable",
    "Biomass and Waste": "Renewable",
    "Wind": "Renewable",
    "Fuel Ethanol": "Renewable",
    "Solar, Tide, Wave, Fuel Cell": "Renewable",
    "Geothermal": "Renewable",
    "Biodiesel": "Renewable",
}

result = {}

for type_nrj, diff_datum in diff.items():
    column = AFFECTATION[type_nrj]
    if column not in result:
        result[column] = diff_datum
    else:
        for index, datum in enumerate(diff_datum):
            result[column][index] += datum

graph = pygal.Line()
graph.title = 'Increase of each type of energy (in TWh)'
for key, values in result.items():
    graph.add(key,  values)

graph.render_to_file('diff_consumption_synth.svg')

