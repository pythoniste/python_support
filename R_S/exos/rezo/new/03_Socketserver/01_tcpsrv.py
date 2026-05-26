"""Serveur TCP avec socketserver.TCPServer + StreamRequestHandler.

À comparer avec 02_Framing/05_makefile_srv.py : ici, la boucle d'accept,
la fermeture des connexions et l'instanciation par client sont
entièrement gérées par le framework.

self.rfile et self.wfile sont EXACTEMENT les objets retournés par
socket.makefile() en mode binaire ("rb" et "wb" respectivement).

Pour arrêter : Ctrl-C (voir atelier 7 pour un arrêt déclenché par
mot-clé, et dossier 07_Concurrence pour le raisonnement complet).
"""
import socketserver


# Autorise le rebind immédiat sur un port en TIME_WAIT — pratique en
# développement quand on redémarre souvent le serveur.
socketserver.TCPServer.allow_reuse_address = True

HOTE = "127.0.0.1"
PORT = 8808


class BonjourHandler(socketserver.StreamRequestHandler):
    """Une instance par connexion entrante.

    Le framework appelle handle() puis ferme la connexion. Pour gérer
    plusieurs messages au sein d'une même connexion, voir l'atelier 3.
    """

    def handle(self) -> None:
        ligne = self.rfile.readline().rstrip(b"\n")
        if not ligne:
            return
        print(f"    Reçu de {self.client_address} : {ligne!r}")
        self.wfile.write(b"Bonjour " + ligne + b".\n")


if __name__ == "__main__":
    with socketserver.TCPServer((HOTE, PORT), BonjourHandler) as serveur:
        print(f"<<< Serveur TCPServer en attente sur {(HOTE, PORT)}")
        print("    (Ctrl-C pour arrêter)")
        serveur.serve_forever()
