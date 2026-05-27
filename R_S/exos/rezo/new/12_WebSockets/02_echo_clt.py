"""Client WebSocket d'echo.

Envoie quelques messages, attend leur écho, ferme.
"""
import asyncio
import websockets


URL = "ws://127.0.0.1:8765"

MESSAGES = ["Bonjour", "WebSocket", "Final"]


async def main():
    async with websockets.connect(URL) as ws:
        print(f"<<< Connecté à {URL}")
        for msg in MESSAGES:
            await ws.send(msg)
            reponse = await ws.recv()
            print(f"  envoyé {msg!r:>10s} reçu {reponse!r}")


if __name__ == "__main__":
    asyncio.run(main())
