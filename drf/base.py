from pathlib import Path
import dj_database_url
from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Configuraciones base de la aplicación
SECRET_KEY = env('SECRET_KEY')
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
else:
    DEBUG = False
    ALLOWED_HOSTS = ['*']



# Configuraciones de la base de datos (se sobreescribirán en producción)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

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

if ENVIRONMENT == 'production':
    DATABASES['default'] = dj_database_url.parse('postgresql://postgres:dMGvaakLJELZvTAacbQXowPiEZsWEZit@monorail.proxy.rlwy.net:15900/railway')
print('Entorno: ',ENVIRONMENT )
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
