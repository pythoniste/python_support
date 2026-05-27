"""Flow complet Bearer Token avec JWT.

Démontre l'enchaînement :
    1. POST /login          (user + password) → reçoit un JWT
    2. GET  /me             (Authorization: Bearer <jwt>)   → identité
    3. GET  /admin          (Authorization: Bearer <jwt>)   → vérifie rôle

Le serveur ne consulte aucune base pour vérifier l'identité —
seule la signature du JWT compte.

Dépendances : `pip install fastapi uvicorn pyjwt`.
"""
import datetime

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel


SECRET = "remplace-moi-par-un-vrai-secret-de-256-bits"
TTL_MINUTES = 60

# En production : base de données, mots de passe hashés (cf. 02).
UTILISATEURS = {
    "alice": {"password": "passw0rd", "role": "user"},
    "admin": {"password": "admin",    "role": "admin"},
}


app = FastAPI()


class IdentifiantsIn(BaseModel):
    user: str
    password: str


@app.post("/login")
def login(payload: IdentifiantsIn):
    info = UTILISATEURS.get(payload.user)
    if not info or info["password"] != payload.password:
        raise HTTPException(401, "Identifiants invalides")

    maintenant = datetime.datetime.now(datetime.timezone.utc)
    token = jwt.encode(
        {
            "sub": payload.user,
            "role": info["role"],
            "iat": maintenant,
            "exp": maintenant + datetime.timedelta(minutes=TTL_MINUTES),
        },
        SECRET,
        algorithm="HS256",
    )
    return {"token": token, "type": "Bearer", "expire_dans_s": TTL_MINUTES * 60}


def utilisateur_courant(authorization: str = Header(...)) -> dict:
    """Dépendance FastAPI : décode le JWT et renvoie les claims."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Token Bearer requis")
    token = authorization[7:]
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Token invalide")


@app.get("/me")
def me(user=Depends(utilisateur_courant)):
    return {"utilisateur": user["sub"], "role": user["role"]}


@app.get("/admin")
def admin(user=Depends(utilisateur_courant)):
    if user["role"] != "admin":
        raise HTTPException(403, "Réservé aux admins")
    return {"message": f"Bienvenue admin {user['sub']}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)
