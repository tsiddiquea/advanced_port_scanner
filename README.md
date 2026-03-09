# Advanced Multithreaded Port Scanner (Python)

A fast, multithreaded TCP port scanner built in Python that performs service detection, banner grabbing, and risk classification for common network services. This project demonstrates practical network reconnaissance techniques used in cybersecurity and penetration testing.


## Overview

This project implements a multithreaded port scanning tool that identifies open TCP ports on a target system and attempts to detect the services running on those ports.

The scanner is designed to simulate how professional security tools perform network reconnaissance during penetration testing.

It supports:

* High-speed multithreaded scanning
* Service detection using known port mappings
* Banner grabbing for service fingerprinting
* Risk classification for sensitive ports
* Scan reporting and logging

The tool is written entirely in Python using only standard libraries, making it portable and easy to run in controlled lab environments.


## Key Features

### Multithreaded Scanning

The scanner uses Python threading and queue-based task distribution to scan multiple ports simultaneously, dramatically improving performance compared to sequential scanning.

### Service Detection

Open ports are mapped to known services such as HTTP, SSH, FTP, and MySQL using a predefined service dictionary.

### Banner Grabbing

When possible, the scanner attempts to retrieve a service banner from open ports to help identify running applications.

### Risk Classification

Certain ports commonly associated with sensitive services are flagged as HIGH RISK:

* FTP (21)
* SSH (22)
* SMB (445)
* RDP (3389)

This provides immediate visibility into potentially exposed services.

### Scan Report Generation

After the scan completes, the tool generates a structured report containing:

* Target host
* Scan timestamp
* List of open ports
* Service name
* Banner information
* Risk classification

The report is saved to: `port_scan_report.txt`

## Project Structure
```
port_scanner/
│
├── port_scanner.py        # Main scanner implementation
├── port_scan_report.txt   # Generated report (after scan)
└── README.md              # Project documentation
```
## Technologies Used
Python Standard Libraries:

* socket — TCP connection handling
* threading — concurrent scanning
* queue — thread-safe port task management
* argparse — command-line argument parsing
* datetime — scan timestamp logging


No external dependencies are required.


## How the Scanner Works

The scanning process consists of several stages:

### 1. Target Resolution

The target hostname is converted into an IP address using:
```
socket.gethostbyname()
```
This allows the scanner to work with both IP addresses and domain names.


### 2. Port Queue Creation

A queue is populated with all ports in the specified range:
```
for port in range(start_port, end_port + 1):
    queue.put(port)
``` 
Each worker thread pulls ports from this queue.


### 3. Multithreaded Port Scanning

Multiple threads attempt TCP connections simultaneously:   
``` 
sock.connect_ex((target_ip, port))
```
If the connection succeeds (result == 0), the port is considered open.


### 4. Banner Grabbing

When a port is open, the scanner attempts to retrieve service banners:
```
sock.recv(1024)
```
This can reveal server software versions or protocols.

Example banners:
```
SSH-2.0-OpenSSH_8.4
220 FTP Server Ready
Apache/2.4.54
```

### 5. Risk Classification

Ports in the predefined list:
```
HIGH_RISK_PORTS = [21, 23, 445, 3389]
```
are labeled HIGH RISK because they often expose sensitive services.


### 6. Report Generation

After scanning completes, results are formatted into a readable report including:
```
Port
Service
Banner
Risk Level
```

## Example Output
Terminal output:
```
Starting Scan...
Target: example.com (104.18.26.120)
Port Range: 1-1024
Scan Time: 2026-03-09 22:42:37.624653

===== PORT SCAN REPORT =====
Target: example.com
Scan Completed: 2026-03-09 22:42:48.698873

[OPEN] Port 80 | Service: HTTP | Risk: Normal
        Banner: No banner
[OPEN] Port 443 | Service: HTTPS | Risk: Normal
        Banner: No banner
```        

Generated report:
```
===== PORT SCAN REPORT =====
Target: example.com
Scan Completed: 2026-03-09 22:42:48.698873

[OPEN] Port 80 | Service: HTTP | Risk: Normal
        Banner: No banner
[OPEN] Port 443 | Service: HTTPS | Risk: Normal
        Banner: No banner
```

## Screenshots

![Terminal Screenshot](image/terminal.jpg)

![Report Screenshot](image/report.jpg)

## Usage
Run the scanner from the terminal:
```
python port_scanner.py <target> --start <start_port> --end <end_port>
```
Example:
```
python port_scanner.py scanme.nmap.org --start 1 --end 1000
```
Scan a local machine:
```
python port_scanner.py 127.0.0.1 --start 1 --end 1024
```
## Performance

Because the scanner uses 100 concurrent threads, it can scan hundreds of ports quickly while maintaining reasonable network load.

Performance depends on:

* Network latency
* Target firewall rules
* Timeout settings



## Security & Ethical Use

This tool is intended for:

* cybersecurity education
* penetration testing labs
* defensive security research
* controlled network auditing

Do not use this scanner on networks or systems without explicit permission.

Unauthorized scanning may violate laws and organizational policies.



## Learning Objectives

This project demonstrates practical concepts used in cybersecurity:

* TCP networking fundamentals
* Socket programming
* Concurrent programming with threads
* Network reconnaissance techniques
* Service fingerprinting
* Security risk identification


## Author

Developed as a cybersecurity learning project to demonstrate network reconnaissance techniques and multithreaded programming in Python.


## License

This project is intended for educational and research purposes only.
Use responsibly and only in authorized environments.