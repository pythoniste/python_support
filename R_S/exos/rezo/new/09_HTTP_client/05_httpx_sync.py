"""Client HTTP — httpx sync.

`pip install httpx`. API quasi identique à requests, mais avec
support async en bonus (cf. 06).
"""
import httpx


def main() -> None:
    with httpx.Client(timeout=10) as client:
        r = client.get("https://httpbin.org/get", params={"param": "demo"})
        r.raise_for_status()
        print(f"Status : {r.status_code}")
        print(f"URL    : {r.json()['url']}")


if __name__ == "__main__":
    main()
