import paramiko
import threading
import re
import os

# Lista de servidores SSH a los que deseas conectarte
servers = [
    {"hostname": "10.0.0.1", "username": "ctello", "password": "@Thais2024*"},
    # Agrega más servidores según sea necesario
]

# Comando base
command_group = "show firewall addrgrp | grep Equipos-LaSalle"
command_member = "show firewall address"

# Ruta del archivo de salida
output_file = "C:\\Jobs\\Data\\Equipos_LaSalle_Detalle.txt"

# Lista para almacenar los resultados
results = []

def ssh_command(server):
    try:
        # Crear una instancia de la clase SSHClient
        ssh = paramiko.SSHClient()
        # Ajustar la política para conectar a servidores desconocidos
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectar al servidor SSH
        ssh.connect(server["hostname"], username=server["username"], password=server["password"])

        # Ejecutar el comando principal para obtener el grupo
        stdin, stdout, stderr = ssh.exec_command(command_group)
        group_output = stdout.read().decode()

        # Agregar el resultado del grupo al archivo
        results.append(f"Servidor: {server['hostname']}\n{group_output.strip()}")

        # Extraer los miembros del grupo usando una expresión regular que considere nombres con espacios
        member_pattern = r'set member ((?:(?:"[^"]+"|\S+)\s*)+)'
        member_match = re.search(member_pattern, group_output)
        if member_match:
            members_str = member_match.group(1)
            # Usar una expresión regular para extraer los nombres de los miembros incluyendo comillas
            members = re.findall(r'"([^"]+)"', members_str)

            # Iterar sobre cada miembro y ejecutar el comando para detalles
            for member in members:
                # Asegurarse de que el nombre del miembro esté entre comillas al ejecutar el comando
                member_command = f'{command_member} "{member}"'
                stdin, stdout, stderr = ssh.exec_command(member_command)
                member_output = stdout.read().decode()
                results.append(f"\n{member_command}:\n{member_output.strip()}")
        else:
            results.append("No se encontraron miembros en el grupo.")

        # Cerrar la conexión SSH
        ssh.close()

    except Exception as e:
        print(f"Error en la conexión a {server['hostname']}: {str(e)}")

# Crear threads para ejecutar comandos en paralelo
threads = []
for server in servers:
    thread = threading.Thread(target=ssh_command, args=(server,))
    threads.append(thread)
    thread.start()

# Esperar a que todos los threads finalicen
for thread in threads:
    thread.join()

# Crear el directorio si no existe
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Guardar los resultados en el archivo
with open(output_file, "w", encoding='utf-8') as file:
    for result in results:
        file.write(result + "\n")

print(f"Resultados guardados en {output_file}")
