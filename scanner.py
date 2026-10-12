
import socket
import ipaddress

target = input("Enter target IP: ")

try:
    target = str(ipaddress.IPv4Address(target))
except ipaddress.AddressValueError:
    print("Invalid IP address!")
    exit()

services = {}

with open("/usr/share/nmap/nmap-services") as file:
    for line in file:
        if line.startswith("#"):
            continue

        parts = line.split()

        if len(parts) >= 3 and parts[1].endswith("/tcp"):
            try:
                port = int(parts[1].split("/")[0])
                rank = float(parts[2])

                if port not in services or rank > services[port][0]:
                    services[port] = (rank, parts[0])
            except ValueError:
                continue

ports = sorted(
    services,
    key=lambda p: services[p][0],
    reverse=True
)[:100]

print(f"\nScanning {target}...\n")

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    try:
        if sock.connect_ex((target, port)) == 0:
            print(f"[+] {port}/tcp OPEN - {services[port][1]}")
    except OSError:
        pass
    finally:
        sock.close()

print("\nScan completed!")

