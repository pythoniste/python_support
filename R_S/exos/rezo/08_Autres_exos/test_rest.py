#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
Exemple de serveur REST
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from bottle import route, run, request

stack = {}


@route('/hello/<name>', method='GET')
def say_hello(name):
    return {'message': "Hello %s" % name}


@route('/stack_lazy', method='GET')
def see_all_stack(key):
    return stack


@route('/stack_lazy/<key>', method='GET')
def see_stack(key):
    return stack.get(key)


@route('/stack', method='GET')
def see_stack(key):
    return {"success": True, "result": stack[key]}


@route('/stack/<key>', method='GET')
def see_stack(key):
    if key not in stack:
        return {"success": False, "message": f"Key {key} does not exist"}
    return {"success": True, "result": stack[key]}


@route('/stack/<key>', method='POST')
def add_into_stack(key):
    if key in stack:
        return {"success": False, "message": f"Key {key} already exists"}
    try:
        stack[key] = request.json
        return {"success": True}
    except:
        return {"success": False, "message": f"Couldn't load JSON input"}


@route('/stack/<key>', method='PUT')
def add_into_stack(key):
    if key not in stack:
        return {"success": False, "message": f"Key {key} does not exist"}
    try:
        stack[key] = request.json
        return {"success": True}
    except:
        return {"success": False, "message": f"Couldn't load JSON input"}


@route('/stack/<key>', method='PATCH')
def add_into_stack(key):
    if key not in stack:
        return {"success": False, "message": f"Key {key} does not exist"}
    try:
        data = request.json
    except:
        return {"success": False, "message": "Couldn't load JSON input"}
    if len(data) == 0:
        return {"success": False, "message": "There is no data"}
    if len(data) > 1:
        return {"success": False, "message": "There is too many data"}
    k, v = data.popitems()
    stack[key][k] = v
    return {"success": True}


@route('/stack/', method='DELETE')
def delete_stack():
    stack.clear()
    return {"success": True}


@route('/stack/<key>', method='DELETE')
def delete_from_stack(key):
    if key not in stack:
        return {"success": False, "message": f"Key {key} does not exist"}
    del stack[key]
    return {"success": True}


run(port=8095)

