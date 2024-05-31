import ssl
import urllib.request
import urllib.parse
import http.cookiejar
import json
import argparse
import os
from datetime import datetime

# Configuración de URL base y credenciales
BASEURL = "https://192.168.1.203:8443"
USERNAME = "ctello"
PASSWORD = "2019*Thais"

# Carpeta para los archivos de registro
LOG_FOLDER = "C:\\Jobs\\Logs"

# Configuración de contexto SSL inseguro
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
cookies = http.cookiejar.CookieJar()

# Definición de la clase UnifiController
class UnifiController():
    def __init__(self, verbose=False, log_file=None):
        self.url = BASEURL
        self.verbose = verbose
        self.log_file = log_file

    def api_request(self, path, data=None):
        if self.verbose:
            print('Solicitud %s/api/%s, data=%s' % (self.url, path, data))
        body = json.dumps(data).encode('ascii') if data else None
        request = urllib.request.Request('%s/api/%s' % (self.url, path), data=body)
        cookies.add_cookie_header(request)
        response = urllib.request.urlopen(request, context=ctx)
        cookies.extract_cookies(response, request)
        return json.loads(response.read())

    def login(self, username, password):
        try:
            login = self.api_request('login', {
                'username': username, 'password': password,
                'sessionTimeout': 600
            })
        except urllib.error.HTTPError as err:
            print('Error al realizar login: %s' % err)

    def call_command_alldevs(self, cmd='restart', opts={}):
        sites = self.api_request('self/sites')
        for site in sites['data']:
            if site['role'] == 'admin':
                devices = self.api_request('s/%s/stat/device' % site['name'])
                for device in devices['data']:
                    if device['type'] == 'uap':
                        log_message = 'Llamar a %s en dispositivo %s IP %s' % (cmd, device['mac'], device['ip'])
                        print(log_message, end='\n' if self.verbose else ': ')
                        if self.log_file:
                            with open(self.log_file, 'a') as log:
                                log.write(log_message + '\n')
                        try:
                            params = {'mac': device['mac'], 'cmd': cmd}
                            if opts.get('soft', False):
                                params['reboot_type'] = 'soft'
                            self.api_request(
                                's/%s/cmd/devmgr' % site['name'],
                                params
                            )
                            print('ok')
                        except urllib.error.HTTPError as e:
                            error_message = 'Error HTTP %s' % e.status
                            print(error_message)
                            if self.log_file:
                                with open(self.log_file, 'a') as log:
                                    log.write(error_message + '\n')

if __name__ == '__main__':
    # Obtener la fecha y hora actual para el nombre del archivo de registro
    now = datetime.now()
    log_filename = now.strftime("%Y-%m-%d-%H-%M-%S.log")
    log_file_path = os.path.join(LOG_FOLDER, log_filename)

    # Asegurarse de que la carpeta de registro exista
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

    # Configuración de argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Reiniciar todos los dispositivos de tipo "uap" en el controlador UniFi')
    parser.add_argument(
        '-s', '--soft', help='Realizar un reinicio suave', action='store_true')
    parser.add_argument(
        '-v', help='Salida detallada', action='store_true')
    parser.add_argument(
        '--log', help='Nombre del archivo de registro', default=log_file_path)
    
    try:
        args = parser.parse_args()
        unifi = UnifiController(verbose=args.v, log_file=args.log)
        unifi.login(USERNAME, PASSWORD)
        unifi.call_command_alldevs('restart', {'soft': args.soft})
    except argparse.ArgumentError as err:
        # print(err)
        parser.print_help()
