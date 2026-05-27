"""Serveur de chat WebSocket — broadcast à tous les clients.

C'est la "killer-app" de WebSocket : un message reçu d'un client est
immédiatement renvoyé à tous les autres, sans polling.
"""
import asyncio
import websockets


HOTE = "127.0.0.1"
PORT = 8765

clients: set[websockets.WebSocketServerProtocol] = set()


async def diffuser(message: str, sauf=None):
    cibles = [c for c in clients if c is not sauf]
    if cibles:
        await asyncio.gather(*(c.send(message) for c in cibles))


async def chat(ws):
    clients.add(ws)
    addr = ws.remote_address
    await diffuser(f"*** {addr} a rejoint ({len(clients)} en ligne) ***", sauf=ws)
    print(f">>> {addr} connecté")
    try:
        async for message in ws:
            print(f"    [{addr}] -> {message!r}")
            await diffuser(f"<{addr}> {message}", sauf=ws)
    finally:
        clients.discard(ws)
        await diffuser(f"*** {addr} a quitté ({len(clients)} restants) ***")
        print(f"<<< {addr} déconnecté")


async def main():
    async with websockets.serve(chat, HOTE, PORT):
        print(f"<<< Chat WebSocket sur ws://{HOTE}:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
