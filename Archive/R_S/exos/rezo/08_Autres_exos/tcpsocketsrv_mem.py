import subprocess
import socketserver
import pickle

params = ('127.0.0.1', 8808)


def affiche_mem():
	output = subprocess.check_output("free", shell=True)
	result=[]
	for line in output.splitlines()[1:]:
		data = line.decode("utf8").split()
		dictionnaire={
			"partition":data[0],
			"total":data[1],
			"used":data[2],
			"free":data[3]}
		result.append(dictionnaire)
	return {'reponse': result}


class ExampleTCPHandler(socketserver.StreamRequestHandler):
	def handle(self):
		data = self.rfile.readline().strip().decode("utf8")
		print(data)
		if data ==  "mem":
			result = affiche_mem()
		else:
			result = "RIEN"
		print(result)
		self.wfile.write(pickle.dumps(result))


if __name__ == '__main__':
	server = socketserver.TCPServer(params, ExampleTCPHandler)
	server.serve_forever()

