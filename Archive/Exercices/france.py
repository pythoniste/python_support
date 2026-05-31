import csv
import pygal
from datetime import datetime

FILENAME_PRODUCTION = "/home/sch-bm/Documents/repositories/python_support/Exercices/Primary Energy Production by source - France, 1900-2016 (in TWh).csv"

FILENAME_CONSUMPTION = "/home/sch-bm/Documents/repositories/python_support/Exercices/Primary Energy Consumption by source - France, 1980-2016 (in TWh).csv"

COLUMNS = ["Oil","Coal","Gas","Nuclear"]

def to_number(datum: str) -> float:
    return float(datum.replace(",", ".").strip() if datum else 0)

with open(FILENAME_PRODUCTION, encoding="utf-8-sig") as f:
    dialect = csv.Sniffer().sniff(f.read())
    f.seek(0)
    reader = csv.DictReader(f, dialect=dialect)
    raw_data = [
        {
            f"{k}_production" if k else "Year": to_number(v) if k else datetime.fromisoformat(v).year 
            for k, v in line.items()
        }
        for line in reader
        if datetime.fromisoformat(line[""]).year  >= 1980
    ]

with open(FILENAME_CONSUMPTION, encoding="utf-8-sig") as f:
    dialect = csv.Sniffer().sniff(f.read())
    f.seek(0)
    reader = csv.DictReader(f, dialect=dialect)
    for index, line in enumerate(reader):
        raw_data[index] |= {
            f"{k}_consumption": to_number(v)
            for k, v in line.items()
            if k
        }

fieldnames = ["Year"] + [f"{col}_production" for col in COLUMNS] + [f"{col}_consumption" for col in COLUMNS]

with open("france.csv", "w") as f:
    writer = csv.DictWriter(f, dialect=csv.unix_dialect, fieldnames=fieldnames, extrasaction="ignore", restval="")
    writer.writeheader()
    writer.writerows(raw_data)


result = {
    col: [line.get(f"{col}_production", 0.0) - line.get(f"{col}_consumption", 0.0) for line in raw_data]
    for col in COLUMNS
}

graph = pygal.Line()
graph.title = 'Net production of energy'
for key, values in result.items():
    graph.add(key,  values)

graph.render_to_file('france.svg')

print(result)
