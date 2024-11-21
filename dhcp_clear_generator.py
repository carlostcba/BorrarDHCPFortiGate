
import os

# Función para convertir una dirección IP a un número entero
def ip_to_int(ip):
    return sum(int(octet) << (8 * i) for i, octet in enumerate(reversed(ip.split("."))))

# Función para convertir un número entero a una dirección IP
def int_to_ip(ip_int):
    return ".".join(str((ip_int >> (8 * i)) & 0xFF) for i in range(3, -1, -1))

# Generador para obtener todas las direcciones IP en un rango
def generate_ip_range(start, end):
    start_int = ip_to_int(start)
    end_int = ip_to_int(end)
    for ip_int in range(start_int, end_int + 1):
        yield int_to_ip(ip_int)

# Función para generar rangos de IP excluyendo ciertas direcciones
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

# Ruta de los archivos
clients_clean_file = "C:\\Jobs\\Data\\clients_clean.txt"
output_file = "C:\\Jobs\\Data\\dhcp_clear.txt"

# Rango de direcciones IP
start_ip = "192.168.160.10"
end_ip = "192.168.167.254"

# Leer las direcciones IP excluidas
excluded_ips = []
if os.path.isfile(clients_clean_file):
    with open(clients_clean_file, "r") as file:
        excluded_ips = [line.strip() for line in file]

# Generar los rangos de IP filtrados
filtered_ranges = list(generate_filtered_ranges(start_ip, end_ip, excluded_ips))

# Guardar los rangos en el archivo de salida
with open(output_file, "w") as file:
    for start, end in filtered_ranges:
        if start == end:
            file.write(f"{start}\n")
        else:
            file.write(f"{start}-{end}\n")

print(f"Archivo {output_file} generado con los rangos filtrados.")
