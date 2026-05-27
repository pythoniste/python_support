"""Serveur WebSocket d'echo.

`pip install websockets`.

À chaque message reçu, le serveur renvoie `ECHO <message>`. Les
clients peuvent rester connectés indéfiniment.
"""
import asyncio
import websockets


HOTE = "127.0.0.1"
PORT = 8765


async def echo(ws):
    addr = ws.remote_address
    print(f">>> Client {addr} connecté")
    try:
        async for message in ws:
            print(f"    [{addr}] -> {message!r}")
            await ws.send(f"ECHO {message}")
    finally:
        print(f"<<< Client {addr} déconnecté")


async def main():
    async with websockets.serve(echo, HOTE, PORT):
        print(f"<<< Serveur WebSocket echo sur ws://{HOTE}:{PORT}")
        await asyncio.Future()                          # tourne pour toujours


if __name__ == "__main__":
    asyncio.run(main())
