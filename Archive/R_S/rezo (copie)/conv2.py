
def int2bytes(nombre):
    return nombre.to_bytes(4, "big", signed=True)

def bytes2int(octets):
    return int.from_bytes(octets, "big", signed=True)

def float2bytes(nombre):
    return nombre.hex().encode("utf-8")

def bytes2float(octets):
    return float.fromhex(octets.decode("utf-8"))

