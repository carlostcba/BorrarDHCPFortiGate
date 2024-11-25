
# Script para Filtrado de IPs y Limpieza de Arrendamientos DHCP

Este script en Python realiza las siguientes tareas:
1. Se conecta a varios servidores mediante SSH para obtener una lista de direcciones IP utilizando el comando `diagnose firewall auth list`.
2. Filtra un rango de IPs especificado, excluyendo las direcciones IP obtenidas de los servidores.
3. Ejecuta comandos de limpieza de arrendamientos DHCP en los servidores según los rangos filtrados.

## Requisitos Previos

- Sistema operativo: **Debian 11/12** o **Ubuntu 20.04/22.04**.
- Acceso a `sudo` o permisos de administrador.
- Conexión a internet.
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

## Instalación y Configuración Automática

El script `setup_clean_dhcp.sh` automatiza la instalación y programación del script `clean_dhcp.py`. Sigue los pasos a continuación para configurarlo:

### 1. Descargar el Script de Configuración

En un terminal, descarga el archivo `setup_clean_dhcp.sh` ejecutando el siguiente comando:

```bash
curl -O https://raw.githubusercontent.com/carlostcba/BorrarDHCPFortiGate/main/setup_clean_dhcp.sh
```

### 2. Asignar Permisos de Ejecución

Después de descargar el archivo, asigna permisos de ejecución con:

```bash
chmod +x setup_clean_dhcp.sh
```

### 3. Ejecutar el Script

Ejecuta el script para instalar las dependencias, configurar el script Python y programar la tarea en `cron`:

```bash
sudo ./setup_clean_dhcp.sh
```

### 4. Confirmar la Configuración

- El script descargará `clean_dhcp.py` y lo colocará en `/usr/local/bin/`.
- Instalará las dependencias necesarias (`paramiko`).
- Programará una tarea en `cron` para ejecutar el script automáticamente todos los días a las 23:00.
- Los logs se almacenarán en `/var/log/clean_dhcp.log`.

### Verificar la Tarea Programada

Para confirmar que la tarea en `cron` se programó correctamente, usa:

```bash
crontab -l
```

Deberías ver una línea similar a:

```bash
0 23 * * * python3 /usr/local/bin/clean_dhcp.py >> /var/log/clean_dhcp.log 2>&1
```

## Manual de Uso

- Si necesitas ejecutar el script manualmente:
  ```bash
  python3 /usr/local/bin/clean_dhcp.py
  ```

- Para ver los logs:
  ```bash
  cat /var/log/clean_dhcp.log
  ```

## Notas

- Asegúrate de que la cuenta de usuario utilizada tenga permisos suficientes para ejecutar los comandos SSH en los servidores.
- El script no guarda ningún dato en archivos; todo el procesamiento se realiza en memoria.

## Licencia

Este script se proporciona bajo la Licencia MIT. Puedes usarlo y modificarlo según tus necesidades.
