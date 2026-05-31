#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur SOAP
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import SOAPpy


if __name__ == "__main__":

	def hello(name):
		return {'message': 'hello %s' % name}

	server = SOAPpy.SOAPServer(("127.0.0.1",8080))
	server.registerFunction(hello)
	server.serve_forever()

