# Importar el módulo 'os' para usar la función 'isfile'
import os

# Rango de direcciones IP
start_ip = "192.168.160.10"
end_ip = "192.168.167.254"

# Función para generar todas las direcciones IP en el rango
def generate_ip_range(start, end):
    start_int = list(map(int, start.split(".")))
    end_int = list(map(int, end.split(".")))

    while start_int <= end_int:
        yield ".".join(map(str, start_int))
        start_int[3] += 1
        for i in range(3, 0, -1):
            if start_int[i] > 255:
                start_int[i] = 0
                start_int[i - 1] += 1

# Ruta del archivo de salida
output_file = "C:\\Jobs\\Data\\dhcp_clear.txt"

# Generar la lista de direcciones IP en el rango
ip_range = list(generate_ip_range(start_ip, end_ip))

# Leer las direcciones IP excluidas desde el archivo clients_clean.txt
excluded_ips = set()
clients_clean_file = "C:\\Jobs\\Data\\clients_clean.txt"

# Verificar si el archivo clients_clean.txt existe
if os.path.isfile(clients_clean_file):
    with open(clients_clean_file, "r") as file:
        for line in file:
            ip = line.strip()
            excluded_ips.add(ip)

# Filtrar las direcciones IP que no están en la lista de exclusión
filtered_ips = [ip for ip in ip_range if ip not in excluded_ips]

# Guardar las direcciones IP restantes en el archivo
with open(output_file, "w") as file:
    for ip_address in filtered_ips:
        file.write(ip_address + "\n")

print(f"Direcciones IP del rango {start_ip} - {end_ip} (excluyendo las del archivo {clients_clean_file}) guardadas en {output_file}")
