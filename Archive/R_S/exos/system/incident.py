import pickle
import json
from datetime import datetime
import sys
from enum import IntEnum
from pathlib import Path
from uuid import uuid4


JSON_FILENAME = "incidents.json"
PICKLE_FILENAME = "incidents.pickle"

DISPLAY_INCIDENT = """Incident n°{o.id}: {o.title}
niveau {o.level} 
créé le {o.created:%d %m %Y à %H %M %S}
modifié le {o.updated:%d %m %Y à %H %M %S}
"""


class Level(IntEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3


class Incident:

    def __init__(self, title):
        self.id = uuid4()
        self._title = title
        self._level = Level.LEVEL_1
        self._created = (now := datetime.now())
        self._updated = now

    def toJSON(self):
        return {
            "id": str(self.id),
            "title": self._title,
            "level": self._level.value,
            "created": self._created.isoformat(),
            "updated": self._updated.isoformat(),
        }

    @classmethod
    def fromJSON(cls, json):
        result = cls(json["title"])
        result.id = json["id"]
        result._title = json["title"]
        result._level = Level(Level(json["level"]))
        result._created = datetime.fromisoformat(json["created"])
        result._updated = datetime.fromisoformat(json["updated"])
        return result

    def up(self):
        match self._level:
            case Level.LEVEL_1:
                self._level = Level.LEVEL_2
                self._updated = datetime.now()
            case Level.LEVEL_2:
                self._level = Level.LEVEL_3
                self._updated = datetime.now()

    def down(self):
        match self._level:
            case Level.LEVEL_3:
                self._level = Level.LEVEL_2
                self._updated = datetime.now()
            case Level.LEVEL_2:
                self._level = Level.LEVEL_1
                self._updated = datetime.now()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self._updated = datetime.now()

    @property
    def short_title(self):
        return self._title[:36].ljust(36)

    @property
    def level(self):
        return self._level

    @property
    def created(self):
        return self._created

    @property
    def updated(self):
        return self._updated

    def display(self):
        print(DISPLAY_INCIDENT.format(o=self))


class Dashboard:

    def __init__(self):
        self.incidents = []

    def add(self, incident):
        self.incidents.append(incident)

    def remove(self, index):
        if 0 <= index < len(self.incidents):
            del self.incidents[index]

    def display(self, index=None):
        if index is not None:
            return self.incidents[index].display()
        print("+" + "-" * 38 + "+" + "-" * 38 + "+")
        print("|" + "ID".center(38) + "|" + "Titre".center(38) + "|")
        print("+" + "-" * 38 + "+" + "-" * 38 + "+")
        for incident in self.incidents:
            print(f"| {incident.id} | {incident.short_title} |")
        print("+" + "-" * 38 + "+" + "-" * 38 + "+")

    def up(self, index):
        if 0 <= index < len(self.incidents):
            self.incidents[index].up()

    def down(self, index):
        if 0 <= index < len(self.incidents):
            self.incidents[index].down()

    def save(self, filename):
        if filename.endswith(".json"):
            with open(filename, "w") as f:
                json.dump([incident.toJSON() for incident in self.incidents], f)
        elif filename.endswith(".pickle"):
            with open(filename, "wb") as f:
                pickle.dump(self.incidents, f)

    def load(self, filename):
        if not Path(filename).exists():
            return
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                self.incidents = [Incident.fromJSON(incident) for incident in json.load(f)]
        elif filename.endswith(".pickle"):
            with open(filename, "rb") as f:
                self.incidents = pickle.load(f)

def menu():
    dashboard = Dashboard()
    while True:
        print("""
        §/! : Charger / Sauvegarder en Pickle
        x/w : Charger / Sauvegarder en JSON
        a   : Afficher tous les incidents
        a X : Afficher l'incident numéro
        +   : Ajouter un incident
        - X : Supprimer l'incident numéro X
        > X : Escalader l'incident numéro X
        < X : désescalader l'incident numéro X
        q   : Quitter
        """)
        choix = input("Quel est votre choix ? ")
        chunks = choix.split(" ", 1)
        match chunks:
            case ["q"]:
                break
            case ["§"]:
                dashboard.load(PICKLE_FILENAME)
            case ["x"]:
                dashboard.load(JSON_FILENAME)
            case ["w"]:
                dashboard.save(JSON_FILENAME)
            case ["!"]:
                dashboard.save(PICKLE_FILENAME)
            case ["a"]:
                dashboard.display()
            case ["+"]:
                dashboard.add(Incident(input("Titre de l'incident ? ")))
            case ["a", index]:
                dashboard.display(int(index))
            case ["-", index]:
                dashboard.remove(int(index))
            case [">", index]:
                dashboard.up(int(index))
            case ["<", index]:
                dashboard.down(int(index))
            case _:
                print("choix non compris")

if __name__ == "__main__":
    menu()
