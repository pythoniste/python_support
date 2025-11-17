import socket
import pickle

params = ('127.0.0.1', 8808)

BUFFER_SIZE = 1024


def send_data(message):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(params)
		s.send(message.strip().encode("utf8")+ b"\n")
		return pickle.loads(s.recv(BUFFER_SIZE))


print(send_data("mem"))

