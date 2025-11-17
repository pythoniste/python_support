from pydantic import BaseModel, Field
import pickle
import json
from datetime import datetime
import sys
from enum import IntEnum
from pathlib import Path
from uuid import uuid4, UUID


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


class Incident(BaseModel):

    id: UUID = Field(default_factory=uuid4, frozen=True)
    title: str
    level: Level = Field(default=Level.LEVEL_1)
    created: datetime = Field(default_factory=datetime.now, frozen=True)
    updated: datetime = Field(default_factory=datetime.now)

    def up(self):
        match self.level:
            case Level.LEVEL_1:
                self.level = Level.LEVEL_2
                self.updated = datetime.now()
            case Level.LEVEL_2:
                self.level = Level.LEVEL_3
                self.updated = datetime.now()

    def down(self):
        match self.level:
            case Level.LEVEL_3:
                self.level = Level.LEVEL_2
                self.updated = datetime.now()
            case Level.LEVEL_2:
                self.level = Level.LEVEL_1
                self.updated = datetime.now()

    @property
    def short_title(self):
        return self.title[:36].ljust(36)

    def display(self):
        print(DISPLAY_INCIDENT.format(o=self))


class Dashboard(BaseModel):

    incidents: list[Incident] = Field(default_factory=list)

    def add(self, incident):
        self.incidents.append(incident)
        from repository import IncidentRepository
        repository = IncidentRepository()
        repository.create(incident)

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
                json.dump(self.model_dump(), f)
        elif filename.endswith(".pickle"):
            with open(filename, "wb") as f:
                pickle.dump(self.incidents, f)

    def load(self, filename):
        if not Path(filename).exists():
            return
        if filename.endswith(".json"):
            with open(filename, "r") as f:
                self.incidents = Dashboard(**json.load(f)).incidents
        elif filename.endswith(".pickle"):
            with open(filename, "rb") as f:
                self.incidents = pickle.load(f)


if __name__ == "__main__":
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
                    dashboard.add(Incident(title=input("Titre de l'incident ? ")))
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

    menu()
