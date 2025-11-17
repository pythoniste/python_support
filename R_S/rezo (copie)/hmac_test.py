#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Illustration du fonctionnement de HMAC
"""


__author__ = "Sébastien CHAZALLET"
__copyright__ = "Copyright 2012"
__credits__ = ["Sébastien CHAZALLET", "InsPyration.org", "Éditions ENI"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Sébastien CHAZALLET"
__email__ = "sebastien.chazallet@laposte.net"
__status__ = "Production"


import hashlib
import hmac

import pickle
from io import BytesIO

import pprint


class SimulatedPipe(object):
	content = BytesIO()
	read = content.read
	write = content.write
	flush = content.flush
	tell = content.tell
	seek = content.seek
	readline = content.readline
simulated = SimulatedPipe()

class SimulatedWriter(object):
	def __init__(self, pipe):
		self.pipe = pipe

	@staticmethod
	def make_digest(key, message):
		"Return a digest for the message."
		return hmac.new(key, message, hashlib.sha1).digest()

	def write(self, key, message):
		pickled = pickle.dumps(message)
		digest = SimulatedWriter.make_digest(key, pickled)
		self.pipe.write(digest + b' ' + bytes(str(len(pickled)), 'utf-8') + b'\n' + pickled)
		self.pipe.flush()
writer = SimulatedWriter(simulated)

class SimulatedReader(object):
	def __init__(self, pipe):
		self.pipe = pipe
		self.position = 0

	def read(self, key):
		position = self.pipe.tell()
		self.pipe.seek(self.position)
		line = self.pipe.readline()
		if not line:
			return
		stored_digest, lenght = line.split(b' ')
		pickled = self.pipe.read(int(lenght))
		self.position = self.pipe.tell()
		self.pipe.seek(position)
		calculated_digest = SimulatedWriter.make_digest(key, pickled)
		#print('Empreinte enregistrée : %s' % stored_digest)
		#print('Empreinte stockée     : %s' % calculated_digest)
		if(stored_digest != calculated_digest):
			print('Données corrompues ou clé incorrecte')
			return
		return pickle.loads(pickled)
reader = SimulatedReader(simulated)

# Test
key = b'ma super cle secrete que personne connait'

# Ecriture de deux entrées correctes
writer.write(key, 'Mon premier message')
writer.write(key, 'Mon deuxieme message')

# Ecriture d'une entrée corrompue en reprennant la fonction d'écriture, mais en calculant mal l'empreinte
pickled = pickle.dumps('Mon troisieme message')
digest = SimulatedWriter.make_digest(key, b'Empreinte de quelque chose de different du message')
#print(digest)
simulated.write(digest + b' ' + bytes(str(len(pickled)), 'utf-8') + b'\n' + pickled)
simulated.flush()

# Lectures
print('Lecture du premier message avec la bonne clé')
print(reader.read(key))
print('Lecture du deuxième message avec une mauvaise clé')
print(reader.read(b'pas la bonne cle'))
print('Lecture du troisième message (corrompu) avec une bonne clé')
print(reader.read(key))

