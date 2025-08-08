import subprocess
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    try:
        output = subprocess.check_output(['ping', '-c', '1', '-W', '1', str(ip)],
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True)
        if "1 received" in output or "bytes from" in output:
            return str(ip)
    except subprocess.CalledProcessError:
        pass
    return None

# Rango que querés escanear
network = ipaddress.IPv4Network('192.168.98.0/24')

# Escaneo concurrente
with ThreadPoolExecutor(max_workers=50) as executor:
    results = list(executor.map(ping_host, network.hosts()))

# Mostrar vivos
for ip in results:
    if ip:
        print(ip)
