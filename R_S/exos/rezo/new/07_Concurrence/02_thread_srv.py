"""Serveur ECHO — version MULTI-THREAD.

ThreadingMixIn crée un thread par connexion entrante. Le code du
handler est strictement synchrone et facile à raisonner.

Daemon_threads = True permet au processus de quitter sans attendre
les threads orphelins en cas de Ctrl-C.
"""
import socketserver
import threading


socketserver.TCPServer.allow_reuse_address = True

HOTE = "127.0.0.1"
PORT = 8808


class EchoHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        addr = self.client_address
        tid = threading.current_thread().name
        print(f">>> [{tid}] Client {addr} connecté")
        for ligne in self.rfile:
            ligne = ligne.rstrip(b"\n")
            if not ligne:
                break
            print(f"    [{tid}] [{addr[1]}] -> {ligne!r}")
            self.wfile.write(b"ECHO " + ligne + b"\n")
            self.wfile.flush()
        print(f"<<< [{tid}] Client {addr} déconnecté")


class ServeurThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True


if __name__ == "__main__":
    with ServeurThread((HOTE, PORT), EchoHandler) as serveur:
        print(f"<<< Serveur THREAD sur {(HOTE, PORT)}")
        serveur.serve_forever()
