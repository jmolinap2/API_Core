import os
from pathlib import Path
import dj_database_url
from environ import Env

env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Configuraciones base de la aplicación
SECRET_KEY = env('SECRET_KEY')
DEBUG = ENVIRONMENT == 'development'
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS') if DEBUG else ['*']

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
else:
    DATABASES = {
        'default': dj_database_url.parse(env('DATABASE_URL'))
    }
# Rutas dentro del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
