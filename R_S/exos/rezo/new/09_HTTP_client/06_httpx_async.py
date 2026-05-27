"""Client HTTP — httpx async (coroutines).

5 requêtes en parallèle via asyncio.gather. Le temps total est
celui de la **plus lente**, pas la somme — c'est tout le point.
"""
import asyncio
import time
import httpx


URLS = [f"https://httpbin.org/delay/{n}" for n in (1, 1, 1, 1, 1)]


async def fetch(client: httpx.AsyncClient, url: str) -> int:
    r = await client.get(url)
    return r.status_code


async def main() -> None:
    debut = time.perf_counter()
    async with httpx.AsyncClient(timeout=30) as client:
        codes = await asyncio.gather(*(fetch(client, u) for u in URLS))
    duree = time.perf_counter() - debut
    print(f"Codes : {codes}")
    print(f"Durée : {duree:.2f} s (sériel attendu : ~{len(URLS)} s)")


if __name__ == "__main__":
    asyncio.run(main())
