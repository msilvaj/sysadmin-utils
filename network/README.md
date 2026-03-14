# Network Port Scanner

A lightweight, threaded port scanner designed for sysadmin network audits.
Useful for checking open ports on servers, network devices, or during security assessments.

## Features

- ✅ Scans common ports (80, 443, 22, 3389, etc.) by default
- 🔄 Multi-threaded for fast scanning
- 📊 Exports results to CSV
- 🌐 Supports IP ranges and hostnames
- 🎯 Custom port ranges (e.g., `20-80`, `80,443,3389`)
- 📁 Load targets from file
- 🛡️ Safe scanning with configurable timeouts

## Quick Start

```bash
# Scan single host (common ports)
python3 port_scanner.py 192.168.1.1

# Scan specific ports
python3 port_scanner.py 192.168.1.1 -p 20-80

# Scan multiple ports
python3 port_scanner.py 192.168.1.1 -p 80,443,3389

# Scan from file with 200 threads
python3 port_scanner.py -f hosts.txt -p 1-1000 -t 200
Installation
No external dependencies required (uses Python standard library).

bash
# Just ensure you have Python 3.7+
python3 --version
Usage
Basic Scanning
bash
# Scan a single server
python3 port_scanner.py 192.168.1.100

# Scan with custom ports
python3 port_scanner.py example.com -p 22,80,443,3389

# Scan a range
python3 port_scanner.py 192.168.1.1 -p 1-1024
Advanced Usage
bash
# Scan multiple hosts from a file
echo "192.168.1.1" > hosts.txt
echo "192.168.1.100" >> hosts.txt
python3 port_scanner.py -f hosts.txt

# Increase threads for faster scanning
python3 port_scanner.py 192.168.1.1 -t 200

# Custom output file
python3 port_scanner.py 192.168.1.1 -o my_scan.csv

# Verbose mode (show closed ports)
python3 port_scanner.py 192.168.1.1 --verbose
Output
Results are saved to port_scan_results.csv by default:

csv
Timestamp,Host,Port,Service,Status
2024-01-15 14:30:00,192.168.1.1,22,SSH,Open
2024-01-15 14:30:00,192.168.1.1,80,HTTP,Open
2024-01-15 14:30:00,192.168.1.1,443,HTTPS,Open
Common Ports Scanned
Port	Service	Description
22	SSH	Secure Shell
80	HTTP	Web Server
443	HTTPS	Secure Web
3389	RDP	Remote Desktop
445	SMB	Windows File Sharing
21	FTP	File Transfer
25	SMTP	Email
53	DNS	Domain Name System
Use Cases
🛡️ Security Audits: Check for unnecessary open ports
🔧 Server Migration: Verify port accessibility
📊 Network Inventory: Document services running
🚨 Incident Response: Identify compromised systems
🧹 Cleanup: Find old/unused services
Tips
Respect Network Policies: Only scan networks you own or have permission to test
Adjust Threads: Use -t 50 for slower networks, -t 200 for local scans
Timeout: Increase --timeout 2 for distant hosts
Combine with other tools: Use scan results with nmap for deeper analysis
Legal Note
This tool is for authorized network testing only. Always obtain proper permissions before scanning any network.
