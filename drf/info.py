# info.py
import os
from datetime import datetime
import django
from drf import settings

base_printed = False

def print_info(ENVIRONMENT, DATABASES, ALLOWED_HOSTS):
    global base_printed
    # Verificar si es la instancia principal del proceso
    if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
        if not base_printed:
            print(f"{'-'*50}")
            print(f"{'Entorno':<25} | {ENVIRONMENT}")
            print(f"{'Versión de Django':<25} | {django.get_version()}")
            print(f"{'Fecha y Hora de Inicio':<25} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'-'*50}")
            print(f"Configuración de la base de datos:")
            print(f"{DATABASES['default']}")
            print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")
            print(f"{'-'*50}")
            print(f"INSTALLED_APPS:")
            for app in settings.INSTALLED_APPS:
                print(f"  - {app}")
            print(f"{'-'*50}")
            print(f"MIDDLEWARE:")
            for mw in settings.MIDDLEWARE:
                print(f"  - {mw}")
            base_printed = True
