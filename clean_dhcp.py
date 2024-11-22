import paramiko
import threading
import re
import os

# Parte 1: Extracción de direcciones IP
servers = [
    {"hostname": "10.0.0.1", "username": "admin", "password": "password"},
    # Agrega más servidores según sea necesario
]

command = "diagnose firewall auth list"
ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
ip_addresses = []

def ssh_command(server, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server["hostname"], username=server["username"], password=server["password"])
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
        ip_addresses.extend(re.findall(ip_pattern, output))
    except Exception as e:
        print(f"Error en la conexión a {server['hostname']}: {str(e)}")

threads = []
for server in servers:
    thread = threading.Thread(target=ssh_command, args=(server, command))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

output_file_clients = "C:\\Jobs\\Data\\clients_clean.txt"
if not os.path.isfile(output_file_clients):
    with open(output_file_clients, 'w') as file:
        file.write("")

with open(output_file_clients, "w") as file:
    for ip_address in ip_addresses:
        file.write(ip_address + "\n")

print("Direcciones IP guardadas en", output_file_clients)

# Parte 2: Generación de rangos filtrados
def ip_to_int(ip):
    return sum(int(octet) << (8 * i) for i, octet in enumerate(reversed(ip.split("."))))

def int_to_ip(ip_int):
    return ".".join(str((ip_int >> (8 * i)) & 0xFF) for i in range(3, -1, -1))

def generate_ip_range(start, end):
    start_int = ip_to_int(start)
    end_int = ip_to_int(end)
    for ip_int in range(start_int, end_int + 1):
        yield int_to_ip(ip_int)

def generate_filtered_ranges(start_ip, end_ip, excluded_ips):
    excluded_set = set(ip_to_int(ip) for ip in excluded_ips)
    current_range_start = None
    for ip in generate_ip_range(start_ip, end_ip):
        ip_int = ip_to_int(ip)
        if ip_int not in excluded_set:
            if current_range_start is None:
                current_range_start = ip
        else:
            if current_range_start:
                yield (current_range_start, int_to_ip(ip_int - 1))
                current_range_start = None
    if current_range_start:
        yield (current_range_start, end_ip)

output_file_dhcp = "C:\\Jobs\\Data\\dhcp_clear.txt"
start_ip = "192.168.160.10"
end_ip = "192.168.167.254"

excluded_ips = []
if os.path.isfile(output_file_clients):
    with open(output_file_clients, "r") as file:
        excluded_ips = [line.strip() for line in file]

filtered_ranges = list(generate_filtered_ranges(start_ip, end_ip, excluded_ips))

with open(output_file_dhcp, "w") as file:
    for start, end in filtered_ranges:
        if start == end:
            file.write(f"{start}\n")
        else:
            file.write(f"{start}-{end}\n")

print(f"Archivo {output_file_dhcp} generado con los rangos filtrados.")

# Parte 3: Limpieza de arrendamientos DHCP
base_command = "execute dhcp lease-clear"
with open(output_file_dhcp, 'r') as file:
    ip_addresses = file.read().splitlines()

for server in servers:
    for ip_address in ip_addresses:
        full_command = f"{base_command} {ip_address}"
        ssh_command(server, full_command)
