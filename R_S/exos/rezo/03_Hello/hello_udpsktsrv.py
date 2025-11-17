import socketserver

params = ('127.0.0.1', 8809)

class ExampleUDPHandler(socketserver.DatagramRequestHandler):
	def handle(self):
		data = self.rfile.readline().strip()
		data = b"Hello " + data + b"."
		self.wfile.write(data)


if __name__ == '__main__':
	server = socketserver.UDPServer(params, ExampleUDPHandler)
	server.serve_forever()

