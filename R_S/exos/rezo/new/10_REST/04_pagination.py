"""Pagination — deux patterns standards.

(a) **Offset/limit** : ?offset=0&limit=20 — simple, mais coûteux
    en base si la liste est immense (skip de N).
(b) **Cursor-based** : ?cursor=<token> — stable même si la liste
    change, plus efficace. Standard pour les feeds (Twitter, Github
    API v4).

Ce fichier montre offset/limit (le plus simple). Le bonus de
l'atelier 5 est le cursor.
"""
from fastapi import FastAPI, Query


app = FastAPI()

# Données simulées : 100 livres.
livres = [{"id": i, "titre": f"Livre #{i}"} for i in range(1, 101)]


@app.get("/livres")
def lister(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> dict:
    """Renvoie une page de `limit` livres à partir de `offset`."""
    sous_ensemble = livres[offset : offset + limit]
    return {
        "donnees": sous_ensemble,
        "pagination": {
            "offset": offset,
            "limit": limit,
            "total": len(livres),
            "suivant": (
                f"/livres?offset={offset + limit}&limit={limit}"
                if offset + limit < len(livres)
                else None
            ),
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)
