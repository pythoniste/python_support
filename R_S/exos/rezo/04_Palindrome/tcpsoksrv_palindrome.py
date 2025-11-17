#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur TCP utilisant socketserver
"""


import socketserver
import string


params = ("127.0.0.1", 8809)


def est_palindrome(chaine):
    chaine = chaine.lower()
    for c in string.whitespace + string.punctuation:
        chaine = chaine.replace(c, "")
    return chaine == chaine[::-1]


class PalindromeTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip().decode("utf-8")
        if est_palindrome(self.data):
            result = b"T"
        else:
            result = b"F"
        self.wfile.write(result)

if __name__ == "__main__":
    server = socketserver.TCPServer(params, PalindromeTCPHandler)
    server.serve_forever()

