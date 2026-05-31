import socket
import json
jsoncontent = {}

address = "127.0.0.1"
port = 8808

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((address, port))

data = {
    "capital": 200000,
    "taux": 4.75,
    "duree": 25,
}

js = json.dumps(data)
print(js)

sock.send(b"\n")

sock.close()

