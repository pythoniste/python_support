import socketserver

params = ('127.0.0.1', 8809)

class ExampleTCPHandler(socketserver.StreamRequestHandler):
	def handle(self):
		data = self.rfile.readline().strip()
		data = b"Hello " + data + b"."
		self.wfile.write(data)


if __name__ == '__main__':
	server = socketserver.TCPServer(params, ExampleTCPHandler)
	server.serve_forever()

