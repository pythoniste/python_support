"""Serveur ECHO — version ASYNCIO (coroutines).

Le code ressemble à du synchrone : `await reader.readline()` lit une
ligne, puis on écrit la réponse. Mais à chaque `await`, la boucle
d'événements peut servir un autre client en parallèle.

`asyncio.start_server` fait tout le travail de socket bas niveau ;
on reçoit deux objets file-like (reader, writer) prêts à l'emploi.

C'est le standard Python moderne pour les serveurs réseau
multi-clients.
"""
import asyncio


HOTE = "127.0.0.1"
PORT = 8808


async def gerer_client(reader: asyncio.StreamReader,
                       writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    print(f">>> Client {addr} connecté")
    while True:
        ligne = await reader.readline()
        if not ligne:
            break
        ligne = ligne.rstrip(b"\n")
        if not ligne:
            break
        print(f"    [{addr[1]}] -> {ligne!r}")
        writer.write(b"ECHO " + ligne + b"\n")
        await writer.drain()
    print(f"<<< Client {addr} déconnecté")
    writer.close()
    await writer.wait_closed()


async def main() -> None:
    serveur = await asyncio.start_server(gerer_client, HOTE, PORT)
    addrs = ", ".join(str(s.getsockname()) for s in serveur.sockets)
    print(f"<<< Serveur ASYNCIO sur {addrs}")
    async with serveur:
        await serveur.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
