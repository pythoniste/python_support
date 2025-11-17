#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur HTTP
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


params = '127.0.0.1', 8016

class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Récupération des informations sur le client.
        parsed = urlparse(self.path)
        infos = [
            'client_adress: %s' % str(self.client_address),
            'address_string: %s' % self.address_string(),
            'command: %s' % self.command,
            'unparsed path: %s' % self.path,
            'parsed path %s' % parsed.path,
            'query: %s' % parsed.query,
            'request_version: %s' % self.request_version,
            'server_version: %s' % self.server_version,
            'sys_version: %s' % self.sys_version,
            'protocol_version: %s' % self.protocol_version,
        ]
        for k, v in self.headers.items():
            infos.append('HEADER %s: %s' % (k, v.strip()))
        # Début de la création de la réponse
        self.send_response(200)
        self.send_header(b'Content-type', b'text/html')
        self.end_headers()
        # Envoi du contenu de la page au navigateur
        infos = b'<ul><li>' + b'</li><li>'.join([bytes(i, 'utf-8') for i in infos]) + b'</li></ul>'
        self.wfile.write(b"""<html><head><title>Hello World</title></head><body><p>Hello World</p>""" + infos + b"""</body></html>""")

server = HTTPServer(params, HelloHandler)
server.serve_forever()

