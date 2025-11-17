
def int2bytes(nombre):
    chaine = str(nombre)
    octets = chaine.encode("utf-8")
    return octets

def bytes2int(octets):
    chaine = octets.decode("utf-8")
    nombre = int(chaine)
    return nombre

def float2bytes(nombre):
    chaine = str(nombre)
    octets = chaine.encode("utf-8")
    return octets

def bytes2float(octets):
    chaine = octets.decode("utf-8")
    nombre = float(chaine)
    return nombre

