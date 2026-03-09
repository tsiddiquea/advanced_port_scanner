import socket
import threading
import argparse
from datetime import datetime
from queue import Queue

# ----------------------------
# CONFIGURATION
# ----------------------------

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
}

HIGH_RISK_PORTS = [21, 23, 445, 3389]

THREAD_COUNT = 100
timeout = 1


# ----------------------------
# SCANNER CLASS
# ----------------------------

class PortScanner:

    def __init__(self, target, start_port, end_port):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.queue = Queue()

    def resolve_target(self):
        try:
            ip = socket.gethostbyname(self.target)
            return ip
        except socket.gaierror:
            print("Invalid host.")
            exit()

    def banner_grab(self, sock):
        try:
            sock.settimeout(1)
            banner = sock.recv(1024).decode().strip()
            return banner
        except:
            return "No banner"

    def scan_port(self):
        while not self.queue.empty():
            port = self.queue.get()

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)

                result = sock.connect_ex((self.target_ip, port))

                if result == 0:
                    service = COMMON_SERVICES.get(port, "Unknown Service")
                    banner = self.banner_grab(sock)
                    risk = "HIGH RISK" if port in HIGH_RISK_PORTS else "Normal"

                    self.open_ports.append((port, service, banner, risk))

                sock.close()

            except:
                pass

            self.queue.task_done()

    def run_scan(self):
        print("\nStarting Scan...")
        print(f"Target: {self.target} ({self.target_ip})")
        print(f"Port Range: {self.start_port}-{self.end_port}")
        print(f"Scan Time: {datetime.now()}\n")

        for port in range(self.start_port, self.end_port + 1):
            self.queue.put(port)

        threads = []
        for _ in range(THREAD_COUNT):
            thread = threading.Thread(target=self.scan_port)
            thread.daemon = True
            thread.start()
            threads.append(thread)

        self.queue.join()

    def generate_report(self):
        report = []
        report.append("===== PORT SCAN REPORT =====")
        report.append(f"Target: {self.target}")
        report.append(f"Scan Completed: {datetime.now()}\n")

        if not self.open_ports:
            report.append("No open ports found.")
        else:
            for port, service, banner, risk in sorted(self.open_ports):
                report.append(
                    f"[OPEN] Port {port} | Service: {service} | Risk: {risk}\n"
                    f"        Banner: {banner}"
                )

        return "\n".join(report)

    def save_report(self, content):
        with open("port_scan_report.txt", "w") as file:
            file.write(content)


# ----------------------------
# MAIN FUNCTION
# ----------------------------

def main():
    parser = argparse.ArgumentParser(description="Advanced Terminal Port Scanner")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")

    args = parser.parse_args()

    scanner = PortScanner(args.target, args.start, args.end)
    scanner.target_ip = scanner.resolve_target()

    scanner.run_scan()
    report = scanner.generate_report()
    scanner.save_report(report)

    print(report)
    print("\nReport saved as port_scan_report.txt")


if __name__ == "__main__":
    main()