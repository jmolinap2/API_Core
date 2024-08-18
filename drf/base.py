import os
from pathlib import Path
import dj_database_url
from environ import Env

env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')
# Definir una variable global
base_printed = False

# Configuraciones base de la aplicación
SECRET_KEY = env('SECRET_KEY')
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
else:
    DEBUG = False
    ALLOWED_HOSTS = ['*']

# Configuración de la base de datos
if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'PORT': env('DATABASE_PORT'),
        }
    }
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
    
    # Verificar si es la instancia principal del proceso
    from datetime import datetime
    import django

    if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
        if not base_printed:
            # Imprimir información
            print(f"\033[92mEntorno:\033[0m {ENVIRONMENT}")
            print(f"\033[94mConfiguración de la base de datos:\033[0m {DATABASES['default']}")
            print(f"\033[93mALLOWED_HOSTS:\033[0m {ALLOWED_HOSTS}")
            print(f"\033[95mVersión de Django:\033[0m {django.get_version()}")
            print(f"\033[96mFecha y Hora de Inicio:\033[0m {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            base_printed = True

if ENVIRONMENT == 'production':
    DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
