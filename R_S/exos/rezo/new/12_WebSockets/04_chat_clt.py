"""Client de chat WebSocket.

Lit `stdin` pour les messages à envoyer, affiche les messages
reçus. Lancer plusieurs instances pour voir le broadcast.

Usage : python3 04_chat_clt.py [pseudo]
"""
import asyncio
import sys

import websockets


URL = "ws://127.0.0.1:8765"


async def emettre(ws):
    """Lit stdin et envoie au serveur."""
    loop = asyncio.get_event_loop()
    while True:
        ligne = await loop.run_in_executor(None, sys.stdin.readline)
        if not ligne:
            break
        await ws.send(ligne.rstrip("\n"))


async def recevoir(ws):
    """Affiche les messages reçus."""
    async for message in ws:
        print(f"  << {message}")


async def main(pseudo: str = "anonyme"):
    async with websockets.connect(URL) as ws:
        await ws.send(f"[{pseudo}] entre dans le chat")
        print(f"<<< Connecté en tant que {pseudo}. Tapez vos messages, Ctrl-D pour quitter.")
        try:
            await asyncio.gather(emettre(ws), recevoir(ws))
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    pseudo = sys.argv[1] if len(sys.argv) > 1 else "anonyme"
    asyncio.run(main(pseudo))
