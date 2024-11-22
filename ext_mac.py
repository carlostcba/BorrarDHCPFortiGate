import re

# Ruta del archivo de entrada y salida
input_file = "C:\\Jobs\\Data\\Equipos_LaSalle_Detalle.txt"
output_file = "C:\\Jobs\\Data\\Equipos_LaSalle_MACs.txt"

# Expresión regular para encontrar direcciones MAC
mac_pattern = r'(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}'

# Lista para almacenar las direcciones MAC
mac_addresses = []

# Leer el archivo de entrada
with open(input_file, "r", encoding='utf-8') as file:
    for line in file:
        # Buscar direcciones MAC en cada línea
        matches = re.findall(mac_pattern, line)
        mac_addresses.extend(matches)

# Eliminar duplicados si es necesario
mac_addresses = list(set(mac_addresses))

# Guardar las direcciones MAC en el archivo de salida
with open(output_file, "w", encoding='utf-8') as file:
    for mac in mac_addresses:
        file.write(mac + "\n")

print(f"Direcciones MAC extraídas y guardadas en {output_file}")
