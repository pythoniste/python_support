from bottle import route, run, request, template, abort

from uuid import uuid4

todos = {}

@route("/todo", method="GET")
def get_all():
    return todos

@route("/todo", method="POST")
def create():
    key = request.json.get("key")
    if not key:
        key = str(uuid4())
    todos[key] = {
        "label": request.json.get("label"),
        "category": request.json.get("category"),
    }

@route("/todo/<key>", method="GET")
def detail(key):
    return {"key": todos.get(key)}

@route("/todo/<key>", method="PUT")
@route("/todo/<key>", method="PATCH")
def update(key):
    if key not in todos:
        abort(404, "No such key.")
    if request.method == "PATCH" and len(request.json) > 1:
        abort(400, "PATCH allow to update one field only.")
    todos[key].update(request.json)

@route("/todo/<key>", method="DELETE")
def delete(key):
    if key not in todos:
        abort(404, "No such key.")
    del todos[key]

run(host="localhost", port=8099)


# utiliser requests en tant que client.

