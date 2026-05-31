#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socketserver

params = ('127.0.0.1', 8808)


class ExampleTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        data = self.rfile.readline()
        print('>>> Reçu: %s', data)
        self.wfile.write(data + b".\n")


if __name__ == '__main__':
    server = socketserver.TCPServer(params, ExampleTCPHandler)
    server.serve_forever()
