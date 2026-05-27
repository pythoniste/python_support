"""Serveur HTTP — FastAPI.

`pip install fastapi uvicorn`. Standard moderne :
- async natif ;
- validation et sérialisation via Pydantic ;
- documentation OpenAPI/Swagger générée automatiquement sur /docs.

Pour lancer : `uvicorn 04_fastapi:app --host 127.0.0.1 --port 8808`
ou directement via le bloc __main__ ci-dessous.
"""
from datetime import datetime

from fastapi import FastAPI, HTTPException


app = FastAPI(title="Service Heure")


@app.get("/heure")
async def heure():
    return {"heure": datetime.now().isoformat()}


@app.get("/heure/{format}")
async def heure_format(format: str):
    if format == "locale":
        return {"heure": datetime.now().strftime("%c")}
    if format == "epoch":
        return {"heure": int(datetime.now().timestamp())}
    raise HTTPException(status_code=400, detail=f"format inconnu : {format!r}")


if __name__ == "__main__":
    import uvicorn
    # Documentation auto sur : http://127.0.0.1:8808/docs
    uvicorn.run(app, host="127.0.0.1", port=8808)
