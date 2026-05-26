"""Les trois modes d'attente d'un socket.

À exécuter :  python3 07_demo_bloquant.py

Observer :
- le timeout déclenche TimeoutError après le délai imparti ;
- le mode non bloquant lève BlockingIOError IMMÉDIATEMENT.

NB : la première démo tente une connexion vers une IP non routable
(10.255.255.1). L'attente forcée est volontaire ; elle dure jusqu'au
timeout, soit 1 seconde.
"""
import socket
import time


# --- Mode timeout -----------------------------------------------------
print("[Timeout] connexion à une IP non routable, timeout = 1 s")
debut = time.time()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(1)
    try:
        s.connect(("10.255.255.1", 81))
    except (TimeoutError, OSError) as exc:
        print(f"  -> {type(exc).__name__} après {time.time() - debut:.2f} s")


# --- Mode non bloquant -----------------------------------------------
print()
print("[Non bloquant] recv() sur un socket vide")
a, b = socket.socketpair()
b.setblocking(False)
debut = time.time()
try:
    b.recv(100)
except BlockingIOError:
    duree_ms = (time.time() - debut) * 1000
    print(f"  -> BlockingIOError immédiatement ({duree_ms:.1f} ms)")

a.close()
b.close()
