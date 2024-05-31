import paramiko

# Lista de servidores SSH a los que deseas conectarte
servers = [
    {"hostname": "10.0.0.1", "username": "ctello", "password": "2019*Thais"},
    # Agrega más servidores según sea necesario
]

# Comando base que deseas ejecutar con la dirección IP como argumento
base_command = "execute dhcp lease-clear"

# Ruta del archivo con las direcciones IP
ip_list_file = "C:\\Jobs\\Data\\dhcp_clear.txt"

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

        print(output)
    except Exception as e:
        print(f"Error en la conexión a {server['hostname']}: {str(e)}")

# Leer las direcciones IP desde el archivo
with open(ip_list_file, 'r') as file:
    ip_addresses = file.read().splitlines()

# Crear el comando para cada dirección IP y ejecutarlo en los servidores
for server in servers:
    for ip_address in ip_addresses:
        full_command = f"{base_command} {ip_address}"
        ssh_command(server, full_command)
