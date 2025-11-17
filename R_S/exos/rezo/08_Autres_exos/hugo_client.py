import socket


params = ('127.0.0.1', 8808)
BUFFER_SIZE = 1024 # default

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(params)

message = input("Entrez un message : ")
s.send(message.encode("utf-8") + b"\n")
data = s.recv(BUFFER_SIZE)
print('\tDonnée récupérée du serveur : %s' % data)

s.close()
