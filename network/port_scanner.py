#!/usr/bin/env python3
"""
port_scanner.py - Network port scanner for sysadmin tasks
Usage: python3 port_scanner.py [options] target
"""

import socket
import argparse
import sys
import csv
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Common ports and their services
COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 67: "DHCP", 68: "DHCP",
    80: "HTTP", 110: "POP3", 123: "NTP", 135: "RPC",
    139: "NetBIOS", 143: "IMAP", 161: "SNMP", 162: "SNMP",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS",
    587: "SMTP-SUB", 636: "LDAPS", 993: "IMAPS",
    995: "POP3S", 1433: "MSSQL", 1521: "Oracle",
    1723: "PPTP", 1883: "MQTT", 2049: "NFS",
    2082: "cPanel", 2083: "cPanel-SSL", 2086: "WHM",
    2087: "WHM-SSL", 2095: "Webmail", 2096: "Webmail-SSL",
    2222: "DirectAdmin", 2375: "Docker", 2376: "Docker-SSL",
    3000: "Node.js", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 5938: "TeamViewer",
    6379: "Redis", 8000: "HTTP-Alt", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt", 9000: "Portainer", 9090: "CockroachDB",
    9200: "Elasticsearch", 27017: "MongoDB", 27018: "MongoDB-SSL"
}

def is_valid_ip(target):
    """Check if target is a valid IP address or range."""
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return False

def scan_port(host, port, timeout=1):
    """Scan a single port on a host."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            return (host, port, service, "Open")
        else:
            return (host, port, "", "Closed")
    except socket.error:
        return (host, port, "", "Error")
    except Exception as e:
        return (host, port, "", f"Error: {str(e)}")

def parse_port_range(port_str):
    """Parse port range string (e.g., '20-80', '80,443,3389')."""
    ports = set()
    
    if not port_str:
        return list(COMMON_PORTS.keys())
    
    # Handle comma-separated list
    if ',' in port_str:
        for part in port_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                ports.update(range(start, end + 1))
            else:
                ports.add(int(part))
    # Handle range
    elif '-' in port_str:
        start, end = map(int, port_str.split('-'))
        ports.update(range(start, end + 1))
    # Single port
    else:
        ports.add(int(port_str))
    
    return sorted(ports)

def scan_target(target, ports, max_threads=100, timeout=1):
    """Scan multiple ports on a single target."""
    open_ports = []
    
    print(f"\n🔍 Scanning {target} ({len(ports)} ports)...")
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(scan_port, target, port, timeout): port for port in ports}
        
        for future in as_completed(futures):
            result = future.result()
            if result and result[3] == "Open":
                host, port, service, status = result
                print(f"   ✅ {host}:{port} ({service}) - {status}")
                open_ports.append(result)
            elif result and result[3] == "Error":
                host, port, _, status = result
                print(f"   ❌ {host}:{port} - {status}")
    
    return open_ports

def load_targets_from_file(filename):
    """Load targets from a file (one per line)."""
    targets = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                target = line.strip()
                if target and not target.startswith('#'):
                    targets.append(target)
        return targets
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        sys.exit(1)

def save_results(results, output_file="port_scan_results.csv"):
    """Save scan results to CSV file."""
    if not results:
        print("⚠️  No open ports found, skipping CSV export.")
        return
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Host", "Port", "Service", "Status"])
        
        for result in results:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, result[0], result[1], result[2], result[3]])
    
    print(f"✅ Results saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Network Port Scanner - Useful for sysadmin network audits",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 port_scanner.py 192.168.1.1
  python3 port_scanner.py 192.168.1.1 -p 20-80
  python3 port_scanner.py 192.168.1.1 -p 80,443,3389
  python3 port_scanner.py -f hosts.txt -p 1-1000 -t 200
  python3 port_scanner.py 192.168.1.0/24 -p 22,80,443 --ping
        """
    )
    
    parser.add_argument("target", nargs="?", help="Target IP address or hostname")
    parser.add_argument("-f", "--file", help="File containing list of targets (one per line)")
    parser.add_argument("-p", "--ports", default="common", help="Ports to scan (e.g., '20-80', '80,443,3389')")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Maximum threads (default: 100)")
    parser.add_argument("-o", "--output", default="port_scan_results.csv", help="Output CSV file")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("--ping", action="store_true", help="Check if host is reachable before scanning")
    parser.add_argument("--verbose", action="store_true", help="Show all ports (including closed)")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.target and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Determine targets
    targets = []
    if args.file:
        targets.extend(load_targets_from_file(args.file))
    if args.target:
        targets.append(args.target)
    
    # Remove duplicates
    targets = list(set(targets))
    
    # Determine ports to scan
    if args.ports.lower() == "common":
        ports = list(COMMON_PORTS.keys())
    else:
        ports = parse_port_range(args.ports)
    
    print(f"🚀 Starting port scan")
    print(f"   Targets: {len(targets)}")
    print(f"   Ports: {len(ports)}")
    print(f"   Threads: {args.threads}")
    print(f"   Timeout: {args.timeout}s")
    print("-" * 50)
    
    all_results = []
    
    # Scan each target
    for target in targets:
        # Basic validation
        if not is_valid_ip(target) and "://" not in target:
            try:
                socket.gethostbyname(target)
            except socket.gaierror:
                print(f"❌ Invalid target: {target}")
                continue
        
        # Perform scan
        results = scan_target(target, ports, args.threads, args.timeout)
        all_results.extend(results)
    
    # Save results
    if all_results:
        save_results(all_results, args.output)
    else:
        print("\n🔍 No open ports found.")
    
    print("\n✅ Scan complete.")

if __name__ == "__main__":
    main()
