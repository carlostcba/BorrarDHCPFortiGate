import paramiko
import threading
import re
import os

# Lista de servidores SSH a los que deseas conectarte
servers = [
    {"hostname": "10.0.0.1", "username": "ctello", "password": "2019*Thais"},
    # Agrega más servidores según sea necesario
]

# Comando que deseas ejecutar en los servidores
command = "diagnose firewall auth list"

# Expresión regular para buscar direcciones IP en la salida del comando
ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

# Lista para almacenar las direcciones IP
ip_addresses = []

def ssh_command(server, command):
    try:
        # Crear una instancia de la clase SSHClient
        ssh = paramiko.SSHClient()
        # Ajustar la política para conectar a servidores desconocidos
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectar al servidor SSH
        ssh.connect(server["hostname"], username=server["username"], password=server["password"])

        # Ejecutar el comando en el servidor
        stdin, stdout, stderr = ssh.exec_command(command)
        # Leer la salida del comando
        output = stdout.read().decode()

        # Cerrar la conexión SSH
        ssh.close()

        # Buscar direcciones IP en la salida del comando
        ip_addresses.extend(re.findall(ip_pattern, output))

    except Exception as e:
        print(f"Error en la conexión a {server['hostname']}: {str(e)}")

# Crear threads para ejecutar comandos en paralelo
threads = []
for server in servers:
    thread = threading.Thread(target=ssh_command, args=(server, command))
    threads.append(thread)
    thread.start()

# Esperar a que todos los threads finalicen
for thread in threads:
    thread.join()

# Ruta del archivo de salida
output_file = "C:\\Jobs\\Data\\clients_clean.txt"

# Verificar si el archivo existe y crearlo si no existe
if not os.path.isfile(output_file):
    with open(output_file, 'w') as file:
        file.write("")  # Crea el archivo vacío si no existe

# Guardar las direcciones IP en el archivo
with open(output_file, "w") as file:
    for ip_address in ip_addresses:
        file.write(ip_address + "\n")

print("Direcciones IP guardadas en", output_file)
