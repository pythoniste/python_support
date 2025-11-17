#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socketserver
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"



import socketserver
import json
import operator
import functools

params = ('127.0.0.1', 8809)

class ExampleTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip().decode("utf8")
        print('data recevied %s' % self.data)
        result = self.repondre()
        print('\tresult = %s' % result)
        self.wfile.write(json.dumps(result).encode('utf8') + b'\n')

    def repondre(self):
        try:
            data = json.loads(self.data)
        except:
            return {"success": False, "reason": "Request decode error"}
        if 'method' not in data:
            return {"success": False, "reason": "Method missing"}
        if 'values' not in data:
            return {"success": False, "reason": "Values missing"}
        try:
            values = map(int, data['values'])
        except:
            return {"success": False, "reason": "Values should be integers"}
        if not values:
            return {"success": False, "reason": "Empty Values parameter"}
        func = getattr(operator, data['method'])
        if func is None:
            return {"success": False, "reason": "Unknow method"}
        result = functools.reduce(func, values)
        return {"success": True, "result": result}


if __name__ == '__main__':
    server = socketserver.TCPServer(params, ExampleTCPHandler)
    server.serve_forever()

