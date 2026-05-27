"""Versioning d'API REST — deux versions coexistent (v1 et v2).

Stratégie la plus courante : préfixer l'URL par /v1, /v2.
Permet de modifier le contrat sans casser les clients existants.

Trois autres stratégies possibles :
- En-tête `Accept: application/vnd.example.v2+json` (plus pur REST,
  moins lisible) ;
- Sous-domaine `v2.api.example.com` ;
- Paramètre de requête `?version=2` (à éviter, peu standard).
"""
from fastapi import FastAPI


app = FastAPI()


# ============ V1 — réponse plate ============

@app.get("/v1/produits/{pid}")
def produit_v1(pid: int) -> dict:
    return {
        "id": pid,
        "nom": "T-shirt",
        "prix": 19.99,
    }


# ============ V2 — réponse structurée avec métadonnées ============

@app.get("/v2/produits/{pid}")
def produit_v2(pid: int) -> dict:
    return {
        "id": pid,
        "nom": "T-shirt",
        "prix": {"montant": 19.99, "devise": "EUR"},
        "_metadonnees": {
            "version": "v2",
            "deprecation_v1": "2026-12-31",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)
