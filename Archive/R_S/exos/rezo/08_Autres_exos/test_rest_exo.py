#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import route, run
import subprocess
import json


@route('/mem/infos', method='GET')
def mem_info():
    df = subprocess.getoutput(f"free")
    for lines in df.splitlines()[1:-1]:
        total = lines.split()[1]
        use = lines.split()[2]
        free = lines.split()[3]
        return {'message': "OK", "mem total": total, "mem used":use, "mem free": free }

@route('/parts/infos', method='GET')
def parts_info():
    const = 90
    result = []
    df = subprocess.getoutput(f"df -h")
    for lines in df.splitlines()[1:]:
        esp = lines.split()[4][:-1]
        disque = lines.split()[5]
        if int(esp) >= const:
            result.append({'message': "ATTENTION", "part": disque, "Espace used": esp})
        
    return json.dumps(result)


if __name__ == "__main__":        
    run(port=8095)

