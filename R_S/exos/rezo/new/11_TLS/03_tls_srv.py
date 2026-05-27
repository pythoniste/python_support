"""Serveur TCP TLS minimal — stdlib `ssl`.

Lance après avoir généré le certificat (02_generer_cert.py).
À utiliser avec 04_tls_clt.py.

C'est la "vraie" base : on prend un socket TCP standard, on
l'enveloppe via SSLContext.wrap_socket, et on parle TLS.
"""
import socket
import ssl


HOTE = "127.0.0.1"
PORT = 8443                                              # convention TLS


def main():
    contexte = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexte.load_cert_chain(certfile="serveur.crt", keyfile="serveur.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_tcp:
        sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_tcp.bind((HOTE, PORT))
        sock_tcp.listen(5)
        print(f"<<< Serveur TLS sur {(HOTE, PORT)}")

        with contexte.wrap_socket(sock_tcp, server_side=True) as serveur:
            while True:
                try:
                    conn, addr = serveur.accept()
                except ssl.SSLError as exc:
                    print(f"!!! Handshake TLS échoué : {exc}")
                    continue
                print(f">>> Client {addr} connecté (TLS {conn.version()})")
                with conn:
                    data = conn.recv(1024)
                    print(f"    Reçu chiffré : {data!r}")
                    conn.sendall(b"ECHO " + data + b"\n")


if __name__ == "__main__":
    main()
