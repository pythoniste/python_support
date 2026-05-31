#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Exemple de serveur UDP utilisant socketserver
"""


import socketserver
import string


params = ("127.0.0.1", 8808)


def est_palindrome(chaine):
    chaine = chaine.lower()
    for c in string.whitespace + string.punctuation:
        chaine = chaine.replace(c, "")
    return chaine == chaine[::-1]


class PalindromeUDPHandler(socketserver.DatagramRequestHandler):
    def handle(self):
        self.data = self.rfile.readline().strip().decode("utf-8")
        if est_palindrome(self.data):
            result = b"T"
        else:
            result = b"F"
        self.wfile.write(result)

if __name__ == "__main__":
    server = socketserver.UDPServer(params, PalindromeUDPHandler)
    server.serve_forever()

