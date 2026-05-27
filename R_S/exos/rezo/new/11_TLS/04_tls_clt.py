"""Client TCP TLS minimal — stdlib `ssl`.

Se connecte au serveur 03_tls_srv.py. Le certificat étant
auto-signé, on indique explicitement au client de le faire
confiance via `load_verify_locations`.
"""
import socket
import ssl


HOTE = "127.0.0.1"
PORT = 8443


def main():
    contexte = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    contexte.load_verify_locations(cafile="serveur.crt")
    # Pour démo locale, on accepte que le hostname soit "localhost"
    # même quand on se connecte par IP. En production : ne pas faire.
    contexte.check_hostname = True

    with socket.create_connection((HOTE, PORT)) as sock_tcp:
        with contexte.wrap_socket(sock_tcp, server_hostname="localhost") as client:
            print(f"<<< Connecté en TLS {client.version()} avec {client.cipher()[0]}")
            print(f"    Certificat serveur :")
            cert = client.getpeercert()
            for nom in cert.get("subject", []):
                print(f"      {nom}")
            client.sendall(b"Bonjour TLS")
            reponse = client.recv(1024)
            print(f"    Réponse en clair : {reponse!r}")


if __name__ == "__main__":
    main()
