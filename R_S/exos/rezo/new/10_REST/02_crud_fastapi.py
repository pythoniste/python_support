"""CRUD complet via FastAPI — 3× plus court que 01_crud_stdlib.py.

`pip install fastapi uvicorn`.

Bonus FastAPI :
- Validation via Pydantic ;
- Documentation OpenAPI sur /docs ;
- Codes HTTP gérés automatiquement (HTTPException, status_code).
"""
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(title="TODOs")


class TodoIn(BaseModel):
    titre: str
    fait: bool = False


class TodoOut(TodoIn):
    id: int


todos: dict[int, TodoOut] = {}
prochain_id = 1


@app.get("/todos")
def lister() -> list[TodoOut]:
    return list(todos.values())


@app.post("/todos", status_code=status.HTTP_201_CREATED)
def creer(payload: TodoIn) -> TodoOut:
    global prochain_id
    todo = TodoOut(id=prochain_id, **payload.model_dump())
    todos[prochain_id] = todo
    prochain_id += 1
    return todo


@app.get("/todos/{tid}")
def lire(tid: int) -> TodoOut:
    if tid not in todos:
        raise HTTPException(404, detail="todo absent")
    return todos[tid]


@app.put("/todos/{tid}")
def remplacer(tid: int, payload: TodoIn) -> TodoOut:
    if tid not in todos:
        raise HTTPException(404, detail="todo absent")
    todos[tid] = TodoOut(id=tid, **payload.model_dump())
    return todos[tid]


@app.delete("/todos/{tid}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer(tid: int) -> None:
    if tid not in todos:
        raise HTTPException(404, detail="todo absent")
    del todos[tid]


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8808)
