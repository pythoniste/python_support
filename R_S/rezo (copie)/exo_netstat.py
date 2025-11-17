import subprocess

def netstat():
    result = subprocess.check_output("netstat")
    print("Il y a {} entrées".format(len(result.splitlines())))
    print("Il y a {} entrées TCP".format(result.count(b"STREAM")))
    print("Il y a {} entrées UDP".format(result.count(b"DGRAM")))

if __name__ == "__main__":
    netstat()

