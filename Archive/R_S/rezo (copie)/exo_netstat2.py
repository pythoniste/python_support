import subprocess

def netstat2():
    result_stream, result_dgram = [], []
    info = subprocess.check_output("netstat")
    for line in info.decode("utf-8").splitlines():
        items = [e for e in line.split(" ") if e]
        if 'STREAM' in items:
            result_stream.append(int(items[items.index('STREAM')+2]))
        elif 'DGRAM' in items:
            result_dgram.append(int(items[items.index('DGRAM')+1]))
    
    return {'STREAM': list(sorted(result_stream)), 'DGRAM': list(sorted(result_dgram))}

if __name__ == "__main__":
    print(netstat2())

