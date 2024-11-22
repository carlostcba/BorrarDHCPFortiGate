**
# SSH IP Management and DHCP Lease Cleanup

Este script permite gestionar direcciones IP de múltiples servidores mediante SSH, generar rangos IP filtrados basados en exclusiones y ejecutar comandos de limpieza de arrendamientos DHCP. Utiliza la biblioteca `paramiko` para realizar conexiones SSH.

## Características

1. **Extracción de Direcciones IP**:
   - Se conecta a una lista de servidores definidos.
   - Ejecuta un comando SSH para extraer direcciones IP basadas en un patrón.
   - Guarda las direcciones IP en un archivo.

2. **Generación de Rangos IP Filtrados**:
   - Genera un rango de direcciones IP basado en un rango inicial y final.
   - Excluye direcciones IP previamente detectadas.
   - Escribe los rangos resultantes en un archivo.

3. **Limpieza de Arrendamientos DHCP**:
   - Ejecuta un comando SSH para limpiar arrendamientos DHCP basados en los rangos generados.

## Requisitos

- Python 3.6 o superior
- Biblioteca `paramiko` para conexiones SSH:
  ```bash
  pip install paramiko
  ```

## Uso

### Configuración

1. **Definir servidores**:
   - Actualiza la variable `servers` con las credenciales y direcciones IP de los servidores:
     ```python
     servers = [
         {"hostname": "10.0.0.1", "username": "admin", "password": "password"},
         # Agrega más servidores según sea necesario
     ]
     ```

2. **Especificar rangos y archivos de salida**:
   - Modifica las variables según tus necesidades:
     - `start_ip` y `end_ip`: Rango IP a procesar.
     - `output_file_clients`: Archivo donde se guardarán las IP extraídas.
     - `output_file_dhcp`: Archivo con los rangos filtrados.

### Ejecución

1. Ejecuta el script:
   ```bash
   python script.py
   ```

2. **Salida**:
   - Las direcciones IP extraídas se guardan en `C:\Jobs\Data\clients_clean.txt`.
   - Los rangos IP filtrados se escriben en `C:\Jobs\Data\dhcp_clear.txt`.

3. **Limpieza DHCP**:
   - El script limpia los arrendamientos DHCP ejecutando comandos en los servidores.

### Estructura del Script

- **Parte 1**: Extracción de direcciones IP desde servidores mediante SSH.
- **Parte 2**: Generación de rangos filtrados excluyendo direcciones IP detectadas.
- **Parte 3**: Limpieza de arrendamientos DHCP en los servidores.

## Personalización

- Ajusta el comando SSH en `command` para extraer direcciones IP según tu configuración.
- Modifica el rango IP y las exclusiones según sea necesario.

## Consideraciones de Seguridad

- Evita almacenar contraseñas en texto plano. Considera usar variables de entorno o herramientas como `keyring`.
- Asegúrate de que los archivos de salida estén protegidos en el sistema.

## Contribuciones

Si deseas mejorar este proyecto, eres bienvenido a enviar tus sugerencias o realizar un fork.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
**
