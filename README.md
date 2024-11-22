
# Script para Filtrado de IPs y Limpieza de Arrendamientos DHCP

Este script en Python realiza las siguientes tareas:
1. Se conecta a varios servidores mediante SSH para obtener una lista de direcciones IP utilizando el comando `diagnose firewall auth list`.
2. Filtra un rango de IPs especificado, excluyendo las direcciones IP obtenidas de los servidores.
3. Ejecuta comandos de limpieza de arrendamientos DHCP en los servidores según los rangos filtrados.

## Requisitos Previos

- Python 3.x instalado en el sistema.
- La biblioteca `paramiko` para comunicación SSH.
- Soporte para ejecución en paralelo mediante hilos (threading).

Instala la biblioteca requerida con:
```bash
pip install paramiko
```

## Uso

1. **Actualizar Detalles de los Servidores**:
   Modifica la lista `servers` en el script con los datos apropiados de hostname, usuario y contraseña:
   ```python
   servers = [
       {"hostname": "10.0.0.1", "username": "usuario", "password": "contraseña"},
       # Agrega más servidores según sea necesario
   ]
   ```

2. **Especificar el Rango de IP**:
   Actualiza las variables `start_ip` y `end_ip` para definir el rango de IPs que deseas filtrar:
   ```python
   start_ip = "192.168.160.10"
   end_ip = "192.168.167.254"
   ```

3. **Ejecutar el Script**:
   Ejecuta el script:
   ```bash
   python clean_dhcp.py
   ```

4. **Resultados**:
   - Muestra las direcciones IP extraídas de los servidores.
   - Genera y muestra los rangos de IP filtrados.
   - Ejecuta los comandos de limpieza de arrendamientos DHCP para los rangos de IP filtrados.

## Características

- Conexión a múltiples servidores mediante SSH de forma paralela usando hilos (threading).
- Filtra rangos de IP de forma dinámica sin usar archivos temporales.
- Envía comandos de limpieza de DHCP a los servidores.

## Flujo del Script

1. **Extracción de Direcciones IP**:
   - Se conecta a cada servidor y obtiene direcciones IP basadas en la salida del comando.
   - Usa expresiones regulares para extraer direcciones IP válidas.

2. **Generación de Rangos Filtrados**:
   - Excluye las direcciones IP obtenidas de un rango especificado.
   - Genera bloques contiguos de direcciones IP filtradas.

3. **Ejecución de Comandos**:
   - Envía comandos de limpieza de arrendamientos DHCP para cada IP o rango de IP.

## Ejemplo de Salida

```
Direcciones IP extraídas: ['192.168.160.12', '192.168.160.15']
Rangos filtrados generados:
192.168.160.10-192.168.160.11
192.168.160.13-192.168.160.14
192.168.160.16-192.168.167.254
```

## Personalización

- Modifica la variable `base_command` para cambiar el comando de limpieza de DHCP:
  ```python
  base_command = "execute dhcp lease-clear"
  ```

- Agrega más servidores a la lista `servers` según sea necesario.

## Notas

- Asegúrate de que la cuenta de usuario utilizada tenga permisos suficientes para ejecutar los comandos SSH en los servidores.
- El script no guarda ningún dato en archivos; todo el procesamiento se realiza en memoria.

## Licencia

Este script se proporciona bajo la Licencia MIT. Puedes usarlo y modificarlo según tus necesidades.


Guarda el script como setup_clean_dhcp.sh.

Dale permisos de ejecución:
bash
Copiar código
chmod +x setup_clean_dhcp.sh
Ejecútalo:
bash
Copiar código
sudo ./setup_clean_dhcp.sh
