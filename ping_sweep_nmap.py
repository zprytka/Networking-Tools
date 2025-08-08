#!/usr/bin/env python3

import subprocess
import ipaddress
import argparse
from concurrent.futures import ThreadPoolExecutor

def ping_host(ip):
    try:
        output = subprocess.check_output(
            ['ping', '-c', '1', '-W', '1', str(ip)],
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        if "1 received" in output or "bytes from" in output:
            return str(ip)
    except subprocess.CalledProcessError:
        pass
    return None

def run_nmap(ip_list, ports):
    print(f"\n Running Nmap scan on {len(ip_list)} host(s) for ports: {ports}\n")
    try:
        subprocess.run(['nmap', '-sT', '-Pn', '-p', ports] + ip_list)
    except FileNotFoundError:
        print("Error: Nmap is not installed or not in your PATH.")

def main():
    parser = argparse.ArgumentParser(description='Ping sweep and optional port scan using Nmap (no raw sockets).')
    parser.add_argument('network', help='Target network range (e.g., 192.168.98.0/24)')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of threads (default: 50)')
    parser.add_argument('-o', '--output', help='File to save live IPs')
    parser.add_argument('-p', '--ports', help='Ports to scan with Nmap (e.g., 22,80,443)', default=None)

    args = parser.parse_args()
    net = ipaddress.IPv4Network(args.network)

    print(f" Starting ping sweep on {args.network}...\n")
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(ping_host, net.hosts()))

    live_hosts = [ip for ip in results if ip]
    
    print("Live hosts found:")
    for ip in live_hosts:
        print(ip)

    if args.output:
        with open(args.output, 'w') as f:
            for ip in live_hosts:
                f.write(ip + '\n')
        print(f"\n📝 Saved results to: {args.output}")

    if args.ports and live_hosts:
        run_nmap(live_hosts, args.ports)

if __name__ == '__main__':
    main()
