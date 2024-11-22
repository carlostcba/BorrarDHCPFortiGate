#!/bin/bash

# Variables
REPO_URL="https://raw.githubusercontent.com/carlostcba/BorrarDHCPFortiGate/main/clean_dhcp.py"
SCRIPT_PATH="/usr/local/bin/clean_dhcp.py"
LOG_FILE="/var/log/clean_dhcp.log"

# Actualización del sistema e instalación de dependencias
echo "Actualizando el sistema e instalando dependencias..."
sudo apt update && sudo apt install -y python3 python3-pip curl cron

# Descargar el script Python
echo "Descargando el script clean_dhcp.py..."
sudo curl -o "$SCRIPT_PATH" "$REPO_URL"
sudo chmod +x "$SCRIPT_PATH"

# Crear el log file si no existe
if [ ! -f "$LOG_FILE" ]; then
    sudo touch "$LOG_FILE"
    sudo chmod 666 "$LOG_FILE"
fi

# Agregar la tarea al cron
CRON_JOB="0 23 * * * python3 $SCRIPT_PATH >> $LOG_FILE 2>&1"
(crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH"; echo "$CRON_JOB") | crontab -

# Verificar que el cron está activo
sudo systemctl enable cron
sudo systemctl start cron

echo "Instalación y configuración completadas. El script se ejecutará diariamente a las 23:00."
