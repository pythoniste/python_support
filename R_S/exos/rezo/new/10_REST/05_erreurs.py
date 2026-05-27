"""Gestion d'erreurs cohérente — codes HTTP et corps standardisés.

Convention adoptée ici :
- Toujours un corps JSON avec une clé `erreur` (libellé court) et
  une clé optionnelle `detail` (explication longue).
- Codes HTTP standards :
    400  : requête malformée (corps invalide)
    401  : non authentifié
    403  : authentifié mais non autorisé
    404  : ressource introuvable
    409  : conflit (ex : duplicata)
    422  : validation échouée (FastAPI le fait automatiquement)
    500  : erreur serveur
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Reservation(BaseModel):
    numero: int
    nom: str


reservations: dict[int, Reservation] = {}


@app.post("/reservations", status_code=201)
def creer(reservation: Reservation):
    if reservation.numero in reservations:
        raise HTTPException(
            status_code=409,
            detail={"erreur": "duplicata", "detail": f"numéro {reservation.numero} déjà réservé"},
        )
    reservations[reservation.numero] = reservation
    return reservation


@app.get("/reservations/{numero}")
def lire(numero: int):
    if numero not in reservations:
        raise HTTPException(
            status_code=404,
            detail={"erreur": "introuvable", "detail": f"réservation #{numero}"},
        )
    return reservations[numero]


@app.delete("/reservations/{numero}", status_code=204)
def supprimer(numero: int):
    if numero not in reservations:
        raise HTTPException(404, detail={"erreur": "introuvable"})
    del reservations[numero]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)
